import sys

from Player import Player, Pencil, AP
from Magician import Magician
from MonkeyKing import MonkeyKing
from Monkey import Monkey
from Menu import Button, Title, Star

from function import WINDOW_WIDTH, WINDOW_HEIGHT, window_surface, WHITE, BLACK

import pygame
from pygame.locals import QUIT

import random

FPS = 120

# mouse button
LEFT = 1
RIGHT = 3

# the width and height of mouse icon 
MOUSEWIDTH = 72
MOUSEHEIGHT = 72

def blit_alpha(target, source, location, opacity): # window 圖片 位置 透明度
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, ( -x, - y ))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)        
    target.blit(temp, location)


def Loading_Page(window_surface, main_clock):
    # font
    start_font = pygame.font.SysFont(None, 60)

    # global variable
    global WINDOW_WIDTH, WINDOW_HEIGHT

    # start page setting
    start_color = 255
    start_color_detect = True
    
    # start the game
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
            elif event.type == pygame.VIDEORESIZE:
                WINDOW_WIDTH, WINDOW_HEIGHT = window_surface.get_size()

        start_text_surface = start_font.render("Press space to start the game!", True, (start_color, start_color, start_color))

        if start_color_detect == True:
            start_color -= 2
            if start_color < 100:
                start_color_detect = False
        else:
            start_color += 2
            if start_color >= 255:
                start_color_detect = True

        window_surface.fill(BLACK)
        window_surface.blit(start_text_surface, (100, WINDOW_HEIGHT/2))
        pygame.display.update()
        main_clock.tick(FPS)


