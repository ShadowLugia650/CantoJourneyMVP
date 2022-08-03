from os import path, listdir
import threading
import pygame
import random
import resources
import ui


screen = "START"
RES_DIR = "Assets"
# TODO: scale up to PC later
canvas = pygame.display.set_mode((736, 414), pygame.FULLSCREEN if ui.is_mobile else 0)
BGCOLOR = (27, 33, 44, 255)
downscale = (canvas.get_width() / 736, canvas.get_height() / 414)
running_anims = {}
animid = 0
font_sizes = resources.AssetStorage(
    # s=("Assets/INSERTFONTFILE", True),
    p=("Calibri", False),
    # titlefont="s72",
    # hdrfont="s60",
    # pkfont="s33",
    # subfont="s38",
    # movefont="s28",
    # smallfont="s24",
    # splainfont=plain_font.f15,
    plainfont="p30",
    descfont="p40",
    choicefont="p60",
    dialogfont="p90",
)

assets = resources.AssetStorage(
    icons=resources.AssetStorage(),
    img=resources.AssetStorage(),
)

def load_assets(subdir):
    from screens import LOADING
    LOADING.inc_load_total(len(listdir(path.join(RES_DIR, subdir))))
    print(LOADING.load_total)
    for f in listdir(path.join(RES_DIR, subdir)):
        # TODO: make it so we can also load SVG, in addition to PNG
        # Hint: consider checking the following
        # 1. Is the item a file?
        # 2. If so, is the extension PNG or SVG?
        if f.endswith(".png"):
            if "_" in f:
                # loads the file into assets
                type_, name, version = f[:-4].split("_")
                assets.insert(subdir+"."+name.replace("-", "."), pygame.image.load(path.join(RES_DIR, subdir, f)))
        if path.isdir(path.join(RES_DIR, subdir, f)):
            if "_" in f:
                # loads the latest version of the file into assets
                type_, name = f.split("_")
                version = len(listdir(path.join(RES_DIR, subdir, f)))
                assets.insert(subdir+"."+name.replace("-", "."), pygame.image.load(path.join(RES_DIR, subdir, f, f + "_v" + str(version) + ".png")))
        LOADING.inc_load_complete(1)
        LOADING.update_load_bar()

# Load assets in thread form while showing the loading screen
ui.loading_screen_while(load_assets, ("icons",))
ui.loading_screen_while(load_assets, ("img",), reset=False)

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
    canvas.fill(BGCOLOR)
    if screen in dir(screens) and hasattr(screens.__dict__[screen], "update"):
        screens.__dict__[screen].update()
    # blit_running_anims()
    pygame.display.update()