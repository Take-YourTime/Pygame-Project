import pygame 
import os
import random 

#建立變數
WIDTH = 600
HEIGHT = 600

FPS = 60 

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)

color_list = [RED , GREEN , BLUE ]


#初始化程式
pygame.init()
pygame.mixer.init()
collision_sound = pygame.mixer.Sound(os.path.join("sound\\collision.wav"))


#更改遊戲的名字
pygame.display.set_caption("小遊戲")

#傳入一個元組 (寬度 and 高度) and 給一個變數 screen 
screen = pygame.display.set_mode((WIDTH , HEIGHT))

#創建一個物件(對時間管理 and 操控)
clock = pygame.time.Clock()

#設定遊戲迴圈的變數
running = True

def draw_rectangle(surface , color , x , y , width_for_rectangle , height):

    #這裡賦值座標跟寬高給rect_fill
    rect_fill = pygame.Rect( x , y , width_for_rectangle , height)

    #這裡畫出矩形->surface就是我們的screen,顏色是紅色,實心
    pygame.draw.rect(surface , color , rect_fill , width = 0 )

def draw_circle(surface, color , center_x, center_y , radius ):

    #定義圓心位置
    center = (center_x , center_y)

    #畫出圓形,surface就是我們的screen, 顏色是綠色, 實心
    pygame.draw.circle(surface , color , center , radius)

class Player(pygame.sprite.Sprite):
    def __init__(self, width , height):
        #初始化物件
        super().__init__()
        #這裡使用 pygame.Surface((width, height)) 創建了一個寬度為 width 像素、高度為 height 像素的 Surface 物件。
        #這將成為精靈的圖片，其寬度和高度可以根據遊戲需求調整。
        self.image = pygame.Surface((width , height))
        self.rect = self.image.get_rect()  # 獲取方塊圖像的矩形區域
        self.rect.center = (150,150)
        #self.rect.center = (WIDTH // 2, HEIGHT // 2)  # 設置方塊圖像的初始位置為視窗中心
        self.speed = 5  # 設置方塊移動的速度

    def update(self): 
    # 繪製方塊
        draw_rectangle(self.image, RED, 0, 0, self.rect.width, self.rect.height)

        #更新方法，根據鍵盤輸入來更新方塊的位置
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0 :  # 如果按下左箭頭鍵
            self.rect.x -= self.speed  # 方塊向左移動
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH :  # 如果按下右箭頭鍵
            self.rect.x += self.speed  # 方塊向右移動
        if keys[pygame.K_UP] and self.rect.top > 0 :  # 如果按下上箭頭鍵
            self.rect.y -= self.speed  # 方塊向上移動
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:  # 如果按下下箭頭鍵
            self.rect.y += self.speed  # 方塊向下移動

class Rock(pygame.sprite.Sprite):
    def __init__(self , radius):
        super().__init__()
        self.image = pygame.Surface((radius*2 , radius*2))
        self.radius = radius
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(0,WIDTH)
        self.rect.centery = random.randrange(0,HEIGHT)
        self.color = random.choice(color_list)
        self.image.set_colorkey(BLACK)    

    def update(self):
        draw_circle(self.image , self.color , self.rect.width // 2 , self.rect.height // 2 , self.radius)


#創建方塊精靈
box = Player(50, 50)  # 創建一個方塊精靈，並指定寬度和高度

rock = Rock(20)

box_sprites = pygame.sprite.Group()  # 創建一個精靈群組
rock_sprites = pygame.sprite.Group() 

# group
box_sprites.add(box)  # 將方塊精靈添加到精靈群組中

rock_sprites.add(rock)

#會生成新石頭(創建一個石頭精靈，放進群組)
def new_rock():
    rock = Rock(20)
    rock_sprites.add(rock)

#遊戲迴圈
while running:
    
    #設定遊戲幀數
    clock.tick(FPS) 
    
    #從for迴圈中得到事件
    for event in pygame.event.get():
            #如果 得到的事件 是 關掉遊戲
        if event.type == pygame.QUIT:
            running = False #那就讓遊戲迴圈停止
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     if event.button == 4 and box.rect.top > 0 :  # 滾輪向上
        #         box.rect.y -= box.speed
        #     elif event.button == 5 and box.rect.bottom < HEIGHT :  # 滾輪向下
        #         box.rect.y += box.speed
        #     elif event.button == 1 and box.rect.left > 0:  # 滑鼠左鍵
        #         box.rect.x -= box.speed
        #     elif event.button == 3 and box.rect.right < WIDTH :  # 滑鼠右鍵
        #         box.rect.x += box.speed
    
    # 繪製背景
    screen.fill(WHITE)

    # update
    box_sprites.update()
    rock_sprites.update()

    # blit
    box_sprites.draw(screen)
    rock_sprites.draw(screen)

    hits = pygame.sprite.groupcollide(box_sprites, rock_sprites, False, True)
    for hit in hits:
        collision_sound.play()
        new_rock()

    #更新畫面!!
    pygame.display.update()



#退出遊戲
pygame.quit()   

