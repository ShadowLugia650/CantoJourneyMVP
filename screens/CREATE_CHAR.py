import pygame
import render
import player

drag_dist = [0, 0]
dragging = False

def drag(event):
    global dragging
    dragging = True

def motion(event):
    global drag_dist
    if dragging:
        drag_dist[0] += event.rel[0]
        drag_dist[1] += event.rel[1]

def drop(event):
    global dragging
    dragging = False

def update():
    pass