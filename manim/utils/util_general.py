import random

from manim import *

############### DEFAULT OPTIONS

random.seed(0)


def set_default_colors():
    VMobject.set_default(color=GRAY)
    Polygon.set_default(color=RED)
    Text.set_default(color=TEXT_COLOR)
    # SurroundingRectangle.set_default(color = RED)
    # SurroundingRectangle.set_default(fill_color = config.background_color)
    # SurroundingRectangle.set_default(fill_opacity = 1)


def make_code(text):
    return Code(
        code=text,
        language="Python",
        tab_width=4,
        style="solarized-light",
        insert_line_no=False,
        font_size=24,
        #        margin=0.15,
        line_spacing=0.6,
    )


############### GENERATING SOUNDS
# self.add_sound(file_name)


def random_click_file():
    return f"audio/click/click_{random.randint(0, 3)}.wav"


def random_pop_file():
    return f"audio/pop/pop_{random.randint(0, 6)}.wav"


def random_whoosh_file():
    return f"audio/whoosh/whoosh_{random.randint(0, 3)}.wav"


whoosh_gain = -8


def random_tick_file():
    return f"audio/tick/tick_{random.randint(0, 7)}.wav"


def random_whoops_file():
    return f"audio/whoops/whoops{random.randint(1, 1)}.mp3"


def random_rubik_file():
    return f"audio/cube/r{random.randint(1, 20)}.wav"


def random_typewriter_file():
    return f"audio/typewriter/t{random.randint(0, 9)}.wav"


def step_sound_file(randomize=True):
    if randomize:
        return random_tick_file()
    else:
        return "audio/tick/tick_0.wav"


############### ANIMATIONS


def arrive_from(obj, dir, buff=0.5):
    pos = obj.get_center()
    obj.align_to(Point().to_edge(dir, buff=0), -dir).shift(buff * dir)
    return obj.animate.move_to(pos)


def nil_object():
    return Dot(radius=0, fill_opacity=0, stroke_opacity=0)


############### SOLARIZED COLORS


# background tones (dark theme)

BASE03 = "#002b36"
BASE02 = "#073642"
BASE01 = "#586e75"

# content tones

BASE00 = "#657b83"
BASE0 = "#839496"
BASE1 = "#93a1a1"

# background tones (light theme)

BASE2 = "#eee8d5"
BASE3 = "#fdf6e3"

# accent tones

YELLOW = "#d0b700"
YELLOW2 = "#b58900"  # The original Solarized yellow
ORANGE = "#c1670c"
ORANGE2 = "#cb4b16"  # The original Solarized orange - too close to red
RED = "#dc322f"
MAGENTA = "#d33682"
VIOLET = "#6c71c4"
BLUE = "#268bd2"
CYAN = "#2aa198"
CYAN2 = "#008080"
GREEN = "#859900"
HIGHLIGHT = YELLOW2

# Alias
GRAY = BASE00
GREY = BASE00

text_color = GRAY
TEXT_COLOR = GRAY
DALLE_ORANGE = r"#%02x%02x%02x" % (254, 145, 4)

# whenever more colors are needed
rainbow = [RED, MAGENTA, VIOLET, BLUE, CYAN, GREEN]
# [RED, ORANGE, GREEN, TEAL, BLUE, VIOLET, MAGENTA]
# [GREEN, TEAL, BLUE, VIOLET, MAGENTA, RED, ORANGE]

from manim import config

config.background_color = BASE2
BACKGROUND_COLOR_LIGHT = BASE2
BACKGROUND_COLOR_DARK = BASE02
BACKGROUND_COLOR = BACKGROUND_COLOR_LIGHT

config.max_files_cached = 1000
set_default_colors()
