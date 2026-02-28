from typing import Any
import pygame
from pygame.sprite import Group
import function
from random import randint

pygame.mixer.init()

class Monkey(pygame.sprite.Sprite):
    raw_image = pygame.image.load(("monkey\\monkey.png")).convert_alpha()
    ATKimages = [   pygame.image.load(("monkey\\attack1_0.png")).convert_alpha(),
                    pygame.image.load(("monkey\\attack1_1.png")).convert_alpha(),
                    pygame.image.load(("monkey\\attack1_2.png")).convert_alpha(),
                    pygame.image.load(("monkey\\attack1_3.png")).convert_alpha(),
                    pygame.image.load(("monkey\\attack1_4.png")).convert_alpha(),
                    pygame.image.load(("monkey\\attack1_5.png")).convert_alpha(),
                    pygame.image.load(("monkey\\attack1_6.png")).convert_alpha(),
                    pygame.image.load(("monkey\\attack1_7.png")).convert_alpha(),
                    pygame.image.load(("monkey\\attack1_8.png")).convert_alpha()]
    walkingImages = [   pygame.image.load(("monkey\\move_1.png")).convert_alpha(),
                        pygame.image.load(("monkey\\move_2.png")).convert_alpha(),
                        pygame.image.load(("monkey\\move_3.png")).convert_alpha()]
    dieImages = [pygame.image.load(("monkey\\die1_0.png")).convert_alpha(),
                 pygame.image.load(("monkey\\die1_1.png")).convert_alpha(),
                 pygame.image.load(("monkey\\die1_2.png")).convert_alpha()]
    mask = pygame.mask.from_surface(raw_image)
    
    showUp_sound = pygame.mixer.Sound("monkey\\show_up.wav")
    showUp_sound.set_volume(0.35)

    def __init__(self, location_x, location_y) -> None:
        super().__init__()
        self.image = Monkey.raw_image
        # images index
        self.index = 0
        self.x_moving_destination = randint(250, 350)
        # attack or not
        self.isATK = False

        # move or not
        self.keepWalking = True

        # skill energy
        self.energy = 300
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (location_x, location_y)
        self.x = float(location_x)
        self.width = Monkey.raw_image.get_width()
        self.height = Monkey.raw_image.get_height()
        self.life = 10
        
    def update(self, player, monkey_BananaHit_group):
        THROW_BANANA_FRAME = 119
        FINAL_FRAME = 180

        if self.keepWalking:
            self.moving()
        elif self.isATK:
            if self.index < THROW_BANANA_FRAME:
                self.image = Monkey.ATKimages[self.index // 20]
                self.index += 1
            elif self.index == THROW_BANANA_FRAME:
                Monkey_BananaHit.hit_face_sound.play()
                monkey_BananaHit_group.add( Monkey_BananaHit(player.rect.centerx - 30, player.rect.top + 60) )
                player.hurt(1)
                self.index += 1
            elif self.index < FINAL_FRAME:
                self.image = Monkey.ATKimages[self.index // 20]
                self.index += 1
            else:
                self.image = Monkey.raw_image
                self.isATK = False
                self.index = 0
        elif self.energy >= 300:
            self.attack()
            self.energy = 0
        else:
            self.energy += 1
    
    def attack(self):
        self.isATK = True
    
    def hurt(self):
        if self.life > 0:
            self.life -= 1
        else:
            self.kill()

    def moving(self):
        if self.rect.left > self.x_moving_destination:
            self.index += 1
            # FRAME_1 = 15
            # FRAME_2 = 45
            # FRAME_3 = 70
            # FINAL_FRAME = 90

            if self.index == 90:
                self.index = 0
                self.image = Monkey.raw_image
            elif self.index >= 70:
                self.x -= 1.5
                self.image = Monkey.walkingImages[2]
            elif self.index >= 45:
                self.x -= 1.5
                self.image = Monkey.walkingImages[1]
            elif self.index >= 15:
                self.x -= 2
                self.image = Monkey.walkingImages[0]
            else:
                self.x -= 0.5
                self.image = Monkey.raw_image
            
            self.rect.left = self.x
            
        else:
            self.index = 0
            self.keepWalking = False
            self.image = Monkey.raw_image


class Monkey_BananaHit(pygame.sprite.Sprite):
    images = [pygame.image.load(("monkey\\banana\\banana1.png")).convert_alpha(),
              pygame.image.load(("monkey\\banana\\banana2.png")).convert_alpha(),
              pygame.image.load(("monkey\\banana\\banana3.png")).convert_alpha(),
              pygame.image.load(("monkey\\banana\\banana4.png")).convert_alpha(),
              pygame.image.load(("monkey\\banana\\banana5.png")).convert_alpha()]
    hit_face_sound = pygame.mixer.Sound("monkey\\banana\\banana_hit_face.wav")
    hit_face_sound.set_volume(0.5)
    
    def __init__(self, location_x, location_y) -> None:
        super().__init__()
        self.image = Monkey_BananaHit.images[0]

        # images index
        self.index = 0
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (location_x, location_y)
        self.y = float(location_y)

    def update(self) -> None:
        if self.index < 50:
            self.image = Monkey_BananaHit.images[self.index // 10]
            self.index += 1
            self.rect.x -= 1
            self.y -= 0.5
            self.rect.y = self.y
        else:
            self.kill()