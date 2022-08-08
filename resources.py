import pygame

pygame.init()
pygame.font.init()


class AssetStorage:
    """
    A class to store arbitrary objects, with extra methods for working with 
    pygame.Surface objects.

    Acts as a dictionary, where keys can also be accessed as attributes

    Example: 
        person = AssetStorage(name="Person", age=25)
        person.name # "Person"
        person.age # 25
        person.get("name") # "Person"
        person.get("doesntexist") # None
        person.register(pets=["Chinchilla"]) 
        person.pets # ["Chinchilla"]
    """

    def __init__(self, **kwargs):
        """
        Constructs a new AssetStorage, inserting the passed in keyword 
            arguments 

        Params:
            **kwargs: keyword arguments passed in to be inserted
        """
        for k in kwargs:
            self.insert(k, kwargs[k])

    def register(self, **kwargs):
        """
        Adds the passed in keyword arguments to the AssetStorage. Alias for put

        Params:
            **kwargs: keywoard arguments passed in to be inserted
        """
        for k in kwargs:
            self.insert(k, kwargs[k])
            # self.__dict__[k] = kwargs[k]

    def put(self, **kwargs):
        """
        Adds the passed in keyword arguments to the AssetStorage. Alias for
            register.

        Params:
            **kwargs: keyword arguments passed in to be inserted
        """
        self.register(**kwargs)

    def insert(self, key, value):
        """
        Insert a key/value pair into the AssetStorage. Can be used recursively
            if there are '.' in the key

        Params:
            key: str: the string key to access the value by
            value: the value to assign to the key
        """
        if '.' in key:
            stor = self
            for substor in key.split('.')[:-1]:
                if stor.get(substor) is None:
                    stor.insert(substor, AssetStorage())
                stor = stor.get(substor)
            stor.insert(key.split('.')[-1], value)
        else:
            self.__dict__[key] = value

    def insert_all(self, dictionary: dict):
        """
        Insert all key/value pairs with string keys from a dict object into the
            AssetStorage

        Params:
            dictionary: dict: The dict object to insert all key/value pairs 
            with string keys from
        """
        for k, v in dictionary.items():
            if type(k) == str:
                self.insert(k, v)

    def scale_all_by(self, ratio, key=None):
        """
        Scales all of the pygame.Surface objects in the AssetStorage by the 
            given ratio

        Params:
            ratio: int, float, [int or float, int or float], or 
                (int or float, int or float)
                The ratio to scale the pygame.Surface objects by, using tuples
                or lists to scale width and height separately.
            key: function = None: a function to be passed into filter() to 
                filter the keys that should be scaled
        """
        if type(ratio) in [tuple, list]:
            for k in filter(key, self.__dict__.keys()):
                # if key is not None and not key(k):
                #     continue
                if type(self.get(k)) == pygame.Surface:
                    self.__dict__[k] = pygame.transform.scale(self.get(k), (int(round(self.get(k).get_width() * ratio[0])), int(round(self.get(k).get_height() * ratio[1]))))
        else:
            for k in filter(key, self.__dict__.keys()):
                # if key is not None and not key(k):
                #     continue
                if type(self.get(k)) == pygame.Surface:
                    self.__dict__[k] = pygame.transform.scale(self.get(k), (int(round(self.get(k).get_width() * ratio)), int(round(self.get(k).get_height() * ratio))))

    def scale_all_to(self, size, key=None):
        """
        Scales all of the pygame.Surface objects in the AssetStorage to the 
            given size

        Params:
            size: (int or float, int or float): The new size for all 
                pygame.Surface objects to be scaled to
            key: function = None: a function to be passed into filter() to 
                filter the keys that should be scaled
        """
        for k in filter(key, self.__dict__.keys()):
            # if key is not None and not key(k):
            #     continue
            if type(self.get(k)) == pygame.Surface:
                self.__dict__[k] = pygame.transform.scale(self.get(k), size)

    def attrs(self):
        """
        Returns a list of the attributes in this AssetStorage
        """
        # consider storing all attrs in a list when inserted
        return [i for i in self.__dict__.keys() if not i.startswith('__') and not callable(self.__dict__[i])]

    def get(self, attr: str, default=None):
        """
        Gets the value of a specified key in the AssetStorage. Can be used 
            recursively if there are '.' in the key

        Params:
            attr: str: the key to get from the AssetStorage
            default = None: The default value to return if the key is not found

        Returns:
            the value associated with the given key or the default value if the
            given key is not found
        """
        if "." in attr:
            stor = self
            for substor in attr.split('.'):
                stor = stor.get(substor)
                if stor is None:
                    return default
            return stor
        else:
            return self.__dict__.get(attr, default)

    def __str__(self, indent=""):
        """
        Returns a string representation of the AssetStorage
        """
        s = ""
        for a in self.attrs():
            if type(self.__dict__[a]) == AssetStorage:
                s += "\n" + indent + a + "=" + self.__dict__[a].__str__(indent+"  ")
            else:
                s += "\n" + indent + a + "=" + str(self.__dict__[a])
        return s

    def from_str(self, string):
        """
        Inserts a string representation of an AssetStorage into this 
            AssetStorage.

        Params:
            string: str: The string representation of the AssetStorage to 
                insert
        """
        lines = string.split("\n")
        stor = self
        opath = []
        previndent = 0
        for line in lines:
            if "=" in line:
                k, v = line.split("=")
                for _ in range(previndent - k.count("  ")):
                    opath.pop()
                if v == "":
                    opath.append(k)
                    continue
                stor = self
                for i in range(k.count("  ")):
                    stor = stor.__dict__.get(opath[i])
                previndent = k.count("  ")
                k = k.strip()
                try:
                    v = int(v)
                except ValueError:
                    try:
                        v = float(v)
                    except ValueError:
                        if "[" in v and "]" in v:
                            v = [int(i) for i in v.strip("][").split(", ") if i != ""]
                        else:
                            if v.title() in ["True", "False"]:
                                v = v.title() == "True"
                stor.register(**{k: v})


