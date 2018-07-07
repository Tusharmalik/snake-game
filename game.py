import random
import sys
import time

import pygame

# check for initializing errors
check_errors = pygame.init()

if check_errors[1] > 0:
    print("Errors")
    sys.exit(-1)
else:
    print('success')

# Play surface
screen = pygame.display.set_mode((720, 460))
pygame.display.set_caption('snake game')

# Colors
red = pygame.Color(255, 0, 0) # game over
green = pygame.Color(0, 255, 0) # snake
black = pygame.Color(0, 0, 0) # score
white = pygame.Color(255, 255, 255) # background
brown = pygame.Color(165, 42, 42) # food

# Frames per second controller
fpsController = pygame.time.Clock()

# Important variables
snakePos = [100, 50]
snakeBody = [[100, 50],[90, 50],[80, 50]]

foodPos = [random.randrange(1,72)*10, random.randrange(1,46)*10]
score = 0
foodSpawn = True

direction = 'RIGHT'
changeto = direction

# game over function
def gameOver():
    myFont = pygame.font.SysFont('monaco', 72) # font of text
    GOsurf = myFont.render('Game Over', True, red) # surface of font
    GOrect = GOsurf.get_rect() # rectangular component of game over
    GOrect.midtop = (360, 15) # points on the screen
    screen.blit(GOsurf, GOrect)
    showScore(0)
    pygame.display.flip()
    time.sleep(5)
    pygame.quit() # pygame exit
    sys.exit() # console exit

# score board
def showScore(choice=1):
    sFont = pygame.font.SysFont('monaco', 24) # font of text 
    Ssurf = sFont.render('Score : {0}'.format(score), True, black) # surface of font
    Srect = Ssurf.get_rect() # rectangular component of score
    if choice == 1:
        Srect.midtop = (80, 10) # points on the screen
    else:
        Srect.midtop = (360, 120) # points on the screen
    screen.blit(Ssurf, Srect)    

# main logic of game
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                changeto = 'RIGHT'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                changeto = 'LEFT'
            if event.key == pygame.K_UP or event.key == ord('w'):
                changeto = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                changeto = 'DOWN'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # validation of direction
    # if we are moving to right then we can't move left and if we are moving left we can't move right,
    # the same goes for top and bottom
    if changeto == 'RIGHT' and not direction == 'LEFT':
        direction = 'RIGHT'
    if changeto == 'LEFT' and not direction == 'RIGHT':
        direction = 'LEFT'
    if changeto == 'UP' and not direction == 'DOWN':
        direction = 'UP'
    if changeto == 'DOWN' and not direction == 'UP':
        direction = 'DOWN'

    # moving the snake position [X, Y]
    if direction == 'RIGHT':
        snakePos[0] = snakePos[0] + 10
    if direction == 'LEFT':
        snakePos[0] = snakePos[0] - 10
    if direction == 'UP':
        snakePos[1] = snakePos[1] - 10
    if direction == 'DOWN':
        snakePos[1] = snakePos[1] + 10

    # snake body mechanism
    snakeBody.insert(0, list(snakePos))
    if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
        score += 1
        foodSpawn = False
    else:
        snakeBody.pop()
    
    # food mechanism
    if foodSpawn == False:
        foodPos = [random.randrange(1,72)*10, random.randrange(1,46)*10]
    foodSpawn = True

    # background
    screen.fill(white)

    # Draw snake
    for pos in snakeBody:
        coodinates_snake = pygame.Rect(pos[0], pos[1], 10, 10)
        pygame.draw.rect(screen, green, coodinates_snake)

    # Draw food
    coodinates_food = pygame.Rect(foodPos[0], foodPos[1], 10, 10)
    pygame.draw.rect(screen, brown, coodinates_food)

    # game over conditions when we go out of screen
    if snakePos[0] > 710 or snakePos[0] < 0: 
        gameOver()
    if snakePos[1] > 450 or snakePos[1] < 0:
        gameOver()

    # game over when we touch ourself
    for block in snakeBody[1:]:
        if snakePos[0] == block[0] and snakePos[1] == block[1]:
            gameOver()

    showScore()
    pygame.display.flip()
    fpsController.tick(15)