import pygame
from pygame.locals import *


class Button(pygame.sprite.Sprite):

    def __init__(self, position, size, colour, text, text_colour, action=None):
        super().__init__()
        self.pos_x = position[0]
        self.pos_y = position[1]
        self.size_x = size[0]
        self.size_y = size[1]
        self.colour = colour
        self.image = pygame.surface.Surface((self.size_x, self.size_y))
        self.image.fill(self.colour)
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
        self.font = pygame.font.Font(None, int(self.size_y * 0.7))
        self.font_image = self.font.render(text, True, text_colour)
        self.font_rect = self.font_image.get_rect(
            center=(self.pos_x, self.pos_y)
            )
        self.action = action

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.font_image, self.font_rect)

    def on_click(self):
        if self.action is not None:
            return self.action()

    def update(self, mouse_clicked):
        if mouse_clicked:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.on_click()


if __name__ == "__main__":

    pygame.init()

    screen = pygame.display.set_mode((800, 800))

    button = Button(
        position=(400, 400),
        size=(150, 50),
        colour=(250, 200, 100),
        text="button",
        text_colour=(0, 0, 0),
        action=lambda: print("You clicked the button!")
    )

    running = True

    hello_counter = 0

    while running:

        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEBUTTONUP:
                mouse_clicked = True

        button.draw(screen)
        button.update(mouse_clicked)

        pygame.display.update()

    pygame.quit()
