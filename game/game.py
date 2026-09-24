from game.player_controller import PlayerController
from game.renderer import Renderer
from core.simulation import Simulation
import pygame

def run_render():
    pygame.init()

    renderer = Renderer()
    simulation = Simulation()
    clock = pygame.time.Clock()
    running = True
    delta_time = 0

    player = simulation.get_entity_by_name("player")
    player_controller = PlayerController()

    while running:
        actions = player_controller.get_actions(player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        simulation.update(delta_time, actions)
        renderer.render(delta_time, simulation)
        delta_time = clock.tick(60) / 1000

    pygame.quit()
