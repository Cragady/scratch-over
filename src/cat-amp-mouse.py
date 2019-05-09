import pygame, sys, os, random, math, winsound, time, game_vars
from pygame.locals import *
from threading import Timer

pygame.init()
pygame.font.init()

window = pygame.display.set_mode((600, 500))

pygame.display.set_caption('Cat & Mouse')

#Pathers
dirname = os.path.dirname(__file__)
if dirname == 'src':
    def pather(file):
        file = '.' + file
        return os.path.join(dirname, file)
else:
    def pather(file):
        return os.path.join(dirname, file)

    

#Grabbers
w, h = pygame.display.get_surface().get_size()
background_image = pygame.image.load(pather('./assets/neon-tun-back.png')).convert()
background_image = pygame.transform.scale(background_image, (w, h))

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
        self.drop_spawn = True
        self.pupspawn = False
        self.pup_down = True
        self.fly_by = True
        self.triple_shoot = False
        self.bull_place = 0
        self.tstart = 0
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
                if self.stype != 'bullet':
                    self.pos[0] = 0
        elif rdir: 
            self.pos[0] += self.speed * spe_schange
            if self.pos[0] > w - self.width:
                if self.stype != 'bullet':
                    self.pos[0] = w - self.width
                if self.stype == 'pup':
                    self.speed *= -1
                if self.stype == 'fly':
                    self.pos = [0, 80]
                    if len(fly_cat) > 0:
                        try:
                            fly_wait.append(fly_cat.pop())
                        except:
                            print('fly_cat can\'t be popped')
        elif ddir:
            self.pos[1] += self.speed * spe_schange
            if self.pos[1] > h:
                if self.stype == 'enemy':
                    self.set_costumes()
                    self.pos = [random.randint(0, w), random.randint(-800, -20)]
                    Gvar.lives -= 1
                elif self.stype == 'drop':
                    self.pos = [random.randint(0, w), random.randint(-800, -20)]
                    try:
                        drop_wait.append(drop_cat.pop())
                    except:
                        print('drop_cat can\'t be popped')
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
            if not Gvar.paused:
                self.check_collision(False)
            window.blit(self.sprite, (self.pos[0], self.pos[1]))
        if self.stype == 'drop':
            self.check_collision(False)
            window.blit(self.sprite, (self.pos[0], self.pos[1]))
        if self.stype == 'pup':
            self.check_collision(False)
            window.blit(self.sprite, (self.pos[0], self.pos[1]))
        if self.stype == 'fly':
            self.check_collision(False)
            window.blit(self.sprite, (self.pos[0], self.pos[1]))


    def check_collision(self, t1):
        #Set diff collisions for the fly-cat
        if self.stype == 'bullet':
            bullpop = bullets.index(self)
            if self.pos[1] < 0 or self.pos[0] < 0 or self.pos[0] > w - self.width:
                try:
                    pre_bullets.append(bullets.pop(bullpop))
                except:
                    print('can\'t pop the ' + bullpop + ' bullet from bullets')
        elif self.stype != 'bullet':
            if self.pos[0] < 0:
                if self.stype == 'pup':
                    self.speed *= -1
                self.pos[0] = 0
            elif self.pos[0] > w - self.width:
                if self.stype == 'pup':
                    self.speed *= -1
                self.pos[0] = w - self.width

        if t1 != False:
            distance = math.sqrt(math.pow(self.ccor[0] - t1.ccor[0], 2) + math.pow(self.ccor[1] - t1.ccor[1], 2))
            if distance < 35:
                if self.stype == 'enemy':
                    if t1.stype == 'bullet':
                        bullpop = bullets.index(t1)
                        try:
                            pre_bullets.append(bullets.pop(bullpop))
                        except:
                            print('can\'t pop the ' + bullpop + ' bullet from bullets')
                    self.set_costumes()
                    self.pos = [random.randint(0, w), random.randint(-800, -20)]
                    return True
                elif self.stype == 'drop': 
                    self.pos = [random.randint(0, w), random.randint(-800, -20)]
                    return True
                elif self.stype == 'fly':
                    if t1.stype == 'bullet':
                        bullp2 = bullets.index(t1)
                        try:
                            pre_bullets.append(bullets.pop(bullp2))
                        except:
                            print('can\'t pop the ' + bullp2 + ' bullet from bullets')
                    self.pos = [0, 80]
                    try:
                        fly_wait.append(fly_cat.pop())
                    except:
                        print('fly_cat can\'t be popped')
                    return True

    def set_costumes(self):
        if self.pos[1] < 0 and Gvar.level > 3:
            new_cos = Gvar.costumes[random.randint(0, 3)]
            self.image = pather(f'./assets/{new_cos["img"]}')
            self.size = new_cos['size']
            self.second_init(self.stype, self.image, self.speed, self.posIn, self.size)

    def array_mover(self):
        if len(pre_bullets) > 0:
            pre_bullets[0].pos = [self.pos[0] + self.width * 0.3, self.pos[1] - self.height * 0.3]
            self.bull_place += 1
            if self.bull_place == 3:
                self.bull_place = 0
            pre_bullets[0].bull_place = self.bull_place
            try:
                bullets.append(pre_bullets.pop(0))
            except:
                print('can\'t pop ind 0 from pre_bullets')

    def shooter(self, press, hold, lvl):
        if self.shooting == False or self.shot == True:
            return
        if press:
            # bullets.append(Sprite('bullet', pather('./assets/bweb2.png'), 0.5, [Player.ccor[0], Player.ccor[1] + 5], [25, 25]))
            self.array_mover()
            self.shooting = False
            self.shot = True
            Timer(0.1, self.shoot_timer).start()
        elif hold: 
            # bullets.append(Sprite('bullet', pather('./assets/bweb2.png'), 0.5, [Player.ccor[0], Player.ccor[1] + 5], [25, 25]))
            self.array_mover()
            self.shooting = False
            if self.triple_shoot:
                Timer(0.015, self.shoot_timer).start()
            else:
                Timer(0.05, self.shoot_timer).start()
        else:
            return

    def shoot_timer(self):
        self.shooting = True

    def spawn_pups(self):
        self.pupspawn = True
        for pup in range(num_pups):
            pups.append(pup_wait[pup])
        pups[0].pos = [0, self.pos[1]]
        pups[1].pos = [w, self.pos[1]]

    def spawn_drop(self, end):
        if self.pupspawn: 
            if self.pup_down:
                self.pup_down = False
                self.down_start = time.time()
            if 10 < end - self.down_start:
                self.pup_down = True
                self.pupspawn = False
                self.drop_spawn = True
                for pup in range(num_pups):
                    try:
                        pups.pop()
                    except:
                        print('pup[] can\'t be popped')
        else:
            if self.drop_spawn:
                self.drop_spawn = False
                self.dstart = time.time()
                self.end_point = random.randint(10, 13)
            ender = end - self.dstart
            if self.end_point < ender:
                self.quit = True
                if len(drop_wait) > 0:
                    try:
                        drop_cat.append(drop_wait.pop())
                    except:
                        print('drop_wait can\'t be popped')
                self.drop_spawn = True

    def spawn_fly(self, end):
        if self.fly_by == True and len(fly_wait) > 0:
            self.fstart = time.time()
            self.fly_by = False
            self.fly_ex = True
            self.fly_end = random.randint(7, 15)
        ender = end - self.fstart
        if self.fly_end <  ender and self.triple_shoot != True:
            if len(fly_wait) > 0:
                self.fly_ex = False
                self.fly_by = True
                try:
                    fly_cat.append(fly_wait.pop())
                except:
                    print('fly_wait can\'t be popped')
        elif self.fly_ex == True:
            return

    def stop_trip(self, end):
        if self.triple_shoot and self.tstart == 0:
            self.tstart = time.time()
        if self.tstart > 0:
            ender = end - self.tstart
            if 6 < ender:
                self.tstart = 0
                self.triple_shoot = False


