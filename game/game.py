from game.player_controller import PlayerController
from game.renderer import Renderer
from core.simulation import Simulation
import pygame

def run():
    pygame.init()

    renderer = Renderer()
    simulation = Simulation()
    clock = pygame.time.Clock()
    running = True
    delta_time = 0

    player = simulation.get_entity_by_name("player")
    player_controller = PlayerController()

    while running:
        commands = player_controller.get_commands(player.id)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        simulation.update(delta_time, commands)
        renderer.render(simulation)
        delta_time = clock.tick(60) / 1000

    pygame.quit()
