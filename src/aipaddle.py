import pygame
from paddle import Paddle
import random
from ball import Ball
import math

class AIPaddle(Paddle):

    def __init__(self, x_pos, y_pos, color, weights=None):
        """initialize a AI paddle"""
        super().__init__(x_pos,y_pos,None)
        
        self.alive = True
        self.score = 0
        self.color = color
        
        if weights is None:
            self.weights = [random.uniform(-1,1) for _ in range (8)]
        else:
            self.weights = weights

    def think(self, SCREEN_HEIGHT, ball:Ball):
        """
        decide movement based on a simple perceptron model
        inputs:
            distance
            angle
            ball_y
            ball_dy
            ball_x
            ball_dx
            paddle_y
        returns:
            -1 for up, 1 for down, 0 for stay
        """
        # get variables needed for distance and angle
        paddle_center = self.rect.center
        ball_center = ball.rect.center
        dist_x = ball_center[0] - paddle_center[0]
        dist_y = ball_center[1] - paddle_center[1]

        # calculate and get all the values needed
        distance = (dist_x**2 + dist_y**2) ** 0.5
        angle = math.atan2(dist_y, dist_x)
        ball_y = ball.rect.centery
        ball_dy = ball.dy
        ball_x = ball.rect.centerx
        ball_dx = ball.dx
        paddle_y = self.y_pos

        inputs = [distance, angle, ball_y, ball_dy, ball_x, ball_dx, paddle_y]
        # calculate inputs with weights
        s = sum (w*i for w, i in zip(self.weights[:-1], inputs)) + self.weights[-1]

        THRESHOLD = 0.2 #  0.1 0.2 0.3
        if s > THRESHOLD:  # strongly positive
            return 1  # Move Down
        elif s < -THRESHOLD: # strongly negative
            return -1 # Move Up
        else: #  weak (close to zero)
            return 0  # Stay

    def mutate(self, rate=0.1, strength=0.5):
        """radomly mutate weights for genetic evolution"""
        new_weights = self.weights[:]
        for i in range(len(self.weights)):
            if random.random() < rate:
                new_weights[i] += random.uniform(-strength, strength)

        return new_weights