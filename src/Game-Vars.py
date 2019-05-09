import pygame, sys, os, random, math, winsound, time
from pygame.locals import *
from threading import Timer

class Game_Vars:
        #Enemy Costumes
    def __init__(self):
        self.costumes = [
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
        self.level = 1
        self.score = 0
        self.lives = 10
        self.speed_enem = 1
        self.speed_all = 1 
        self.firing = True
        self.keys = {}
        self.game_loop = True
        self.music = True
        self.once = True
        self.messgo = True
        self.first_time = True
        self.firstxt = True
        self.secondtxt = False
        self.thirdtxt = False
        self.sscreen = True
        self.pause_time = 0
        self.last_pause = 0
        self.mw_trans = 2.8
        self.paused = False
        self.messcolor = [0, 0, 0]
        self.messfont = pygame.font.SysFont('Arial', 30)
        self.mess_surface = pygame.Surface((300, 100))
        self.myfont = pygame.font.SysFont('Arial', 20)
        self.text_surface = pygame.Surface((100,75))


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

    def show_message(self, window, w, h):
        if self.messgo:
            if self.first_time:
                self.first_time = False
                Timer(0.2, self.message_timer, [20]).start()
            if self.firstxt:
                self.messcolor = [255, 255, 255]
            elif self.secondtxt:
                self.messcolor = [255, 153, 229]
            elif self.thirdtxt:
                self.messcolor = [0, 255, 255]
            message = self.messfont.render('Automatic Fire Mode', False, self.messcolor)
            spaceage = self.messfont.render('(Hold Spacebar)', False, self.messcolor)
            tw, th = message.get_rect().size
            sw, sh = spaceage.get_rect().size
            mw, mh = self.mess_surface.get_rect().size
            
            
            self.mess_surface.fill((0, 0, 0))
            self.mess_surface.blit(message, (mw / 2 - tw / 2, mh * 0.25 - th * 0.25))
            self.mess_surface.blit(spaceage, (mw * 0.5 - sw * 0.5, mh * 0.75 - sh * 0.75))
            self.mess_surface.set_alpha(150)
            window.blit(self.mess_surface, (w / 2 - mw / 2, h / 2 - mh / 2))

    def message_timer(self, counter):
        Timer(0.2, self.message_switch, [counter]).start()

    def message_switch(self, counter):
        counter -= 1
        if counter < 0:
            self.messgo = False
            return
        if self.firstxt:
            self.firstxt = False
            self.secondtxt = True
            self.message_timer(counter)
        elif self.secondtxt:
            self.secondtxt = False
            self.thirdtxt = True
            self.message_timer(counter)
        elif self.thirdtxt:
            self.thirdtxt = False
            self.firstxt = True
            self.message_timer(counter)


    def score_card(self, window):
        lives_write = str(self.lives)
        if self.lives < 0:
            lives_write = 0
        scoresurface = self.myfont.render(f'Score: {str(self.score)}', False, (0, 0, 0))
        livessurface = self.myfont.render(f'Lives: {str(lives_write)}', False, (0, 0, 0))
        levelsurface = self.myfont.render(f'Level: {str(self.level)}', False, (0, 0, 0))
        self.text_surface.fill((255, 255, 255))
        self.text_surface.blit(scoresurface, (0, 0))
        self.text_surface.blit(livessurface, (0, 20))
        self.text_surface.blit(levelsurface, (0, 40))
        self.text_surface.set_alpha(200)
        window.blit(self.text_surface, (0, 0))

    def speed_watcher(self, sall, enem, bullets, pups, Gvar):
        if sall:
            return len(bullets) * 0.06 + len(pups) * 0.1 + 1
        else: 
            if Gvar.level < 4:
                return len(bullets) * 0.06 + len(pups) * 0.06 + 1
            else: 
                return len(bullets) * 0.06 + len(pups) * 0.06 + 3
                
    def pause(self, pauser, bullets, pups, drop_cat, fly_cat, enem_lis, w, h, window, Player, background_image, Gvar, pather, pre_bullets, fly_wait):
        all_arr = bullets + pups + drop_cat + fly_cat + enem_lis
        pause_start = time.time()
        self.paused = True
        self.mus_switch = True
        if self.pause_time != 0:
            self.last_pause = self.pause_time

        pause_font = pygame.font.SysFont('Arial', 35)
        pause_surface = pygame.Surface((w - 100, h - 100))
        pspw, psph = pause_surface.get_size()
        pause_surface.set_alpha(120)
        pspesc = pause_font.render('Paused, Enter/Esc to unpause', False, [255, 255, 255])
        pspew, pspeh = pspesc.get_rect().size
        while pauser:
            window.blit(background_image, [0, 0])
            Player.handle_spawn(window, Gvar, w, h, bullets, pather, pre_bullets, fly_wait, fly_cat)
            for Sprite in all_arr:
                Sprite.handle_spawn(window, Gvar, w, h, bullets, pather, pre_bullets, fly_wait, fly_cat)
            self.score_card(window)
            if self.level == 3:
                self.show_message(window, w, h)

            #Set Pause screen here
            pause_surface.blit(pspesc, [pspw / 2 - pspew / 2, psph /2 - pspeh / 2])
            window.blit(pause_surface, [(w - pspw) / 2, (h - psph) / 2])

            pygame.display.update()
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F4 and pygame.key.get_mods() & pygame.KMOD_ALT:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
                        self.paused = False
                        self.pause_time = time.time() - pause_start
                        Gvar.keys = {}
                        pauser = False
                    elif event.key == pygame.K_RETURN:
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
                        self.paused = False
                        self.pause_time = time.time() - pause_start
                        Gvar.keys = {}
                        pauser = False