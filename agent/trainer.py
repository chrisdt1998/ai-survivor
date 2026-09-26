from agent.agent import Agent
from core.simulation import Simulation
import copy

import matplotlib.pyplot as plt
# from IPython import display
from game.renderer import Renderer

FPS = 15
TIME_DELTA = 1 / FPS
PLOT_FILE = 'agent/training_plot.png'
PLOT_SAVE_INTERVAL = 10

def plot(scores, mean_scores, show=False, save=False):
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.text(len(scores) - 1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores) - 1, mean_scores[-1], str(mean_scores[-1]))
    if save:
        plt.savefig(PLOT_FILE)
    if show:
        plt.pause(0.001)


def train(renderer: Renderer | None = None, model_path='', nbr_games=20000, show_plot=False):
    if show_plot:
        plt.ion()
    else:
        # Non-interactive backend: no window, works headless
        plt.switch_backend('Agg')
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    current_score = 0
    # agent = Agent(mode='train', model_path=model_path)
    simulation = Simulation()
    agent = Agent(mode='train', model_path=model_path)
    agent.reset_game(simulation)
    if renderer:
        renderer.set_simulation(simulation)
    current_iter = 0
    while agent.n_games < nbr_games:
        # Get previous state
        state_old = agent.get_state(simulation)

        # Get move
        final_move = agent.get_action(state_old)

        # Perform move and get new state
        reward, done = agent.play_step(final_move, simulation, TIME_DELTA)
        current_score += reward
        if renderer:
            renderer.render(TIME_DELTA)
        state_new = agent.get_state(simulation)

        # Train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, agent.model_target, done)

        # Store state, action and reward
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # Train long memory, plot result
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
            save_plot = agent.n_games % PLOT_SAVE_INTERVAL == 0
            if show_plot or save_plot:
                plot(plot_scores, plot_mean_scores, show=show_plot, save=save_plot)
            simulation = Simulation()
            agent.reset_game(simulation)
            if renderer:
                renderer.set_simulation(simulation)
            current_score = 0

        current_iter += 1
        if current_iter == 1:
            agent.model_main.save(file_name='initial_test_save.pth')
        if current_iter % 2000 == 0:
            print("Updating model target")
            agent.model_target = copy.deepcopy(agent.model_main)