def play_music(sarr, end):
    if Gvar.music:
        if sarr == 0:
            Gvar.music = False
            pygame.mixer.music.load(muse_arr[sarr])
            pygame.mixer.music.play(-1)
            pygame.mixer.music.queue(muse_arr[2])
        else:
            ender = end - Gvar.mix_stop
            if Gvar.async_mus:
                Gvar.async_mus = False
                pygame.mixer.music.load(muse_arr[2])
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(muse_arr[1]))
            if Gvar.mix_stop != False:
                if Gvar.pause_time != 0 and Gvar.mus_switch:
                    Gvar.mus_switch = False
                    Gvar.mw_trans += Gvar.pause_time
                transit = Gvar.mw_trans
                if transit - 0.045 < ender < transit:
                    Gvar.music = False
                    Gvar.mix_stop = False
                    pygame.mixer.music.play(-1)
            # Timer(2.873, pygame.mixer.music.play, [-1]).start()

def once_only():
    if Gvar.once == True:
        pygame.mixer.music.stop()
        Gvar.once = False
        Gvar.music = True
        Gvar.async_mus = True
        Gvar.mus_switch = False
        Gvar.mix_stop = time.time()

def global_inits():
    global muse_arr, Gvar, Player, number_of_bullets, bullets, pre_bullets, num_pups, pups, pup_wait, drop_cat, drop_wait, fly_cat, fly_wait, number_of_enemies, enem_lis
    #Knitting more game vars
    
    muse_arr = [
        pather('./assets/08 Looping Steps.mp3'),
        pather('./assets/Intro.wav'),
        pather('./assets/06 Slider.mp3')
        ]

    pygame.mixer.init()
    ng_vars = game_vars.game_vars
    Gvar = ng_vars()

    #Set Player Sprite
    Player = Sprite('player', pather('./assets/player.png'), 0.4, [w / 2, h - 40], [60, 45])

    #Set Bullets
    number_of_bullets = 50
    bullets = []
    pre_bullets = []
    for bulletss in range(number_of_bullets):
        pre_bullets.append(Sprite('bullet', pather('./assets/bweb2.png'), 0.35, [-30, -30], [25, 25]))

    #Power Up
    num_pups = 2
    pups = []
    pup_wait = []
    drop_cat = []
    drop_wait = [Sprite('drop', pather('./assets/drop-cat.png'), 0.12, [random.randint(0, w), random.randint(-1200, -20)], [60, 45])]
    for pupss in range(num_pups):
        pup_wait.append(Sprite('pup', pather('./assets/drop-cat.png'), 0.6, [-140, -140], [60, 45]))

    fly_cat = []
    fly_wait = [Sprite('fly', pather('./assets/fly-cat.png'), 0.3, [0, 80], [100, 75])]

    #Set Enemies
    number_of_enemies = 15
    enem_lis = []
    for enemiess in range(number_of_enemies):
        enem_lis.append(Sprite('enemy', pather('./assets/bmouse.png'), 0.12, [random.randint(0, w), random.randint(-1200, -20)], [50, 65]))

