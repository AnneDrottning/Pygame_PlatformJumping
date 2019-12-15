# Import packages
import pygame as     pg
import random
from   os     import path

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

        # Get the font name for the system, get the closest match to
        # what we want
        self.font_name = pg.font.match_font(FONT_NAME)

        # Load data needed for the game:
        self.load_data()

    def load_data(self):
        # Want to load the highscore file to see if we have a previous
        # highscore
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'w') as f:
            # 'w' will create a file if it does not exist, and allow
            # both reading and writing
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

    def new(self):
        # To start a new game
        self.score       = 0
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
                # Remove the platforms if they go off the screen
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10
        # If we die:
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        # Need to spawn new platforms to keep the game going
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            p = Platform(random.randrange(0, WIDTH - width),
                         random.randrange(-75, -30),
                         width, 20)
            self.platforms.add(p)
            self.all_sprites.add(p)

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
        self.screen.fill(BGCOLOUR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # After drawing everything, we flip the display
        pg.display.flip()

    def show_start_screen(self):
        # Game start screen
        self.screen.fill(BGCOLOUR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, Space to jump", 22, WHITE,
                        WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH/2,
                        HEIGHT * 3 / 4)
        self.draw_text("High Score: " + str(self.highscore), 22, WHITE,
                        WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # Game over / start over screen
        if not self.running:
            return
        self.screen.fill(BGCOLOUR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE,
                        WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to play again", 22, WHITE,
                        WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGHSCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WHITE,
                            WIDTH / 2, HEIGHT / 2 + 40)

        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        # Will pause the game, waiting for a key event.
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting      = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        # Function to draw the text we want
        font             = pg.font.Font(self.font_name, size)
        text_surface     = font.render(text, True, color)
        text_rect        = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

# Make an instance of the game object:
g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()
pg.quit()
