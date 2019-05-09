import pygame, sys, os, random, math, winsound, time
from pygame.locals import *
from threading import Timer

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

    def movement(self, ldir, rdir, ddir, udir, spe_schange, w, h, Gvar, fly_cat, pather, fly_wait):
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
                    self.set_costumes(Gvar, pather)
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

    def handle_spawn(self, window, Gvar, w, h, bullets, pather, pre_bullets, fly_wait, fly_cat):
        if self.stype == 'player':
            window.blit(self.sprite, (self.pos[0], self.pos[1]))
        if self.stype == 'enemy':
            self.check_collision(False, w, h, bullets, Gvar, pather, pre_bullets, fly_wait, fly_cat)
            if self.pos[1] >= 0:
                window.blit(self.sprite, (self.pos[0], self.pos[1]))
        if self.stype == 'bullet':
            if not Gvar.paused:
                self.check_collision(False, w, h, bullets, Gvar, pather, pre_bullets, fly_wait, fly_cat)
            window.blit(self.sprite, (self.pos[0], self.pos[1]))
        if self.stype == 'drop':
            self.check_collision(False, w, h, bullets, Gvar, pather, pre_bullets, fly_wait, fly_cat)
            window.blit(self.sprite, (self.pos[0], self.pos[1]))
        if self.stype == 'pup':
            self.check_collision(False, w, h, bullets, Gvar, pather, pre_bullets, fly_wait, fly_cat)
            window.blit(self.sprite, (self.pos[0], self.pos[1]))
        if self.stype == 'fly':
            self.check_collision(False, w, h, bullets, Gvar, pather, pre_bullets, fly_wait, fly_cat)
            window.blit(self.sprite, (self.pos[0], self.pos[1]))


    def check_collision(self, t1, w, h, bullets, Gvar, pather, pre_bullets, fly_wait, fly_cat):
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
                    self.set_costumes(Gvar, pather)
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

    def set_costumes(self, Gvar, pather):
        if self.pos[1] < 0 and Gvar.level > 3:
            new_cos = Gvar.costumes[random.randint(0, 3)]
            self.image = pather(f'./assets/{new_cos["img"]}')
            self.size = new_cos['size']
            self.second_init(self.stype, self.image, self.speed, self.posIn, self.size)

    def array_mover(self, pre_bullets, bullets):
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

    def shooter(self, press, hold, lvl, pre_bullets, bullets):
        if self.shooting == False or self.shot == True:
            return
        if press:
            # bullets.append(Sprite('bullet', pather('./assets/bweb2.png'), 0.5, [Player.ccor[0], Player.ccor[1] + 5], [25, 25]))
            self.array_mover(pre_bullets, bullets)
            self.shooting = False
            self.shot = True
            Timer(0.1, self.shoot_timer).start()
        elif hold: 
            # bullets.append(Sprite('bullet', pather('./assets/bweb2.png'), 0.5, [Player.ccor[0], Player.ccor[1] + 5], [25, 25]))
            self.array_mover(pre_bullets, bullets)
            self.shooting = False
            if self.triple_shoot:
                Timer(0.015, self.shoot_timer).start()
            else:
                Timer(0.05, self.shoot_timer).start()
        else:
            return

    def shoot_timer(self):
        self.shooting = True

    def spawn_pups(self, num_pups, pups, pup_wait, w):
        self.pupspawn = True
        for pup in range(num_pups):
            pups.append(pup_wait[pup])
        pups[0].pos = [0, self.pos[1]]
        pups[1].pos = [w, self.pos[1]]

    def spawn_drop(self, end, num_pups, drop_wait, pups, drop_cat):
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

    def spawn_fly(self, end, fly_wait, fly_cat):
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