import pygame
from paddle import Paddle
from ball import Ball
from gamestate import GameState

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


def startGame(type, game_exit):
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
    score_text = font.render(str(gs.game_score), True, TEXT_COLOR)
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

    # --------- main loop --------- #
    while not game_exit:

        # check if user exited out of window (x)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True


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
            gs.incGameScore()
        elif type == "two-player" and ball.rect.colliderect(right_paddle.rect):
            ball.bouncePaddle(right_paddle)
            gs.incGameScore()

        # ball collision (reset game)
        if ball.rect.left <= 0:
            if type == "two-player": 
                gs.incP2()
            else: # in practice, player score is the highest game score
                gs.checkGameScore()
            gs.resetGameScore()
            ball.reset()
        elif ball.rect.right >= SCREEN_WIDTH:
            gs.incP1()
            if type == "two-player": 
                gs.resetGameScore()
                ball.reset()
            else: # in practice should bounce off
                gs.incGameScore()
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


        score_text = font.render(str(gs.game_score), True, TEXT_COLOR)

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

        pygame.draw.rect(canvas, ball.color, ball.rect, ball.radius)


        # --------- update display --------- #

        pygame.display.flip()
        clock.tick(FPS)


    pygame.quit()


def menu(game_exit):
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

    two_player_text = player_font.render("Two-Player", True, button_text_color)
    two_player_text_rect = two_player_text.get_rect(center=two_player_rect.center)

    practice_text = player_font.render("Practice", True, button_text_color)
    practice_text_rect = practice_text.get_rect(center=practice_rect.center)

    # menu loop
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if two_player_rect.collidepoint(mouse_pos):
                    startGame("two-player", game_exit)
                elif practice_rect.collidepoint(mouse_pos):
                    startGame("practice", game_exit)

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

        pygame.display.flip()
        clock.tick(FPS)


# ------------- MAIN ------------- #

# pygame setup
canvas = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Genetic Pong AI")
game_exit = False

# run the menu sequence
menu(game_exit)