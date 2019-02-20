import pygame, sys, random
from pygame.locals import *

pygame.init()

window = pygame.display.set_mode((600, 500), pygame.RESIZABLE)

pygame.display.set_caption('Cat & Mouse')

#Grabbers
w, h = pygame.display.get_surface().get_size()
background_image = pygame.image.load('neon-tun-back.png').convert()
background_image = pygame.transform.scale(background_image, (w, h))

#Sprite Template
class Sprite:
    def __init__(self, stype, image, speed, posIn, size):
        self.stype = stype
        self.image = pygame.image.load(image).convert_alpha()
        self.sprite = self.image
        self.speed = speed
        self.posIn = posIn
        self.size = size
        self.setter()

    def set_size(self):
        self.sprite = pygame.transform.scale(self.sprite, self.size)


    def set_pos(self):
        self.posIn[0] -= self.width * 0.5
        self.posIn[1] -= self.height * 0.5
        if self.stype == 'bmouse':
            if self.posIn[0] < 0:
                self.posIn[0] = 0
            elif self.posIn[0] > w - self.width:
                print('hit', w)
                self.posIn[0] = w - self.width

        self.pos = self.posIn

    def set_trackers(self):
        self.rect = self.sprite.get_rect()
        self.center = self.sprite.get_rect().center
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()

    def setter(self):
        if self.size != False:
            self.set_size()
        self.set_trackers()
        self.set_pos()

    def movement(self, ldir, rdir, ddir, udir):
        if ldir:
            self.pos[0] -= self.speed
            if self.pos[0] < 0:
                self.pos[0] = 0
        elif rdir: 
            self.pos[0] += self.speed
            if self.pos[0] > w - self.width:
                self.pos[0] = w - self.width
        elif ddir:
            self.pos[1] += self.speed
            if self.pos[1] > h:
                self.pos[0] = random.randint(0, w)
                self.pos[1] = h - 250
        elif udir:
            self.pos[1] -= self.speed

    # def check_collision():


#Set Player Sprite
Player = Sprite('player', 'player.png', 0.5, [w / 2, h - 40], [60, 35])
#Set Enemies
enem_lis = []
for i in range(9):
    i = Sprite('bmouse', 'bmouse.png', 0.05, [random.randint(0, w), -20], [40, 65])
    enem_lis.append(i)

player_dir = False
key_left = False
key_right = False
key_up = False
key_down = False
game_loop = True

while game_loop:
    window.blit(background_image, [0, 0])

    #The below is for sizing and resizing purposes //if I get to it that is
    # pygame.draw.rect(window, (200, 0, 0), (window.get_width()/3, 
    #     window.get_height()/3, window.get_width()/3,
    #     window.get_height()/3))

    #Show Player
    window.blit(Player.sprite, (Player.pos[0], Player.pos[1]))
    for Eneblitz in enem_lis:
        window.blit(Eneblitz.sprite, (Eneblitz.pos[0], Eneblitz.pos[1]))

    #Events
    for event in pygame.event.get():

        if (event.type == pygame.QUIT):
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                key_left = True
            elif event.key == pygame.K_RIGHT:
                key_right = True
            if event.key == pygame.K_DOWN:
                key_down = True
            elif event.key == pygame.K_UP:
                key_up = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                key_left = False
            elif event.key == pygame.K_RIGHT:
                key_right = False
            if event.key == pygame.K_DOWN:
                key_down = False
            elif event.key == pygame.K_UP:
                key_up = False

    #Movement listeners
    Player.movement(key_left, key_right, False, False)

    for Enemies in enem_lis:
        Enemies.movement(False, False, True, False)
        

    #Update Portions of screen
    pygame.display.update()

delay = input('Press enter to finish, but if you\'re seeing this, something broke')