# Import packages
import pygame as pg
import random

# Import files
from constants import *
from sprites   import *

class Game:
    def __init__(self):
        # Initialize the game window, etc.
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock  = pg.time.Clock()

        # Game variable to determine wether the game is running or not:
        self.running = True

    def new(self):
        # To start a new game
        # Create the sprites
        self.all_sprites = pg.sprite.Group()
        self.platforms   = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat) # Exploding the list
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # The actual game loop
        # Keep loop running at the right speed
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # The game loop update
        # Update:
        self.all_sprites.update()
        # Check if the player hits a platform
        # Only want to see if we are falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
        # Want to check if we need to scroll the screen
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)

    def events(self):
        # The game loop events
        # Process input events:
        for event in pg.event.get():
            # Check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        # Drawing the game loop to the screen
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        # After drawing everything, we flip the display
        pg.display.flip()

    def show_start_screen(self):
        # Game start screen
        pass

    def show_go_screen(self):
        # Game over / start over screen
        pass

# Make an instance of the game object:
g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()
pg.quit()
