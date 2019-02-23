import pygame, sys, os, random, math, winsound
from pygame.locals import *
from threading import Timer

pygame.init()
pygame.font.init()

window = pygame.display.set_mode((600, 500))

pygame.display.set_caption('Cat & Mouse')

#Set Text Pt.1
myfont = pygame.font.SysFont('Arial', 20)
text_surface = pygame.Surface((100, 75))

#Pathers
dirname = os.path.dirname(__file__)
def pather(file):
    return os.path.join(dirname, file)

#Grabbers
w, h = pygame.display.get_surface().get_size()
background_image = pygame.image.load(pather('../assets/neon-tun-back.png')).convert()
background_image = pygame.transform.scale(background_image, (w, h))

class game_vars:
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
    level = 1
    score = 0
    lives = 10
    speed_enem = 1
    speed_all = 1 
    firing = True
    keys = {}
    game_loop = True

    #Score Watching
    def score_watcher(self, sc):
        if sc < 20:
            return 1
        elif sc >= 20 and sc <= 29:
            return 2
        elif sc >= 30 and sc <= 49:
            return 3
        elif sc >= 50:
            return 4

    def speed_watcher(self, sall, enem):
        if sall:
            return len(bullets) * 0.06 + 1
        else: 
            if Gvar.level < 3:
                return len(bullets) * 0.06 + 1
            else: 
                return len(bullets) * 0.06 + 3
                
    def pause(self, pauser):
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

#Sprite Template
class Sprite:
    def __init__(self, stype, image, speed, posIn, size):
        self.second_init(stype, image, speed, posIn, size)

    def second_init(self, stype, image, speed, posIn, size):
        self.stype = stype
        self.image = pygame.image.load(image).convert_alpha()
        self.size = size
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
                if self.stype == 'enemy':
                    self.set_costumes()
                    self.pos = [random.randint(0, w), random.randint(-800, -20)]
                    Gvar.lives -= 1
        elif udir:
            self.pos[1] -= self.speed * spe_schange

    def handle_spawn(self):
        if self.stype == 'player':
            window.blit(self.sprite, (self.pos[0], self.pos[1]))
        if self.stype == 'enemy':
            self.check_collision(False)
            if self.pos[1] >= 0:
                window.blit(self.sprite, (self.pos[0], self.pos[1]))
        if self.stype == 'bullet':
            self.check_collision(False)
            window.blit(self.sprite, (self.pos[0], self.pos[1]))


    def check_collision(self, t1):
        #Set diff collisions for the fly-cat
        if self.stype == 'bullet':
            bullpop = bullets.index(self)
            if (self.pos[1] or self.pos[0]) < 0 or self.pos[0] > w - self.width:
                pre_bullets.append(bullets.pop(bullpop))
        elif self.stype == 'enemy' or 'player' or 'dropcat':
        # if self.stype == 'enemy' or 'player' or 'dropcat':
            if self.pos[0] < 0:
                self.pos[0] = 0
            elif self.pos[0] > w - self.width:
                self.pos[0] = w - self.width

        if t1 != False:
            distance = math.sqrt(math.pow(self.ccor[0] - t1.ccor[0], 2) + math.pow(self.ccor[1] - t1.ccor[1], 2))
            if distance < 35:
                if(self.stype == 'enemy'):
                    bullpop = bullets.index(t1)
                    pre_bullets.append(bullets.pop(bullpop))
                    self.set_costumes()
                    self.pos = [random.randint(0, w), random.randint(-800, -20)]
                    return True

    def set_costumes(self):
        if self.pos[1] < 0 and Gvar.level > 3:
            new_cos = Gvar.costumes[random.randint(0, 3)]
            self.image = pather(f'../assets/{new_cos["img"]}')
            self.size = new_cos['size']
            self.second_init(self.stype, self.image, self.speed, self.posIn, self.size)

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
            Timer(0.1, self.shoot_timer).start()
        elif hold: 
            # bullets.append(Sprite('bullet', pather('../assets/bweb2.png'), 0.5, [Player.ccor[0], Player.ccor[1] + 5], [25, 25]))
            self.array_mover()
            self.shooting = False
            Timer(0.05, self.shoot_timer).start()
        else:
            return

    def shoot_timer(self):
        self.shooting = True

