from typing import Any
import pygame
import math
import pandas

from pygame.sprite import Group

from function import get_normalize_vector, numberFollowTarget, WINDOW_WIDTH, WINDOW_HEIGHT, WHITE
from random import randint

class Player(pygame.sprite.Sprite):
    raw_image = pygame.image.load(("player/stand1_1.png")).convert_alpha()

    def __init__(self, location_x, location_y):
        super().__init__()
        self.image = Player.raw_image
        self.ATKimages = [  [ pygame.image.load(("player//swingO1_0.png")).convert_alpha(),
                              pygame.image.load(("player//swingO1_1.png")).convert_alpha(),
                              pygame.image.load(("player//swingO1_2.png")).convert_alpha() ],
                            [ pygame.image.load(("player//swingO2_0.png")).convert_alpha(),
                              pygame.image.load(("player//swingO2_1.png")).convert_alpha(),
                              pygame.image.load(("player//swingO2_2.png")).convert_alpha() ],
                            [ pygame.image.load(("player//swingO1_0.png")).convert_alpha(),
                              pygame.image.load(("player//swingO3_1.png")).convert_alpha(),
                              pygame.image.load(("player//swingO3_2.png")).convert_alpha() ] ]
        self.ATKseries_index = 0 # 0 ~ 2
        self.ATKseries_photo_index = 0 # 0 ~ 2
        self.isATK = False
        self.rect = self.raw_image.get_rect()
        self.rect.topleft = (location_x, location_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.width = Player.raw_image.get_width()
        self.height = Player.raw_image.get_height()
        self.life = 50
        self.power = 100
        # font
        self.life_font = pygame.font.SysFont(None, 40)
        self.life_text_surface = self.life_font.render("Life: {}".format(self.life), True, (WHITE))
    
    def update(self):
        if self.power < 100:
            self.power += 1
        
        if self.isATK == True:
            self.image = self.ATKimages[self.ATKseries_index][self.ATKseries_photo_index // 11]

            ATKSERIES_FINAL_INDEX = 2            # 3 - 1
            ATKSERIES_PHOTO_FINAL_INDEX = 32     # 11*3 - 1

            # Change ATK photo
            if self.ATKseries_photo_index == ATKSERIES_PHOTO_FINAL_INDEX:
                self.ATKseries_photo_index = 0
                self.isATK = False
                # Change ATK photo series 
                if self.ATKseries_index == ATKSERIES_FINAL_INDEX:
                    self.ATKseries_index = 0
                else:
                    self.ATKseries_index += 1
            else:
                self.ATKseries_photo_index += 1
        else:
            self.image = Player.raw_image
        
    def attack(self):
        if self.power > 0:
            self.isATK = True
            self.power -= 30

    def hurt(self, damage):
        self.life -= damage
        self.life_text_surface = self.life_font.render("Life: {}".format(self.life), True, (WHITE))


# 用於發射的子彈
class Pencil(pygame.sprite.Sprite):
    raw_image = pygame.image.load(("pencil.png")).convert_alpha()
    hit_sound = pygame.mixer.Sound("hit.wav")
    hit_sound.set_volume(0.5)

    def __init__(self, width, height, location, destination):
        super().__init__()
        self.image = Pencil.raw_image
        self.angle = 0
        # rotate image
        if destination[0] - location[0] == 0:
            # 特例情況：除數為0
            self.image = pygame.transform.rotate(self.image, 90)
            self.angle = 90
        else:
            # 藉由發射位置與滑鼠位置形成的直角三角形，先以arctan函數求得弧度，再代入弧度轉角度的公式
            # Original function: math.atan((destination[1] - location[1]) / (destination[0] - location[0])) * 360 / 2 / math.pi * (-1)
            # 以下為化簡後的結果
            self.angle = math.atan( (destination[1] - location[1]) / (destination[0] - location[0]) ) * (-180) / math.pi
            self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.topleft = location
        self.mask = pygame.mask.from_surface(self.image)
        self.width = width
        self.height = height
        self.location = location
        self.vector_x, self.vector_y = get_normalize_vector(location[0], location[1], destination[0], destination[1])
        # pencil speed
        self.multiple = 13
        # survial time
        self.time = 0
        
    
    def update(self, magician_group, stone_group, banana_group, monkeyKing_group, monkey_group, pencilFolded_group):
        
        # adjust moving speed
        if(self.time > 35):
            self.multiple = 15
        elif(self.time > 25):
            self.multiple = 3
            self.time += 1
        elif(self.time > 20):
            self.multiple = 4
            self.time += 1
        elif(self.time > 15):
            self.multiple = 5
            self.time += 1
        else:
            self.time += 1
        
        # pencil move
        self.location = (self.location[0] + self.vector_x * self.multiple, self.location[1] + self.vector_y * self.multiple)
        self.rect.topleft = self.location

        if(self.location[0] > WINDOW_WIDTH + self.width or self.location[0] < -(self.width) or self.location[1] > WINDOW_HEIGHT + self.height or self.location[1] < -(self.height)):
            self.kill()
            return
        
        # Whether hit monstrer
        for magician in magician_group:
            # The two rectangles overlap
            if magician.rect.colliderect(self.rect):
                # The two picture mask overlap
                if magician.mask.overlap(self.mask, (self.rect.left - magician.rect.left, self.rect.top - magician.rect.top)):
                    Pencil.hit_sound.play()
                    pencilFolded_group.add( PencilFolded(self.rect.topleft, self.angle) )
                    self.kill()
                    magician.update()
                    return
        
        for stone in stone_group:
            if stone.rect.colliderect(self.rect):
                if stone.mask.overlap(self.mask, (self.rect.left - stone.rect.left, self.rect.top - stone.rect.top)):
                    pencilFolded_group.add( PencilFolded(self.rect.topleft, self.angle) )
                    self.kill()
                    stone.kill()
                    return
        
        for banana in banana_group:
            if banana.rect.colliderect(self.rect):
                if banana.mask.overlap(self.mask, (self.rect.left - banana.rect.left, self.rect.top - banana.rect.top)):
                    pencilFolded_group.add( PencilFolded(self.rect.topleft, self.angle) )
                    self.kill()
                    banana.kill()
                    return
            
        for monkeyKing in monkeyKing_group:
            if monkeyKing.rect.colliderect(self.rect):
                if monkeyKing.mask.overlap(self.mask, (self.rect.left - monkeyKing.rect.left, self.rect.top - monkeyKing.rect.top)):
                    Pencil.hit_sound.play()
                    pencilFolded_group.add( PencilFolded(self.rect.topleft, self.angle) )
                    self.kill()
                    monkeyKing.hurt()
                    return
        
        for monkey in monkey_group:
            if monkey.rect.colliderect(self.rect):
                if monkey.mask.overlap(self.mask, (self.rect.left - monkey.rect.left, self.rect.top - monkey.rect.top)):
                    Pencil.hit_sound.play()
                    pencilFolded_group.add( PencilFolded(self.rect.topleft, self.angle) )
                    self.kill()
                    monkey.hurt()
                    return

class PencilFolded(pygame.sprite.Sprite):
    raw_images = [pygame.image.load(("pencil_fold.png")).convert_alpha(),
                  pygame.image.load(("pencil_fold_1.png")).convert_alpha()]

    def __init__(self, location, angle) -> None:
        super().__init__()
        self.image = pygame.transform.rotate(PencilFolded.raw_images[randint(0, 1)], angle)
        # rotate image
        self.rect = self.image.get_rect()
        self.rect.x = location[0]
        self.rect.centery = location[1]
        # image opacity
        self.opacity = 255
        
    
    def update(self) -> None:
        self.opacity -= 5
        if self.opacity <= 0:
            self.kill()

# attck energy
class AP(pygame.sprite.Sprite):

    raw_image = pygame.image.load(("player//APline.png")).convert_alpha()
    raw_image = pygame.transform.scale(raw_image, (100, 20))

    def __init__(self, location) -> None:
        super().__init__()
        self.image = AP.raw_image
        self.rect = self.image.get_rect()
        self.rect.topleft = location
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.isAPchange = False
    
    def update(self, player_AP) -> None:
        if self.isAPchange and player_AP > 0:
            newWidth = numberFollowTarget(self.width, player_AP, 0.5)
            if(self.width - newWidth <= 1):
                self.isAPchange = False
            else:
                self.image = pygame.transform.scale(AP.raw_image, (newWidth, self.height))
                self.width = newWidth
        if 0 < player_AP < 100:
            self.image = pygame.transform.scale(AP.raw_image, (player_AP, self.height))