import copy
import random
from collections import deque
from types import SimpleNamespace

import numpy as np
import torch

from agent.model import Linear_QNet, QTrainer
from core.actions.action import MoveAction
from core.entity import Entity
from core.simulation import Simulation
from core.vector2 import Vector2

AGENT_VIEWING_DISTANCE = 8.5
DANGER_DISTANCE = 1.5  # Slightly above the enemies' attack range (1.0)
GRID_SIZE = int(AGENT_VIEWING_DISTANCE * 2)
STATE_SIZE = (2 * GRID_SIZE * GRID_SIZE) + 3 + 3  # (enemies + powerups) * GRID_SIZE * GRID_SIZE + (has_powerup, dx, dy) + (has_homestead, dx, dy)
MAX_MEMORY = 100000
BATCH_SIZE = 64
MIN_MEMORY_TO_TRAIN = 1000
TRAIN_EVERY_N_STEPS = 4
LR = 0.0001
INTIAL_RANDOMNESS = 0.75
FINAL_RANDOMNESS = 0.01
RANDOMNESS_DECAY = 0.0015


class Agent:
    reward_system = SimpleNamespace(
        player_killed=-10,
        homestead_destroyed=-10,
        enemy_killed=0.1,
        powerup_collected=5,
        base_damage=-0.01,  # Per 10 damage taken by the player or the homestead
        nearby_enemy=-0.05,
        time_alive=0.01,
        powerup_distance=1,
    )

    def __init__(self, mode='test', model_path='') -> None:
        self.n_games = 0
        # self.epsilon = 1
        self.epsilon = INTIAL_RANDOMNESS
        self.epsilon_decay = RANDOMNESS_DECAY
        self.epsilon_min = FINAL_RANDOMNESS
        self.gamma = 0.99  # Discount rate, should be smaller than 1
        self.memory = deque(maxlen=MAX_MEMORY)
        self.num_non_random_moves = 0
        self.num_random_moves = 0
        self.mode = mode
        self.player: Entity | None = None
        if mode == 'train':
            if not model_path:
                self.model_main = Linear_QNet(STATE_SIZE, 480, 5)  # State size, hidden size and output action size
                self.model_target = copy.deepcopy(self.model_main)
                self.trainer = QTrainer(self.model_main, lr=LR, gamma=self.gamma)
            else:
                # Load the model from the model path
                self.model_main = Linear_QNet(STATE_SIZE, 480, 5)
                self.model_main.load_state_dict(torch.load(model_path))
                self.model_target = copy.deepcopy(self.model_main)
                self.trainer = QTrainer(self.model_main, lr=LR, gamma=self.gamma)
        elif mode == 'test':
            if model_path is None:
                raise Exception("Model path cannot be None when mode is 'test'")
            self.model_main = Linear_QNet(STATE_SIZE, 480, 5)
            self.model_main.load_state_dict(torch.load(model_path))
            self.model_main.eval()


    def reset_game(self, simulation):
        self.player = simulation.get_entity_by_name('player')

    def get_bucketed_position(self, position_1: float, position_2: float) -> int:
        return int(position_1 - position_2 + AGENT_VIEWING_DISTANCE)

    def populate_state(self, state, entities):
        for entity in entities:
            bucket_position_x = self.get_bucketed_position(entity.position.x, self.player.position.x)
            bucket_position_y = self.get_bucketed_position(entity.position.y, self.player.position.y)
            # if 0 <= bucket_position_x < GRID_SIZE and 0 <= bucket_position_y < GRID_SIZE:
            state[bucket_position_x][bucket_position_y] += 1

    def get_nearby_entities(self, player, simulation, distance=AGENT_VIEWING_DISTANCE):
        entities_in_range = simulation.get_entities_in_range(player.position, distance)
        homestead = None
        enemies = []
        powerups = []
        for entity in entities_in_range:
            if entity.entity_type == 'homestead':
                homestead = entity
            elif entity.entity_type == 'powerup':
                powerups.append(entity)
            elif entity.entity_type == 'enemy':
                enemies.append(entity)
        return SimpleNamespace(homestead=homestead, enemies=enemies, powerups=powerups)

    def get_state(self, simulation: Simulation) -> np.ndarray:
        entities_in_range = self.get_nearby_entities(self.player, simulation)

        enemies_state = np.zeros((GRID_SIZE, GRID_SIZE))
        self.populate_state(enemies_state, entities_in_range.enemies)

        powerups_state = np.zeros((GRID_SIZE, GRID_SIZE))
        self.populate_state(powerups_state, entities_in_range.powerups)

        # Closest powerup
        closest_powerup = simulation.get_closest(self.player.position, 100, lambda x: x.entity_type == 'powerup')
        if closest_powerup:
            np_powerup_coords = np.array([1.0, (closest_powerup.position.x - self.player.position.x) / simulation.map_width, (closest_powerup.position.y - self.player.position.y) / simulation.map_length])
        else:
            np_powerup_coords = [0.0, 0.0, 0.0]

        homestead = simulation.get_closest(self.player.position, 100, lambda x: x.entity_type == 'homestead')
        if homestead:
            homestead_rel_coords = np.array([1.0, (homestead.position.x - self.player.position.x) / simulation.map_width, (homestead.position.y - self.player.position.y) / simulation.map_length])
        else:
            homestead_rel_coords = [0.0, 0.0, 0.0]

        return np.concatenate((enemies_state.flatten(), powerups_state.flatten(), np_powerup_coords, homestead_rel_coords))

    def get_action(self, state):
        final_move = [0, 0, 0, 0, 0]
        # random moves: tradeoff exploration / exploitation
        if random.uniform(0, 1) < self.epsilon and self.mode != 'test':
            self.num_random_moves += 1
            move = random.randint(0, 4)
        else:
            self.num_non_random_moves += 1
            state = torch.tensor(state, dtype=torch.float)
            # print(state)
            prediction = self.model_main(state)
            # print("prediction made")
            # print(prediction)
            move = torch.argmax(prediction).item()
            # print(move)
        final_move[int(move)] = 1
        return final_move

    def convert_action_to_vector(self, action):
        final_move = [
            Vector2(0, 1),  # Down
            Vector2(-1, 0),  # Left
            Vector2(0, -1),  # Up
            Vector2(1, 0),  # Right
        ]
        move_idx = action.index(1)
        # If move_idx == 4, it means just don't move
        actions = []
        if move_idx != 4:
            actions.append(MoveAction(self.player, final_move[action.index(1)]))
        return actions

    def play_step(self, action, simulation, time_delta):
        is_powerup = lambda e: e.entity_type == 'powerup'
        closest_powerup = simulation.get_closest(self.player.position, filter=is_powerup)
        prev_powerup_dist = self.player.position.distance_to(closest_powerup.position) if closest_powerup else None

        actions = self.convert_action_to_vector(action)
        simulation.update(time_delta, actions)

        done = False
        reward = 0
        for event_type, data in simulation.event_queue:
            if event_type == 'entity_destroyed':
                if data.entity_type == 'player':
                    reward += self.reward_system.player_killed
                    done = True
                if data.entity_type == 'homestead':
                    reward += self.reward_system.homestead_destroyed
                    done = True
                if data.entity_type == 'enemy':
                    reward += self.reward_system.enemy_killed
                if data.entity_type == 'powerup':
                    reward += self.reward_system.powerup_collected
            elif event_type == 'entity_attacked':
                if data['target'].entity_type in ('player', 'homestead'):
                    reward += self.reward_system.base_damage * data['damage']

        simulation.drain_events()

        if not self.player.is_destroyed:
            entities_in_danger_zone = self.get_nearby_entities(self.player, simulation, distance=DANGER_DISTANCE)
            reward += len(entities_in_danger_zone.enemies) * self.reward_system.nearby_enemy
            # For staying alive
            reward += self.reward_system.time_alive
            if closest_powerup and not closest_powerup.is_destroyed:
                closest_powerup_dist = self.player.position.distance_to(closest_powerup.position)

                reward += self.reward_system.powerup_distance * (prev_powerup_dist - closest_powerup_dist)

        return reward, done

    def train_short_memory(self, state, action, reward, next_state, model_target, done):
        self.trainer.train_step(state, action, reward, next_state, model_target, done)

    def train_long_memory(self, model_target):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        states = np.array(states)
        actions = np.array(actions)
        rewards = np.array(rewards)
        next_states = np.array(next_states)
        dones = np.array(dones)
        self.trainer.train_step(states, actions, rewards, next_states, model_target, dones)

    def remember(self, state, action, reward, next_state, done):
        # print(state)
        self.memory.append((state, action, reward, next_state, done))
    
    
