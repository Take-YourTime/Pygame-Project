import pygame
from datetime import datetime

from function import circle_location

class Number(pygame.sprite.Sprite):
    def __init__(self, x, y, index, text, text_size, text_color, time):
        super().__init__()
        # object attributes
        self.x = x
        self.y = y
        self.original_x = x
        self.original_y = y
        self.index = index
        self.r = (index+1) * 60 # 自身所處圓半徑
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, text_size)
        self.time = time-1

        # set up
        self.text_surface = self.font.render(self.text, True, self.text_color, None) # 內容 / 抗鋸齒? / 字體顏色 / 背景顏色 or 透明
        self.rect = self.text_surface.get_rect()
        self.rect.center = (self.x, self.y)

    def draw(self, surface):
        surface.blit(self.text_surface, self.rect)

    # set new text
    def set_text(self, text):
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.text_color, None)
        self.rect = self.text_surface.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self, mode, time, group):
        match mode:
            case "second":
                if(self.time == time.second):  # 若時間相同，則不更新
                    return
                
                self.time = time.second
                degree = time.second * 6
                for second in group:
                    second.x, second.y = circle_location(second.r, degree)
                    second.x += second.original_x
                    second.y += second.original_y
                    second.set_text(str(time.second))
            case "minute":
                if(self.time == time.minute):  # 若時間相同，則不更新
                    return
                
                self.time = time.minute
                degree = time.minute * 6
                for minute in group:
                    minute.x, minute.y = circle_location(minute.r, degree)
                    minute.x += minute.original_x
                    minute.y += minute.original_y
                    minute.set_text(str(time.minute))
            case "hour":
                if(self.time == time.minute):  # 若時間相同，則不更新
                    return
                self.time = time.minute
                degree = time.hour * 15 + time.minute * 0.25
                for hour in group:
                    hour.x, hour.y = circle_location(hour.r, degree)
                    hour.x += hour.original_x
                    hour.y += hour.original_y
                    hour.set_text(str(time.hour))
            case _:
                print("Wrong mode with time!")
                pygame.quit()


    def move(self, move_x, move_y):
        self.x += move_x
        self.y += move_y
        self.rect.center = (self.x, self.y)