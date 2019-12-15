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
        self.player = Player()
        self.all_sprites.add(self.player)
        p1 = Platform(0, HEIGHT - 40, WIDTH, 40)
        self.all_sprites.add(p1)
        self.platforms.add(p1)
        p2 = Platform(WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20)
        self.all_sprites.add(p2)
        self.platforms.add(p2)
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
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            self.player.pos.y = hits[0].rect.top
            self.player.vel.y = 0


    def events(self):
        # The game loop events
        # Process input events:
        for event in pg.event.get():
            # Check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

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
