from calendar import c
import pygame
import render
import player
import resources

drag_dist = [0, 0]
dragging = False
scroll_offs = {
    "hair": 0,
    "body": 0,
    "face": 0,
    "shirt": 0,
    "pants": 0,
    "shoes": 0,
    "colour": 0,
}

crop_offs = {
    "hair": (0, 0),
    "body": (0, 0),
    "face": (0, 0),
    "shirt": (0, 0),
    "pants": (0, 0),
    "shoes": (0, 0),
}

EMPTY_92x92 = pygame.Surface((92 * min(render.downscale), 92 * min(render.downscale)), pygame.SRCALPHA)
CUSTOMS_OFFS = (0, 0)
CUSTOMS_SPACING = (43 * render.downscale[0], 43 * render.downscale[1])#(43 * min(render.downscale), 43 * min(render.downscale))
EMPTY_46x46 = pygame.Surface((46 * min(render.downscale), 46 * min(render.downscale)), pygame.SRCALPHA)
COLOUR_OFFS = (0, 0)
COLOUR_SPACING = (15, 15)
COMING_SOON = resources.render_text_with_icons("Coming\nsoon!", render.fs.paragraph, (0, 0, 0, 255), align="center")
# TEMP
customs_buttons = [
    resources.Button(
        (CUSTOMS_OFFS[0] + (CUSTOMS_SPACING[0] + EMPTY_92x92.get_width()) * (i % 2), CUSTOMS_OFFS[1] + (CUSTOMS_SPACING[1] + EMPTY_92x92.get_height()) * (i // 2)), 
        EMPTY_92x92
    ) for i in range(4)
]
colour_buttons = [
    resources.Button(
        (COLOUR_OFFS[0] + (COLOUR_SPACING[0] + EMPTY_46x46.get_width()) * (i % 2), COLOUR_OFFS[1] + (COLOUR_SPACING[1] + EMPTY_46x46.get_height()) * (i // 2)), 
        # render.assets.img.PC
        EMPTY_46x46
    ) for i in range(20)
]
tab_buttons = {
    # k: resources.Button() for i, k in enumerate([player.customs.attrs(key=lambda a: "colour" not in a)])
}
# tab_buttons["colour"] = resources.Button()
cur_tab = "hair"
choosing_colour = False

def drag(event):
    global dragging, drag_dist
    dragging = True
    drag_dist = [0, 0]

def motion(event):
    global drag_dist
    if dragging:
        drag_dist[0] += event.rel[0]
        drag_dist[1] += event.rel[1]

def drop(event):
    global dragging, scroll_offs, cur_tab, choosing_colour
    dragging = False
    if abs(drag_dist[0]) < 50 and abs(drag_dist[1]) < 50: # is tap
        if not choosing_colour:
            for i, btn in enumerate(customs_buttons):
                if btn.collide_point(event.pos):
                    idx = i + 2 * scroll_offs[cur_tab]
                    # startswith is before the 'c'
                    if any([a.startswith(str(idx)) for a in render.assets.img.PChara.get(cur_tab.title()).attrs()]):
                        # Only if idx exists in the cur_tab assets
                        player.customs.insert(cur_tab, idx)
                    if not any([a.endswith(str(player.customs.get(cur_tab + "_colour"))) for a in render.assets.img.PChara.get(cur_tab.title()).attrs()]):
                        # If the colour does not exist in the current style, revert colour to 0
                        player.customs.insert(cur_tab + "_colour", 0)
        else:
            for i, btn in enumerate(colour_buttons):
                if btn.collide_point(event.pos):
                    idx = i + 5 * scroll_offs["colour"]
                    # endswith is after the 'c'
                    if any([a.endswith(str(idx)) for a in render.assets.img.PChara.get(cur_tab.title()).attrs()]):
                        # only if colour exists for current style
                        player.customs.insert(cur_tab + "_colour", idx)
        for tab, btn in tab_buttons:
            if btn.collide_point(event.pos):
                if tab == "colour":
                    if cur_tab != "body":
                        # No colours for body, those are designated by body number
                        choosing_colour = not choosing_colour
                        scroll_offs["colour"] = 0
                else:
                    cur_tab = tab
    else: # is swipe
        if drag_dist[1] > 50:
            if choosing_colour:
                pass
            elif scroll_offs[cur_tab] < len(render.assets.img.PChara.get(cur_tab.title()).attrs()) / 2 - 2:
                scroll_offs[cur_tab] += 1
        elif drag_dist[1] < -50:
            if choosing_colour:
                pass
            elif scroll_offs[cur_tab] > 1:
                scroll_offs[cur_tab] -= 1

def update():
    # blit tab backdrop box
    for btn in tab_buttons:
        # tabs
        btn.blit_on(render.canvas)
    if choosing_colour:
        for i, btn in enumerate(colour_buttons):
            render.canvas.blit(render.assets.img.PChara.Color.get(str(i + 5 * scroll_offs["colour"])), btn.pos)
            if not any([a.endswith(str(idx)) for a in render.assets.img.PChara.get(cur_tab.title()).attrs()]):
                btn.blit_on(render.canvas, with_centered=COMING_SOON)
    else:
        for i, btn in enumerate(customs_buttons):
            idx = i + 2 * scroll_offs[cur_tab]
            if any([a.startswith(str(idx)) for a in render.assets.img.PChara.get(cur_tab.title()).attrs()]):
                render.canvas.blit(render.assets.img.PChara.get(cur_tab.title()).get(str(idx) + ("c0" if cur_tab != "body" else "")), btn.pos)
    # current player sprite
    render.canvas.blit(player.sprite, (render.canvas.get_width() * 0.25, render.canvas.get_height() * 0.5 - player.sprite.get_height() / 2))
    # player nameplate