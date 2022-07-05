import pygame
from pygametools.label import Label, Button

# Initialise pygame
pygame.init()

# Set the dimensions of the screen
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the name and icon of the window
# pygame.display.set_caption("pygame")
# icon = pygame.image.load("filename")
# icon = pygame.transform.scale(icon, (32, 32))
# pygame.display.set_icon(icon)

# Find out delta and create clock
clock = pygame.time.Clock()
fps = 60
delta = 1000 // fps

# Background colour
background_colour = (255, 255, 255)

# Main loop
is_running = True
while is_running:

    screen.fill(background_colour)

    # Check if the window is closed
    if pygame.event.peek(pygame.QUIT):
        is_running = False

    # Update the window and find delta
    pygame.display.update()
    delta = clock.tick(fps)

# Exit pygame
pygame.quit()
