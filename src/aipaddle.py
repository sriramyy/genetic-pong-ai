import pygame
from paddle import Paddle
import random

class AIPaddle(Paddle):

    def __init__(self, x_pos, y_pos, color, weights=None):
        """initialize a AI paddle"""
        super().__init__(x_pos,y_pos,None)
        
        self.alive = True
        self.score = 0
        self.color = color
        
        if weights is None:
            self.weights = [random.uniform(-1,1) for _ in range (5)]
        else:
            self.weights = weights

    def think(self, ball_y, ball_dy, paddle_y, paddle_dy):
        """
        decide movement based on a simple perceptron model
        inputs:
            ball_y
            ball_dy
            paddle_y
            paddle_dy
        returns:
            -1 for up, 1 for down, 0 for stay
        """

        inputs = [ball_y, ball_dy, paddle_y, paddle_dy]
        # calculate inputs with weights
        s = sum (w*i for w, i in zip(self.weights[:-1], inputs)) + self.weights[-1]

        if s > 0.5:   return 1  # UP
        elif s < 0.5: return -1 # DOWN
        else:         return 0  # STAY

    def mutate(self, rate=0.1, strength=0.5):
        """radomly mutate weights for genetic evolution"""
        for i in range(len(self.weights)):
            if random.random() < rate:
                self.weights[i] += random.uniform(-strength, strength)