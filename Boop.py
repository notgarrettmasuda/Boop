import pygame
import os
import random
import time

pygame.init()

os.chdir('C:/users/garre/OneDrive/Documents/Python/My Projects/Boop')

clock = pygame.time.Clock()
FPS = 60

#screen lengths
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600


#show screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Boop")

#fonts
font = pygame.font.SysFont('Arial', 27)

#images
#sprite_img = pygame.image.load(os.path.join("img", "Baka San.png")).convert_alpha()
sprite_img = pygame.image.load(os.path.join("img", "Bald Kaiya.png")).convert_alpha()
sprite_width = sprite_img.get_width()
sprite_height = sprite_img.get_height()
sprite_img = pygame.transform.scale(sprite_img, (int(sprite_width * 0.15), int(sprite_height * 0.15)))

finger_img = pygame.image.load(os.path.join("img", "Finger.png")).convert_alpha()
finger_width = finger_img.get_width()
finger_height = finger_img.get_height()
finger_img = pygame.transform.scale(finger_img, (int(finger_width * 0.05), int(finger_height * 0.05)))

boba_img = pygame.image.load(os.path.join("img", "Boba.png")).convert_alpha()
boba_width = boba_img.get_width()
boba_height = finger_img.get_height()
boba_img = pygame.transform.scale(boba_img, (int(finger_width * 0.1), int(finger_height * 0.12)))

heart_img = pygame.image.load(os.path.join("img", "Heart.png")).convert_alpha()
heart_width = heart_img.get_width()
heart_height = heart_img.get_height()
heart_img = pygame.transform.scale(heart_img, (int(heart_width * 0.09), int(heart_height * 0.09)))

drinkSoundChannel = pygame.mixer.Channel(1)
drinkSound = pygame.mixer.Sound("DrinkFinish.wav")
damageSound = pygame.mixer.Sound("DamageSound.wav")
#pygame.mixer.music.load('BackgroundMusic.wav')
#pygame.mixer.music.set_volume(0.2)

#colors
CYAN = (100, 240, 240)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MILKTEA = (221,196,163)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def get_rect_x(self):
        return self.rect.x
    
    def get_rect_y(self):
        return self.rect.y
    
    def updatePosition(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        screen.blit(self.image, self.rect)

class Lives(Sprite):
    def __init__(self, img, x, y):
        Sprite.__init__(self, img, x, y)        

class Player(Sprite):
    def __init__(self, img,  x, y):
        Sprite.__init__(self, img, x, y)
        self.boost = 300
        self.boostBar = pygame.draw.rect(screen, MILKTEA, pygame.Rect(10, 560, 100, 30))
        self.lives = 3
        self.points = 0
        self.debuff = False

    def movement(self, keys_pressed, speed, border):
        #basic movement
        if self.debuff == True:
            speed = speed/2
        if (keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]) and self.rect.x - border > 0:
            self.rect.x -= speed
        if (keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]) and self.rect.x + border + self.rect.width < SCREEN_WIDTH:
            self.rect.x += speed
        if (keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]) and self.rect.y - border > 0:
            self.rect.y -= speed
        if (keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]) and self.rect.y + border + self.rect.height < SCREEN_HEIGHT:
            self.rect.y += speed

        #Boost
        if keys_pressed[pygame.K_SPACE] == False:
            if self.boost <= 300:
                self.boost += 0.01
                if self.boost >= 3:
                    self.debuff = False
        if keys_pressed[pygame.K_SPACE] and self.boost >= 0:
            if (keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]) and self.rect.x - border > 0:
                self.boost -= 5
                self.rect.x -= speed * 2
            if (keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]) and self.rect.x + border + self.rect.width < SCREEN_WIDTH:
                self.boost -= 5
                self.rect.x += speed * 2
            if (keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]) and self.rect.y - border > 0:
                self.boost -= 5
                self.rect.y -= speed * 2
            if (keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]) and self.rect.y + border + self.rect.height < SCREEN_HEIGHT:
                self.boost -= 5
                self.rect.y += speed * 2
            if self.boost <= 0:
                self.debuff = True

    def displayLives(self):
        for i in range(self.lives):
            heart = Lives(heart_img, SCREEN_WIDTH - 100 + (40 * i), 25)
            heart.draw()
    
    def displayBoost(self):
        self.boostBar = pygame.draw.rect(screen, MILKTEA, pygame.Rect(10, 560, self.boost, 30))
        boostFont = pygame.font.Font(None, 25)
        boostText = round((self.boost/300) * 100)
        if boostText <= 0:
            boostText = 0
        elif boostText == 100:
            boostText = "max"
        draw_text(f'{boostText}' + "%", boostFont, BLACK, 10, 560)

