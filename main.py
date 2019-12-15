import pygame
import random

WIDTH  = 360
HEIGHT = 480
FPS    =  30

# Define the colours we want to use:
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

# Initialize pygame and create the window
pygame.init()
pygame.mixer.init()
screen = pygame.set_caption("Platform Jumping")
clock  = pygame.time.Clock()
