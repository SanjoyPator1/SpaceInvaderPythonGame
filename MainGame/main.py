import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()  # This line will be always there in the game file
pygame.font.init()

# create our screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')  # to store the image in a variable

# Background music
mixer.music.load("background.wav")
mixer.music.play(-1)  # -1 to play it continuously in a loop

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370  # Little bit left from the middle of the screen,so that it will be perfectly in the middle (HORIZONTALLY)
playerY = 480  # Little bit upward from the bottom line
playerXChange = 0
playerYChange = 0

# Enemy
enemyXSpeed = 4  # here the initial value is 0.3 since it moving from starting of the game
enemyYSpeed = 40  # change will be 40 pixels  in downward direction

# multiple enemies - list

enemyImg = []
enemyX = []
enemyY = []
enemyXChange = []
enemyYChange = []
num_of_enemies = 20

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyXChange.append(enemyXSpeed)
    enemyYChange.append(enemyYSpeed)

# Bullet
# READY - U can't see the bullet
# FIRE - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletXChange = 0
bulletYChange = 10  # change will be 10 pixels  in upward direction
bulletState = "ready"

# Score code
score_value = 0
font = pygame.font.Font('starsFighters.ttf', 20)

textX = 10
textY = 10

# Game over font
over_font = pygame.font.Font('spaceAge.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (190, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))  # screen.blit() function is used to display the image


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fireBullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 20, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# infinite Game loop
running = True  # This is given so that it doesn't freeze and the close button works and game runs and etc etc.
while running:

    # RGB Red Green Blue
    screen.fill((0, 0, 0))

    # background
    screen.blit(background, (0, 0))
    # since the background image size is heavy so every time during the while iteration the image has to load,
    # so the spaceship and aliens are slow so increase the speed of enemy and ship

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            # print("some key pressed")
            if event.key == pygame.K_LEFT:
                # print("LEFT pressed")
                playerXChange = -5
            if event.key == pygame.K_RIGHT:
                # print("RIGHT pressed")
                playerXChange = 5

            if event.key == pygame.K_SPACE:
                # print("Spacebar pressed")
                if bulletState == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX  # Get the players current x coordinate
                    fireBullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print("key is RELEASED")
                playerXChange = 0

    playerX += playerXChange

    # BOUNDARIES
    if playerX <= 0:  # It gives us a border we can't go beyond the left
        playerX = 0

    elif playerX > 736:  # It cant go beyond the right border
        playerX = 736

    # Enemy movement

    for i in range(num_of_enemies):

        # Game over

        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyXChange[i]
        if enemyX[i] <= 0:  # It gives us a border we can't go beyond the left
            enemyXChange[i] = 4
            enemyY[i] += enemyYChange[i]

        elif enemyX[i] >= 736:  # It cant go beyond the right border
            enemyXChange[i] = -4
            enemyY[i] += enemyYChange[i]

            # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY = 480
            bulletState = "ready"
            score_value += 1

            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bulletState = "ready"

    if bulletState == "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletYChange

    # playerY += playerYChange
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()  # This line will always be there to tell them that it needs to be updated
