import pygame
import random
from pygame.sprite import Sprite
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    RLEACCEL,
)
from common.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SNAKE_BLOCK_WIDTH,
    SNAKE_BLOCK_HEIGHT,
)

LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'

SNAKE_INITIAL_LENGTH = 10
SNAKE_BODY_COLOR = (0, 102, 0)

START_CENTER_X = random.randint(0, SCREEN_WIDTH)
START_CENTER_Y = random.randint(0, SCREEN_HEIGHT)

INITIAL_DIRECTION = LEFT


class Snake(Sprite):
    def __init__(self):
        super(Snake, self).__init__()
        self.body = []
        self.turns = []
        # self.surf = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('images/jet.png'), (50, 50)),
        # -90)\ .convert() self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        for i in range(SNAKE_INITIAL_LENGTH):
            surf = pygame.Surface((SNAKE_BLOCK_WIDTH, SNAKE_BLOCK_HEIGHT))
            surf.fill(SNAKE_BODY_COLOR)
            rect = surf.get_rect(
                center=(
                    (START_CENTER_X + SNAKE_BLOCK_WIDTH / 2) + i * SNAKE_BLOCK_WIDTH,
                    (START_CENTER_Y + SNAKE_BLOCK_WIDTH / 2)
                )
            )
            self.body.append([surf, rect, INITIAL_DIRECTION])

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            if self.body[0][2] != DOWN:
                self.turns.append((UP, self.body[0][1].center))
        if pressed_keys[K_DOWN]:
            if self.body[0][2] != UP:
                self.turns.append((DOWN, self.body[0][1].center))
        if pressed_keys[K_LEFT]:
            if self.body[0][2] != RIGHT:
                self.turns.append((LEFT, self.body[0][1].center))
        if pressed_keys[K_RIGHT]:
            if self.body[0][2] != LEFT:
                self.turns.append((RIGHT, self.body[0][1].center))

        # Move

        for i in range(len(self.body)):
            for turn in self.turns:
                if self.body[i][1].center == turn[1]:
                    direction = turn[0]
                    self.body[i][2] = direction
                    if i == len(self.body) - 1:
                        self.turns.remove(turn)

            self.move_body_part(self.body[i], self.body[i][2])

    @staticmethod
    def move_body_part(body_part, direction):
        if direction == UP:
            body_part[1].move_ip(0, -SNAKE_BLOCK_WIDTH)
        elif direction == DOWN:
            body_part[1].move_ip(0, SNAKE_BLOCK_WIDTH)
        elif direction == LEFT:
            body_part[1].move_ip(-SNAKE_BLOCK_WIDTH, 0)
        elif direction == RIGHT:
            body_part[1].move_ip(SNAKE_BLOCK_WIDTH, 0)

    def add_body(self):
        tail = self.body.pop(len(self.body) - 1)
        surf = pygame.Surface((SNAKE_BLOCK_WIDTH, SNAKE_BLOCK_HEIGHT))
        surf.fill(SNAKE_BODY_COLOR)
        rect = surf.get_rect(center=tail[1].center)
        self.body.append([surf, rect, tail[2]])
        self.move_body_part(tail, self.opposite(tail[2]))
        self.body.append(tail)

    @staticmethod
    def opposite(direction):
        if direction == UP:
            return DOWN
        elif direction == DOWN:
            return UP
        elif direction == LEFT:
            return RIGHT
        elif direction == RIGHT:
            return LEFT

    def detect_body_collision(self):
        for i in range(1, len(self.body)):
            if self.body[0][1].colliderect(self.body[i][1]):
                return True
        return False

    def detect_apple_collision(self, apple_rect):
        if self.body[0][1].colliderect(apple_rect):
            return True
        else:
            return False

    def detect_wall_collision(self):
        if self.body[0][1].left < 0:
            return True
        elif self.body[0][1].right > SCREEN_WIDTH:
            return True
        elif self.body[0][1].top < 0:
            return True
        elif self.body[0][1].bottom > SCREEN_HEIGHT:
            return True
        else:
            return False

    @property
    def head(self):
        return self.body[0]
