import pygame

class Paddle:

    width = 20
    height = 100
    color = (255,255,255)
    speed = 5

    def __init__(self, x_pos, y_pos, type):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.type = type

    def createRect(self):
        """create/update a Rect object for the paddles"""
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
