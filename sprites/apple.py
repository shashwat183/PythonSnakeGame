import random

import pygame
from pygame.sprite import Sprite

from common.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    APPLE_WIDTH,
    APPLE_HEIGHT,
)


class Apple(Sprite):
    def __init__(self):
        super(Apple, self).__init__()
        self.surf = pygame.Surface((APPLE_WIDTH, APPLE_HEIGHT))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect()

    def create_new_apple(self, snake):
        collision = True
        while collision:
            center = self.create_center()
            self.surf = pygame.Surface((APPLE_WIDTH, APPLE_HEIGHT))
            self.surf.fill((255, 0, 0))
            self.rect = self.surf.get_rect(center=center)
            for i in range(1, len(snake.body)):
                if snake.body[i][1].colliderect(self.rect):
                    collision = True
                    break
                else:
                    collision = False

    @staticmethod
    def create_center():
        return (
            random.randint(0 + APPLE_WIDTH, SCREEN_WIDTH - APPLE_WIDTH),
            random.randint(0 + APPLE_HEIGHT, SCREEN_HEIGHT - APPLE_HEIGHT)
        )