# Genetic Pong ML
Pong using a genetic machine learning algorithm, implemented using PyGame

<img src="https://github.com/user-attachments/assets/fadb27b2-77b3-43ca-8653-4a06ff78549a" alt="" style="width:50%; height:auto;">

### General Instructions
Choose gamemode you want to play by using the main menu. If you would like to go back to the main menu, use the `ESC` key, this will not save any progress from the previous activity. 

## Pong Base Game
Can play the pong base game with two different gamemodes
- Two-Player - standard two player pong experience

  <img src="https://github.com/user-attachments/assets/3680529c-b547-4839-88b2-9dbd42e94f2d" alt="" style="width:50%; height:auto;">
  
  - Score represents each player score and Center Score represents current rally
- Practice - allows player to hit aganist a blank wall
   
  <img src="https://github.com/user-attachments/assets/fd7ee53e-ff8e-4b84-a399-7fe5481493fb" alt="" style="width:50%; height:auto;">

  - Score represents highest rally and Center Score represents current rally

### General Constants
*main.py constants*
- `SCREEN_WIDTH`
- `SCREEN_HEIGHT`
- `FPS`

*ball.py constants*
- `speed_x`
- `speed_y`

*paddle.py constants*
- `width`
- `height`
- `speed`

## Genetic Algorithm Mode
Trains a genetic ML model to play the game (simple perceptron model).

![image](https://github.com/user-attachments/assets/1e933114-0fdd-4b60-84ff-7bff982c9c57)

### Statistics Meaning
- Gen - Generation simulation is currently on
- SCR - Current Score
- PG SCR - Previous generation score
- Alive% - How many paddles are currently active/alive
- Overall HS - Overall Highscore across all simulated generations
- A.WGTS - Average Weights in the previous generation

### Weights
- distance - distance between ball and paddle
- angle - angle between ball and paddle
- ball_y - y of the ball
- ball_dy - change of y of the ball
- ball_x - x of the ball
- ball_dx - change of x of the ball
- paddle_y - current y of the paddle

Based on the above weights, `think` function returns a -1 (down), 1 (up), or 0 (stay).

### ML Training Constants
- `POPULATION` - paddles simulated each generation
- `GENERATIONS` - total number of generations simulated
- `PADDLE_X` - starting X of paddle
- `MUTATION_RATE` - how many paddles mutated (random)
- `MUTATION_STRENGTH` - range of how much the mutated paddles differ from original
