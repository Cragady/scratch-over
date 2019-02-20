import pygame, sys
from pygame.locals import *

pygame.init()

window = pygame.display.set_mode((600, 600), pygame.RESIZABLE)

pygame.display.set_caption('Cat & Mouse')

#Grabbers
w, h = pygame.display.get_surface().get_size()

#Sprite Template
class Sprite:
    def __init__(self, image, speed, posIn, size):
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
        elif udir:
            self.pos[1] -= self.speed





#Set player
# player = pygame.image.load('player.png').convert_alpha()
# player = pygame.transform.scale(player, (60, 35))
# player_rect = player.get_rect()
# player_rect.center = window.get_rect().center
# player_width, player_height = player.get_size()
# playerPos = [w / 2 - player_width * 0.5, 550]
# player_speed = 2

#Set Player Sprite
Player = Sprite('player.png', 2, [w / 2, 567], [60, 35])

player_dir = False
key_left = False
key_right = False
key_up = False
key_down = False
game_loop = True

while game_loop:
    window.fill((255, 255, 255))

    #The below is for sizing and resizing purposes //if I get to it that is
    pygame.draw.rect(window, (200, 0, 0), (window.get_width()/3, 
        window.get_height()/3, window.get_width()/3,
        window.get_height()/3))

    #Show Player
    window.blit(Player.sprite, (Player.pos[0], Player.pos[1]))

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

    #Movement listener
    Player.movement(key_left, key_right, key_down, key_up)
    # if key_left:
    #     Player.pos[0] -= Player.speed
    #     if Player.pos[0] < 0:
    #         Player.pos[0] = 0
    # elif key_right:
    #     Player.pos[0] += Player.speed
    #     if Player.pos[0] > (w - Player.width):
    #         Player.pos[0] = w - Player.width
    # elif key_down:
    #     Player.pos[1] += Player.speed
    #     if Player.pos[1] > (h - Player.height):
    #         Player.pos[1] = h - Player.height
    # elif key_up:
    #     Player.pos[1] -= Player.speed
    #     if Player.pos[1] < 0:
    #         Player.pos[1] = 0
    # if key_left:
    #     playerPos[0] -= player_speed
    #     if playerPos[0] < 0:
    #         playerPos[0] = 0
    #     print(f'{w - player_width}')
    # elif key_right:
    #     playerPos[0] += player_speed
    #     if playerPos[0] > (w - player_width):
    #         playerPos[0] = w - player_width
    # elif key_down:
    #     playerPos[1] += player_speed
    #     if playerPos[1] > (h - player_width):
    #         playerPos[1] = h - player_width
    # elif key_up:
    #     playerPos[1] -= player_speed
    #     if playerPos[1] < 0:
    #         playerPos[1] = 0

    pygame.display.update()
    # pygame.display.flip()

delay = input('Press enter to finish.')