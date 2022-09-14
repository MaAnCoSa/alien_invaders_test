import pygame
import random
import math
from pygame import mixer



# Initializes the pygame
pygame.init()

# Creates the screen
screen = pygame.display.set_mode((800, 600))

# Establishing title and logo
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("images/SI_logo.png")
pygame.display.set_icon(icon)


# Fonts to be used through the game
titleFont = pygame.font.Font('fonts/Skygraze.otf', 72)
scoreFont = pygame.font.Font('fonts/Skygraze.otf', 32)
GO_font = pygame.font.Font('fonts/Skygraze.otf', 64)


# Background img
backImg = pygame.image.load("images/6508496.jpg")

# Background music
mixer.music.load('sound/background.wav')
mixer.music.play(-1)

# Player (spaceshp)
playerImg = pygame.image.load("images/spaceship.png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0
playerSpeedX = 0.3

# Enemies (little aliens)
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6

for i in range(num_enemies):
    enemyImg.append(pygame.image.load("images/alien.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)


# Bullet (there will, technically, only be one bullet)
bulletImg = pygame.image.load("images/bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = 1.5

bullet_state = "ready"



# Function to display the score in screen
score_value = 0
textX = 10
textY = 10
def show_score(x, y):
    score = scoreFont.render('Score : ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Function to display the player's spaceship
def player(x, y):
    screen.blit(playerImg, (x, y))

# Function to display an enemy alien
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Function to fire the bullet.
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))
    
# Function to check if the bullet impacted with an alien
def isCollision(x1, y1, x2, y2):
    dist = math.sqrt(math.pow((x2-x1), 2) + math.pow((y2-y1), 2))
    if dist < 27:
        return True
    else:
        return False

# Function to display the GAME OVER screen if player loses
def game_over_screen():
    GO_text = GO_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(GO_text, (200, 250))




# GAME LOOP
running = True
while running:

    # Placing the background image
    screen.blit(backImg, (0, -100))
    
    # Allows the window to close.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        # If keystroke is pressed, check for movement.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -playerSpeedX
            if event.key == pygame.K_RIGHT:
                playerX_change = playerSpeedX
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bulletX = playerX
                fire_bullet(bulletX, bulletY)
                bullet_sound = mixer.Sound('sound/laser.wav')
                bullet_sound.play()
        # If a key was unpressed, stop its movement.
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                
        

    
    # Boundaries for player
    playerX += playerX_change
    
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    
    # Loop for each enemy alien.
    for i in range(num_enemies):
        
        # If an alien reaches the bottom, player loses.
        if enemyY[i] > 440:
            for j in range(num_enemies):
                enemyY[j] = 2000
            game_over_screen()
            break
        
        # This keeps the aliens moving.
        enemyX[i] += enemyX_change[i]
        
        # Boundaries of enemies AND change in their direction.
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
            
        # Collision for bullet and alien
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('sound/explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        
        # This displays the enemy alien on screen every frame.
        enemy(enemyX[i], enemyY[i], i)

        
        
    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480
    
    


    # Displays player and score.
    player(playerX, playerY)
    show_score(textX, textY)

    # Updates the screen
    pygame.display.update()