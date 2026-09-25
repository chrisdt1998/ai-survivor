from game.player_controller import PlayerController
from game.renderer import Renderer
from core.simulation import Simulation
import pygame

def run_render():
    pygame.init()

    simulation = Simulation()
    renderer = Renderer(simulation)
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
            if event.type == pygame.WINDOWRESIZED:
                print("resized")

        simulation.update(delta_time, actions)
        simulation.drain_events()
        renderer.render(delta_time)

        delta_time = clock.tick(60) / 1000

    pygame.quit()