class Button:
    """
    A class representing a button on screen, with the ability to detect mouse
        collision and display on a surface

    Attributes:
        pos: (int or float, int or float): The position at which to display 
            this button
        sprite: pygame.Surface: The sprite of the button to be displayed
    """

    def __init__(self, pos, sprite: pygame.Surface):
        """
        Constructs a new Button object

        Params:
            pos: (int or float, int or float): The position at which to display
                this button
            sprite: pygame.Surface: The sprite of the button to be displayed
        """
        self.pos = pos
        self.sprite = sprite

    def move(self, new_pos):
        """
        Move this button to a new position 

        Params:
            new_pos: (int or float, int or float): The position to move this
                button to
        """
        self.pos = new_pos

    def resize(self, new_size):
        """
        Resize the sprite of this button

        Params:
            new_size: int, float, (int or float, int or float): The new size to
                resize the sprite to. If provided as an int or float, 
                multiplies the width and height by that value, otherwise 
                provides the new width and height to use
        """
        if type(new_size) in [int, float, tuple, list]:
            self.sprite = pygame.transform.scale(self.sprite, new_size if type(new_size) in [tuple, list] else (int(round(self.sprite.get_width() * new_size)), int(round(self.sprite.get_height() * new_size))))

    def collide_point(self, point):
        """
        Determines if a given point collides with this button

        Params:
            point: (int or float, int or float): The position to check 
                collision with.
        """
        return pygame.Rect(self.pos, self.sprite.get_size()).collidepoint(point)

    def collide_rect(self, rect: pygame.Rect):
        """
        Determines if a given rectangle collides with this button

        Params:
            rect: pygame.Rect: the rectangle to check collision with
        """
        return pygame.Rect(self.pos, self.sprite.get_size()).colliderect(rect)

    def blit_on(self, surface: pygame.Surface, offset=(0, 0), with_centered: pygame.Surface=None):
        """
        Blits (displays) this button on a given surface at the specified 
            position

        Params:
            surface: pygame.Surface: The surface on which to display this 
                button
            offset: (int or float, int or float) = (0, 0): The offset from this
                button's position to display at
            with_centered: pygame.Surface = None: A surface to display at the
                center of this button (pasted on top)
        """
        surface.blit(self.sprite, (self.pos[0] + offset[0], self.pos[1] + offset[1]))
        if with_centered:
            surface.blit(with_centered, (self.pos[0] + offset[0] + self.sprite.get_width() / 2 - with_centered.get_width() / 2, self.pos[1] + offset[1] + self.sprite.get_height() / 2 - with_centered.get_height() / 2))


class FontFamily:
    default_sizes = [10, 12, 18, 20, 25, 30]
    def __init__(self, fontpath, issys=False, nondefault_sizes=[], include_bold=False, include_italics=False):
        ftype = pygame.font.SysFont if issys else pygame.font.Font
        for size in self.default_sizes + nondefault_sizes:
            self.__dict__["f" + str(size)] = ftype(fontpath, size)
            if include_bold:
                self.__dict__["b" + str(size)] = ftype(fontpath, size)
                self.__dict__["b" + str(size)].bold = True
            if include_italics:
                self.__dict__["i" + str(size)] = ftype(fontpath, size)
                self.__dict__["i" + str(size)].italic = True


def scaled_font_set(font_sizes, downscale=(1, 1)):
    assets = AssetStorage(**{
        # attr: (pygame.font.Font if font_sizes.__dict__[font_sizes.__dict__[attr][0]][1] else pygame.font.SysFont)(font_sizes.__dict__[font_sizes.__dict__[attr][0]], round(int(font_sizes.__dict__[attr][1:]) * downscale[0])) for attr in font_sizes.attrs() if len(attr) > 1#"font" in attr
        attr: (pygame.font.Font if font_sizes.get(font_sizes.get(attr)[0])[1] else pygame.font.SysFont)(font_sizes.get(font_sizes.get(attr)[0])[0], round(int(font_sizes.get(attr)[1:]) * downscale[0])) for attr in font_sizes.attrs() if len(attr) > 1
        # attr: (pygame.font.Font if font_sizes.__dict__[font_sizes.__dict__[attr][0]][1] else pygame.font.SysFont)(font_sizes.__dict__[font_sizes.__dict__[attr][0]][0], round(int(font_sizes.__dict__[attr][1:]) * downscale_by[0])) for attr in font_sizes.attrs() if "font" in attr
    })
    return assets

