import pygame
import sys
from pygame.locals import *

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
    
    def move(self, keys):
        if keys[K_LEFT] or keys[K_a]:
            self.x -= self.speed
        if keys[K_RIGHT] or keys[K_d]:
            self.x += self.speed

        # Limita la barra all'interno della finestra di gioco
        if self.x < 0:
            self.x = 0
        if self.x > width - self.width:
            self.x = width - self.width
    
    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))

class Ball:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.direction_x = 1
        self.direction_y = -1
    
    def move(self):
        self.x += self.speed * self.direction_x
        self.y += self.speed * self.direction_y

        # Rimbalzo sui bordi
        if self.x < self.radius or self.x > width - self.radius:
            self.direction_x *= -1
        if self.y < self.radius:
            self.direction_y *= -1
        
        # Controllo collisione con la barra
        if self.y + self.radius > paddle.y and self.x > paddle.x and self.x < paddle.x + paddle.width:
            self.direction_y *= -1
        
        # Controllo se la palla è caduta
        if self.y > height:
            game_over()

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius)

def game_over():
    pygame.quit()
    sys.exit()

paddle_width = 100
paddle_height = 10
paddle_speed = 1
paddle = Paddle(width // 2 - paddle_width // 2, height - paddle_height - 10, paddle_width, paddle_height, paddle_speed)

ball_radius = 10
ball_speed = 0.5
ball = Ball(width // 2, height // 2, ball_radius, ball_speed)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            game_over()

    keys = pygame.key.get_pressed()
    paddle.move(keys)
    ball.move()

    screen.fill((0, 0, 0))
    paddle.draw()
    ball.draw()

    pygame.display.update()
