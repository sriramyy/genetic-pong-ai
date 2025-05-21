import pygame
import random

class Ball:

    radius = 8
    color = (255,255,255)
    
    # initial speeds
    speed_x = 4
    speed_y = 4 
    


    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - self.radius, SCREEN_HEIGHT // 2 - self.radius, self.radius * 2, self.radius * 2)
        self.dx = self.speed_x
        self.dy = self.speed_y

    def reset(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

        factor = random.random()
        if factor < 0.3 or factor >= 0:
            factor = 1

        direction_positive = True if random.random() >= 0.5 else False

        self.dx *= factor if direction_positive else -factor