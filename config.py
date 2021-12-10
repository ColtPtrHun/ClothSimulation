__author__ = "Péter Kerekes"

# Setting up color objects. Tuple: ordered, immutable collection of items
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (0, 0, 127)

FONT_SIZE = 18
FONT_OFFSET = 10

SCREEN_SIZE = (1024, 768)
SCREEN_SCALE = 40 # [pixel] = 1[m]
SCREEN_BACKGROUND = DARK_BLUE

dT = 1 / 60 # [FPS]
TETHERING_ITERATIONS = 2
g = 9.81

PAUSE = 0
PLAY = 1

LEFT_MOUSE_BUTTON = 1
MIDDLE_MOUSE_BUTTON = 2
RIGHT_MOUSE_BUTTON = 3