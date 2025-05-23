import pygame

# P1 - Left
# P2 - Right

class GameState:


    def __init__(self):
        self.p1_score = 0
        self.p2_score = 0
        self.game_score = 0

    def print(self):
        """prints current game standing to the console"""
        print("P1 ", self.p1_score, " - ", self.p2_score, " P2")

    def incP1(self):
        """increments P1 score by 1"""
        self.p1_score += 1

    def incP2(self):
        """increments P2 score by 1"""
        self.p2_score += 1

    def reset(self, player):
        """resets score for specified player (P1,P2,All)"""
        if player == "P1":
            self.p1_score = 0
        elif player == "P2":
            self.p2_score = 0
        elif player == "All":
            self.p1_score = 0
            self.p2_score = 0
    
    def incGameScore(self):
        """increments the total game score (rally score)"""
        self.game_score += 1

    def resetGameScore(self):
        """resets the total game score (rally score)"""
        self.game_score = 0
