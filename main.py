import pygame
from pygame.locals import *
from snake import Snake
from apple import Apple

# Initialise pygame
pygame.init()


# Main menu function
def main_menu():
    pass


# Game loop function
def game_loop():
    pygame.init()
    clock = pygame.time.Clock()

    screen_width = 500
    screen_height = 500
    screen = pygame.display.set_mode((screen_width, screen_height))

    running = True

    snake = Snake(screen_width / 2, screen_height / 2)
    apple = Apple(screen_width, screen_height)

    collided = False

    while running:

        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        screen.fill((0, 0, 0))

        if apple is None:
            apple = Apple(screen_width, screen_height)

        screen.blit(apple.image, apple.rect)

        if pygame.sprite.collide_rect(snake.head, apple):
            snake.grow()
            apple = None

        pressed_keys = pygame.key.get_pressed()

        tail_collision = pygame.sprite.spritecollideany(
            snake.head, snake.tail_sprites)
        if tail_collision:
            collided = True
            running = False

        snake.update(pressed_keys, screen_width, screen_height)
        snake.draw(screen)

        pygame.display.update()

    return collided


# Run the game
main_menu()
collided = game_loop()

if collided:
    pygame.time.wait(5000)

# Shut down pygame once the game loop ends
pygame.quit()