def is_touching(pos1, size1, pos2, size2):
    return pygame.Rect(pos1, size1).colliderect(pygame.Rect(pos2, size2))

def split_multiline(text, font, max_size):
    """
    Split a string into multiple lines to ensure all lines have a width 
        less than or equal to the max_size

    Params:
        text: str: The string to split
        font: pygame.font.Font: The font the string will be rendered in
        max_size: int or float: The maximum width the text should take up
    Returns:
        a list of strings from the original text, split to meet the size 
            requirements
    """
    text_split = []
    if "\n" in text:
        text = text.split("\n")
    if type(text) == str:
        text = [text]
    for l in text:
        if font.size(l)[0] > max_size:
            words = l.split(' ')
            lines = []
            cur_l = ""
            cur_w = 0
            while cur_w < len(words):
                while font.size(cur_l)[0] + font.size(words[cur_w])[0] < max_size:
                    cur_l += words[cur_w] + " "
                    cur_w += 1
                    if cur_w >= len(words):
                        break
                lines.append(cur_l)
                cur_l = ""
            text_split.extend(lines)
        else:
            text_split.append(l)
    return text_split

def render_text_with_icons(text, font, color, icon_list:AssetStorage=AssetStorage(), downscaled_icons=None, spacing=5, bgcolor=(0, 0, 0, 0), align="left"):
    """
    Renders a string with delimited icons to be displayed in pygame

    Params:
        text: str or list: A string or list of strings to be rendered. 
            This string may or may not contain icons defined in the icon_list,
            delimited by the pipe "|" character. The lines will be rendered on 
            multiple different lines separated by the '\n' character or by 
            different entries in the list.
            e.g. "This\nis |my_icon|" is equivalent to ["This", "is |my_icon|"]
        font: pygame.font.Font: The font in which to render the text.
        color: (int, int, int, int): The color in which to render the text, in
            the form RGBA.
        icon_list: AssetStorage: An AssetStorage or similar object containing 
            all of the icons, where calling icon_list.get("my_icon") will 
            return the pygame.Surface containing my_icon.
        downscaled_icons: (float, float) or bool = None: 
            CURRENTLY UNIMPLEMENTED
            Whether or not to downscale the icons in icon_list. If True, scales
            automatically based on the screen size.
        spacing: int = 5: The pixel spacing between lines of text and between 
            text and icons
        bgcolor: (int, int, int, int) = (0, 0, 0, 0): The background color for 
            the text. Note: Will only fill in the area behind the text on the 
            Surface, may not look very nice as a text box.
        align: str = "left": The text alignment, can be "left", "right", or 
            "center"
    """
    lines = []
    text_lines = text if type(text) == list else text.split("\n")
    for text_line in text_lines:
        if "|" in text_line:
            chunks = []
            n_icons = text_line.count("|") / 2
            for i, s in enumerate(text_line.split("|")):
                if i % 2 == 0:
                    chunks.append(font.render(s, True, color))
                else:
                    if i < n_icons * 2:
                        s = s.replace("'", "")
                        ico = None
                        if icon_list.get(s) is not None:
                            ico = icon_list.get(s).copy()
                        # if downscaled_icons is not None:
                        #     if type(downscaled_icons) == tuple:
                        #         ico = pygame.transform.scale(ico, (int(ico.get_width() * downscaled_icons[0]), int(ico.get_height() * downscaled_icons[1])))
                        #     elif downscaled_icons == True:
                        #         ico = pygame.transform.scale(ico, (int(ico.get_width() * downscale[0]), int(ico.get_height() * downscale[1])))
                        chunks.append(ico)
            line = pygame.Surface((sum([i.get_width() + spacing for i in chunks]), max(i.get_height() for i in chunks)), pygame.SRCALPHA)
            cur_x = 0
            for chunk in chunks:
                line.blit(chunk, (cur_x, line.get_height() / 2 - chunk.get_height() / 2))
                cur_x += chunk.get_width() + spacing
            lines.append(line)
        else:
            lines.append(font.render(text_line, True, color))
    s = pygame.Surface((max([i.get_width() for i in lines]), sum([i.get_height() + spacing for i in lines]) if len(lines) > 0 else 1),
                       pygame.SRCALPHA)
    s.fill(bgcolor)
    cur_y = 0
    for i in range(len(lines)):
        x = 0
        if align == "left":
            x = 0
        elif align == "right":
            x = s.get_width() - lines[i].get_width()
        elif align == "center":
            x = s.get_width() / 2 - lines[i].get_width() / 2
        s.blit(lines[i], (x, cur_y))
        cur_y += lines[i].get_height() + spacing
    return s