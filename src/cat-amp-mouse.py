import pygame, sys, os, random, math, winsound
from pygame.locals import *
from threading import Timer

pygame.init()

window = pygame.display.set_mode((600, 500), pygame.RESIZABLE)

pygame.display.set_caption('Cat & Mouse')

#Pathers
dirname = os.path.dirname(__file__)
def pather(file):
    return os.path.join(dirname, file)

#Grabbers
w, h = pygame.display.get_surface().get_size()
background_image = pygame.image.load(pather('../assets/neon-tun-back.png')).convert()
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
        self.origspeed = speed
        self.posIn = posIn
        self.ccor = [0, 1]
        self.shooting = True
        self.shot = False
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

    def movement(self, ldir, rdir, ddir, udir, spe_schange):
        self.set_centers()
        if ldir:
            self.pos[0] -= self.speed * spe_schange
            if self.pos[0] < 0:
                self.pos[0] = 0
        elif rdir: 
            self.pos[0] += self.speed * spe_schange
            if self.pos[0] > w - self.width:
                self.pos[0] = w - self.width
        elif ddir:
            self.pos[1] += self.speed * spe_schange
            if self.pos[1] > h:
                self.pos = [random.randint(0, w), random.randint(-800, -20)]
        elif udir:
            self.pos[1] -= self.speed * spe_schange

    def handle_spawn(self):
        if self.stype == 'player':
            window.blit(self.sprite, (self.pos[0], self.pos[1]))
        if self.stype == 'enemy':
            self.check_collision(False)
            window.blit(self.sprite, (self.pos[0], self.pos[1]))
        if self.stype == 'bullet':
            self.check_collision(False)
            window.blit(self.sprite, (self.pos[0], self.pos[1]))


    def check_collision(self, t1):
        #Set diff collisions for the fly-cat
        if self.stype == 'bullet':
            if self.pos[1] < 0:
                bullpop = bullets.index(self)
                pre_bullets.append(bullets.pop(bullpop))
            if self.pos[0] < 0:
                bullpop = bullets.index(self)
                pre_bullets.append(bullets.pop(bullpop))
            elif self.pos[0] > w - self.width:
                bullpop = bullets.index(self)
                pre_bullets.append(bullets.pop(bullpop))
        elif self.stype == 'enemy' or 'player' or 'dropcat':
        # if self.stype == 'enemy' or 'player' or 'dropcat':
            if self.pos[0] < 0:
                self.pos[0] = 0
            elif self.pos[0] > w - self.width:
                self.pos[0] = w - self.width


        if t1 != False:
            distance = math.sqrt(math.pow(self.ccor[0] - t1.ccor[0], 2) + math.pow(self.ccor[1] - t1.ccor[1], 2))
            if distance < 45:
                if(self.stype == 'enemy'):
                    self.pos = [random.randint(0, w), random.randint(-800, -20)]
                    return True

    def set_costumes(self):
        global costumes
        new_cos = costumes[random.randint(0, 3)]
        self.image = pygame.image.load(new_cos['img']).convert_alpha()
        self.size = new_cos['size']

    def array_mover(self):
        if len(pre_bullets) > 0:
            pre_bullets[0].pos = [self.ccor[0], self.ccor[1]]
            bullets.append(pre_bullets.pop(0))

    def shooter(self, press, hold, lvl):
        if self.shooting == False or self.shot == True:
            return
        if press:
            # bullets.append(Sprite('bullet', pather('../assets/bweb2.png'), 0.5, [Player.ccor[0], Player.ccor[1] + 5], [25, 25]))
            self.array_mover()
            self.shooting = False
            self.shot = True
            Timer(0.3, self.shoot_timer).start()
        elif hold: 
            # bullets.append(Sprite('bullet', pather('../assets/bweb2.png'), 0.5, [Player.ccor[0], Player.ccor[1] + 5], [25, 25]))
            self.array_mover()
            self.shooting = False
            Timer(0.05, self.shoot_timer).start()
        else:
            return

    def shoot_timer(self):
        self.shooting = True

    

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
key_space = False
level = 1
score = 0
lives = 3
speed_enem = 1
speed_all = 1 
firing = True
keys = {}
game_loop = True

