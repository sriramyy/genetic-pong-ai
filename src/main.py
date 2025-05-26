import pygame
from paddle import Paddle
from ball import Ball
from gamestate import GameState
from aipaddle import AIPaddle
import random

# init pygame
pygame.init()

# constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BACKGROUND_COLOR = (0,0,0)
TEXT_COLOR = (100, 100, 100)
FPS = 60
# paddle constants -> in paddle.py
# ball constants -> in ball.py
# gamestate constants -> in gamestate.py

# text setup
font = pygame.font.Font(None, 60)
player_font = pygame.font.Font(None, 32)


def startGame(canvas, clock, type):
    """
    function starts the pong game with a specified type: 
    "two-player" - starts two-palyer game | "practice" - starts one-player game with right wall
    """

    # paddle starting positions, and init paddle objects
    left_paddle = Paddle(50, (SCREEN_HEIGHT-Paddle.height)//2, "left")
    if type == "two-player": right_paddle = Paddle(SCREEN_WIDTH-Paddle.width-50, (SCREEN_HEIGHT-Paddle.height)//2, "right")

    # create GameState
    gs = GameState()

    # update text
    score_text = font.render(str(gs.rally_score), True, TEXT_COLOR)
    score_text_rect = score_text.get_rect()
    score_text_rect.center = (SCREEN_WIDTH//2 , SCREEN_HEIGHT//2)

    p1score_text = player_font.render(str(gs.p1_score), True, TEXT_COLOR)
    p1score_text_rect = p1score_text.get_rect()
    p1score_text_rect.center = (SCREEN_WIDTH*(1/6) , left_paddle.y_pos)

    if type == "two-player":
        p2score_text = player_font.render(str(gs.p2_score), True, TEXT_COLOR)
        p2score_text_rect = p2score_text.get_rect()
        p2score_text_rect.center = (SCREEN_WIDTH*(5/6), right_paddle.y_pos)

    # create Rect objects for the paddles
    left_paddle.createRect();
    if type == "two-player": right_paddle.createRect();

    # create Rect for ball
    ball = Ball(SCREEN_WIDTH, SCREEN_HEIGHT)

    running = True

    # --------- main loop --------- #
    while running:

        # check if user exited out of window (x)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "MENU"

        # --------- game logic --------- #

        # continious key press check/handling
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            left_paddle.y_pos -= left_paddle.speed
        if keys[pygame.K_s]:
            left_paddle.y_pos += left_paddle.speed

        if type == "two-player":
            if keys[pygame.K_UP]:
                right_paddle.y_pos -= right_paddle.speed
            if keys[pygame.K_DOWN]:
                right_paddle.y_pos += right_paddle.speed

        # paddle boundary checking 
        if left_paddle.y_pos < 0:
            left_paddle.y_pos = 0
        elif left_paddle.y_pos > SCREEN_HEIGHT - left_paddle.height:
            left_paddle.y_pos = SCREEN_HEIGHT - left_paddle.height

        if type == "two-player":
            if right_paddle.y_pos < 0:
                right_paddle.y_pos = 0
            elif right_paddle.y_pos > SCREEN_HEIGHT - right_paddle.height:
                right_paddle.y_pos = SCREEN_HEIGHT - right_paddle.height

        # update paddle rect
        left_paddle.createRect()
        if type == "two-player": right_paddle.createRect()

        # ball movement
        ball.rect.x += ball.dx
        ball.rect.y += ball.dy

        # ball bounce collision (top/bottom wall) 
        if ball.rect.top <= 0 or ball.rect.bottom >= SCREEN_HEIGHT:
            ball.bounceWall()

        # ball bounce collision (paddles) 
        if ball.rect.colliderect(left_paddle.rect):
            ball.bouncePaddle(left_paddle)
            gs.incRallyScore()
        elif type == "two-player" and ball.rect.colliderect(right_paddle.rect):
            ball.bouncePaddle(right_paddle)
            gs.incRallyScore()

        # ball collision (reset game)
        if ball.rect.left <= 0:
            if type == "two-player": 
                gs.incP2()
            else: # in practice, player score is the highest game score
                gs.checkRallyScore()
            gs.resetRallyScore()
            ball.reset()
        elif ball.rect.right >= SCREEN_WIDTH:
            gs.incP1()
            if type == "two-player": 
                gs.resetRallyScore()
                ball.reset()
            else: # in practice should bounce off
                gs.incRallyScore()
                ball.bounceRightWall()

        # update the text each turn

        GOLD_TEXT = (255, 215, 0)
        # make text gold for ahead player 
        if type == "two-player":   
            if gs.p1_score > gs.p2_score:
                p1score_text = player_font.render(str(gs.p1_score), True, GOLD_TEXT)
                p2score_text = player_font.render(str(gs.p2_score), True, TEXT_COLOR)
            elif gs.p2_score > gs.p1_score:
                p1score_text = player_font.render(str(gs.p1_score), True, TEXT_COLOR)
                p2score_text = player_font.render(str(gs.p2_score), True, GOLD_TEXT)
            else:
                p1score_text = player_font.render(str(gs.p1_score), True, TEXT_COLOR)
                p2score_text = player_font.render(str(gs.p2_score), True, TEXT_COLOR)
        else:
            p1score_text = player_font.render(str(gs.prac_high_score), True, GOLD_TEXT)


        score_text = font.render(str(gs.rally_score), True, TEXT_COLOR)

        # keep the player score text attatched to the respective paddle
        p1score_text_rect.center = (SCREEN_WIDTH*(1/6) , left_paddle.y_pos)
        if type == "two-player": p2score_text_rect.center = (SCREEN_WIDTH*(5/6), right_paddle.y_pos)

        # --------- drawing --------- #

        canvas.fill(BACKGROUND_COLOR)
        canvas.blit(score_text, score_text_rect)
        canvas.blit(p1score_text, p1score_text_rect)
        if type == "two-player": canvas.blit(p2score_text, p2score_text_rect)


        pygame.draw.rect(canvas, left_paddle.color, left_paddle.rect)
        if type == "two-player": pygame.draw.rect(canvas, right_paddle.color, right_paddle.rect)

        pygame.draw.ellipse(canvas, ball.color, ball.rect, ball.radius)


        # --------- update display --------- #

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


def startAITraining(canvas, clock):
    """visualizes and runs the genetic algorithm AI simulation with a variable amount of paddles"""

    POPULATION = 50
    GENERATIONS = 10
    SELECTION_AMT = 5
    PADDLE_X = 50
    MUTATION_RATE = 0.1
    MUTATION_STRENGTH = 0.5 

    # create initial population
    paddles = []
    for i in range(POPULATION):
        color = (255, 255, 255, int(50 + 205 * (i / POPULATION)))
        paddle = AIPaddle(PADDLE_X, (SCREEN_HEIGHT - Paddle.height)//2, color=color)
        paddles.append(paddle)

    for generation in range(GENERATIONS):
        # reset all paddles and the ball
        for paddle in paddles:
            paddle.y_pos = (SCREEN_HEIGHT - Paddle.height)//2
            paddle.createRect()
            paddle.alive = True
            paddle.score = 0

        ball = Ball(SCREEN_WIDTH, SCREEN_HEIGHT)

        running = True
        frame = 0
        while running and any(paddle.alive for paddle in paddles):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "MENU"

            # move and update paddles
            for paddle in paddles:
                if not paddle.alive:
                    continue
                move = paddle.think(ball.rect.centery, ball.dy, paddle.y_pos, 0)
                if move == -1:
                    paddle.y_pos -= paddle.speed
                elif move == 1:
                    paddle.y_pos += paddle.speed
                paddle.y_pos = max(0, min(SCREEN_HEIGHT - paddle.height, paddle.y_pos))
                paddle.createRect()

            # ball movement
            ball.rect.x += ball.dx
            ball.rect.y += ball.dy
            if ball.rect.top <= 0 or ball.rect.bottom >= SCREEN_HEIGHT:
                ball.bounceWall()
            if ball.rect.right >= SCREEN_WIDTH:
                ball.bounceRightWall()

            # if the ball reaches the left wall, check which paddles hit it
            if ball.rect.left <= 50:
                survivors = []
                for paddle in paddles:
                    if ball.rect.colliderect(paddle.rect):
                        survivors.append(paddle)
                        paddle.score += 1  # Only survivors get a score
                # eliminate all paddles that did not hit the ball
                for paddle in paddles:
                    if paddle not in survivors:
                        paddle.alive = False
                # only bounce the ball if there was at least one survivor
                if survivors:
                    ball.rect.left = survivors[0].rect.right
                    ball.bouncePaddle(survivors[0])
                else:
                    ball.reset()

            # Drawing
            canvas.fill(BACKGROUND_COLOR)
            for paddle in paddles:
                if not paddle.alive:
                    continue
                surf = pygame.Surface((paddle.width, paddle.height), pygame.SRCALPHA)
                surf.fill(paddle.color)
                canvas.blit(surf, (paddle.x_pos, paddle.y_pos))
            pygame.draw.ellipse(canvas, ball.color, ball.rect)
            gen_text = player_font.render(f"Gen {generation+1}", True, (255,255,0))
            alive_text = player_font.render(f"{(sum(paddle.alive for paddle in paddles)/POPULATION)*100}% Alive ({sum(paddle.alive for paddle in paddles)})", True, (255,255,0))
            canvas.blit(gen_text, (100, 10))
            canvas.blit(alive_text, (100, 40))

            pygame.display.flip()
            clock.tick(FPS)
            frame += 1

        # print best score
        print(f"Generation {generation+1}: Best Score = {max(paddle.score for paddle in paddles)}")

        # ---- GENETIC ALGORITHM ---- 


def menu(canvas, clock):
    """function for the menu, launches game directly"""
    # text setup
    menu_text = font.render("Genetic Pong AI", True, (255,255,255))
    menu_text_rect = menu_text.get_rect()
    menu_text_rect.center = (SCREEN_WIDTH//2 , SCREEN_HEIGHT//5)

    # button setup
    button_width, button_height = 200, 60
    button_color = (100, 100, 100)
    button_hover_color = (255, 255, 255)
    button_text_color = (0, 0, 0)

    two_player_rect = pygame.Rect((SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT//2 - 80), (button_width, button_height))
    practice_rect = pygame.Rect((SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT//2 + 10), (button_width, button_height))
    ai_training_rect = pygame.Rect((SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT//2 + 100), (button_width, button_height))

    two_player_text = player_font.render("Two-Player", True, button_text_color)
    two_player_text_rect = two_player_text.get_rect(center=two_player_rect.center)

    practice_text = player_font.render("Practice", True, button_text_color)
    practice_text_rect = practice_text.get_rect(center=practice_rect.center)

    ai_training_text = player_font.render("AI Training", True, button_text_color)
    ai_training_text_rect = ai_training_text.get_rect(center=ai_training_rect.center)

    # menu loop

    running = True  
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                return "QUIT"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if two_player_rect.collidepoint(mouse_pos):
                    return "TWO_PLAYER"
                elif practice_rect.collidepoint(mouse_pos):
                    return "PRACTICE"
                elif ai_training_rect.collidepoint(mouse_pos):
                    return "AI_TRAINING"

        canvas.fill(BACKGROUND_COLOR)
        canvas.blit(menu_text, menu_text_rect)

        mouse_pos = pygame.mouse.get_pos()

        # draw Two-Player button
        if two_player_rect.collidepoint(mouse_pos):
            pygame.draw.rect(canvas, button_hover_color, two_player_rect)
        else:
            pygame.draw.rect(canvas, button_color, two_player_rect)
        canvas.blit(two_player_text, two_player_text_rect)

        # draw Practice button
        if practice_rect.collidepoint(mouse_pos):
            pygame.draw.rect(canvas, button_hover_color, practice_rect)
        else:
            pygame.draw.rect(canvas, button_color, practice_rect)
        canvas.blit(practice_text, practice_text_rect)

        # draw AI training button
        if ai_training_rect.collidepoint(mouse_pos):
            pygame.draw.rect(canvas, button_hover_color, ai_training_rect)
        else:
            pygame.draw.rect(canvas, button_color, ai_training_rect)
        canvas.blit(ai_training_text, ai_training_text_rect)

        pygame.display.flip()
        clock.tick(FPS)


# -------------------------- MAIN -------------------------- #
def main():
    """main function to lead into other functions, allows ESC to backtrack"""
    # pygame setup
    canvas = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Genetic Pong AI")
    current_state = "MENU"
    running = True

    while running:
        if current_state == "MENU":
            action = menu(canvas, clock)
            if action == "QUIT": running = False
            elif action == "PRACTICE": current_state = "GAME_PRACTICE"
            elif action == "TWO_PLAYER": current_state = "GAME_TWO_PLAYER"
            elif action == "AI_TRAINING": current_state = "GAME_AI_TRAINING"
        
        elif current_state == "GAME_PRACTICE":
            game_result = startGame(canvas, clock, "practice")
            if game_result == "QUIT": running = False
            else: current_state = "MENU"

        elif current_state == "GAME_TWO_PLAYER":
            game_result = startGame(canvas, clock, "two-player")
            if game_result == "QUIT": running = False
            else: current_state = "MENU"

        elif current_state == "GAME_AI_TRAINING":
            ai_result = startAITraining(canvas, clock)
            if ai_result == "QUIT": running = False
            else: current_state = "MENU"



if __name__ == '__main__':
    main()