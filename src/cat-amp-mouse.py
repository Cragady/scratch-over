import pygame, sys, os, random, math, winsound
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
        self.size = size
        if stype == 'enemy' and level >= 4:
            self.set_costumes()
        self.sprite = self.image
        self.speed = speed
        self.posIn = posIn
        self.ccor = [0, 1]
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

    def set_centers(self):
        self.ccor[0] = self.pos[0] + self.width * 0.5
        self.ccor[1] = self.pos[1] + self.height * 0.5

    def setter(self):
        if self.size != False:
            self.set_size()
        self.set_trackers()
        self.set_pos()

    def movement(self, ldir, rdir, ddir, udir):
        self.set_centers()
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
                # self.pos[0] = random.randint(0, w)
                # self.pos[1] = h - 250
                self.pos = [random.randint(0, w), random.randint(-800, -20)]
        elif udir:
            self.pos[1] -= self.speed

    def handle_spawn(self):
        if self.stype == 'player':
            window.blit(self.sprite, (self.pos[0], self.pos[1]))
        if self.stype == 'enemy':
            self.check_collision(False)
            window.blit(self.sprite, (self.pos[0], self.pos[1]))

    def check_collision(self, t1):
        #Set diff collisions for the fly-cat
        if self.pos[0] < 0:
            self.pos[0] = 0
        elif self.pos[0] > w - self.width:
            self.pos[0] = w - self.width

        if t1 != False:
            distance = math.sqrt(math.pow(self.ccor[0] - t1.ccor[0], 2) + math.pow(self.ccor[1] - t1.ccor[1], 2))
            if distance < 45:
                # print('You Hit the Hitter!')
                if(self.stype == 'enemy'):
                    self.pos = [random.randint(0, w), random.randint(-800, -20)]
                # print(t1.pos)

    def set_costumes(self):
        global costumes
        new_cos = costumes[random.randint(0, 3)]
        print(new_cos)
        self.image = pygame.image.load(new_cos['img']).convert_alpha()
        self.size = new_cos['size']
    

#Enemy Costumes
costumes = [
    {
        'img': 'bmouse.png',
        'size': [40, 65]
    },
    {
        'img': 'b-c.png',
        'size': [40, 65]
    },
    {
        'img': 'b-a.png',
        'size': [40, 65]
    },
    {
        'img': 'b-t.png',
        'size': [40,65]
    }
]

#Game Vars
player_dir = False
key_left = False
key_right = False
key_up = False
key_down = False
level = 0
score = 0
lives = 3
game_loop = True

#Set Player Sprite
Player = Sprite('player', 'player.png', 0.5, [w / 2, h - 40], [60, 35])
#Set Enemies
number_of_enemies = 20
enem_lis = []
for i in range(number_of_enemies):
    enem_lis.append(Sprite('enemy', 'bmouse.png', 0.05, [random.randint(0, w), random.randint(-800, -20)], [40, 65]))

while game_loop:
    window.blit(background_image, [0, 0])

    #The below is for sizing and resizing purposes //if I get to it that is
    # pygame.draw.rect(window, (200, 0, 0), (window.get_width()/3, 
    #     window.get_height()/3, window.get_width()/3,
    #     window.get_height()/3))
    
    #Show Player
    Player.handle_spawn()
    for Eneblitz in enem_lis:
        Eneblitz.handle_spawn()

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

    #Collision listeners
    # for Enecolz in enem_lis:
        # Enecolz.check_collision(Player)


    #Movement/Collision listeners
    Player.movement(key_left, key_right, False, False)

    for Enemies in enem_lis:
        Enemies.check_collision(Player)
        Enemies.movement(False, False, True, False)
        

    #Update Portions of screen
    pygame.display.update()

delay = input('Press enter to finish, but if you\'re seeing this, something broke')