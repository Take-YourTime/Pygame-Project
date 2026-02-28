import pygame
import random
from function import get_normalize_vector, WINDOW_WIDTH, WINDOW_HEIGHT

pygame.mixer.init()

class Magician(pygame.sprite.Sprite):
    raw_image = pygame.image.load(("magicion.png")).convert_alpha()
    
    def __init__(self, width, height) -> None:
        super().__init__()
        self.image = pygame.transform.scale(Magician.raw_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (WINDOW_WIDTH + 10, random.randint(0, 150))
        self.mask = pygame.mask.from_surface(self.image)
        self.width = width
        self.height = height
        self.life = 10
        self.skill_energy = 0
        self.skill_consume = random.randint(200, 400)
        self.move_times = random.randint(150, 500)
    
    def move(self, magician_move_group):
        if self.move_times > 0:
            self.rect.topleft = (self.rect.topleft[0] - 1, self.rect.topleft[1])
            self.move_times -= 1
        else:
            magician_move_group.remove(self)

    def update(self):
        if self.life == 1:
            self.kill()
        else:
            self.life -= 1

    def attack(self, stone_group):  
        if(self.skill_energy >= self.skill_consume):
            self.skill_energy = 0
            stone_group.add( Stone(29, 26, (self.rect.topleft[0] + 10, self.rect.topleft[1] + 30), (random.randint(20, 100), random.randint(WINDOW_HEIGHT - 230, WINDOW_HEIGHT -80))) )
        else:
            self.skill_energy += 1



class Stone(pygame.sprite.Sprite):
    raw_image = pygame.image.load(("stone.png")).convert_alpha()

    def __init__(self, width, height, location, destination):
        super().__init__()
        self.image = pygame.transform.scale(Stone.raw_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = location
        self.mask = pygame.mask.from_surface(self.image)
        self.width = width
        self.height = height
        self.location = location
        self.vector_x, self.vector_y = get_normalize_vector(location[0], location[1], destination[0], destination[1])
        # stone speed
        self.multiple = 12

    
    def update(self, player):
        # stone move
        self.location = (self.location[0] + self.vector_x * self.multiple, self.location[1] + self.vector_y * self.multiple)
        self.rect.topleft = self.location

        if(self.location[0] > WINDOW_WIDTH + self.width or self.location[0] < -(self.width) or self.location[1] > WINDOW_HEIGHT + self.height or self.location[1] < -(self.height)):
            self.kill()
        elif player.rect.colliderect(self.rect):
            # The two picture mask overlap
            if player.mask.overlap(self.mask, (self.rect.left - player.rect.left, self.rect.top - player.rect.top)):
                self.kill()
                player.hurt(1)
