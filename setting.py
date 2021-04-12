import pygame
pygame.init()

# FONT SETTING
SMALLFONT = pygame.font.Font(None, 10)
MEDIUMFONT = pygame.font.Font(None, 20)
LARGEFONT = pygame.font.Font(None, 30)

# SCREEN SETTING
WIDTH = 300
CELL_WIDTH = WIDTH // 3
TOP_DOWN_BUFFER = 100

# COLOR SETTING
GREYISH = (200, 200, 200)
DARKGREY = (100, 100, 100)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LIGHTRED = (100, 0, 0)
GREEN = (0, 255, 0)
GREENSHADE = (100, 200, 100)
LIGHTGREEN = (0, 100, 0)
LIGHTESTGREEN = (100, 200, 100)
BLUE = (0, 0, 255)
LIGHTBLUE = (0, 0, 100)

# BOARD SETTING
BOARD = [
    ['', '', ''],
    ['', '', ''],
    ['', '', '']
]