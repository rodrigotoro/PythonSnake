import pygame
from pygame.locals import *

class SnakeSegment(pygame.sprite.Sprite):

    def __init__(self, size, pos_x, pos_y, colour=(100, 255, 100)):
        super().__init__()
        self.size = size
        self.image = pygame.surface.Surface((self.size, self.size))
        self.colour = colour
        self.image.fill(self.colour)
        self.rect = self.image.get_rect(center = (pos_x, pos_y))


    def update(self, pos_x, pos_y):
        self.rect.move_ip(pos_x, pos_y)


class Snake():

    def __init__(self, pos_x, pos_y):
        self.size = 20
        self.speed = 1
        self.head = SnakeSegment(self.size, pos_x, pos_y, colour = (200, 255, 200))
        self.vel_x = 0
        self.vel_y = 0
        self.tail_pos_x = []
        self.tail_pos_y = []
        self.tail = pygame.sprite.Group()
        self.tail.add(SnakeSegment(self.size, pos_x, pos_y))

        
    def update_velocity(self, pressed_keys):
        if pressed_keys[K_RIGHT] and self.vel_x != -self.speed:
            self.vel_x = self.speed
            self.vel_y = 0
        if pressed_keys[K_LEFT] and self.vel_x != self.speed:
            self.vel_x = -self.speed
            self.vel_y = 0
        if pressed_keys[K_UP] and self.vel_y != self.speed:
            self.vel_x = 0
            self.vel_y = -self.speed
        if pressed_keys[K_DOWN] and self.vel_y != -self.speed:
            self.vel_x = 0
            self.vel_y = self.speed


    def update(self, pressed_keys):
        # Append head's position to history
        self.tail_pos_x.append(self.head.rect.centerx)
        self.tail_pos_y.append(self.head.rect.centery)

        # Update velocity based on pressed keys
        self.update_velocity(pressed_keys)

        # Update head position based on velocity
        self.head.rect.move_ip(self.vel_x, self.vel_y)

        # Update tail positions based on tail_pos arrays
        for i, segment in enumerate(self.tail.sprites()):
            segment.update(self.tail_pos_x[-i * 1000], self.tail_pos_y[-i * 1000])


    def draw(self, surface):
        surface.blit(self.head.image, self.head.rect)
        self.tail.draw(surface)


if __name__ == "__main__":
    pygame.init()

    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 500
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    running = True

    snake = Snake(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

    while running:

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        
        screen.fill((0, 0, 0))
        
        pressed_keys = pygame.key.get_pressed()

        snake.update(pressed_keys)
        snake.draw(screen)

        pygame.display.update()