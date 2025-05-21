import pygame
from paddle import Paddle
from ball import Ball

# constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BACKGROUND_COLOR = (0,0,0)
FPS = 60
# paddle constants -> in paddle.py
# ball constants -> in ball.py

# paddle starting positions, and init paddle objects
left_paddle = Paddle(50, (SCREEN_HEIGHT-Paddle.height)//2)
right_paddle = Paddle(SCREEN_WIDTH-Paddle.width-50, (SCREEN_HEIGHT-Paddle.height)//2)

# pygame setup
pygame.init()
canvas = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Genetic Pong AI")
game_exit = False

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

    # boundary checking 
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

    # ball bounce collision (top wall) -> reverse y direction
    if ball.rect.top <= 0 or ball.rect.bottom >= SCREEN_HEIGHT:
        ball.dy *= -1

    # ball bounce collision (paddles) -> reverse x direction


    # ball collision (end game)
    if ball.rect.left <= 0 or ball.rect.right >= SCREEN_WIDTH:
        ball.reset(SCREEN_WIDTH, SCREEN_HEIGHT)

    # --------- drawing ---------

    canvas.fill(BACKGROUND_COLOR)

    pygame.draw.rect(canvas, left_paddle.color, left_paddle.rect)
    pygame.draw.rect(canvas, right_paddle.color, right_paddle.rect)

    pygame.draw.rect(canvas, ball.color, ball.rect, ball.radius)


    # --------- update display ---------

    pygame.display.flip()
    clock.tick(FPS)



pygame.quit()

