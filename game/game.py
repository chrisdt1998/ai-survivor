from game.renderer import Renderer
from core.simulation import Simulation
from agent.agent import Agent


def run_render():
    simulation = Simulation()
    renderer = Renderer()
    renderer.set_simulation(simulation)
    renderer.run()


def run_with_agent():
    simulation = Simulation()
    renderer = Renderer()
    agent = Agent(mode='test', model_path='agent/checkpoints/500_model.pth')
    agent.reset_game(simulation)
    renderer.set_simulation(simulation)
    print('running with agent')
    renderer.run(agent)
