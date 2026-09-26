import copy
import random
from collections import deque
from types import SimpleNamespace
from core.actions.action import MoveAction
from core.vector2 import Vector2

import numpy as np
import torch
from agent.model import Linear_QNet, QTrainer

from core.simulation import Simulation

AGENT_VIEWING_DISTANCE = 4.5
DANGER_DISTANCE = 0.5
GRID_SIZE = int(AGENT_VIEWING_DISTANCE * 2)
STATE_SIZE = 3 * GRID_SIZE * GRID_SIZE  # (enemies + player + powerups) * GRID_SIZE * GRID_SIZE
MAX_MEMORY = 20000
BATCH_SIZE = 32
LR = 0.00001


class Agent:
    reward_system = SimpleNamespace(
        player_killed=-10,
        homestead_destroyed=-10,
        enemy_killed=0.1,
        powerup_collected=0.5,
        base_damage=-0.1,
        nearby_enemy=-0.05,
        nearby_powerup=0.1,
    )

    def __init__(self, mode='test', model_path='') -> None:
        self.n_games = 0
        # self.epsilon = 1
        self.epsilon = 0.25
        self.epsilon_decay = 0.00005
        self.epsilon_min = 0.01
        self.gamma = 0.99  # Discount rate, should be smaller than 1
        self.memory = deque(maxlen=MAX_MEMORY)
        self.num_non_random_moves = 0
        self.num_random_moves = 0
        self.mode = mode
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

    def get_bucketed_position(self, position_1: float, position_2: float) -> int:
        return int(position_1 - position_2 + AGENT_VIEWING_DISTANCE)

    def populate_state(self, state, entities):
        for entity in entities:
            bucket_position_x = self.get_bucketed_position(entity.position.x, entity.position.x)
            bucket_position_y = self.get_bucketed_position(entity.position.y, entity.position.y)

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
        player = simulation.get_entity_by_name('player')
        entities_in_range = self.get_nearby_entities(player, simulation)

        # Player and boundary
        player_state = np.zeros((GRID_SIZE, GRID_SIZE))
        player_state[GRID_SIZE // 2][GRID_SIZE // 2] = 1
        if entities_in_range.homestead:
            self.populate_state(player_state, [entities_in_range.homestead])
        # TODO: Do the boundary?

        enemies_state = np.zeros((GRID_SIZE, GRID_SIZE))
        self.populate_state(enemies_state, entities_in_range.enemies)

        powerups_state = np.zeros((GRID_SIZE, GRID_SIZE))
        self.populate_state(powerups_state, entities_in_range.powerups)
        return np.concatenate((player_state.flatten(), enemies_state.flatten(), powerups_state.flatten()))

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
            # print(prediction)
            move = torch.argmax(prediction).item()
            # print(move)
        final_move[int(move)] = 1
        return final_move

    def play_step(self, action, simulation, time_delta):
        player = simulation.get_entity_by_name('player')
        final_move = [
            Vector2(0, 1),  # Down
            Vector2(-1, 0),  # Left
            Vector2(0, -1),  # Up
            Vector2(1, 0),  # Right
        ]
        move_idx = action.index(1)
        # If move_idx == 4, it means just don't move
        if move_idx != 4:
            action = MoveAction(player, final_move[action.index(1)])
            simulation.update(time_delta, [action])
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
            # TODO: also add reward for damage done to base/player

        simulation.drain_events()

        entities_in_danger_zone = self.get_nearby_entities(player, simulation, distance=DANGER_DISTANCE)
        reward += len(entities_in_danger_zone.enemies) * self.reward_system.nearby_enemy
        reward += len(entities_in_danger_zone.powerups) * self.reward_system.nearby_powerup
        # For staying alive
        reward += 0.001

        return reward, done

    def train_short_memory(self, state, action, reward, next_state, model_target, done):
        self.trainer.train_step(state, action, reward, next_state, model_target, done)

    def train_long_memory(self, model_target):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, model_target, dones)

    def remember(self, state, action, reward, next_state, done):
        # print(state)
        self.memory.append((state, action, reward, next_state, done))
    
    