def Menu_Page(window_surface, main_clock):
    # global variable
    global WINDOW_WIDTH, WINDOW_HEIGHT

    # load pictures
    menu_RAWimage = pygame.image.load(("sunset.jpg")).convert()
    menu_image = pygame.transform.scale(menu_RAWimage, (WINDOW_WIDTH, WINDOW_HEIGHT))

    # load BGM and sound
    pygame.mixer.music.load("menu\\JustAnotherMapleLeaf.mp3")
    pygame.mixer.music.set_volume(0.5)

    # setting variable
    opacity = 0
    frame = 0

    # color changing
    monkeyText_color = 255
    monkeyText_color_detect = True
    battleText_color = 255
    battleText_color_detect = True

    # button
    start_button = Button((800, 220), 238, 75, "START", 90)
    setting_button = Button((800, 330), 228, 58, "SETTING", 66)
    exit_button = Button((800, 420), 120, 58, "EXIT", 66)

    # Title
    tilte_monkey = Title((150, 200), "Monkey", 120)
    tilte_battle = Title((250, 350), "Battle", 120)

    # group
    button_group = pygame.sprite.Group()
    button_group.add(start_button)
    button_group.add(setting_button)
    button_group.add(exit_button)
    star_group = pygame.sprite.Group()
    star_group.add(Star((WINDOW_WIDTH, 0)))

    # play menu BGM
    pygame.mixer.music.play(-1)

    # menu
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # click mouse
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                if start_button.isCollideMouse == True:
                    tilte_battle.kill()
                    tilte_monkey.kill()
                    for star in star_group:
                        star.kill()
                    for button in button_group:
                        button.kill()
                    return
                elif exit_button.isCollideMouse == True:
                    pygame.quit()
                    sys.exit()
                else:
                    star_group.add(Star((WINDOW_WIDTH, 0)))
            elif event.type == pygame.VIDEORESIZE:
                WINDOW_WIDTH, WINDOW_HEIGHT = window_surface.get_size()
                menu_image = pygame.transform.scale(menu_RAWimage, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        if frame == 100:
            star_group.add(Star((WINDOW_WIDTH, 0)))
            star_group.add(Star((WINDOW_WIDTH, 0)))
            frame = 0
        else:
            frame += 1

        '''
        if monkeyText_color_detect == True:
            monkeyText_color -= 1
            if monkeyText_color < 180:
                monkeyText_color_detect = False
        else:
            monkeyText_color += 1
            if monkeyText_color >= 255:
                monkeyText_color_detect = True
        '''
        if battleText_color_detect == True:
            battleText_color -= 2
            if battleText_color < 3:
                battleText_color_detect = False
        else:
            battleText_color += 1
            if battleText_color >= 255:
                battleText_color_detect = True


        # clear window
        window_surface.fill(BLACK)

        if opacity <= 255:
            blit_alpha(window_surface, menu_image, (0, 0), opacity)
            opacity += 1
        else:
            window_surface.blit(menu_image, (0, 0))

        # draw button
        for button in button_group:
            button.draw()

        for star in star_group:
            blit_alpha(window_surface, star.image, star.rect.topleft, star.opacity)
        tilte_monkey.draw(monkeyText_color)
        tilte_battle.draw(battleText_color)

        # update
        star_group.update()
        button_group.update()
        pygame.display.update()

        # 控制遊戲迴圈迭代速率
        main_clock.tick(FPS)


def Game(window_surface, main_clock):
    # global variable
    global WINDOW_WIDTH, WINDOW_HEIGHT

    # sound
    shoot_sound = pygame.mixer.Sound("shoot.wav")

    # load BGM
    pygame.mixer.music.load("Motivation.mp3")
    pygame.mixer.music.set_volume(0.4)

    # load background
    background = pygame.image.load(("school.png")).convert_alpha()

    
    player = Player(70, WINDOW_HEIGHT-273)
    playerAP = AP((100, 200))

    # sprites group
    pencil_group = pygame.sprite.Group()
    pencilFolded_group = pygame.sprite.Group()

    magician_group = pygame.sprite.Group()
    magician_move_group = pygame.sprite.Group()
    stone_group = pygame.sprite.Group()

    monkeyKing_group = pygame.sprite.Group()
    banana_group = pygame.sprite.Group()
    bananaHit_group = pygame.sprite.Group()

    monkey_group = pygame.sprite.Group()
    monkey_BananaHit_group = pygame.sprite.Group()

    # variable setting
    WHITE = (255, 255, 255)


    # monkey magician monkeyKing
    wave = [[2, 1, 0],
            [3, 0, 1],
            [4, 2, 1],
            [5, 3, 2]]
    index = 0
    
    # game start setting
    Monkey.showUp_sound.play()
    for _ in range( wave[index][0] ):
        x = random.randint(WINDOW_WIDTH, WINDOW_WIDTH + 150)
        monkey_group.add( Monkey(x, WINDOW_HEIGHT - 176) )
    for _ in range( wave[index][1] ):
        new_magician = Magician(100, 100)
        magician_group.add( new_magician )
        magician_move_group.add( new_magician )
    for _ in range( wave[index][2] ):
        x = random.randint(WINDOW_WIDTH, WINDOW_WIDTH + 150)
        monkeyKing_group.add( MonkeyKing(x, WINDOW_HEIGHT - 373) )
    
    pygame.mixer.music.play(-1)

    # game
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                if(player.power >= 30):
                    playerAP.isAPchange = True
                    shoot_sound.play()
                    pencil_group.add( Pencil(45, 5, (player.rect.centerx + 3, player.rect.centery - 10), (pygame.mouse.get_pos())) )
                    player.attack()
            elif event.type == pygame.VIDEORESIZE:
                WINDOW_WIDTH, WINDOW_HEIGHT = window_surface.get_size()
        

        if len(magician_group) == 0 and len(monkey_group) == 0 and len(monkeyKing_group) == 0:
            index += 1
            if index == len(wave):
                window_surface.fill(BLACK)
                # BGM fades out
                pygame.mixer.music.fadeout(500)
                return
            else:
                Monkey.showUp_sound.play()
                for _ in range( wave[index][0] ):
                    x = random.randint(WINDOW_WIDTH, WINDOW_WIDTH + 150)
                    monkey_group.add( Monkey(x, WINDOW_HEIGHT - 176) )
                for _ in range( wave[index][1] ):
                    new_magician = Magician(100, 100)
                    magician_group.add( new_magician )
                    magician_move_group.add( new_magician )
                for _ in range( wave[index][2] ):
                    x = random.randint(WINDOW_WIDTH, WINDOW_WIDTH + 150)
                    monkeyKing_group.add( MonkeyKing(x, WINDOW_HEIGHT - 373) )
    
        
        # Clear the window
        window_surface.fill(BLACK)

        # Update
        pencil_group.update(magician_group, stone_group, banana_group, monkeyKing_group, monkey_group, pencilFolded_group)
        for magician in magician_group:
            magician.attack(stone_group)
        for magician in magician_move_group:
            magician.move(magician_move_group)
        monkeyKing_group.update(banana_group)
        monkey_group.update(player, monkey_BananaHit_group)
        banana_group.update(player, bananaHit_group)
        stone_group.update(player)
        player.update()
        playerAP.update(player.power)
        bananaHit_group.update()
        monkey_BananaHit_group.update()
        pencilFolded_group.update()

        # Draw the pictures
        window_surface.blit(background, (0, 0))
        pencil_group.draw(window_surface)
        magician_group.draw(window_surface)
        monkeyKing_group.draw(window_surface)
        monkey_group.draw(window_surface)
        banana_group.draw(window_surface)
        stone_group.draw(window_surface)
        
        # Draw player
        window_surface.blit(player.image, (player.rect.topleft))
        
        # Draw 命中特效
        monkey_BananaHit_group.draw(window_surface)
        bananaHit_group.draw(window_surface)
        for pencilFolded in pencilFolded_group:
            blit_alpha(window_surface, pencilFolded.image, pencilFolded.rect.topleft, pencilFolded.opacity)

        # Draw Life point
        window_surface.blit(playerAP.image, (playerAP.rect.topleft))
        window_surface.blit(player.life_text_surface, (50, 50))

        pygame.display.update()
        main_clock.tick(FPS)


def End(window_surface, main_clock):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Clear the window
        window_surface.fill(BLACK)

        pygame.display.update()
        main_clock.tick(FPS)

    

def main():

    # Waiting for the system getting ready.
    pygame.time.delay(500)

    # clock
    main_clock = pygame.time.Clock()

    Loading_Page(window_surface, main_clock)
    
    Menu_Page(window_surface, main_clock)
    
    Game(window_surface, main_clock)
    
    End(window_surface, main_clock)

if __name__ == '__main__':    
    main()