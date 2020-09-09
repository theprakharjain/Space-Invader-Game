import pygame
import random
import math
from pygame import mixer

# ****************************************  INITIALIZATION  ******************************************************
# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Put all the code in main function to restart the game on clicking "Play Again" button


def main():

    # Background Image
    background = pygame.image.load("images\space_background2.jpg")

    # Background Sound (mixer.music is used when the sound is continuous)
    mixer.music.load("sounds\Background.wav")
    mixer.music.play(-1)  # Adding "-1" makes it play on a loop

    # Title and Icon
    pygame.display.set_caption("The Space Invaders")
    icon = pygame.image.load("images\spaceship.png")
    pygame.display.set_icon(icon)

    # *************************************  VARIABLES AND CLASSES  ******************************************************

    # Button Class

    class button():
        def __init__(self, color, x, y, width, height, text=""):
            self.color = color
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.text = text

        # function to draw the button
        def draw(self, screen, outline=None):
            if outline:
                pygame.draw.rect(screen, outline, (self.x-2,
                                                   self.y-2, self.width+4, self.height+4), 0)

            pygame.draw.rect(screen, self.color,
                             (self.x, self.y, self.width, self.height), 0)

            if self.text != "":
                button_font = pygame.font.Font("font\Freesansbold.ttf", 24)
                text = button_font.render(self.text, True, (255, 255, 255))
                screen.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                                   self.y + (self.height/2 - text.get_height()/2)))

        def isOver(self, pos):  # POS is the mouse position in form of tuple of x,y coordinates
            if pos[0] > self.x and pos[0] < self.x + self.width:
                if pos[1] > self.y and pos[1] < self.y + self.height:
                    return True
                else:
                    return False

    # Player image and position
    player_img = pygame.image.load("images\player.png")
    playerX = 370
    playerY = 480
    playerX_change = 0

    # Enemy image and position
    enemy_img = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []

    num_of_enemies = 6

    for i in range(num_of_enemies):
        enemy_img.append(pygame.image.load("images\Alien1.png"))
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(3)
        enemyY_change.append(40)

    # # Bullet image and position
    bullet_img = pygame.image.load("images\Bullet.png")
    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 10
    # making bullet_state as global so that it can be manupulated in any function after adding global keyword
    global bullet_state
    # "ready" state means you cant see the bullet on the screen and "fire" is that bullet is moving
    bullet_state = "ready"

    # Score
    score_value = 0
    font = pygame.font.Font("font\Freesansbold.ttf", 32)

    # score position on screen
    textX = 10
    textY = 10

    # Game over text
    game_over_font = pygame.font.Font("font\Freesansbold.ttf", 60)

    # Game Re-start Button
    greenbutton = button((0, 255, 0), 330, 380,
                         150, 60, "PLAY AGAIN")

    # *************************************  FUNCTIONS  ******************************************************

    # Function to render the score on screen

    def show_score(x, y):
        score = font.render("Score: " + str(score_value),
                            True, (255, 255, 255))
        screen.blit(score, (x, y))

    # Function to show game over text

    def game_over_text():
        over_text = game_over_font.render(
            "GAME OVER", True, (255, 255, 255))
        screen.blit(over_text, (220, 250))

    def player(x, y):
        # Drawing image of Player on screen
        screen.blit(player_img, (playerX, playerY))

    def enemy(x, y, i):
        # Drawing image of enemy on screen and "i" from the multiple enemy for loop
        screen.blit(enemy_img[i], (x, y))

    # Function to provide true or false value of collision

    def is_collision(enemyX, enemyY, bulletX, bulletY):

        # Math formula to compute distance between 2 coordinates
        distance = math.sqrt(math.pow((enemyX-bulletX), 2) +
                             math.pow((enemyY-bulletY), 2))

        # Assesing the collision
        if distance < 27:
            return True
        else:
            return False

    # Function to change the state of bullet from "ready" to "fire"
    def fire_bullet(x, y):
        global bullet_state
        bullet_state = "fire"
        # Drawing image of bullet on screen & "+16, +10" keeps the bullet in the middle of the spaceship
        screen.blit(bullet_img, (x + 16, y + 10))

    # *************************************  GAME LOOP  ******************************************************

    # Game Loop
    running = True
    while running:

        # Screen Colour
        screen.fill((0, 0, 0))

        # Background Image
        screen.blit(background, (0, 0))

        # Event Check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # keystroke check
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    playerX_change = -4
                if event.key == pygame.K_RIGHT:
                    playerX_change = 4
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":  # So space doesnt changes the direction of bullet after firing
                        # To play bullet sound
                        bullet_sound = mixer.Sound("sounds\laser.wav")
                        bullet_sound.play()

                        bulletX = playerX  # So that bullet does not follow the ship after firing
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

            # Gets the mouse position
            pos = pygame.mouse.get_pos()

            # Mouse hover color change feature of button
            if event.type == pygame.MOUSEMOTION:
                if greenbutton.isOver(pos):
                    greenbutton.color = (255, 0, 0)
                else:
                    greenbutton.color = (0, 255, 0)

            # Restarting the game on clicking the Play Again Button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if greenbutton.isOver(pos):
                    main()
                else:
                    break

        # Changing value of playerX with keystrokes (Player Movement)
        playerX += playerX_change

        # Keeping the player in the game window
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        for i in range(num_of_enemies):

            # Game Over Display
            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000

                game_over_text()
                screen.blit(enemy_img[0], (370, 180))

                # Restart Button Display
                greenbutton.draw(screen, outline=True)

            # Changing value of enemyX (Enemy Movement)
            enemyX[i] += enemyX_change[i]

            # Keeping the enemy in the game window
            if enemyX[i] <= 0:
                enemyX_change[i] = 3
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -3
                enemyY[i] += enemyY_change[i]

            # Detecting collision
            collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision == True:

                # To play explosion sound
                explosion_sound = mixer.Sound("sounds\explosion.wav")
                explosion_sound.play()

                # reseting the bullet after the collision
                bulletY = 480
                bullet_state = "ready"
                # updating the score
                score_value += 1

                # Re-Spawning the enemy
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

            # Adding/Calling enemy to screen and manipulating its coordinates
            enemy(enemyX[i], enemyY[i], i)

        # Bullet movement

            # Reseting Bullet
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

            # Firing Bullet
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        # Adding/Calling player to screen and manipulating its coordinates
        player(playerX, playerY)

        # Calling show score function to show the score on the screen
        show_score(textX, textY)

        # Updates the changes in display
        pygame.display.update()


# Execution of Main Function
main()
