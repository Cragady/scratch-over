import pygame, sys, os, random, math, winsound, time, Game_Vars, Sprite
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
elif dirname =='__pycache__':
    def pather(file):
        file = '../.' + file
        return os.path.join(dirname, file)
else:
    def pather(file):
        return os.path.join(dirname, file)

#Grabbers
w, h = pygame.display.get_surface().get_size()
background_image = pygame.image.load(pather('./assets/neon-tun-back.png')).convert()
background_image = pygame.transform.scale(background_image, (w, h))


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
    NG_Vars = Game_Vars.Game_Vars
    Gvar = NG_Vars()

    #Set Player Sprite
    NSprite = Sprite.Sprite
    Player = NSprite('player', pather('./assets/player.png'), 0.4, [w / 2, h - 40], [60, 45])

    #Set Bullets
    number_of_bullets = 50
    bullets = []
    pre_bullets = []
    for bulletss in range(number_of_bullets):
        pre_bullets.append(NSprite('bullet', pather('./assets/bweb2.png'), 0.35, [-30, -30], [25, 25]))

    #Power Up
    num_pups = 2
    pups = []
    pup_wait = []
    drop_cat = []
    drop_wait = [NSprite('drop', pather('./assets/drop-cat.png'), 0.12, [random.randint(0, w), random.randint(-1200, -20)], [60, 45])]
    for pupss in range(num_pups):
        pup_wait.append(NSprite('pup', pather('./assets/drop-cat.png'), 0.6, [-140, -140], [60, 45]))

    fly_cat = []
    fly_wait = [NSprite('fly', pather('./assets/fly-cat.png'), 0.3, [0, 80], [100, 75])]

    #Set Enemies
    number_of_enemies = 15
    enem_lis = []
    for enemiess in range(number_of_enemies):
        enem_lis.append(NSprite('enemy', pather('./assets/bmouse.png'), 0.12, [random.randint(0, w), random.randint(-1200, -20)], [50, 65]))

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
                    Gvar.pause(True, bullets, pups, drop_cat, fly_cat, enem_lis, w, h, window, Player, background_image, Gvar, pather, pre_bullets, fly_wait)
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
        Player.handle_spawn(window, Gvar, w, h, bullets, pather, pre_bullets, fly_wait, fly_cat)
        if Gvar.level > 0:
            end = time.time()
            Player.spawn_drop(end, num_pups, drop_wait, pups, drop_cat)
            Player.spawn_fly(end, fly_wait, fly_cat)
            Player.stop_trip(end)
        Player.movement(Gvar.keys.get('key_left', False), Gvar.keys.get('key_right', False), False, False, Gvar.speed_watcher(True, False, bullets, pups, Gvar), w, h, Gvar, fly_cat, pather, fly_wait)
        if Gvar.level < 3:
            Player.shooter(Gvar.keys.get('key_space'), False, Gvar.level, pre_bullets, bullets)
        else: 
            Player.shooter(False, Gvar.keys.get('key_space'), Gvar.level, pre_bullets, bullets)
        for Bullet in bullets:
            Bullet.handle_spawn(window, Gvar, w, h, bullets, pather, pre_bullets, fly_wait, fly_cat)
            if Player.triple_shoot and len(bullets) > 0:
                bulli = Bullet.bull_place
                if bulli == 1:
                    Bullet.movement(True, False, False, True, Gvar.speed_watcher(True, False, bullets, pups, Gvar), w, h, Gvar, fly_cat, pather, fly_wait)
                elif bulli == 2:
                    Bullet.movement(False, True, False, True, Gvar.speed_watcher(True, False, bullets, pups, Gvar), w, h, Gvar, fly_cat, pather, fly_wait)
                elif bulli == 3:
                    Bullet.movement(False, False, False, True, Gvar.speed_watcher(True, False, bullets, pups, Gvar), w, h, Gvar, fly_cat, pather, fly_wait)
            Bullet.movement(False, False, False, True, Gvar.speed_watcher(True, False, bullets, pups, Gvar), w, h, Gvar, fly_cat, pather, fly_wait)

        for Drop in drop_cat:
            Drop.handle_spawn(window, Gvar, w, h, bullets, pather, pre_bullets, fly_wait, fly_cat)
            if Drop.check_collision(Player, w, h, bullets, Gvar, pather, pre_bullets, fly_wait, fly_cat):
                try:
                    drop_wait.append(drop_cat.pop())
                except:
                    print('drop_cat can\'t be popped')
                Player.spawn_pups(num_pups, pups, pup_wait, w)
            Drop.movement(False, False, True, False, Gvar.speed_watcher(False, True, bullets, pups, Gvar), w, h, Gvar, fly_cat, pather, fly_wait)
            
        for Fly in fly_cat:
            Fly.handle_spawn(window, Gvar, w, h, bullets, pather, pre_bullets, fly_wait, fly_cat)
            for Bullet in bullets:
                if Fly.check_collision(Bullet, w, h, bullets, Gvar, pather, pre_bullets, fly_wait, fly_cat):
                    Gvar.lives += 1
                    if Gvar.level > 3:
                        Player.triple_shoot = True
            Fly.movement(False, True, False, False, Gvar.speed_watcher(True, False, bullets, pups, Gvar), w, h, Gvar, fly_cat, pather, fly_wait)

        for Pup in pups:
            Pup.handle_spawn(window, Gvar, w, h, bullets, pather, pre_bullets, fly_wait, fly_cat)
            Pup.movement(False, True, False, False, Gvar.speed_watcher(False, True, bullets, pups, Gvar), w, h, Gvar, fly_cat, pather, fly_wait)

        for Enemies in enem_lis:
            # Enemies.check_collision(Bullet) #This may be different
            Enemies.handle_spawn(window, Gvar, w, h, bullets, pather, pre_bullets, fly_wait, fly_cat)
            for Bullet in bullets:
                if Enemies.check_collision(Bullet, w, h, bullets, Gvar, pather, pre_bullets, fly_wait, fly_cat):
                    Gvar.score += 1
            for Pup in pups:
                Enemies.check_collision(Pup, w, h, bullets, Gvar, pather, pre_bullets, fly_wait, fly_cat)
            Enemies.movement(False, False, True, False, Gvar.speed_watcher(False, True, bullets, pups, Gvar), w, h, Gvar, fly_cat, pather, fly_wait)
            
        Gvar.score_card(window)

        if Gvar.level == 3:
            Gvar.show_message(window, w, h)

        pygame.display.update()
        
start_screen()