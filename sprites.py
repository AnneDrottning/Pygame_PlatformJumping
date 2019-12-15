# This is the sprite classes for the platform Game

# Import packages
import pygame as pg

# Import files
from constants import *

# Shortcuts:
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self):
        # Initialize a pygame sprite:
        pg.sprite.Sprite.__init__(self)

        # Create a simple sprite:
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW);
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)

        # Position, velocity and acceleration
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)


    def update(self):
        self.acc = vec(0, 0.5)
        # Check what keys are pressed:
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACCELERATION
        if keys[pg.K_RIGHT]:
            self.acc.x =  PLAYER_ACCELERATION

        # Adjust the sprite placement according to the speed
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + (0.5 * self.acc)

        # Wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH


        self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        # Want to define the size and position everytime we define a new
        # platform
        pg.sprite.Sprite.__init__(self)
        self.image  = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect   = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