#Set Player Sprite
Player = Sprite('player', pather('../assets/player.png'), 0.5, [w / 2, h - 40], [60, 35])
#Set Bullets
number_of_bullets = 50
bullets = []
pre_bullets = []
for i in range(number_of_bullets):
    pre_bullets.append(Sprite('bullet', pather('../assets/bweb.png'), 0.75, [Player.ccor[0], Player.ccor[1] + 5], [25, 25]))
#Set Enemies
number_of_enemies = 20
enem_lis = []
for i in range(number_of_enemies):
    enem_lis.append(Sprite('enemy', pather('../assets/bmouse.png'), 0.1, [random.randint(0, w), random.randint(-800, -20)], [40, 65]))

#Score Watching
def score_watcher(sc):
    if sc < 20:
        return 1
    elif sc >= 20 and sc <= 29:
        return 2
    elif sc >= 30 and sc <= 49:
        return 3
    elif sc >= 50:
        return 4

def speed_watcher(sall, enem):
    if sall:
        return len(bullets) * 0.06 + 1
    else: 
        if level < 3:
            return len(bullets) * 0.06 + 1
        else: 
            return len(bullets) * 0.06 + 3

def pause(pauser):
    while pauser == True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pauser = False
                elif event.key == pygame.K_RETURN:
                    pauser = False
                elif event.key == pygame.K_F4 and pygame.key.get_mods() & pygame.KMOD_ALT:
                    pygame.quit()
                    sys.exit()

while game_loop:
    # speedwatcher = 1
    window.blit(background_image, [0, 0])

    #The below is for sizing and resizing purposes //if I get to it that is
    # pygame.draw.rect(window, (200, 0, 0), (window.get_width()/3, 
    #     window.get_height()/3, window.get_width()/3,
    #     window.get_height()/3))
    
    #Show Sprites
    # Player.handle_spawn()
    # for Bullet in bullets:
    #     Bullet.handle_spawn()
    #     Bullet.change_speed(speedwatcher)

    # for Eneblitz in enem_lis:
    #     Eneblitz.handle_spawn()

    #Events
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # key_left = True
                keys['key_left'] = True
            elif event.key == pygame.K_RIGHT:
                # key_right = True
                keys['key_right'] = True
            elif event.key == pygame.K_SPACE:
                keys['key_space'] = True
                        
            elif event.key == pygame.K_RETURN:
                pause(True)
            elif event.key == pygame.K_ESCAPE:
                game_loop = False
            elif event.key == pygame.K_F4 and pygame.key.get_mods() & pygame.KMOD_ALT:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                del keys['key_left']
            elif event.key == pygame.K_RIGHT:
                del keys['key_right']
            elif event.key == pygame.K_SPACE:
                Player.shot = False
                del keys['key_space']

    #Score Listener
    level = score_watcher(score)

    #Keys/Collision listeners
    Player.handle_spawn()
    Player.movement(keys.get('key_left', False), keys.get('key_right', False), False, False, speed_watcher(True, False))
    if level < 3:
        Player.shooter(keys.get('key_space'), False, level)
    else: 
        Player.shooter(False, keys.get('key_space'), level)
    # Player.shooter(keys.get('key_space'), keys.get('space_press'))
    for Bullet in bullets:
        Bullet.handle_spawn()
        Bullet.movement(False, False, False, True, speed_watcher(True, False))

    for Enemies in enem_lis:
        # Enemies.check_collision(Bullet) #This may be different
        Enemies.handle_spawn()
        for Bullet in bullets:
            if Enemies.check_collision(Bullet):
                score += 1
                print(score)
        Enemies.movement(False, False, True, False, speed_watcher(False, True))
        

    #Update Portions of screen
    pygame.display.update()