__author__ = "Péter Kerekes"

# Setting up color objects. Tuple: ordered, immutable collection of items
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DEEP_BLUE = (0, 0, 192)
DARK_BLUE = (0, 0, 127)

FONT_SIZE = 18
FONT_OFFSET = 10

SCREEN_SIZE = (1024, 768)
SCREEN_SCALE = 40 # [pixel] = 1[m]
global SCREEN_BACKGROUND
SCREEN_BACKGROUND = DEEP_BLUE

dT = 1 / 60 # [FPS]
g = 9.81
TETHERING_ITERATIONS = 2
STICK_SELECT_TOLERANCE = .5
STICK_SELECT_THRESHOLD = .15

PAUSE = 0
PLAY = 1

LEFT_MOUSE_BUTTON = 1
MIDDLE_MOUSE_BUTTON = 2
RIGHT_MOUSE_BUTTON = 3