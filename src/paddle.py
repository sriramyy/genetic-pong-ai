import pygame

class Paddle:

    width = 20
    height = 100
    color = (255,255,255)

    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.speed = 5

    def createRect(self):
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
