from os import path
import pygame
import render
import resources

DIALOG_PATH = "Assets/dialogue"
data = resources.AssetStorage()

def dialogue_from_file(fpath, file_in_path=True):
    """ Reads in the specified file in Assets/dialogue and loads its data into
    data
    """
    with open(path.join(DIALOG_PATH, fpath)) as f:
        text = f.read()
        if file_in_path:
            data.insert(fpath.split(".")[0], resources.AssetStorage())
            data.get(fpath.split(".")[0]).from_str(text)
        else:
            data.from_str(text)

def render_dialogue(attr):
    """ Renders out the specified dialogue attribute in data
    """
    profile = data.get(attr).get("profile")
    profile = render.assets.get(profile)
    bubble = data.get(attr).get("bubble")
    bubble = render.assets.get(bubble).copy()
    surf = pygame.Surface((render.canvas.get_width(), max(
        0 if bubble is None else bubble.get_height(),
        0 if profile is None else profile.get_height()
    )), pygame.SRCALPHA)
    if bubble:
        text_offs_x = 30 / 378 * bubble.get_width()
        speaker = data.get(attr).get("speaker")
        if speaker:
            speaker_offs_y = 19 / 135 * bubble.get_height()
            bubble.blit(resources.render_text_with_icons(speaker, render.fs.subtitle, (0, 0, 0, 255), render.assets.icon), (text_offs_x, speaker_offs_y))
        text = data.get(attr).get("text")
        if text:
            text_offs_y = 52 / 135 * bubble.get_height()
            bubble.blit(resources.render_text_with_icons(text, render.fs.header1, (0, 0, 0, 255), render.assets.icon), (text_offs_x, text_offs_y))
        surf.blit(bubble, (surf.get_width() / 2 - bubble.get_width() / 2, surf.get_height() / 2 - bubble.get_height() / 2))
    if profile:
        # TODO: make the profile show up on the correct side of the speech bubble
        surf.blit(profile, (0, surf.get_height() / 2 - profile.get_height() / 2))
    return surf