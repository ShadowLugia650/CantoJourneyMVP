# from sys import argv
import threading
import pygame
import render
import ui

pygame.init()


def run():
    while True:
        for event in pygame.event.get():
            ui.handle_event(event)
        render.update()

def devconsole():
    while True:
        inp = input(">")
        if inp.startswith("pyexec "):
            try:
                exec(inp[7:])
            except Exception as e:
                print(e)

if __name__ == "__main__":
    # pygame.display.set_icon(pygame.image.load(""))
    pygame.display.set_caption("")
    # maybe parse CLAs

    # Maybe Load Save Data
    # Join render loading threads
    if not ui.is_mobile:
        threading.Thread(target=devconsole, daemon=True).start()
    run()