def start_screen():
    first_time = True
    start_font = pygame.font.SysFont('Arial', 23)
    play_font = pygame.font.SysFont('Arial', 35)
    start_surface = pygame.Surface((w - 100, h - 100))
    ssw, ssh = start_surface.get_size()
    start_surface.set_alpha(120)
    sarrow = start_font.render('Left and Right arrows to move', False, [255, 255, 255])
    sspace = start_font.render('Space to shoot', False, [255, 255, 255])
    sesc = start_font.render('Esc to quit game. On start screen, this closes the window', False, [255, 255, 255])
    senter = start_font.render('Enter to pause. On start screen, this starts the game', False, [255, 255, 255])
    sstarter = play_font.render('Enter/Space to play!', False, [255, 255, 255])
    ssaw, ssah = sarrow.get_rect().size
    sssw, sssph = sspace.get_rect().size
    ssesw, ssesh = sesc.get_rect().size
    ssenw, ssenh = senter.get_rect().size
    ssstw, sssth = sstarter.get_rect().size

    game_overimg = pygame.image.load(pather('./assets/stop.png')).convert_alpha()
    game_overimg = pygame.transform.scale(game_overimg, (round(w * 0.6), h))
    gow, goh = game_overimg.get_size()

    while True:
        window.blit(background_image, [0, 0])
        if not first_time:
            window.blit(game_overimg, [w / 2 - gow / 2, 0])
        start_surface.blit(sarrow, [ssw / 2 - ssaw / 2, ssh / 4])
        start_surface.blit(sspace, [ssw / 2 - sssw / 2, ssh / 4 + ssah])
        start_surface.blit(sesc, [ssw / 2 - ssesw / 2, ssh / 4 + ssah * 2])
        start_surface.blit(senter, [ssw / 2 - ssenw / 2, ssh / 4 + ssah * 3])
        start_surface.blit(sstarter, [ssw / 2 - ssstw / 2, ssh / 4 + ssah * 5])
        window.blit(start_surface, [(w - ssw) / 2, (h - ssh) / 2])

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                Player.quit = True
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Player.quit = True
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_F4 and pygame.key.get_mods() & pygame.KMOD_ALT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    first_time = False
                    global_inits()
                    main()
                elif event.key == pygame.K_RETURN:
                    first_time = False
                    global_inits()
                    main()

        
        pygame.display.update()

