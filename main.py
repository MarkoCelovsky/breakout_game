#Import the pygame library and initialise the game engine
import pygame
#Let's import the Paddle Class & the Ball Class
from paddle import Paddle
from ball import Ball
from brick import Brick

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play()


def play_music():
   if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
   else:
        pygame.mixer.music.unpause()


def read_attempts():
    try:
        with open("attempts.txt", "r") as file:
            successful_attempts = int(file.readline())
            failed_attempts = int(file.readline())
    except (FileNotFoundError, ValueError):
        successful_attempts, failed_attempts = 0, 0
    return successful_attempts, failed_attempts

def write_attempts(successful_attempts, failed_attempts):
    with open("attempts.txt", "w") as file:
        file.write(str(successful_attempts) + "\n")
        file.write(str(failed_attempts) + "\n")

def display_attempts(screen, successful_attempts, failed_attempts):
    font = pygame.font.Font(None, 48)
    success_text = font.render(f"Successful Attempts: {successful_attempts}", 1, WHITE)
    fail_text = font.render(f"Failed Attempts: {failed_attempts}", 1, WHITE)
    hint = font.render("Press any key to start", 1, WHITE)

    screen.blit(success_text, (200, 250))
    screen.blit(fail_text, (200, 300))
    screen.blit(hint, (200, 350))

def draw_button(screen, text, x, y, width, height, color, font):
    button = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, button)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)
    return button
   
def handle_buttons(screen):
    button_font = pygame.font.Font(None, 36)
    play_again_button = draw_button(screen, "Play Again", 100, 400, 200, 50, (0, 128, 0), button_font)
    close_button = draw_button(screen, "Close", 500, 400, 200, 50, (128, 0, 0), button_font)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if play_again_button.collidepoint(mouse_pos):
                    return True

                if close_button.collidepoint(mouse_pos):
                    running = False
                    return False

        pygame.display.flip()



successful_attempts, failed_attempts = read_attempts()



# Define some colors
WHITE = (255,255,255)
DARKBLUE = (36,90,190)
LIGHTBLUE = (0,176,240)
YELLOW = (1,1,1)
RED = (255,0,0)
ORANGE = (255,100,0)
YELLOW = (255,255,0)

score = 0
lives = 3

# Open a new window
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Breakout Game")


#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()

#Create the Paddle
paddle = Paddle(LIGHTBLUE, 100, 10)
paddle.rect.x = 350
paddle.rect.y = 560

#Create the ball sprite
ball = Ball(WHITE, 5)
ball.rect.x = 345
ball.rect.y = 195

all_bricks = pygame.sprite.Group()
for i in range(7):
    brick = Brick(RED,80,30)
    brick.rect.x = 60 + i* 100
    brick.rect.y = 60
    all_sprites_list.add(brick)
    all_bricks.add(brick)
for i in range(7):
    brick = Brick(ORANGE,80,30) 
    brick.rect.x = 60 + i* 100
    brick.rect.y = 100
    all_sprites_list.add(brick)
    all_bricks.add(brick)
for i in range(7):
    brick = Brick(YELLOW,80,30)
    brick.rect.x = 60 + i* 100
    brick.rect.y = 140
    all_sprites_list.add(brick)
    all_bricks.add(brick)

# Add the paddle and the ball to the list of sprites
all_sprites_list.add(paddle)
all_sprites_list.add(ball)

# The loop will carry on until the user exits the game (e.g. clicks the close button).
carryOn = True

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

screen.fill(DARKBLUE)
display_attempts(screen, successful_attempts, failed_attempts)
pygame.display.flip()

game_start = False
while not game_start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
            game_start = True
        elif event.type == pygame.KEYDOWN:
            game_start = True

# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              carryOn = False # Flag that we are done so we exit this loop
        if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if music_button.collidepoint(mouse_pos):
                    play_music()

    #Moving the paddle when the use uses the arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.moveLeft(5)
    if keys[pygame.K_RIGHT]:
        paddle.moveRight(5)

    # --- Game logic should go here
    all_sprites_list.update()

    #Check if the ball is bouncing against any of the 4 walls:
    if ball.rect.x>=790:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x<=0:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y>590:
        ball.velocity[1] = -ball.velocity[1]
        lives -= 1
        if lives == 0:
            #Display Game Over Message for 3 seconds
            font = pygame.font.Font(None, 74)
            text = font.render("GAME OVER", 1, WHITE)
            failed_attempts += 1
            write_attempts(successful_attempts, failed_attempts)
            screen.blit(text, (250,300))
            pygame.display.flip()
            play_again = handle_buttons(screen)
            if play_again:
                       # Reset game state and start a new game
                all_sprites_list.empty()
                all_bricks.empty()

                # Create the player paddle
                paddle = Paddle(LIGHTBLUE, 100, 10)
                paddle.rect.x = 350
                paddle.rect.y = 560
                all_sprites_list.add(paddle)

                # Create the ball
                ball = Ball(WHITE, 5)
                ball.rect.x = 345
                ball.rect.y = 195
                all_sprites_list.add(ball)

                # Create bricks
                for i in range(7):
                    brick = Brick(RED,80,30)
                    brick.rect.x = 60 + i* 100
                    brick.rect.y = 60
                    all_sprites_list.add(brick)
                    all_bricks.add(brick)
                for i in range(7):
                    brick = Brick(ORANGE,80,30) 
                    brick.rect.x = 60 + i* 100
                    brick.rect.y = 100
                    all_sprites_list.add(brick)
                    all_bricks.add(brick)
                for i in range(7):
                    brick = Brick(YELLOW,80,30)
                    brick.rect.x = 60 + i* 100
                    brick.rect.y = 140
                    all_sprites_list.add(brick)
                    all_bricks.add(brick)
                # Reset lives
                lives = 3
                score = 0
                screen.fill(DARKBLUE)
                display_attempts(screen, successful_attempts, failed_attempts)
                pygame.display.flip()

                game_start = False
                while not game_start:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            carryOn = False
                            game_start = True
                        elif event.type == pygame.KEYDOWN:
                            game_start = True
            else:
                carryOn = False


    if ball.rect.y<40:
        ball.velocity[1] = -ball.velocity[1]

    #Detect collisions between the ball and the paddles
    if pygame.sprite.collide_mask(ball, paddle):
      ball.rect.x -= ball.velocity[0]
      ball.rect.y -= ball.velocity[1]
      ball.bouncePaddle()

    #Check if there is the ball collides with any of bricks
    brick_collision_list = pygame.sprite.spritecollide(ball,all_bricks,False)
    for brick in brick_collision_list:
      ball.bounce()
      score += 1
      brick.kill()
      if len(all_bricks)==0:
           #Display Level Complete Message for 3 seconds
            font = pygame.font.Font(None, 74)
            text = font.render("LEVEL COMPLETE", 1, WHITE)
            successful_attempts += 1
            write_attempts(successful_attempts, failed_attempts)
            screen.blit(text, (200,300))
            pygame.display.flip()
            play_again = handle_buttons(screen)
            if play_again:
                       # Reset game state and start a new game
                all_sprites_list.empty()
                all_bricks.empty()

                # Create the player paddle
                paddle = Paddle(LIGHTBLUE, 100, 10)
                paddle.rect.x = 350
                paddle.rect.y = 560
                all_sprites_list.add(paddle)

                # Create the ball
                ball = Ball(WHITE, 5)
                ball.rect.x = 345
                ball.rect.y = 195
                all_sprites_list.add(ball)

                # Create bricks
                for i in range(7):
                    brick = Brick(RED,80,30)
                    brick.rect.x = 60 + i* 100
                    brick.rect.y = 60
                    all_sprites_list.add(brick)
                    all_bricks.add(brick)
                for i in range(7):
                    brick = Brick(ORANGE,80,30) 
                    brick.rect.x = 60 + i* 100
                    brick.rect.y = 100
                    all_sprites_list.add(brick)
                    all_bricks.add(brick)
                for i in range(7):
                    brick = Brick(YELLOW,80,30)
                    brick.rect.x = 60 + i* 100
                    brick.rect.y = 140
                    all_sprites_list.add(brick)
                    all_bricks.add(brick)
                # Reset lives
                lives = 3
                score = 0
                
                screen.fill(DARKBLUE)
                display_attempts(screen, successful_attempts, failed_attempts)
                pygame.display.flip()

                game_start = False
                while not game_start:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            carryOn = False
                            game_start = True
                        elif event.type == pygame.KEYDOWN:
                            game_start = True
            else:
                carryOn = False

    # --- Drawing code should go here
    # First, clear the screen to dark blue.
    screen.fill(DARKBLUE)
    pygame.draw.line(screen, WHITE, [0, 38], [800, 38], 2)

    # Display the score and the number of lives at the top of the screen 
    font = pygame.font.Font(None, 34)
    text = font.render("Score: " + str(score), 1, WHITE)
    screen.blit(text, (20,10))
    text = font.render("Lives: " + str(lives), 1, WHITE)
    screen.blit(text, (650,10))
    button_font = pygame.font.Font(None, 22)
    music_button = draw_button(screen, "Play Music", 350, 5, 100, 40, (0, 128, 0), button_font)
    


    #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
    all_sprites_list.draw(screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

#Once we have exited the main program loop we can stop the game engine:
pygame.quit()

