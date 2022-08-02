import threading
import pygame
import random
import resources


screen = "START"
RES_DIR = "Assets"
canvas = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
downscale = (canvas.get_width() / 1920, canvas.get_height() / 1080)
running_anims = {}
animid = 0
font_sizes = resources.AssetStorage(
    s=("Assets/INSERTFONTFILE", True),
    p=("Calibri", False),
    titlefont="s72",
    hdrfont="s60",
    pkfont="s33",
    subfont="s38",
    movefont="s28",
    smallfont="s24",
    # splainfont=plain_font.f15,
    plainfont="p30",
    descfont="p40",
    choicefont="p60",
    dialogfont="p90",
)

def scaled_font_set(downscale_by=True):
    if downscale_by == True:
        downscale_by = downscale
    assets = resources.AssetStorage(**{
        attr: (pygame.font.Font if font_sizes.__dict__[font_sizes.__dict__[attr][0]][1] else pygame.font.SysFont)(font_sizes.__dict__[font_sizes.__dict__[attr][0]][0], round(int(font_sizes.__dict__[attr][1:]) * downscale_by[0])) for attr in font_sizes.attrs() if "font" in attr
    })
    return assets

fs = scaled_font_set(downscale)

def blit_running_anims():
    for a in set(running_anims.keys()):
        if a not in running_anims:
            continue
        if running_anims[a] == "done":#type(running_anims[a]) == str:
            running_anims.pop(a)
        else:
            try:
                canvas.blit(running_anims[a][0], running_anims[a][1])
            except TypeError:
                print("Couldn't blit {}".format(running_anims[a]))
            except AttributeError:
                print("Anim deleted mid blit {}".format(a))

def update():
    # canvas.fill((0, 0, 0, 255))
    import screens
    if screen in dir(screens) and hasattr(screens.__dict__[screen], "update"):
        screens.__dict__[screen].update()
    # blit_running_anims()
    pygame.display.update()