class Finger(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self, finger_img, x, y)

    def movement(self, speed, x, y):
        if self.rect.x >= x:
            self.rect.x -= speed
        if self.rect.x <= x:
            self.rect.x += speed
        if self.rect.y >= y:
            self.rect.y -= speed
        if self.rect.y < y:
            self.rect.y += speed

class Boba(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self, boba_img, x, y)
        self.time = 100
        self.health = pygame.draw.rect(screen, MILKTEA, pygame.Rect(self.rect.x - (boba_width * 0.01), self.rect.y - 10, 52, 5))

    def update(self):
        self.rect.x = random.randint(100, 500)
        self.rect.y = random.randint(100, 500)

    def draw(self):
        screen.blit(self.image, self.rect)
        self.health = pygame.draw.rect(screen, MILKTEA, pygame.Rect(self.rect.x - 4, self.rect.y - 10, self.time/2, 5))

Kaiya = Player(sprite_img, 300, 300)
finger = Finger(50, 50)
milkTea = Boba(random.randint(100, 500), random.randint(100, 500))

gameOverFont = pygame.font.Font(None, 50)
gameOverText = gameOverFont.render("Game Over", True, BLACK)
gameOverTextRect = gameOverText.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

playAgainButtonFont = pygame.font.SysFont('Arial', 26)
playAgainButtonText = playAgainButtonFont.render('Play Again?', True, BLACK)
playAgainTextRect = playAgainButtonText.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 30))
playAgainButton = pygame.Rect(0, 0, 125, 30)
playAgainButton.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 30)

#text function
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def damageDetection():
    if pygame.Rect.colliderect(finger.rect, pygame.draw.rect(screen, WHITE, pygame.Rect(Kaiya.get_rect_x() + (sprite_width * 0.07), Kaiya.get_rect_y() + (sprite_height * 0.09), 10, 10))):
        damageSound.play()
        Kaiya.lives -= 1
        finger.rect.x = 50
        finger.rect.y = 50

def eatBoba():
    if (pygame.Rect.colliderect(Kaiya.rect, pygame.draw.rect(screen, CYAN, pygame.Rect(milkTea.get_rect_x() + (boba_width * 0.02), milkTea.get_rect_y() + (boba_height * 0.8), 25, 50)))):
        if drinkSoundChannel.get_busy() == False:   
            drinkSoundChannel.play(drinkSound)
        milkTea.time -= 1
        if Kaiya.boost <= 300:
            Kaiya.boost += 1
        if milkTea.time == 0:
            Kaiya.points += 1
            milkTea.update()
            milkTea.time = 100
            drinkSound.stop()
    else:
        drinkSound.stop()

def countDown():
    countDownFont = pygame.font.Font(None, 50)
    for i in reversed(range(1,4)):
        screen.fill(CYAN)
        pygame.draw.rect(screen, WHITE, pygame.Rect(50, 50, 500, 500))
        draw_text('Boba: ' + f'{Kaiya.points}', font, WHITE, 10, 10)
        countDownText = countDownFont.render(f'{i}', True, BLACK)
        countDownTextRect = countDownText.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(countDownText, countDownTextRect)
        pygame.display.update()
        time.sleep(1)

#pygame.mixer.music.play(-1)
countDown()

def main():
    run = True

    while run:
        play = True
        clock.tick(FPS)

        screen.fill(CYAN)
        pygame.draw.rect(screen, WHITE, pygame.Rect(50, 50, 500, 500))
        draw_text('Boba: ' + f'{Kaiya.points}', font, WHITE, 10, 10)

        damageDetection()
        eatBoba()
        Kaiya.draw()
        Kaiya.displayLives()
        Kaiya.displayBoost()
        finger.draw()
        milkTea.draw()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if Kaiya.lives == 0:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if playAgainButton.collidepoint(event.pos):
                        #pygame.mixer.music.play(-1)
                        Kaiya.points = 0
                        Kaiya.lives = 3
                        Kaiya.updatePosition(300, 300)
                        countDown()
        
        if Kaiya.lives == 0:
            #pygame.mixer.music.stop()
            play = False
            screen.blit(gameOverText, gameOverTextRect)
            a, b = pygame.mouse.get_pos()
            if playAgainButton.x <= a <= playAgainButton.x + 100 and playAgainButton.y <= b <= playAgainButton.y + 50:
                pygame.draw.rect(screen, (192,192,192), playAgainButton)
            else:
                pygame.draw.rect(screen, (128, 128, 128), playAgainButton)
            screen.blit(playAgainButtonText, playAgainTextRect)
            

        if play == True:
            keys_pressed = pygame.key.get_pressed()
            Kaiya.movement(keys_pressed, 5, 50)
            finger.movement(2.5, Kaiya.get_rect_x() + (sprite_width * 0.05), Kaiya.get_rect_y() + (sprite_height * 0.09))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()