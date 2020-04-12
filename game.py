import pygame

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_w,
)

from sprites.apple import Apple
from sprites.snake import Snake
from common.constants import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
snake = Snake()
apple = Apple()
apple.create_new_apple(snake)
clock = pygame.time.Clock()
font = pygame.font.SysFont('monospace', 16)
score_color = (255, 255, 255)
fps = 15
score = 0

with open('scores.txt', 'r+') as fp:
    max_score = fp.read()

running = True

while running:
    clock.tick(fps)
    pressed_keys = pygame.key.get_pressed()

    if snake.detect_apple_collision(apple.rect):
        snake.add_body()
        apple.create_new_apple(snake)
        fps = fps + 1
        score = score + 10

    if snake.detect_body_collision():
        running = False
    elif snake.detect_wall_collision():
        running = False

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    screen.fill((0, 0, 0))
    for surf in snake.body:
        screen.blit(surf[0], surf[1])

    screen.blit(apple.surf, apple.rect)
    
    score_text = font.render(f'Score {score}', 1, score_color)
    max_score_text = font.render(f'High Score {max_score}', 1, score_color)
    screen.blit(score_text, (0, 0))
    screen.blit(max_score_text, (100, 0))
    snake.update(pressed_keys)
    pygame.display.flip()

if score > int(max_score):
    with open('scores.txt', 'w') as fp:
        fp.write(str(score))

pygame.quit()
