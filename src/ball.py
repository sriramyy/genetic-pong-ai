import pygame
import random

class Ball:

    radius = 8
    color = (255,255,255)
    
    # initial speeds
    speed_x = 5
    speed_y = 5 
    
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        """initialize the ball using the screen width and height"""
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - self.radius, SCREEN_HEIGHT // 2 - self.radius, self.radius * 2, self.radius * 2)
        self.dx = self.speed_x
        self.dy = self.speed_y
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

    def reset(self):
        """reset the ball back into the middle of the screen"""
        self.rect.center = (self.screen_width//2, self.screen_height//2)

        factor = random.random()
        if factor < 0.3 or factor >= 0:
            factor = 1

        direction_positive = True if random.random() >= 0.5 else False

        self.dx *= factor if direction_positive else -factor


    def bounceWall(self):
        """bounce ball off of the top or bottom walls"""
        self.dy *= -1

    def bouncePaddle(self, paddle):
        """bounce ball off of either the left or right paddles"""
        self.dx *= -1
        
        if (paddle.type == "left"):
            self.rect.left = paddle.rect.right
        elif (paddle.type == "right"):
            self.rect.right = paddle.rect.left

    def bounceRightWall(self):
        """special bounce for practice mode"""
        self.dx *= -1