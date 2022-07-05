import pygame
import random
import math
from pygametools.label import Label, Button


# Initialise pygame
pygame.init()

# Set the dimensions of the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 640

# Set the name and icon of the window
pygame.display.set_caption("2048")
icon = pygame.image.load("assets/2048_logo.svg.png")
icon = pygame.transform.scale(icon, (32, 32))
pygame.display.set_icon(icon)

# Find out delta and create clock
clock = pygame.time.Clock()
fps = 60


class Colour:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    LIGHT_PINK = (255, 209, 223)
    LIGHT_BLUE = (213, 209, 255)
    LIGHT_YELLOW = (255, 250, 209)
    ORANGE = (255, 173, 51)
    OFF_RED = (255, 69, 69)
    PURPLE = (202, 69, 255)
    DARK_BLUE = (57, 26, 135)
    GOLD = (255,215,0)
    GRAY = (125, 125, 125)
    SQUARE_BG = (199, 187, 171)
    SQUARE_OUTLINE = (182, 163, 148)
