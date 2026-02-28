import sys, time
import random

import pygame
from pygame.locals import Color, QUIT, MOUSEBUTTONDOWN, USEREVENT, USEREVENT
from pygame.sprite import Group

#---------------------Global variables---------------------------------
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
IMAGEWIDTH = 32*8
IMAGEHEIGHT = 23*8
START_MARK_WIDTH = 256
START_MARK_HEIGHT = 100

# color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FPS = 60

# the width and height of mouse icon 
MOUSEWIDTH = 72
MOUSEHEIGHT = 72
#----------------------------------------------------------------------

# pygame初始化
pygame.init()
pygame.mixer.init()

# load window surface
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Mosquito War')

pygame.time.delay(500)

# clock
main_clock = pygame.time.Clock()
#----------------------------------------------------------------------

# 蚊子隨機位置
def get_random_position(widow_width, window_height, image_width, image_height):
    random_x = random.randint(30, widow_width - image_width)
    random_y = random.randint(30, window_height - image_height)
    return random_x, random_y

# 繪製透明圖片
def blit_alpha(target, source, location, opacity): # window 圖片 位置 透明度
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, ( -x, - y ))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)        
    target.blit(temp, location)

# 判斷蚊子是否滅絕
def mosquito_extint(mosquito_list):
    # mosquito list is empty
    if not mosquito_list:
        return True
    else:
        return False