#Knitting more game vars
Gvar = game_vars()
#Set Player Sprite
Player = Sprite('player', pather('../assets/player.png'), 0.4, [w / 2, h - 40], [60, 45])
#Set Bullets
number_of_bullets = 50
bullets = []
pre_bullets = []
for bulletss in range(number_of_bullets):
    pre_bullets.append(Sprite('bullet', pather('../assets/bweb2.png'), 0.35, [Player.ccor[0], Player.ccor[1] + 5], [25, 25]))
#Set Enemies
number_of_enemies = 15
enem_lis = []
temp_enem = []
for enemiess in range(number_of_enemies):
    enem_lis.append(Sprite('enemy', pather('../assets/bmouse.png'), 0.12, [random.randint(0, w), random.randint(-1200, -20)], [50, 65]))

def main():

    while Gvar.game_loop:
        if Gvar.lives < 0:
                Gvar.game_loop = False
        # speedwatcher = 1
        window.blit(background_image, [0, 0])
        #The below is for sizing and resizing purposes //if I get to it that is
        # pygame.draw.rect(window, (200, 0, 0), (window.get_width()/3, 
        #     window.get_height()/3, window.get_width()/3,
        #     window.get_height()/3))

        #Events
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # key_left = True
                    Gvar.keys['key_left'] = True
                elif event.key == pygame.K_RIGHT:
                    # key_right = True
                    Gvar.keys['key_right'] = True
                elif event.key == pygame.K_SPACE:
                    Gvar.keys['key_space'] = True
                            
                elif event.key == pygame.K_RETURN:
                    Gvar.pause(True)
                elif event.key == pygame.K_ESCAPE:
                    Gvar.game_loop = False
                elif event.key == pygame.K_F4 and pygame.key.get_mods() & pygame.KMOD_ALT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    del Gvar.keys['key_left']
                elif event.key == pygame.K_RIGHT:
                    del Gvar.keys['key_right']
                elif event.key == pygame.K_SPACE:
                    Player.shot = False
                    del Gvar.keys['key_space']

        #Score Listener
        Gvar.level = Gvar.score_watcher(Gvar.score)

        #Keys/Collision listeners
        Player.handle_spawn()
        Player.movement(Gvar.keys.get('key_left', False), Gvar.keys.get('key_right', False), False, False, Gvar.speed_watcher(True, False))
        if Gvar.level < 3:
            Player.shooter(Gvar.keys.get('key_space'), False, Gvar.level)
        else: 
            Player.shooter(False, Gvar.keys.get('key_space'), Gvar.level)
        # Player.shooter(Gvar.keys.get('key_space'), Gvar.keys.get('space_press'))
        for Bullet in bullets:
            Bullet.handle_spawn()
            Bullet.movement(False, False, False, True, Gvar.speed_watcher(True, False))

        for Enemies in enem_lis:
            # Enemies.check_collision(Bullet) #This may be different
            Enemies.handle_spawn()
            for Bullet in bullets:
                if Enemies.check_collision(Bullet):
                    Gvar.score += 1
            Enemies.movement(False, False, True, False, Gvar.speed_watcher(False, True))
        
        #Setting Text
        lives_write = str(Gvar.lives)
        if Gvar.lives < 0:
            lives_write = 0
        scoresurface = myfont.render(f'Score: {str(Gvar.score)}', False, (0, 0, 0))
        livessurface = myfont.render(f'Lives: {str(lives_write)}', False, (0, 0, 0))
        levelsurface = myfont.render(f'Level: {str(Gvar.level)}', False, (0, 0, 0))
        text_surface.fill((255, 255, 255))
        text_surface.blit(scoresurface, (0, 0))
        text_surface.blit(livessurface, (0, 20))
        text_surface.blit(levelsurface, (0, 40))
        text_surface.set_alpha(200)
        window.blit(text_surface, (0, 0))
        # window.blit(scoresurface, (0, 0))

        #Update Portions of screen
        pygame.display.update()

main()