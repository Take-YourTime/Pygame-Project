import pygame
from datetime import datetime

from Number import Number

# Glabal Constants
WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 800

FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
LIGHT_PURPLE = (230, 120, 230)


# initialization
pygame.init()
pygame.font.init()

# 主視窗
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)   # size / 屬性(可改變大小)
pygame.display.set_caption("Digital and Analog clock")  # set title

# clock
main_clock = pygame.time.Clock()

current_time = datetime.now() # current time

# background
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

# objects
second = Number(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, 0, str(current_time.second), 60, WHITE, current_time.second)
seconds = pygame.sprite.Group()
seconds.add(second)
for i in range(1, 7):
    seconds.add(Number(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, i, str(current_time.second), 60, WHITE, current_time.second))

minute = Number(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, 0, str(current_time.minute), 70, LIGHT_BLUE, current_time.minute)
minutes = pygame.sprite.Group()
minutes.add(minute)
for i in range(1, 5):
    minutes.add(Number(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, i, str(current_time.minute), 70, LIGHT_BLUE, current_time.minute))

hour = Number(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, 0, str(current_time.hour), 80, LIGHT_PURPLE, current_time.minute)
hours = pygame.sprite.Group()
hours.add(hour)
for i in range(1, 3):
    hours.add(Number(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, i, str(current_time.hour), 80, LIGHT_PURPLE, current_time.minute))

# main loop
running = True
while running:
    # event detect
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
    
    # update
    current_time = datetime.now()
    second.update("second", current_time, seconds)
    minute.update("minute", current_time, minutes)
    hour.update("hour", current_time, hours)

    #  draw
    window_surface.fill(BLACK)
    window_surface.blit(background, (0, 0))
    for number in seconds:
        number.draw(window_surface)
    for number in minutes:
        number.draw(window_surface)
    for number in hours:
        number.draw(window_surface)

    # update
    pygame.display.update()
    main_clock.tick(FPS)

