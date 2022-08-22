import pygame
import time
import threading
from datetime import datetime
import render
import resources


# DEV GLOBALS
is_mobile = True
try:
    import android
except ImportError:
    is_mobile = False
load_prevscrn = None
loading_thds = 0

# OPTION GLOBALS


def _thd_loading_screen_while(function, args, reset=True, join_thd=None):
    global load_prevscrn, loading_thds
    if join_thd:
        join_thd.join()
    from screens import LOADING
    if load_prevscrn is None:
        load_prevscrn = render.screen
        render.screen = "LOADING"
    if reset:
        LOADING.reset()
    function(*args)
    loading_thds -= 1
    if loading_thds == 0:
        render.screen = load_prevscrn
        load_prevscrn = None

def loading_screen_while(function, args, reset=True, join_thd=None):
    global loading_thds
    thd = threading.Thread(target=_thd_loading_screen_while, args=(function, args, reset, join_thd), daemon=True)
    thd.start()
    loading_thds += 1
    return thd

def default_log(msg):
    """ 
    Prints a message to the console with the current time

    Params:
        msg: The message to print (anything that can be formatted as a str)
    """
    print("{}: {}".format(datetime.now().strftime("%H:%M:%S.%f"), msg))

def handle_event(event):
    """ 
    Handles the specified event, passing it off to the current screen 
        script based on the event type

    Params:
        event: A pygame event
    """
    global running
    import screens
    import player
    if event.type == pygame.QUIT:
        player.save()
        running = False
        pygame.quit()
        quit()
    elif event.type == pygame.KEYUP:
        if render.screen in screens.__dict__:
            if hasattr(screens.__dict__[render.screen], "key"):
                screens.__dict__[render.screen].key(event)
    elif event.type == pygame.MOUSEMOTION:
        if render.screen in screens.__dict__:
            if hasattr(screens.__dict__[render.screen], "hover"):
                screens.__dict__[render.screen].hover(event)
            elif hasattr(screens.__dict__[render.screen], "motion"):
                screens.__dict__[render.screen].motion(event)
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if render.screen in screens.__dict__:
            if event.button in [4, 5]:
                if hasattr(screens.__dict__[render.screen], "scroll"):
                    screens.__dict__[render.screen].scroll(event)
            else:
                if hasattr(screens.__dict__[render.screen], "drag"):
                    screens.__dict__[render.screen].drag(event)
    elif event.type == pygame.MOUSEBUTTONUP:
        if render.screen in screens.__dict__:
            if event.button in [4, 5]:
                pass
            else:
                if hasattr(screens.__dict__[render.screen], "drop"):
                    screens.__dict__[render.screen].drop(event)
                elif hasattr(screens.__dict__[render.screen], "click"):
                    screens.__dict__[render.screen].click(event)
    elif event.type == pygame.TEXTINPUT:
        if render.screen in screens.__dict__:
            if hasattr(screens.__dict__[render.screen], "text_input"):
                screens.__dict__[render.screen].text_input(event)
