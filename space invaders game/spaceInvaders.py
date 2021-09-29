import pygame, sys, random, time


# general setup
pygame.init()
clock = pygame.time.Clock()

# screen
screen_width = 500
screen_heigth = 800
screen = pygame.display.set_mode((screen_width, screen_heigth))
pygame.display.set_caption('space invaders')

# imagas
bg = pygame.image.load('stars.jpg')
spaceShipimg = pygame.image.load('space-invaders.png')
alienimg = pygame.image.load('alien.png')

# colors
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

# score and text
score = 0
font = pygame.font.SysFont('comincsans', 40, True, True)

# spaceShip class
class spaceShip (object):
    def __init__(self, x, y, width, heigth):
        self.x = x
        self.y = y
        self. width = width
        self.height = heigth
        self.vel = 5 
        self.right = 0
        self.bottom = 0

    def draw(self, screen):
        screen.blit(spaceShipimg, (self.x, self.y,))
        
    def powerUpCollision(self):
        if self.y <= powerUp.y <= (self.y + self.height) and self.x <= powerUp.x <= (self.x + self.width):
            powerUp.state = 'of'
            self.vel = 7.5



# bullet class
class projectile (object):
    def __init__(self, radius, color):
        self.x = 0
        self.y = 0
        self.radius = radius
        self.color = color
        self.vel = 10
        self.state = 'ready'
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self, screen):
        if self.state == 'fire':
            self.y -= self.vel
            self.draw(screen)

        if self.y <= 0:
            self.state = 'ready'
    
    def fire(self, x, y):
        if self.state == 'ready':
            self.state = 'fire'
            self.x = x
            self.y = y


# enemy class
class enemy (object):
    def __init__(self, width, height):
        self.x = random.randint(25, 425)
        self.y = 0
        self.width = width
        self.height = height
        self.vel = 3
        self.number = 0
    
    def draw(self, screen):
            self.number += 1
            screen.blit(alienimg, (self.x, self.y))
            

    def enemymvmnt(self):
        self.y += self.vel
        if self.y >= 800:
            self.number -= 1

    def respawn (self):
        global score
        if self.y >= 800:
            self.y = 0
            self.x = random.randint(25, 425)
            self.draw(screen)
            score -= 1

    def bulletCollision(self):
        global score
        if self.y <= bullet.y <= (self.y + self.height) and self.x <= bullet.x <= (self.x + self.width):
            self.y = 0
            self.x = random.randint(25, 425)
            self.draw(screen)
            score += 1
   
    def levelUp(self):
        global score
        if score == 20:
            self.vel = 4
        if score == 30:
            self.vel = 5
        if score == 40:
            self.vel = 6
        if score == 55:
            self.vel = 6.5

class powers(object):
    def __init__(self, radius, color):
        self.x = random.randint(25, 425)
        self.y = 0
        self.radius = radius
        self.color = color
        self.vel = 4
        self.state = 'of'

    def draw(self, screen):
        if self.state == 'on':
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def checkScore(self):
        if score == 1:
            self.state = 'on'

    def movement(self):
        if self.state == 'on':
            self.y += self.vel

    def respawn(self):
        if self.y >= 800:
            self.state = 'of'


# fuction for controlling the player with arrow keys
def playerMovement():
    keys = pygame.key.get_pressed()
    player.right = player.x + player.width
    player.bottom = player.y + player.height

    if keys[pygame.K_UP]:
        player.y -= player.vel

    if keys[pygame.K_DOWN]:
        player.y += player.vel
        
    if keys[pygame.K_LEFT]:
        player.x -= player.vel

    if keys[pygame.K_RIGHT]:
        player.x += player.vel

    if player.y <= 0:
        player.y = 0

    if player.bottom > screen_heigth:
        player.y = screen_heigth - player.height

    if player.x <= 0:
        player.x = 0

    if player.right > screen_width:
        player.x = screen_width - player.width


# redrawing game window
def redraw():
    screen.blit(bg, (0,0))
    player.draw(screen)
    alliens.draw(screen)
    text = font.render('score: ' + str(score), 1, white)
    screen.blit(text, (360, 20))

# objects
player = spaceShip(225, 375, 64, 64)
bullet = projectile(6, red)
alliens = enemy(64, 64)
powerUp = powers(8, blue)
# main loop
while True:
    clock.tick(75)

    redraw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet.state == 'ready':
                    bullet.fire(player.x + player.width/2, player.y)

    playerMovement()

    bullet.move(screen)

    alliens.enemymvmnt()

    alliens.respawn()

    alliens.bulletCollision()

    alliens.levelUp()

    powerUp.checkScore()

    powerUp.draw(screen)

    powerUp.movement()

    powerUp.respawn()
    
    player.powerUpCollision()
    
    pygame.display.flip()



