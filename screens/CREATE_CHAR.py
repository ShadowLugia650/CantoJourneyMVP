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
EMPTY_29x56 = pygame.Surface(render.min_scaled_size((29, 56)), pygame.SRCALPHA)
EMPTY_56x29 = pygame.Surface(render.min_scaled_size((56, 29)), pygame.SRCALPHA)
TAB_DATA = resources.AssetStorage(
    BACK=EMPTY_56x29.copy(),
    SEL_BACK=EMPTY_56x29.copy(),
    SIDE_BACK=EMPTY_29x56.copy(),
    SEL_SIDE_BACK=EMPTY_29x56.copy(),
    TAB_COLOUR = (159, 159, 159, 255),
    TAB_SEL_COLOUR = (217, 217, 217, 255),   
    BG_COLOUR = (217, 217, 217, 255),   
    TAB_TEXT_COLOUR = (0, 0, 0, 255)
)
pygame.draw.rect(TAB_DATA.BACK, TAB_DATA.TAB_COLOUR, pygame.Rect((0, 0), EMPTY_56x29.get_size()), border_top_left_radius=2, border_top_right_radius=2)
pygame.draw.rect(TAB_DATA.SEL_BACK, TAB_DATA.TAB_SEL_COLOUR, pygame.Rect((0, 0), EMPTY_56x29.get_size()), border_top_left_radius=2, border_top_right_radius=2)
pygame.draw.rect(TAB_DATA.SIDE_BACK, TAB_DATA.TAB_COLOUR, pygame.Rect((0, 0), EMPTY_29x56.get_size()), border_top_right_radius=2, border_bottom_right_radius=2)
pygame.draw.rect(TAB_DATA.SEL_SIDE_BACK, TAB_DATA.TAB_SEL_COLOUR, pygame.Rect((0, 0), EMPTY_29x56.get_size()), border_top_right_radius=2, border_bottom_right_radius=2)
tab_buttons = {
    # k: resources.Button() for i, k in enumerate(player.customs.attrs(key=lambda a: "colour" not in a))
    k.lower(): resources.Button(
        (
            289 * render.downscale[0] + i * EMPTY_56x29.get_width(), 
            72 * render.downscale[1]
        ),
        EMPTY_56x29
    ) for i, k in enumerate(["skin"] + PARTS)
}
# tab_buttons["skin"] = resources.Button(render.downscaled_size((289, 72)), EMPTY_56x29)
tab_buttons["colour"] = resources.Button(render.downscaled_size((627, 101)), EMPTY_29x56)
TAB_TEXT = {
    tab: resources.render_text_with_icons(tab.title(), render.fs.paragraph, TAB_DATA.TAB_TEXT_COLOUR) for tab in tab_buttons
}
TAB_TEXT["colour"] = pygame.transform.rotate(TAB_TEXT["colour"], 270)
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
    player.generate_sprite()

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
        for tab, btn in tab_buttons.items():
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
    pygame.draw.rect(render.canvas, TAB_DATA.BG_COLOUR, pygame.Rect(render.downscaled_size((289, 101)), render.min_scaled_size((338, 254))), border_bottom_left_radius=2, border_bottom_right_radius=2)
    for tab, btn in tab_buttons.items():
        # tabs
        if tab != "colour":
            render.canvas.blit(TAB_DATA.SEL_BACK if cur_tab == tab else TAB_DATA.BACK, btn.pos)
        else:
            render.canvas.blit(TAB_DATA.SEL_SIDE_BACK if choosing_colour else TAB_DATA.SIDE_BACK, btn.pos)
        btn.blit_on(render.canvas, with_centered=TAB_TEXT[tab])
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