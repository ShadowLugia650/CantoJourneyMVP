import pygame
import render
import resources
import ui

def save():
    pass

def load():
    pass

customs = resources.AssetStorage(
    skin=0,
    hair=0,
    hair_colour=0,
    face=0,
    face_colour=0,
    shirt=0,
    shirt_colour=0,
    pants=0,
    pants_colour=0,
    shoes=0,
    shoes_colour=0,
)

# sprites
sprite = None
head_sprite = resources.AssetStorage(
    small=None,
    SMALL_SCALE=57/137.5,
    medium=None,
    MEDIUM_SCALE=102/137.5,
    large=None
)

# other data
seat = "14A"

def generate_sprite():
    global sprite, head_sprite
    sprite = pygame.Surface(render.assets.img.PChara.Body.get("0").xpt2.get_size(), pygame.SRCALPHA)
    sprite.blit(render.assets.img.PChara.Body.get(str(customs.skin)).xpt2, (0, 0))
    sprite.blit(render.assets.img.PChara.Pants.get(str(customs.pants) + "c" + str(customs.pants_colour)).xpt2, (0, 0))
    sprite.blit(render.assets.img.PChara.Shirt.get(str(customs.shirt) + "c" + str(customs.shirt_colour)).xpt2, (0, 0))
    sprite.blit(render.assets.img.PChara.Shoes.get(str(customs.shoes) + "c" + str(customs.shoes_colour)).xpt2, (0, 0))
    sprite.blit(render.assets.img.PChara.Head.get(str(customs.skin)).xpt2, (0, 0))
    sprite.blit(render.assets.img.PChara.Face.get(str(customs.face) + "c" + str(customs.face_colour)).xpt2, (0, 0))
    sprite.blit(render.assets.img.PChara.Hair.get(str(customs.hair) + "c" + str(customs.hair_colour)).xpt2, (0, 0))
    head_sprite.insert("large", pygame.Surface(render.assets.img.PChara.Face.get("0c0").xpt2.get_size(), pygame.SRCALPHA))
    head_sprite.large.blit(render.assets.img.PChara.Head.get(str(customs.skin)).xpt2, (0 ,0))
    head_sprite.large.blit(render.assets.img.PChara.Face.get(str(customs.face) + "c" + str(customs.face_colour)).xpt2, (0, 0))
    head_sprite.large.blit(render.assets.img.PChara.Hair.get(str(customs.hair) + "c" + str(customs.hair_colour)).xpt2, (0, 0))
    head_sprite.insert("medium", pygame.transform.scale(head_sprite.large, (round(head_sprite.large.get_width() * head_sprite.MEDIUM_SCALE), round(head_sprite.large.get_height() * head_sprite.MEDIUM_SCALE))))
    # TODO: Add small
    head_sprite.insert("small", pygame.transform.scale(head_sprite.large, (round(head_sprite.large.get_width() * head_sprite.SMALL_SCALE), round(head_sprite.large.get_height() * head_sprite.SMALL_SCALE))))

# ui.loading_screen_while(generate_sprite, (), False, render.img_load_thd)