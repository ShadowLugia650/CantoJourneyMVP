from os import path
import pygame
import render
import resources
import threading

load_lock = threading.Lock()
load_complete = 0
load_total = 0
load_complete_old = 0
load_complete_new = 0
which_bar = 0

FOX_SCALE = 88/409 * min(render.downscale)
FOX = pygame.image.load(path.join(render.RES_DIR, "img", "img_Fox_v1.png"))
FOX = pygame.transform.scale(FOX, (round(FOX.get_width() * FOX_SCALE), round(FOX.get_height() * FOX_SCALE)))
# TODO: Fix scaling
BAR_BG_COLOR = (255, 255, 255, 255)
BAR_COLOR = (0, 0, 0, 255)
BAR_SIZE = (render.canvas.get_width() * 0.6, render.canvas.get_height() * 0.05)
BAR_BG = pygame.Surface(BAR_SIZE, pygame.SRCALPHA)
BAR_BG.fill(BAR_BG_COLOR)
loading_bar = pygame.Surface((0, BAR_SIZE[1]), pygame.SRCALPHA)

def reset():
    global load_total, load_complete, loading_bar
    load_lock.acquire()
    load_total = 0
    load_complete = 0
    loading_bar = pygame.Surface((0, BAR_SIZE[1]), pygame.SRCALPHA)
    load_lock.release()

def inc_load_complete(inc=1):
    global load_complete
    load_lock.acquire()
    load_complete += inc
    load_lock.release()

def inc_load_total(inc=1):
    global load_total
    load_lock.acquire()
    load_total += inc
    load_lock.release()

def update_load_bar():
    global loading_bar, load_complete_old, load_complete_new
    # TASK 1
    # TODO: make it so that the loading bar only updates if the percentage
    # increased
    # Hint: consider saving the current percentage in a variable so that when
    # this function is called, we can check the percentage against the old 
    # stored one
    # Aaron's notes:
    # float x = current percentage (load_complete / load_total), float y = old percentage (what x was before). y = 0. if x >= y, y = x. if x > 100, break (kinda unneeded).

    load_complete_new = (load_complete / load_total)

    if load_complete_old < load_complete_new:
        load_lock.acquire()
        loading_bar = pygame.Surface(
            (int(round(BAR_SIZE[0] * load_complete / (load_total if load_total > 0 else 1))), BAR_SIZE[1]),
            pygame.SRCALPHA)
        loading_bar.fill(BAR_COLOR)
        load_lock.release()

    load_complete_old = (load_complete/load_total)

    # TASK 2
    if which_bar == 1:
        render.canvas.fill((187, 226, 255, 255))

def update():
    render.canvas.blit(BAR_BG, (render.canvas.get_width() / 2 - BAR_BG.get_width() / 2, render.canvas.get_height() / 2 - BAR_BG.get_height() / 2))
    render.canvas.blit(loading_bar, (render.canvas.get_width() / 2 - BAR_BG.get_width() / 2, render.canvas.get_height() / 2 - BAR_BG.get_height() / 2))
    render.canvas.blit(FOX, (render.canvas.get_width() / 2 - BAR_BG.get_width() / 2 + loading_bar.get_width() - FOX.get_width() / 2, render.canvas.get_height() / 2 - FOX.get_height() / 2))

    if which_bar == 1:
        render.canvas.fill((187, 226, 255, 255))
        
    #else:
