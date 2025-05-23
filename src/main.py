import pygame
from paddle import Paddle
from ball import Ball
from gamestate import GameState

# constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BACKGROUND_COLOR = (0,0,0)
TEXT_COLOR = (100, 100, 100)
FPS = 60
# paddle constants -> in paddle.py
# ball constants -> in ball.py
# gamestate constants -> in gamestate.py

# paddle starting positions, and init paddle objects
left_paddle = Paddle(50, (SCREEN_HEIGHT-Paddle.height)//2, "left")
right_paddle = Paddle(SCREEN_WIDTH-Paddle.width-50, (SCREEN_HEIGHT-Paddle.height)//2, "right")

# create GameState
gs = GameState()

# pygame setup
pygame.init()
canvas = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Genetic Pong AI")
game_exit = False

# text setup
font = pygame.font.Font(None, 60)
player_font = pygame.font.Font(None, 32)

score_text = font.render(str(gs.game_score), True, TEXT_COLOR)
score_text_rect = score_text.get_rect()
score_text_rect.center = (SCREEN_WIDTH//2 , SCREEN_HEIGHT//2)

p1score_text = player_font.render(str(gs.p1_score), True, TEXT_COLOR)
p1score_text_rect = p1score_text.get_rect()
p1score_text_rect.center = (SCREEN_WIDTH*(1/6) , left_paddle.y_pos)

p2score_text = player_font.render(str(gs.p2_score), True, TEXT_COLOR)
p2score_text_rect = p2score_text.get_rect()
p2score_text_rect.center = (SCREEN_WIDTH*(5/6), right_paddle.y_pos)

# create Rect objects for the paddles
left_paddle.createRect();
right_paddle.createRect();

# create Rect for ball
ball = Ball(SCREEN_WIDTH, SCREEN_HEIGHT)



# --------- main loop ---------
while not game_exit:

    # check if user exited out of window (x)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True


    # --------- game logic ---------

    # continious key press check/handling
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        left_paddle.y_pos -= left_paddle.speed
    if keys[pygame.K_s]:
        left_paddle.y_pos += left_paddle.speed

    if keys[pygame.K_UP]:
        right_paddle.y_pos -= right_paddle.speed
    if keys[pygame.K_DOWN]:
        right_paddle.y_pos += right_paddle.speed

    # paddle boundary checking 
    if left_paddle.y_pos < 0:
        left_paddle.y_pos = 0
    elif left_paddle.y_pos > SCREEN_HEIGHT - left_paddle.height:
        left_paddle.y_pos = SCREEN_HEIGHT - left_paddle.height

    if right_paddle.y_pos < 0:
        right_paddle.y_pos = 0
    elif right_paddle.y_pos > SCREEN_HEIGHT - right_paddle.height:
        right_paddle.y_pos = SCREEN_HEIGHT - right_paddle.height

    # update paddle rect
    left_paddle.createRect()
    right_paddle.createRect()

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
    elif ball.rect.colliderect(right_paddle.rect):
        ball.bouncePaddle(right_paddle)
        gs.incGameScore()

    # ball collision (reset game)
    if ball.rect.left <= 0:
        gs.incP2()
        gs.resetGameScore()
        ball.reset()
        gs.print()
    elif ball.rect.right >= SCREEN_WIDTH:
        gs.incP1()
        gs.resetGameScore()
        ball.reset()
        gs.print()

    # update the text each turn

    score_text = font.render(str(gs.game_score), True, TEXT_COLOR)
    p1score_text = player_font.render(str(gs.p1_score), True, TEXT_COLOR)
    p2score_text = player_font.render(str(gs.p2_score), True, TEXT_COLOR)

    p1score_text_rect.center = (SCREEN_WIDTH*(1/6) , left_paddle.y_pos)
    p2score_text_rect.center = (SCREEN_WIDTH*(5/6), right_paddle.y_pos)

    
    
    # --------- drawing ---------

    canvas.fill(BACKGROUND_COLOR)
    canvas.blit(score_text, score_text_rect)
    canvas.blit(p1score_text, p1score_text_rect)
    canvas.blit(p2score_text, p2score_text_rect)


    pygame.draw.rect(canvas, left_paddle.color, left_paddle.rect)
    pygame.draw.rect(canvas, right_paddle.color, right_paddle.rect)

    pygame.draw.rect(canvas, ball.color, ball.rect, ball.radius)


    # --------- update display ---------

    pygame.display.flip()
    clock.tick(FPS)



pygame.quit()

