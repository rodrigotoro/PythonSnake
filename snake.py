import pygame
from pygame.locals import *

GREEN = (0, 255, 0)
CYAN = (0, 255, 255)


class SnakeSegment(pygame.sprite.Sprite):

    def __init__(self, size, pos_x, pos_y, colour=GREEN):
        super().__init__()
        self.size = size
        self.image = pygame.surface.Surface((self.size, self.size))
        self.colour = colour
        self.image.fill(self.colour)
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

    def update(self, pos_x, pos_y):
        self.rect.centerx = pos_x
        self.rect.centery = pos_y


class Snake():

    def __init__(self, pos_x, pos_y):
        self.size = 20
        self.speed = 3
        self.head = SnakeSegment(self.size, pos_x, pos_y, colour=CYAN)
        self.vel_x = 0
        self.vel_y = 0
        self.tail_pos_x = []
        self.tail_pos_y = []
        self.tail = []
        self.all_segments = pygame.sprite.Group()
        self.initial_tail_length = 2
        for _ in range(self.initial_tail_length):
            self.tail.append(SnakeSegment(self.size, pos_x, pos_y))
        self.all_segments.add(*self.tail, self.head)

        # Tail sprites grouped for collision detection
        self.tail_sprites = pygame.sprite.Group()

    def grow(self):
        last_segment_pos_x = self.tail[-1].rect.centerx
        last_segment_pos_y = self.tail[-1].rect.centery
        self.tail.append(SnakeSegment(
            self.size, last_segment_pos_x, last_segment_pos_y)
            )
        self.all_segments.add(self.tail[-1])
        self.tail_sprites.add(self.tail[-1])

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

    def update(self, pressed_keys, screen_width, screen_height):
        # Append head's position to history
        self.tail_pos_x.append(self.head.rect.centerx)
        self.tail_pos_y.append(self.head.rect.centery)

        # Update velocity based on pressed keys
        self.update_velocity(pressed_keys)

        # Update head position based on velocity
        self.head.rect.move_ip(self.vel_x, self.vel_y)

        # Enforce world limits
        if self.head.rect.right < 0:
            self.head.rect.left = screen_width
        if self.head.rect.left > screen_width:
            self.head.rect.right = 0
        if self.head.rect.bottom < 0:
            self.head.rect.top = screen_height
        if self.head.rect.top > screen_height:
            self.head.rect.bottom = 0

        # Update tail positions based on tail_pos arrays
        displacement = int(self.size / self.speed) + 1
        for i, segment in enumerate(self.tail):
            if len(self.tail_pos_x) > (i + 1) * displacement:
                segment.update(
                    self.tail_pos_x[- (i + 1) * displacement],
                    self.tail_pos_y[- (i + 1) * displacement])

        # Clean up tail_pos arrays
        tail_positions_length = len(self.tail_pos_x)
        required_length = (len(self.tail) + 1) * displacement
        if tail_positions_length > required_length:
            self.tail_pos_x = self.tail_pos_x[-required_length:]
            self.tail_pos_y = self.tail_pos_y[-required_length:]

    def draw(self, surface):
        self.all_segments.draw(surface)
