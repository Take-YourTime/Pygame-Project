from Pieces import PiecesGroup
from Pieces import Pieces
from Setting import *
import pygame
import math
import os
import sys

pygame.init()

word = os.path.join("img" , "font.ttf")

#---------------------<初始設定>---------------------
#========>物件<========
#Clock
clock = pygame.time.Clock()
#Screen
win = pygame.display.set_mode((WIN_WIDTH_HEIGHT,WIN_WIDTH_HEIGHT))    #Build a screen  
pygame.display.set_caption("五子棋")  #Screen Title
white_img = pygame.image.load(os.path.join("img","White.png")).convert_alpha()
white_img = pygame.transform.scale(white_img,(UNIT_LENGTH-3,UNIT_LENGTH-3)) #縮放
black_img = pygame.image.load(os.path.join("img","Black.png")).convert_alpha()
black_img = pygame.transform.scale(black_img,(UNIT_LENGTH-3,UNIT_LENGTH-3)) #縮放 
#PieceGroup
piecegroup = PiecesGroup()
#---------------------<DEF>---------------------

# 繪製透明圖片
def blit_alpha(target, source, location, opacity): # window 圖片 位置 透明度
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, ( -x, - y ))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)        
    target.blit(temp, location)


def draw_text(surface:pygame.surface.Surface, text:str , size:int , x:float , y:float , color:tuple) -> None:
    font = pygame.font.Font( word , size )
    text_surface = font.render( text , True , color ) 
    text_rect = text_surface.get_rect()
    text_rect.centerx = x 
    text_rect.centery = y 
    surface.blit(text_surface , text_rect)

def get_mouse_coordinate() -> tuple:
    mouse_pos = pygame.mouse.get_pos()  #獲得滑鼠位置
    x = math.floor(mouse_pos[0]/UNIT_LENGTH-0.5)    #無條件捨去
    y = math.floor(mouse_pos[1]/UNIT_LENGTH-0.5)    #無條件捨去
    return (x,y)

#背景繪製
def draw_background(surface:pygame.surface.Surface) -> None:
    #背景顏色
    surface.fill(WIN_BACKGROUND_COLOR)
    
    color = (0,0,0) #Black
    width = 1
    #畫直線
    for i in range(WAY):
        start_pos = (UNIT_LENGTH*(i+1),UNIT_LENGTH)
        end_pos = (UNIT_LENGTH*(i+1),UNIT_LENGTH*WAY)
        pygame.draw.line(surface,color,start_pos,end_pos,width)
    #畫橫線
        start_pos = (UNIT_LENGTH,UNIT_LENGTH*(i+1))
        end_pos = (UNIT_LENGTH*WAY,UNIT_LENGTH*(i+1))
        pygame.draw.line(surface,color,start_pos,end_pos,width)
    #中心點
        if i == 8:  
            pygame.draw.circle(surface ,color ,(UNIT_LENGTH*i, UNIT_LENGTH*i) , 5)
        elif i == 4:
            pygame.draw.circle(surface , color , ((UNIT_LENGTH*i, UNIT_LENGTH*i)) , 5)
            pygame.draw.circle(surface , color , ((UNIT_LENGTH*i, UNIT_LENGTH*(WAY-i+1))) , 5)
        elif i == 12:
            pygame.draw.circle(surface , color , ((UNIT_LENGTH*i, UNIT_LENGTH*i)) , 5)
            pygame.draw.circle(surface , color , ((UNIT_LENGTH*i, UNIT_LENGTH*(WAY-i+1))) , 5)
            

    #劃出誰拿黑誰拿白
    draw_text(win , "玩家1" , 30 , 80 , 725 , BLACK)
    draw_text(win , "玩家2" , 30 , 670 , 725 , BLACK )
    win.blit(white_img , (580 , 705))
    win.blit(black_img , (130 , 705))

    #畫橫線
    # for i in range(WAY):
    #     start_pos = (UNIT_LENGTH,UNIT_LENGTH*(i+1))
    #     end_pos = (UNIT_LENGTH*WAY,UNIT_LENGTH*(i+1))
    #     pygame.draw.line(surface,color,start_pos,end_pos,width)

def draw_win(surface:pygame.surface.Surface) -> None:
    if(piecegroup.winner != 0): #要先有贏家
        
        color = (255, 0, 0)   #red
        start_pos = (UNIT_LENGTH * (piecegroup.win_start[0] + 1), UNIT_LENGTH * (piecegroup.win_start[1] + 1))
        end_pos = (UNIT_LENGTH * (piecegroup.win_end[0] + 1), UNIT_LENGTH * (piecegroup.win_end[1] + 1))
        width = 5
        pygame.draw.line(surface, color, start_pos, end_pos, width)
        #畫出勝利者的圖示
        draw_text(win, f"玩家{piecegroup.winner} is winner!!", 50, 375, 375, (176, 72, 255))
        pygame.display.update()
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False

        piecegroup.winner = 0
        piecegroup.reset()
        return True
    return False


def Loading_Page(window_surface, main_clock):
    pygame.init()
    # font
    start_font = pygame.font.SysFont(None, 60)

    # global variable
    global WIN_WIDTH_HEIGHT

    # start page setting
    start_color = 255
    start_color_detect = True
    running = True

    # start the game
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
        window_surface.blit(start_text_surface, (100, WIN_WIDTH_HEIGHT/2))
        pygame.display.update()
        main_clock.tick(FPS)

    


#--------------------<Main>---------------------
def main() -> None:

    global piecegroup
    running = True

    while running:
        clock.tick(FPS) #畫面更新頻率
        #key_down = False

        pos = get_mouse_coordinate()

        #取得輸入input
        for event in pygame.event.get():
            #關閉視窗
            if event.type == pygame.QUIT:   
                pygame.quit()
                sys.exit()

            #滑鼠按下
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                if piecegroup.winner == 0:  #若產生贏家就停下來
                    #if key_down == True:
                        #key_down = False
                    
                    if((pos[0] >= 0) and (pos[0] < WAY and (pos[1] >= 0) and (pos[1] < WAY))):
                        piecegroup.move(pos[0], pos[1])
                        if piecegroup.winner != 0:
                            print("Winner is", piecegroup.winner)
            
            #按下鍵盤按鍵，且按下的是R鍵                
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r :  
                if piecegroup.winner != 0:  #產生贏家才可以開新的一局
                    #piecegroup = PiecesGroup()
                    piecegroup.reset()     
        
        #更新遊戲update
        
        #畫面顯示render
        draw_background(win)

        if((pos[0] >= 0) and (pos[0] < WAY) and (pos[1] >= 0) and (pos[1] < WAY)):  #呈現點下滑鼠後要放置的棋子
            if piecegroup.check(pos[0], pos[1]) == True:
                piece = Pieces(pos[0], pos[1], piecegroup.turn)
                blit_alpha(win, piece.image, (piece.rect.topleft), 100)
                piece.kill()
        
        piecegroup.draw(win)
        if draw_win(win):
            running = False

        pygame.display.update() #Update Screen


#---------------------<     >---------------------
if(__name__ == "__main__"):

    index = 0

    while True:
        if index == 0:
            Loading_Page(win, clock)
            index = 1
        elif index == 1:
            main()
            index = 0

    pygame.quit()