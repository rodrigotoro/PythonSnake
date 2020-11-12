import pygame
from pygame.locals import *
from snake import Snake
from apple import Apple
from button import Button


# Main menu function
def main_menu():
    running = True
    end_game = False

    def next_scene():
        nonlocal running
        running = False

    while running:
        CLOCK.tick(30)
        pressed_keys = pygame.key.get_pressed()
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == QUIT or pressed_keys[K_ESCAPE]:
                running = False
                end_game = True
            if event.type == MOUSEBUTTONUP:
                mouse_clicked = True

        SCREEN.fill((0, 0, 0))

        title_font = pygame.font.Font(None, 60)
        title_image = title_font.render("PYTHON SNAKE", True, (0, 255, 0))
        title_rect = title_image.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
        SCREEN.blit(title_image, title_rect)

        start_game_button = Button(
            position=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50),
            size=(200, 50),
            colour=(0, 255, 0),
            text="Start Game",
            text_colour=(0, 0, 0),
            action=next_scene
        )
        start_game_button.draw(SCREEN)
        start_game_button.update(mouse_clicked)

        pygame.display.update()

    return end_game



# Game loop function
def game_loop():
    running = True

    snake = Snake(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    apple = Apple(SCREEN_WIDTH, SCREEN_HEIGHT)
    score = 0

    collided = False

    while running:
        CLOCK.tick(60)
        pressed_keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT or pressed_keys[K_ESCAPE]:
                running = False

        SCREEN.fill((0, 0, 0))

        if apple is None:
            apple = Apple(SCREEN_WIDTH, SCREEN_HEIGHT)

        SCREEN.blit(apple.image, apple.rect)

        if pygame.sprite.collide_rect(snake.head, apple):
            score += 1
            print(score)
            snake.grow()
            apple = None

        tail_collision = pygame.sprite.spritecollideany(
            snake.head, snake.tail_sprites)
        if tail_collision:
            collided = True
            running = False

        snake.update(pressed_keys, SCREEN_WIDTH, SCREEN_HEIGHT)
        snake.draw(SCREEN)

        pygame.display.update()

    return collided


# Initialise game
pygame.init()
CLOCK = pygame.time.Clock()
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Run game
end_game = main_menu()

if not end_game:
    collided = game_loop()

if collided:
    pygame.time.wait(5000)

# Shut down pygame
pygame.quit()
