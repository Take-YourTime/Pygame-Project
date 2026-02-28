#from typing import Any
import pygame
import function

pygame.mixer.init()

class MonkeyKing(pygame.sprite.Sprite):
    # class共享資源
    raw_image = pygame.image.load(("monkeyKing\\monkeyKing.png")).convert_alpha()
    skill_sound = pygame.mixer.Sound("monkeyKing\\light_saber.wav")
    skill_sound.set_volume(0.9)
    throw_sound = pygame.mixer.Sound("monkeyKing\\throw.wav")
    throw_sound.set_volume(0.6)
    
    def __init__(self, location_x, location_y) -> None:
        super().__init__()
        self.image = MonkeyKing.raw_image
        # images index
        self.index = 0
        self.ATKimages = [pygame.image.load(("monkeyKing\\monkey_boss_attack0.png")).convert_alpha(),
                          pygame.image.load(("monkeyKing\\monkey_boss_attack1.png")).convert_alpha(), 
                          pygame.image.load(("monkeyKing\\monkey_boss_attack2.png")).convert_alpha(),
                          pygame.image.load(("monkeyKing\\monkey_boss_attack3.png")).convert_alpha(),
                          pygame.image.load(("monkeyKing\\monkey_boss_attack4.png")).convert_alpha(),
                          pygame.image.load(("monkeyKing\\monkey_boss_attack5.png")).convert_alpha(),
                          pygame.image.load(("monkeyKing\\monkey_boss_attack6.png")).convert_alpha(),
                          pygame.image.load(("monkeyKing\\monkey_boss_attack7.png")).convert_alpha(),
                          pygame.image.load(("monkeyKing\\monkey_boss_attack8.png")).convert_alpha(),
                          pygame.image.load(("monkeyKing\\monkey_boss_attack9.png")).convert_alpha()]
        self.isATK = False
        # skill energy
        self.energy = 300
        self.walkingImages = [  pygame.image.load(("monkeyKing\\walking1.png")).convert_alpha(),
                                pygame.image.load(("monkeyKing\\walking2.png")).convert_alpha(),
                                pygame.image.load(("monkeyKing\\walking3.png")).convert_alpha(),
                                pygame.image.load(("monkeyKing\\walking4.png")).convert_alpha(),
                                pygame.image.load(("monkeyKing\\walking5.png")).convert_alpha(),
                                pygame.image.load(("monkeyKing\\walking6.png")).convert_alpha() ]
        self.keepWalking = True
        self.rect = self.image.get_rect()
        self.rect.topleft = (location_x, location_y)
        self.mask = pygame.mask.from_surface(MonkeyKing.raw_image)
        self.width = MonkeyKing.raw_image.get_width()
        self.height = MonkeyKing.raw_image.get_height()
        self.life = 50
    
    def update(self, banana_group) -> None:

        THROW_BANANA_FRAME = 80
        FINAL_FRAME = 100
        if self.keepWalking:
            self.walking()
        elif self.isATK:
            if self.index == 0:
                MonkeyKing.skill_sound.play()
                self.index += 1
            elif self.index < THROW_BANANA_FRAME :
                self.image = self.ATKimages[self.index // 10]
                self.index += 1
            elif self.index == THROW_BANANA_FRAME: 
                MonkeyKing.throw_sound.play()
                banana_group.add( Banana( (self.rect.center[0], (self.rect.top + self.height // 2)) ) )
                banana_group.add( Banana( (self.rect.center[0], (self.rect.top + self.height // 2 + 20)) ) )
                banana_group.add( Banana( (self.rect.center[0], (self.rect.top + self.height // 2 - 20)) ) )
                self.image = self.ATKimages[8]
                self.index += 1
            elif self.index < FINAL_FRAME:
                self.image = self.ATKimages[9]
                self.index += 1
            else:
                self.image = MonkeyKing.raw_image
                self.isATK = False
                self.index = 0
        elif self.energy >= 500:
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

    def walking(self):
        if self.rect.left > 700:
            self.rect.left -= 1
            self.index += 1

            if self.index == 107:
                self.index = 0
            else:
                self.image = self.walkingImages[self.index // 18]
        else:
            self.index = 0
            self.keepWalking = False
            self.image = MonkeyKing.raw_image
    


class Banana(pygame.sprite.Sprite):
    raw_image = pygame.image.load(("banana\\banana0.png")).convert_alpha()
    mask = pygame.mask.from_surface(raw_image)
    roalingImages = [   pygame.image.load(("banana\\banana0.png")).convert_alpha(),
                        pygame.image.load(("banana\\banana1.png")).convert_alpha(),
                        pygame.image.load(("banana\\banana2.png")).convert_alpha(),
                        pygame.image.load(("banana\\banana3.png")).convert_alpha(),
                        pygame.image.load(("banana\\banana4.png")).convert_alpha(),
                        pygame.image.load(("banana\\banana5.png")).convert_alpha(),
                        pygame.image.load(("banana\\banana6.png")).convert_alpha(),
                        pygame.image.load(("banana\\banana7.png")).convert_alpha()]

    def __init__(self, location):
        super().__init__()    
        self.image = Banana.raw_image
        self.images_index = 0
        self.width = Banana.raw_image.get_width()
        self.rect = self.image.get_rect()
        self.rect.topleft = location
    
    def update(self, player, bananaHit_group):
        if self.rect.x < -self.width:
            self.kill()
            return
        elif player.rect.colliderect(self.rect):
            if player.mask.overlap(Banana.mask, (self.rect.left - player.rect.left, self.rect.top - player.rect.top)):
                self.kill()
                player.hurt(5)
                bananaHit_group.add( BananaHit(self.rect.topleft) )
                return
        
        # banana speed
        self.rect.x -= 5

        # FINAL FRAME is 36
        if self.images_index == 40:
            self.image = Banana.raw_image
            self.images_index = 0
        else:
            self.image = Banana.roalingImages[self.images_index // 5]
            self.images_index += 1
        

class BananaHit(pygame.sprite.Sprite):
    hitImages = [   pygame.image.load(("banana\\hit0.png")).convert_alpha(),
                    pygame.image.load(("banana\\hit1.png")).convert_alpha(),
                    pygame.image.load(("banana\\hit2.png")).convert_alpha()]
    
    def __init__(self, location):
        super().__init__()
        self.image = BananaHit.hitImages[0]
        self.imageIndex = 0
        self.rect = BananaHit.hitImages[0].get_rect()
        self.rect.topleft = location
    
    def update(self):
        FINAL_FRAME = 30

        if self.imageIndex < FINAL_FRAME:
            self.image = BananaHit.hitImages[self.imageIndex // 10]
            self.imageIndex += 1
        else:
            self.kill()