import pygame
import random
import math
from pygame import mixer

pygame.init()

# Displays game screen
screen = pygame.display.set_mode((800, 600))

# Background
bg = pygame.image.load('background.png')

# This decides the duration of the game loop
running = True

# Title and logo
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0

# Multiple Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6

# Setting position for each enemy
for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyImg[i] = pygame.transform.scale(enemyImg[i], (64, 64))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 100))
    enemyX_change.append(4)
    enemyY_change.append(30)

# Bullet
# Ready - Bullet can't be seen on the screen
# Fire - Bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score text
score_val = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 0
textY = 0

#Game_over text
over_font = pygame.font.Font("freesansbold.ttf", 64)


def game_over():
    game = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game, (200, 250))


def show_score(x, y):
    score = font.render("Score : " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (textX, textY))


# Writing function so that player appears on the screen
def player(x, y):
    screen.blit(playerImg, (x, y))


# Writing function so that enemy appears on the screen
def enemy(x, y, ind):
    screen.blit(enemyImg[ind], (x, y))


# Writing function so that when bullet is fired, it's fired from the centre of spaceship
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# if distance between enemy and bullet is close enough
def isCollision(eX, eY, bX, bY):
    dist = math.sqrt(math.pow(eX - bX, 2) + math.pow(eY - bY, 2))
    if dist < 27:
        return True
    return False


# Game loop
while running:
    # RGB = red, green, blue
    screen.fill((0, 0, 0))

    screen.blit(bg, (0, 0))
    # An event is anything u do in the screen
    for event in pygame.event.get():
        # Close button
        if event.type == pygame.QUIT:
            running = False

        # if key is pressed check whether it's left or right
        # if SPACE is pressed, fire bullet
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # if key is unpressed, then spaceship doesn't move
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Restricting player's movement if it hits on boundaries
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movements
    for i in range(no_of_enemies):

        if enemyY[i] > 440:
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        # if collision occurs, reset bullet state and position the enemy and update score
        if collision:
            collisionSound = mixer.Sound("explosion.wav")
            collisionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_val += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        # Reappearance of the enemy
        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    pygame.draw.line(bg, (255, 0, 0), [0, 485], [800, 485], 2)
    show_score(textX, textY)
    pygame.display.update()
