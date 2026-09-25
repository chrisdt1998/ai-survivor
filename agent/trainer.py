from agent.agent import Agent
from core.simulation import Simulation
import copy

import matplotlib.pyplot as plt
from IPython import display

plt.ion()


def plot(scores, mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    # plt.ylim(ymin=0)
    plt.text(len(scores) - 1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores) - 1, mean_scores[-1], str(mean_scores[-1]))
    plt.show(block=False)
    plt.pause(.1)



def train(show_visuals=True, model_path=None, nbr_games=20000):
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    current_score = 0
    # agent = Agent(mode='train', model_path=model_path)
    simulation = Simulation()
    agent = Agent(mode='train', )
    current_iter = 0
    while current_iter < 20000:
        # Get previous state
        state_old = agent.get_state(simulation)

        # Get move
        final_move = agent.get_action(state_old)

        # Perform move and get new state
        reward, done = agent.play_step(final_move, simulation)
        state_new = agent.get_state(simulation)

        # Train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, agent.model_target, done)

        # Store state, action and reward
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # Train long memory, plot result
            simulation = Simulation()
            agent.epsilon = agent.epsilon - agent.epsilon_decay if agent.epsilon > agent.epsilon_min else agent.epsilon_min
            agent.n_games += 1
            agent.train_long_memory(agent.model_target)

            if current_score > record:
                record = current_score
                print("Saving top scoring model")
                agent.model_main.save(file_name='top_scoring_model.pth')

            if agent.n_games % 1000 == 0:
                print(f"Saving model at {agent.n_games} games")
                agent.model_main.save(file_name=f'{agent.n_games}_model.pth')

            print('Game', agent.n_games, 'Score', current_score, 'Record:', record, 'Epsilon:', agent.epsilon)
            print('Non-random moves:', agent.num_non_random_moves, 'Random moves:', agent.num_random_moves, '% Random:', agent.num_random_moves / (agent.num_non_random_moves + agent.num_random_moves) * 100, '% Non-random:', agent.num_non_random_moves / (agent.num_non_random_moves + agent.num_random_moves) * 100)
            agent.num_non_random_moves = 0
            agent.num_random_moves = 0

            plot_scores.append(current_score)
            total_score += current_score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)
            current_score = 0

        current_iter += 1
        if current_iter % 2000 == 0:
            print("Updating model target")
            agent.model_target = copy.deepcopy(agent.model_main)