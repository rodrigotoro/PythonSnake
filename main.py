import pygame
from pygame.locals import *
from snake import Snake
from apple import Apple
from button import Button
from score_manager import ScoreManager


# Main menu function
def main_menu():
    running = True
    framerate = 30
    end_game = False

    def next_scene():
        nonlocal running
        running = False

    title_font = pygame.font.SysFont("courier", 60)

    while running:
        CLOCK.tick(framerate)
        pressed_keys = pygame.key.get_pressed()
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == QUIT or pressed_keys[K_ESCAPE]:
                running = False
                end_game = True
            if event.type == MOUSEBUTTONUP:
                mouse_clicked = True

        SCREEN.fill((0, 0, 0))


        title_1_image = title_font.render("PYTHON", True, (0, 255, 0))
        title_1_rect = title_1_image.get_rect(
            center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 120))
        SCREEN.blit(title_1_image, title_1_rect)


        title_2_image = title_font.render("SNAKE", True, (0, 255, 0))
        title_2_rect = title_2_image.get_rect(
            center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
        SCREEN.blit(title_2_image, title_2_rect)

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
    framerate = 60
    running = True
    paused = False

    snake = Snake(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    apple = Apple(SCREEN_WIDTH, SCREEN_HEIGHT)

    global SCORE
    score_font = pygame.font.Font(None, 40)

    collided = False

    while running:
        CLOCK.tick(framerate)
        pressed_keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            if event.type == KEYDOWN and event.key == K_SPACE:
                paused = not paused

        SCREEN.fill((0, 0, 0))

        if apple is None:
            apple = Apple(SCREEN_WIDTH, SCREEN_HEIGHT)

        SCREEN.blit(apple.image, apple.rect)

        if pygame.sprite.collide_rect(snake.head, apple):
            SCORE += 1
            snake.grow()
            apple = None

        tail_collision = pygame.sprite.spritecollideany(
            snake.head, snake.tail_sprites)
        if tail_collision:
            collided = True
            running = False

        if not paused:
            snake.update(pressed_keys, SCREEN_WIDTH, SCREEN_HEIGHT)
        snake.draw(SCREEN)

        # Display Score
        score_image = score_font.render(str(SCORE), True, (255, 250, 50))
        score_rect = score_image.get_rect(top=10, right=SCREEN_WIDTH-20)
        SCREEN.blit(score_image, score_rect)

        pygame.display.update()


# Game over scene
def game_over():
    running = True
    framerate = 30

    game_over_font = pygame.font.Font(None, 60)
    game_over_displayed_frames = 0
    game_over_display_time = framerate * 3

    player_name = ""

    while running:
        CLOCK.tick(framerate)

        for event in pygame.event.get():
            # Exit behaviours
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

            # Name input mechanic
            if event.type == KEYDOWN and event.key != K_ESCAPE:
                if event.key == K_BACKSPACE:
                    player_name = player_name[:-1]
                if event.key == K_RETURN:
                    if len(player_name) > 0:
                        SCORE_MANAGER.add_score(player_name, SCORE)
                        running = False
                if len(player_name) < 10:
                    player_name += event.unicode.upper()

        SCREEN.fill((0, 0, 0))

        # Display game over message
        if game_over_displayed_frames < game_over_display_time:
            game_over_image = game_over_font.render(
                "GAME OVER",
                True,
                (0, 255, 0))
            game_over_rect = game_over_image.get_rect(
                center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

            SCREEN.blit(game_over_image, game_over_rect)
            game_over_displayed_frames += 1

        # Final score and name prompt
        if game_over_displayed_frames == game_over_display_time:
            score_text_image = game_over_font.render(
                f"Score: {SCORE}",
                True,
                (0, 255, 0)
                )
            score_text_rect = score_text_image.get_rect(
                center=(SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 150)
            )
            SCREEN.blit(score_text_image, score_text_rect)

            game_over_image = game_over_font.render(
                "Type your name",
                True,
                (0, 255, 0)
            )
            game_over_rect = game_over_image.get_rect(
                center=(SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 50)
            )
            SCREEN.blit(game_over_image, game_over_rect)

            player_name_image = game_over_font.render(
                player_name.upper(),
                True,
                (255, 255, 255)
            )
            player_name_rect = player_name_image.get_rect(
                center=(SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + 50)
            )
            SCREEN.blit(player_name_image, player_name_rect)

        pygame.display.update()


# Highscore Scene
def highscores():
    running = True
    framerate = 30

    score_title_font = pygame.font.Font(None, 100)
    score_font = pygame.font.Font(None, 50)

    highscores = SCORE_MANAGER.get_scores()

    while running:
        CLOCK.tick(framerate)

        for event in pygame.event.get():
            # Exit behaviours
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        SCREEN.fill((0, 0, 0))

        score_title_image = score_title_font.render("High Scores", True, (0, 255, 0))
        score_title_rect = score_title_image.get_rect(
            center=(SCREEN_WIDTH/2, 120)
        )
        SCREEN.blit(score_title_image, score_title_rect)

        for i, highscore in enumerate(highscores):
            if i == 0:
                font_colour = (255, 215, 0)
            elif i == 1:
                font_colour = (192, 192, 192)
            elif i == 2:
                font_colour = (205, 127, 50)
            else:
                font_colour = (0, 255, 0)
            highscore_name = highscore[1]
            highscore_number = str(highscore[2])
            highscore_name_image = score_font.render(highscore_name, True, font_colour)
            highscore_number_image = score_font.render(highscore_number, True, font_colour)
            x = SCREEN_WIDTH / 2
            y = 150 + (70 * (i + 1))
            highscore_name_rect = highscore_name_image.get_rect(right=x, top=y)
            highscore_number_rect = highscore_number_image.get_rect(left=x+20, top=y)

            SCREEN.blit(highscore_name_image, highscore_name_rect)
            SCREEN.blit(highscore_number_image, highscore_number_rect)

        pygame.display.update()



# Initialise game
pygame.init()
CLOCK = pygame.time.Clock()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCORE = 0

# Initialise score_manager
SCORE_MANAGER = ScoreManager()
SCORE_MANAGER.connect()

# Run game
end_game = main_menu()

if not end_game:
    score = game_loop()

game_over()
highscores()

# Shut down the game
SCORE_MANAGER.disconnect()
pygame.quit()
