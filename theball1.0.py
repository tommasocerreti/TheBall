import pygame
import sys
from pygame.locals import *

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1
        self.radius = 20
    
    def move(self, keys):
        if keys[K_w] and self.y > self.radius:
            self.y -= self.speed
        if keys[K_s] and self.y < height - self.radius:
            self.y += self.speed
        if keys[K_a] and self.x > self.radius:
            self.x -= self.speed
        if keys[K_d] and self.x < width - self.radius:
            self.x += self.speed

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius)

ball = Ball(width // 2, height // 2)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    ball.move(keys)

    screen.fill((0, 0, 0))
    ball.draw()

    pygame.display.update()