class Mosquito(pygame.sprite.Sprite):
    def __init__(self, width, height, random_x, random_y):
        super().__init__()
        self.raw_image = pygame.image.load(("bug.png")).convert_alpha()
        self.image = pygame.transform.scale(self.raw_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (random_x, random_y)
        self.width = width
        self.height = height 
        self.life = 6
        self.energe = 0

# 蚊子被打到後的流血特效
class Blood(pygame.sprite.Sprite):
    def __init__(self, width, height, location_x, location_y):
        super().__init__()
        self.raw_image = pygame.image.load(("blood.png")).convert_alpha()
        self.image = pygame.transform.scale(self.raw_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (location_x, location_y)
        self.width = width
        self.height = height
        self.life = 40
    
    def update(self, blood_list):
        if self.life <= 1:
            blood_list.remove(self)
            self.kill()
        else:
            self.life -= 1

# 玩家大招：火魔法陣
class Magic_circle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 512
        self.height = 512
        self.raw_image = pygame.image.load(("magic_circle.png")).convert_alpha()
        self.image = pygame.transform.scale(self.raw_image, (self.width, self.height))
        self.raw_image = self.image
        self.rect = self.image.get_rect()
        
        self.x = (WINDOW_WIDTH - self.width) / 2
        self.y = WINDOW_HEIGHT
        self.rect.topleft = (self.x, self.y)
        self.angle = 0
        self.opacity = 10
        
        self.opacity_det = False
        self.mode = 'a'

    def update(self):
        match self.mode:
            # 火魔法陣 淡入+上升
            case 'a':
                self.y -= 12
                self.rect.topleft = (self.x, self.y)
                self.opacity += 2
                if self.y < (WINDOW_HEIGHT - self.height) / 2:
                    self.mode = 'b'
            # 火魔法陣 淡入淡出+旋轉
            case 'b':
                temp_x, temp_y = self.rect.center
                self.angle = (self.angle + 1) % 360
                self.image = pygame.transform.rotate(self.raw_image, self.angle)
                self.rect = self.image.get_rect()
                self.rect.center = (temp_x, temp_y)
                
                if self.opacity_det == False:
                    self.opacity += 1
                    if self.opacity >= 250:
                        self.opacity_det = True
                else:
                    self.opacity -= 4

# 蚊子被火魔法陣燒死的特效
class Fire(pygame.sprite.Sprite):
    def __init__(self, width, height, location_x, location_y):
        super().__init__()
        self.raw_image = pygame.image.load(("fire.png")).convert_alpha()
        self.image = pygame.transform.scale(self.raw_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (location_x, location_y)
        self.width = width
        self.height = height
        self.life = 50
    
    def update(self, fire_list):
        if self.life <= 1:
            fire_list.remove(self)
            self.kill()
        else:
            self.life -= 1

# 橢圓形
class Oval(pygame.sprite.Sprite):
    def __init__(self, width, height, location_x, location_y):
        super().__init__()
        self.raw_image = pygame.image.load(("blue_rect.png")).convert_alpha()
        self.image = pygame.transform.scale(self.raw_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (location_x, location_y)
        self.width = width
        self.height = height

# 在隨機位置生成一隻蚊子
def create_new_mosquito(mosquito_list):
    random_x, random_y = get_random_position(WINDOW_WIDTH, WINDOW_HEIGHT, IMAGEWIDTH, IMAGEHEIGHT)
    mosquito = Mosquito(IMAGEWIDTH, IMAGEHEIGHT, random_x, random_y)
    mosquito_list.append(mosquito)
    return mosquito_list

'''
==============================================================================================
==============================================================================================
=========================================頁面=================================================
'''
def loading_page():
    # font
    start_font = pygame.font.SysFont(None, 60)

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

def menu():
    # image
    menu_background = pygame.image.load(("menu.png")).convert()
    menu_background = pygame.transform.scale(menu_background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    game_start1 = pygame.image.load(("start_mark1.png")).convert_alpha()
    game_start1 = pygame.transform.scale(game_start1, (START_MARK_WIDTH, START_MARK_HEIGHT))
    game_start2 = pygame.image.load(("start_mark2.png")).convert_alpha()
    game_start2 = pygame.transform.scale(game_start2, (START_MARK_WIDTH, START_MARK_HEIGHT))
    game_start_rect = pygame.Rect(WINDOW_WIDTH - 300, WINDOW_HEIGHT - 400, START_MARK_WIDTH, START_MARK_HEIGHT)
    
    # font
    play_font = pygame.font.SysFont(None, 70)
    play_text_surface = play_font.render("Play", True, (255, 240, 100))

    # sound
    startmark_sound = pygame.mixer.Sound("start_mark_sound.wav")
    startmark_sound.set_volume(0.5)

    # play menu BGM
    pygame.mixer.music.load("BreathAndLife.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

    # menu setting
    mouse_in_startmark = False
    opacity = 0

    # menu
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif game_start_rect.collidepoint((pygame.mouse.get_pos())):
                # 滑鼠選中開始按鈕特效
                if mouse_in_startmark == False:
                    startmark_sound.fadeout(170)
                    startmark_sound.play()
                    mouse_in_startmark = True
                # 開始遊戲
                elif event.type == MOUSEBUTTONDOWN:
                    window_surface.fill(BLACK)
                    pygame.display.update()
                    # bgm淡出    
                    pygame.mixer.music.fadeout(500)
                    return 'b'
            elif mouse_in_startmark == True:
                mouse_in_startmark = False

        window_surface.fill(BLACK)
        
        # 渲染物件
        blit_alpha(window_surface, menu_background, (0, 0), opacity)
        if opacity < 255:
            opacity += 1
            
        if mouse_in_startmark:
            window_surface.blit(game_start2, (game_start_rect.topleft))
        else:
            window_surface.blit(game_start1, (game_start_rect.topleft))
        window_surface.blit(play_text_surface, ( play_text_surface.get_rect( center = (WINDOW_WIDTH - 300 + START_MARK_WIDTH/2, WINDOW_HEIGHT - 400 + START_MARK_HEIGHT/2) ) ) )
        pygame.display.update()
        main_clock.tick(FPS)
    
def game():
    # load image
    background = pygame.image.load(("forest.jpg")).convert()
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    new_cursor = pygame.image.load(("hand.png")).convert_alpha()
    new_cursor = pygame.transform.scale(new_cursor, (MOUSEWIDTH, MOUSEHEIGHT))
    pause_image = pygame.image.load(("pause.png")).convert_alpha()
    pause_image = pygame.transform.scale(pause_image, (40, 40))
    pause_rect = pygame.Rect(WINDOW_WIDTH - 55, 15, 40, 40)
    
    # load BGM and sound
    hit_sound = pygame.mixer.Sound("hit.wav")
    hit_sound.set_volume(1.0)
    swing_sound = pygame.mixer.Sound("swing.wav")
    swing_sound.set_volume(0.8)
    kill_sound = pygame.mixer.Sound("kill.wav")
    mosquito_create_sound = pygame.mixer.Sound("magic.wav")
    fire_sound = pygame.mixer.Sound("fire.wav")
    fire_sound.set_volume(0.3)

    # font
    text_font = pygame.font.SysFont(None, 70)
    my_font = pygame.font.SysFont(None, 50)

    # mosquito moving setting
    reload_mosquito_event = USEREVENT + 1
    pygame.time.set_timer(reload_mosquito_event, 300)

    # play game BGM
    pygame.mixer.music.load("Mortals.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    opacity = 0
    points = 0
    # the quantity of killed mosquito
    kill_quantity = 0
    # the quantity of new born mosquito
    count = 0
    skill_energe = 0
    mosquito_group = []
    blood_group = []
    magic_circle_group = []
    fire_group = []

    # 初始產生兩隻蚊子
    create_new_mosquito(mosquito_group)
    create_new_mosquito(mosquito_group)

    # 淡入畫面
    while opacity < 255:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        window_surface.fill(BLACK)
        blit_alpha(window_surface, background, (0, 0), opacity)
        opacity += 3
        pygame.display.update()
        main_clock.tick(FPS)

    # Game
    while True:
        # 偵測事件
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == reload_mosquito_event:
                # 偵測到重新整理事件，固定時間讓蚊子換新位置
                for mosquito in mosquito_group:
                    random_x, random_y = get_random_position(WINDOW_WIDTH, WINDOW_HEIGHT, IMAGEWIDTH, IMAGEHEIGHT)
                    mosquito.rect.topleft = (random_x, random_y)
                
            elif event.type == MOUSEBUTTONDOWN:
                swing_sound.play()
                # 遊戲暫停
                if pause_rect.collidepoint((pygame.mouse.get_pos())):
                    # 播放「遊戲暫停」音效 
                    pygame.mixer.Sound("pause.mp3").play()

                    continue_sound = pygame.mixer.Sound("start_mark_sound.wav")
                    continue_sound.set_volume(0.7)
                    
                    pause_background = pygame.image.load("pause_background.png").convert_alpha()
                    pause_background = pygame.transform.scale(pause_background, (WINDOW_WIDTH, WINDOW_HEIGHT))

                    continue_mark = Oval(510, 180, WINDOW_WIDTH/2 - 255,  WINDOW_HEIGHT/2 - 100)
                    text_continue = text_font.render("Continue", True, (WHITE))
                    text_continue_rect = text_continue.get_rect(center = continue_mark.rect.center)
                    
                    back_to_menu = Oval(510, 180,  WINDOW_WIDTH/2 - 255,  WINDOW_HEIGHT/2 + 100)
                    text_backtomenu = text_font.render("Back to menu", True, (WHITE))
                    text_backtomenu_rect = text_backtomenu.get_rect(center = back_to_menu.rect.center)
                    continue_to_game = False

                    blit_alpha(window_surface, pause_background, (0, 0), 100)
                    window_surface.blit(continue_mark.image, (continue_mark.rect.topleft))
                    window_surface.blit(back_to_menu.image, (back_to_menu.rect.topleft))
                    window_surface.blit(text_continue, (text_continue_rect))
                    window_surface.blit(text_backtomenu, (text_backtomenu_rect))
                    
                    pygame.display.update()
                    
                    while True:
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event.type == MOUSEBUTTONDOWN:
                                if continue_mark.rect.topleft[0] < pygame.mouse.get_pos()[0] < continue_mark.rect.topleft[0] + continue_mark.width and continue_mark.rect.topleft[1] < pygame.mouse.get_pos()[1] < continue_mark.rect.topleft[1] + continue_mark.height:
                                    continue_to_game = True
                                elif back_to_menu.rect.topleft[0] < pygame.mouse.get_pos()[0] < back_to_menu.rect.topleft[0] + back_to_menu.width and back_to_menu.rect.topleft[1] < pygame.mouse.get_pos()[1] < back_to_menu.rect.topleft[1] + back_to_menu.height:
                                    # 回到菜單
                                    for mosquito in mosquito_group:
                                        mosquito.kill()
                                    for magic_circle in magic_circle_group:
                                        magic_circle.kill()
                                    for fire in fire_group:
                                        fire.kill()
                                    for blood in blood_group:
                                        blood.kill()
                                    return 'a'
                        # 回到遊戲
                        if continue_to_game:
                            break
                        
                        main_clock.tick(FPS)
                    
                    continue_mark.kill()
                    back_to_menu.kill()
                    continue_sound.play()

                else:
                    # 當使用者點擊滑鼠時，檢查是否滑鼠位置 x, y 有在蚊子圖片上
                    for mosquito in mosquito_group:
                        if mosquito.rect.collidepoint((pygame.mouse.get_pos())):
                            hit_sound.play()
                            
                            # The mosquito die
                            if mosquito.life == 1:
                                kill_sound.play()
                                mosquito_group.remove(mosquito)
                                mosquito.kill()
                                kill_quantity += 1

                                # 蚊子滅絕 遊戲結束
                                if mosquito_extint(mosquito_group):
                                    window_surface.fill(BLACK)
                                    pygame.display.update()

                                    for fire in fire_group:
                                        fire.kill()
                                    for blood in blood_group:
                                        blood.kill()
                                    # bgm淡出
                                    pygame.mixer.music.fadeout(1200)
                                    fire_sound.fadeout(1200)
                                    calculate_points(points, kill_quantity)
                                    return 'a'
                                else:
                                    skill_energe += 5
                            else:
                                mosquito.life -= 1
                                
                                # 打中蚊子特效
                                blood = Blood(IMAGEWIDTH, IMAGEHEIGHT, mosquito.rect.topleft[0], mosquito.rect.topleft[1])
                                blood_group.append(blood)
                                
                                points += 5
                                skill_energe += 1
                                break
            
            elif event.type == pygame.KEYDOWN and skill_energe >= 10:
                if event.key == pygame.K_SPACE:
                    fire_sound.fadeout(1000)
                    fire_sound.play()  
                    skill_energe -= 10

                    magic_circle = Magic_circle()
                    magic_circle_group.append(magic_circle)

                    for mosquito in mosquito_group:
                        if mosquito.life <= 2:
                            mosquito.kill()
                            mosquito_group.remove(mosquito)
                            kill_quantity += 1
                            fire = Fire(IMAGEWIDTH, IMAGEHEIGHT+160, mosquito.rect.topleft[0], mosquito.rect.topleft[1])
                            fire_group.append(fire)
                            skill_energe += 1
                        else:
                            mosquito.life -= 2
                    
                    # 蚊子滅絕 遊戲結束
                    if mosquito_extint(mosquito_group):
                        window_surface.fill(BLACK)
                        pygame.display.update()

                        for fire in fire_group:
                            fire.kill()
                        for blood in blood_group:
                            blood.kill()
                        # bgm淡出
                        pygame.mixer.music.fadeout(1200)
                        fire_sound.fadeout(1200)
                        calculate_points(points, kill_quantity)
                        return 'a'
        # 新增蚊子
        if count and len(mosquito_group) < 10:
            mosquito_create_sound.play()
            while count >= 1:
                create_new_mosquito(mosquito_group)
                count -= 1
                if len(mosquito_group) >= 10:
                    break

        # 背景顏色，清除畫面
        window_surface.fill(BLACK)
        
        # 遊戲分數儀表板
        points_text_surface = my_font.render("Points: {}".format(points), True, (WHITE))

        # 玩家能量
        energe_text_surface = my_font.render("Energe: {}".format(skill_energe), True, (WHITE))

        # 蚊子數量
        mosquito_quantity_text_surface = my_font.render("Mosquitoes: {}".format(len(mosquito_group)), True, (WHITE))

        # 渲染物件 同時進行更新
        window_surface.blit(background, (0, 0))
        for blood in blood_group:
            window_surface.blit(blood.image, blood.rect)
            blood.update(blood_group)

        for fire in fire_group:
            window_surface.blit(fire.image, fire.rect)
            fire.update(fire_group)
        
        for magic_circle in magic_circle_group:
            blit_alpha(window_surface, magic_circle.image, (magic_circle.rect.topleft), magic_circle.opacity)
            if magic_circle.opacity >= 10:
                magic_circle.update()          
            else:
                magic_circle_group.remove(magic_circle)
                magic_circle.kill()
        
        for mosquito in mosquito_group:
            window_surface.blit(mosquito.image, mosquito.rect)
            # 蚊子能量>=500時，產生新的蚊子；否則蚊子的能量增加
            if mosquito.energe >= 500:
                mosquito.energe -= 500
                count += 1
            else:
                mosquito.energe += random.randint(0, 3)
        
        window_surface.blit(points_text_surface, (10, 10))
        window_surface.blit(energe_text_surface, (10, 50))
        window_surface.blit(mosquito_quantity_text_surface, (10, 90))
        window_surface.blit(pause_image, (pause_rect.topleft))
        window_surface.blit(new_cursor, (pygame.mouse.get_pos()[0] - MOUSEWIDTH/2, pygame.mouse.get_pos()[1] - MOUSEHEIGHT/2))

        # 畫面更新
        pygame.display.update()
        
        # 控制遊戲迴圈迭代速率
        main_clock.tick(FPS)

def calculate_points(final_points, final_killed):
    # load pictures
    sunset = pygame.image.load(("sunset.jpg")).convert()
    sunset =  pygame.transform.scale(sunset, (WINDOW_WIDTH, WINDOW_HEIGHT))

    # font
    points_font = pygame.font.Font("Ragara.otf", 90)
    
    # text
    points_text_surface = points_font.render("Final Points: {}".format(final_points), True, (WHITE))
    kill_quantity_surface = points_font.render("Killed {} mosquito".format(final_killed), True, (WHITE))

    pygame.mixer.music.load("wind_path.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

    opacity = 0

    while opacity < 255:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        window_surface.fill(BLACK)
        blit_alpha(window_surface, sunset, (0, 0), opacity)
        opacity += 1
        pygame.display.update()
        main_clock.tick(FPS)

    # the end of the game
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    window_surface.fill(BLACK)
                    pygame.display.update()

                    # bgm淡出    
                    pygame.mixer.music.fadeout(100)
                    return

        # 遊戲分數儀表板
        window_surface.blit(sunset, (0, 0))
        window_surface.blit(points_text_surface, points_text_surface.get_rect(topleft = (20, WINDOW_HEIGHT / 2 - 60)))
        window_surface.blit(kill_quantity_surface, kill_quantity_surface.get_rect(topleft = (20, WINDOW_HEIGHT / 2 + 60)))

        # 畫面更新
        pygame.display.update()
        # 控制遊戲迴圈迭代速率
        main_clock.tick(FPS)

#-------------------------------------------------------------------------------------

def main():
    
    loading_page()

    # 切換頁面變數
    mode = 'a'
    
    while True:
        match mode:
            # 遊戲菜單
            case 'a':
                mode = menu()

            # 遊戲頁面
            case 'b':
                mode = game()

            # 計分頁面 (目前不會從這邊執行到)
            case 'c':
                calculate_points(0, 0)
                mode = 'a'

if __name__ == '__main__':    
    main()