import pygame
import render
import resources


def save():
    pass

def load():
    pass

customs = resources.AssetStorage(
    body=0,
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
head_sprite = None

# other data
seat = "14A"

def generate_sprite():
    global sprite, head_sprite
    sprite = pygame.Surface(render.assets.img.PChara.Body.get("0").get_size(), pygame.SRCALPHA)
    sprite.blit(render.assets.img.PChara.Body.get(str(customs.body)), (0, 0))
    sprite.blit(render.assets.img.PChara.Pants.get(str(customs.pants) + "c" + str(customs.pants_colour)), (0, 0))
    sprite.blit(render.assets.img.PChara.Shirt.get(str(customs.shirt) + "c" + str(customs.shirt_colour)), (0, 0))
    sprite.blit(render.assets.img.PChara.Shoes.get(str(customs.shoes) + "c" + str(customs.shoes_colour)), (0, 0))
    sprite.blit(render.assets.img.PChara.Head.get(str(customs.body)), (0, 0))
    sprite.blit(render.assets.img.PChara.Face.get(str(customs.face) + "c" + str(customs.face_colour)), (0, 0))
    sprite.blit(render.assets.img.PChara.Hair.get(str(customs.hair) + "c" + str(customs.hair_colour)), (0, 0))
    head_sprite = pygame.Surface(render.assets.img.PChara.Face.get("0c0").get_size(), pygame.SRCALPHA)
    head_sprite.blit(render.assets.img.PChara.Head.get(str(customs.body)), (0 ,0))
    head_sprite.blit(render.assets.img.PChara.Face.get(str(customs.face) + "c" + str(customs.face_colour)), (0, 0))
    head_sprite.blit(render.assets.img.PChara.Hair.get(str(customs.hair) + "c" + str(customs.hair_colour)), (0, 0))