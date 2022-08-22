import pygame
import render

test = pygame.image.load("Assets/svg/svg_FlightAttendant-Chat_v1.svg")
testx2 = pygame.transform.scale(test, (round(test.get_width() * 2), round(test.get_height() * 2)))
testxpt5 = pygame.transform.scale(test, (round(test.get_width() / 2), round(test.get_height() / 2)))
testxpt5x4 = pygame.transform.scale(testxpt5, (round(test.get_width() * 2), round(test.get_height() * 2)))

def update():
    render.canvas.blit(test, (0, 0))
    render.canvas.blit(testxpt5, (0, 100))
    render.canvas.blit(testx2, (100, 0))
    render.canvas.blit(testxpt5x4, (100, 200))