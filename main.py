import pygame
from pygame.locals import *

# Define window properties
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("The OG Python Snake!")

# Snake class
class Snake(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__
        self.surface = pygame.Surface((20, 20))
        self.surface.fill((100, 255, 100))
        self.rect = self.surface.get_rect()
        self.rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        self.speed = 5
        self.velocity_x = 0
        self.velocity_y = 0
        # self.segments = ["segment1", "segment2"]
        # self.trail_positions = [(x, y), (x, y)]


    def update(self, pressed_keys):
        """Update the snake's position and enforce world boundaries.
        """
        
        # Update the snake's velocity
        # Don't allow the snake to change direction 180 degs
        if pressed_keys[K_RIGHT] and self.velocity_x != -self.speed:
            self.velocity_x = self.speed
            self.velocity_y = 0
        if pressed_keys[K_LEFT] and self.velocity_x != self.speed:
            self.velocity_x = -self.speed
            self.velocity_y = 0
        if pressed_keys[K_UP] and self.velocity_y != self.speed:
            self.velocity_x = 0
            self.velocity_y = -self.speed
        if pressed_keys[K_DOWN] and self.velocity_y != -self.speed:
            self.velocity_x = 0
            self.velocity_y = self.speed

        # Change position based on x and y velocity
        self.rect.move_ip(self.velocity_x, self.velocity_y)

        # Set world boundaries
        if self.rect.right < 0:
            self.rect.left = WINDOW_WIDTH
        if self.rect.left > WINDOW_WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = WINDOW_HEIGHT
        if self.rect.top > WINDOW_HEIGHT:
            self.rect.bottom = 0


def main():
    """
    Game loop
    """

    # Initialise game clock to control framerate
    clock = pygame.time.Clock()

    # Set game state
    running = True

    # Instantiate snake
    snake = Snake()

    while running:
        # Set framerate
        clock.tick(60)

        # Logic to exit the game
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        # Draw background
        window.fill((0, 0, 0))

        # Update snake's position
        snake.update(pygame.key.get_pressed())

        # Draw snake on main window
        window.blit(snake.surface, snake.rect)

        # Update display
        pygame.display.update()


# Run game loop
main()

# Quit nicely when game loop finishes
pygame.quit()