from game.renderer import Renderer
from core.simulation import Simulation

def run_render():
    simulation = Simulation()
    renderer = Renderer()
    renderer.set_simulation(simulation)
    renderer.run()
