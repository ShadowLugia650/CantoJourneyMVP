import pygame
import render
import ui
import player
import resources

drag_dist = [0, 0]
dragging = False
PARTS = ["Hair", "Face", "Shirt", "Pants", "Shoes"]

scroll_offs = {
    "hair": 0,
    "skin": 0,
    "face": 0,
    "shirt": 0,
    "pants": 0,
    "shoes": 0,
    "colour": 0,
}

crop_offs = {
    "hair": render.min_scaled_size((-21, 0)),
    # "skin": (0, 0),
    "face": render.min_scaled_size((-65, -54)),
    "shirt": render.min_scaled_size((-65, -114)),
    "pants": render.min_scaled_size((-65, -158)),
    "shoes": render.min_scaled_size((-65, -176)),
}

EMPTY_92x92 = pygame.Surface((92 * min(render.downscale), 92 * min(render.downscale)), pygame.SRCALPHA)
CUSTOMS_OFFS = render.downscaled_size((344, 126))
CUSTOMS_SPACING = render.min_scaled_size((43, 43)) # (43 * render.downscale[0], 43 * render.downscale[1])#(43 * min(render.downscale), 43 * min(render.downscale))
EMPTY_46x46 = pygame.Surface((46 * min(render.downscale), 46 * min(render.downscale)), pygame.SRCALPHA)
COLOUR_OFFS = render.downscaled_size((323, 116))
COLOUR_SPACING = render.min_scaled_size((15, 15)) # (15, 15)
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
        (COLOUR_OFFS[0] + (COLOUR_SPACING[0] + EMPTY_46x46.get_width()) * (i % 5), COLOUR_OFFS[1] + (COLOUR_SPACING[1] + EMPTY_46x46.get_height()) * (i // 5)), 
        # render.assets.img.PC
        EMPTY_46x46
    ) for i in range(20)
]
tab_buttons = {
    # k: resources.Button() for i, k in enumerate(player.customs.attrs(key=lambda a: "colour" not in a))
    # k.lower(): resources.Button() for i, k in enumerate(PARTS)
}
# tab_buttons["skin"] = resources.Button()
# tab_buttons["colour"] = resources.Button()
cur_tab = "skin"
choosing_colour = False

def init_cropped_styles():
    from screens import LOADING
    for part in ["Face", "Shirt", "Pants", "Shoes"]:
        styles = render.assets.img.PChara.get(part).attrs(key=lambda a: a.endswith("0"))
        LOADING.inc_load_total(len(styles))
        for style in styles:
            if render.assets.img.PChara.get(part).get(style).get("xpt2"):
                crop = pygame.Surface(EMPTY_92x92.get_size(), pygame.SRCALPHA)
                crop.blit(render.assets.img.PChara.get(part).get(style).xpt2, crop_offs[part.lower()])
                render.assets.img.PChara.get(part).get(style).insert("cropped", crop)
            LOADING.inc_load_complete()
            LOADING.update_load_bar()
    hairscale = 92/152
    styles = render.assets.img.PChara.Hair.attrs(key=lambda a: a.endswith("0"))
    LOADING.inc_load_total(len(styles))
    for hstyle in styles:
        if render.assets.img.PChara.Hair.get(hstyle).get("xpt2"):
            crop = pygame.Surface(EMPTY_92x92.get_size(), pygame.SRCALPHA)
            hair = render.assets.img.PChara.Hair.get(hstyle).xpt2
            smhair = pygame.transform.scale(hair, (round(hair.get_width() * hairscale), round(hair.get_height() * hairscale)))
            crop.blit(smhair, crop_offs["hair"])
            render.assets.img.PChara.Hair.get(hstyle).insert("cropped", crop)
        LOADING.inc_load_complete()
        LOADING.update_load_bar()
    # print("cropped complete")

ui.loading_screen_while(init_cropped_styles, (), False, render.img_load_thd)

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
                        if not any([a.endswith(str(player.customs.get(cur_tab)) + "c" + str(player.customs.get(cur_tab + "_colour"))) for a in render.assets.img.PChara.get(cur_tab.title()).attrs()]):
                            # If the colour does not exist in the current style, revert colour to 0
                            player.customs.insert(cur_tab + "_colour", 0)
                        player.generate_sprite()
        else:
            for i, btn in enumerate(colour_buttons):
                if btn.collide_point(event.pos):
                    idx = i + 5 * scroll_offs["colour"]
                    # endswith is after the 'c'
                    if any([a.endswith(str(player.customs.get(cur_tab)) + "c" + str(idx)) for a in render.assets.img.PChara.get(cur_tab.title()).attrs()]):
                        # only if colour exists for current style
                        player.customs.insert(cur_tab + "_colour", idx)
                        player.generate_sprite()
        for tab, btn in tab_buttons:
            if btn.collide_point(event.pos):
                if tab == "colour":
                    if cur_tab != "skin":
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
            idx = i + 5 * scroll_offs["colour"]
            render.canvas.blit(render.assets.img.PChara.Color.get(str(idx)), btn.pos)
            if not any([a.endswith(str(player.customs.get(cur_tab)) + "c" + str(idx)) for a in render.assets.img.PChara.get(cur_tab.title()).attrs()]):
                btn.blit_on(render.canvas, with_centered=COMING_SOON)
    else:
        for i, btn in enumerate(customs_buttons):
            idx = i + 2 * scroll_offs[cur_tab]
            if any([a.startswith(str(idx)) for a in render.assets.img.PChara.get(cur_tab.title()).attrs()]):
                if cur_tab == "skin": 
                    render.canvas.blit(render.assets.img.PChara.Skin.get(str(idx)), btn.pos)
                else:
                    render.canvas.blit(render.assets.img.PChara.get(cur_tab.title()).get(str(idx) + "c0").cropped, btn.pos)
    # current player sprite
    render.canvas.blit(player.sprite, (render.canvas.get_width() * 0.1, render.canvas.get_height() * 0.5 - player.sprite.get_height() / 2))
    # player nameplate