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
        self.touch_count = 0  # Contatore dei tocchi
        
    def move(self):
        self.x += self.speed * self.direction_x
        self.y += self.speed * self.direction_y

        # Rimbalzo sui bordi
        if self.x < self.radius or self.x > width - self.radius:
            self.direction_x *= -1
            self.touch_count += 1  # Incremento del contatore dei tocchi
        if self.y < self.radius:
            self.direction_y *= -1
            self.touch_count += 1  # Incremento del contatore dei tocchi
        
        # Controllo collisione con la barra
        if self.y + self.radius > paddle.y and self.x > paddle.x and self.x < paddle.x + paddle.width:
            self.direction_y *= -1
        
        # Controllo se la palla è caduta
        if self.y > height:
            game_over()
            
        # Aggiornamento del punteggio
        global score
        score = self.touch_count

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius)
        
    
def game_over():
    font = pygame.font.SysFont("Arial", 50)
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    play_again_text = font.render("Press Enter to Play Again", True, (255, 255, 255))
    text_rect = game_over_text.get_rect(center=(width // 2, height // 2))
    play_again_rect = play_again_text.get_rect(center=(width // 2, height // 2 + 50))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_RETURN:  # Modifica dell'evento da MOUSEBUTTONDOWN a KEYDOWN e verifica del tasto Enter
                return  # Uscita dalla funzione game_over per riavviare una nuova partita
    
        screen.fill((0, 0, 0))
        screen.blit(game_over_text, text_rect)
        screen.blit(play_again_text, play_again_rect)
        pygame.display.update()
        
def reset_game():
    global paddle, ball
    paddle = Paddle(width // 2 - paddle_width // 2, height - paddle_height - 10, paddle_width, paddle_height, paddle_speed)
    ball = Ball(width // 2, height // 2, ball_radius, ball_speed)

paddle_width = 100
paddle_height = 10
paddle_speed = 1
paddle = Paddle(width // 2 - paddle_width // 2, height - paddle_height - 10, paddle_width, paddle_height, paddle_speed)

ball_radius = 10
ball_speed = 0.5
ball = Ball(width // 2, height // 2, ball_radius, ball_speed)

font = pygame.font.SysFont("Arial", 20)  # Font per il contatore dei tocchi
score = 0  # Variabile per il punteggio

game_running = True

while game_running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    keys = pygame.key.get_pressed()
    paddle.move(keys)
    ball.move()

    screen.fill((0, 0, 0))
    paddle.draw()
    ball.draw()

    # Aggiornamento del punteggio
    score_text = font.render("Score: {}".format(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    if ball.y > height:
        game_over()
        game_running = False

    pygame.display.update()


reset_game()  # Avvia la prima partita

while True:  # Ciclo per avviare nuove partite dopo la schermata di game over
    reset_game()
    game_running = True
    score = 0  # Reimposta il punteggio a zero
    
    while game_running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        paddle.move(keys)
        ball.move()

        screen.fill((0, 0, 0))
        paddle.draw()
        ball.draw()

        # Aggiornamento del punteggio
        score_text = font.render("Score: {}".format(score), True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        if ball.y > height:
            game_over()
            game_running = False

        pygame.display.update()
