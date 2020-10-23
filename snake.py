import pygame
from pygame.locals import *
import random

GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
RED = (255, 0, 0)

# Initialise pygame
pygame.init()

# SnakeSegment and Snake classes
class SnakeSegment(pygame.sprite.Sprite):

    def __init__(self, size, pos_x, pos_y, colour=GREEN):
        super().__init__()
        self.size = size
        self.image = pygame.surface.Surface((self.size, self.size))
        self.colour = colour
        self.image.fill(self.colour)
        self.rect = self.image.get_rect(center = (pos_x, pos_y))


    def update(self, pos_x, pos_y):
        self.rect.centerx = pos_x
        self.rect.centery = pos_y


class Snake():

    def __init__(self, pos_x, pos_y):
        self.size = 20
        self.speed = 3
        self.head = SnakeSegment(self.size, pos_x, pos_y, colour = CYAN)
        self.vel_x = 0
        self.vel_y = 0
        self.tail_pos_x = []
        self.tail_pos_y = []
        self.tail = [] # tail segment objects go here
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
        self.tail.append(SnakeSegment(self.size, last_segment_pos_x, last_segment_pos_y))
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


# Apple class
class Apple(pygame.sprite.Sprite):

    def __init__(self, max_x, max_y):
        super().__init__()
        self.size = 10
        self.image = pygame.surface.Surface((self.size, self.size))
        self.image.fill(RED)
        self.pos_x = random.randint(0, max_x)
        self.pos_y = random.randint(0, max_y)
        self.rect = self.image.get_rect(center = (self.pos_x, self.pos_y))


# Main game loop function
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

        tail_collision = pygame.sprite.spritecollide(snake.head, snake.tail_sprites, dokill = False)
        if tail_collision:
            collided = True
            running = False

        snake.update(pressed_keys, screen_width, screen_height)
        snake.draw(screen)

        pygame.display.update()
    
    return collided


# Run the game
collided = game_loop()

if collided:
    pygame.time.wait(5000)

# Shut down pygame once the game loop ends
pygame.quit()