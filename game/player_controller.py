from core.vector2 import Vector2
from core.actions.action import MoveAction
import pygame

class PlayerController:

    def get_commands(self, player_id: int) -> list:
        keys = pygame.key.get_pressed()

        direction = Vector2()
        if keys[pygame.K_w] or keys[pygame.K_z]:
            direction.y -= 1
        if keys[pygame.K_s]:
            direction.y += 1
        if keys[pygame.K_a] or keys[pygame.K_q]:
            direction.x -= 1
        if keys[pygame.K_d]:
            direction.x += 1
        
        if direction.length() > 0:
            return [MoveAction(player_id, direction)]
        else:
            return []
        