def main():
    while Gvar.game_loop:

        if Gvar.lives < 0:
            pygame.mixer.music.stop()            
            pygame.mixer.stop()
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(pather('./assets/Meow.mp3.wav')))
            Gvar.game_loop = False

        if Gvar.level < 4:
            if pygame.mixer.music.get_busy() == False:
                play_music(0, False)
        else:
            once_only()
            end = time.time()
            play_music(1, end)
        
                
        window.blit(background_image, [0, 0])

        #Events
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                Player.quit = True
                pygame.mixer.music.stop()
                pygame.mixer.stop()
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
                    pygame.mixer.music.pause()
                    pygame.mixer.pause()
                    Gvar.keys = {}
                    Gvar.pause(True, bullets, pups, drop_cat, fly_cat, enem_lis, w, h, window, Player, background_image, Gvar)
                elif event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    pygame.mixer.stop()
                    Gvar.keys = {}
                    Gvar.game_loop = False
                elif event.key == pygame.K_F4 and pygame.key.get_mods() & pygame.KMOD_ALT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    Gvar.keys.pop('key_left', None)
                elif event.key == pygame.K_RIGHT:
                    Gvar.keys.pop('key_right', None)
                elif event.key == pygame.K_SPACE:
                    Player.shot = False
                    Gvar.keys.pop('key_space', None)

        #Score Listener
        Gvar.level = Gvar.score_watcher(Gvar.score)

        #Keys/Collision listeners
        Player.handle_spawn()
        if Gvar.level > 0:
            end = time.time()
            Player.spawn_drop(end)
            Player.spawn_fly(end)
            Player.stop_trip(end)
        Player.movement(Gvar.keys.get('key_left', False), Gvar.keys.get('key_right', False), False, False, Gvar.speed_watcher(True, False, bullets, pups, Gvar))
        if Gvar.level < 3:
            Player.shooter(Gvar.keys.get('key_space'), False, Gvar.level)
        else: 
            Player.shooter(False, Gvar.keys.get('key_space'), Gvar.level)
        for Bullet in bullets:
            Bullet.handle_spawn()
            if Player.triple_shoot and len(bullets) > 0:
                bulli = Bullet.bull_place
                if bulli == 1:
                    Bullet.movement(True, False, False, True, Gvar.speed_watcher(True, False, bullets, pups, Gvar))
                elif bulli == 2:
                    Bullet.movement(False, True, False, True, Gvar.speed_watcher(True, False, bullets, pups, Gvar))
                elif bulli == 3:
                    Bullet.movement(False, False, False, True, Gvar.speed_watcher(True, False, bullets, pups, Gvar))
            Bullet.movement(False, False, False, True, Gvar.speed_watcher(True, False, bullets, pups, Gvar))

        for Drop in drop_cat:
            Drop.handle_spawn()
            if Drop.check_collision(Player):
                try:
                    drop_wait.append(drop_cat.pop())
                except:
                    print('drop_cat can\'t be popped')
                Player.spawn_pups()
            Drop.movement(False, False, True, False, Gvar.speed_watcher(False, True, bullets, pups, Gvar))
            
        for Fly in fly_cat:
            Fly.handle_spawn()
            for Bullet in bullets:
                if Fly.check_collision(Bullet):
                    Gvar.lives += 1
                    if Gvar.level > 3:
                        Player.triple_shoot = True
            Fly.movement(False, True, False, False, Gvar.speed_watcher(True, False, bullets, pups, Gvar))

        for Pup in pups:
            Pup.handle_spawn()
            Pup.movement(False, True, False, False, Gvar.speed_watcher(False, True, bullets, pups, Gvar))

        for Enemies in enem_lis:
            # Enemies.check_collision(Bullet) #This may be different
            Enemies.handle_spawn()
            for Bullet in bullets:
                if Enemies.check_collision(Bullet):
                    Gvar.score += 1
            for Pup in pups:
                Enemies.check_collision(Pup)
            Enemies.movement(False, False, True, False, Gvar.speed_watcher(False, True, bullets, pups, Gvar))
            
        Gvar.score_card(window)

        if Gvar.level == 3:
            Gvar.show_message(window, w, h)

        pygame.display.update()
        
start_screen()