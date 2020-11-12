import pygame
import random

RED = (255, 0, 0)


class Apple(pygame.sprite.Sprite):

    def __init__(self, max_x, max_y):
        super().__init__()
        self.size = 10
        self.image = pygame.surface.Surface((self.size, self.size))
        self.image.fill(RED)
        self.pos_x = random.randint(0, max_x)
        self.pos_y = random.randint(0, max_y)
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
