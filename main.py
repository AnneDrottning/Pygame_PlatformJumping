# Credits:
# Art from Kenney.nl
# Happy Tune by http://opengameart.org/users/syncopika
# Yippee by http://opengameart.org/users/snabisch

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
        img_dir  = path.join(self.dir, 'img')
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            # 'w' will create a file if it does not exist, and allow
            # both reading and writing
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        # Load the spritesheet
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        # Load some sounds:
        self.snd_dir     = path.join(self.dir, 'snd')
        self.jump_sound  = pg.mixer.Sound(path.join(self.snd_dir, 'Jump.wav'))
        self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Powerup9.wav'))

    def new(self):
        # To start a new game
        self.score       = 0
        # Create the sprites
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms   = pg.sprite.Group()
        self.powerups    = pg.sprite.Group()
        self.mobs        = pg.sprite.Group()
        self.player = Player(self)
        for plat in PLATFORM_LIST:
            Platform(self, *plat) # Exploding the list
        self.mob_timer = 0 # When the last mob was spawned
        # Music to play during the game
        pg.mixer.music.load(path.join(self.snd_dir, 'happytune.wav'))
        self.run()

    def run(self):
        # The actual game loop
        # Play the music:
        pg.mixer.music.play(loops=-1) # loop infinetly
        # Keep loop running at the right speed
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        # Let the music gradually fadeout:
        pg.mixer.music.fadeout(500)

    def update(self):
        # The game loop update
        # Update:
        self.all_sprites.update()

        # Check if we want to spawn a mob or not:
        now = pg.time.get_ticks()
        if now - self.mob_timer > MOB_SPAWN_FREQ + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)
        # Check if we hit the mob:
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        if mob_hits:
            self.playing = False


        # Check if the player hits a platform
        # Only want to see if we are falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                # Want to land on the lowest platform:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                # Want to finesse how the character lands on the platforms
                if self.player.pos.x < lowest.rect.right + 10 and \
                   self.player.pos.x > lowest.rect.left - 10:
                   # Only want to land on the platform if our feet are above it
                   if self.player.pos.y < lowest.rect.centery:
                       self.player.pos.y   = lowest.rect.top
                       self.player.vel.y   = 0
                       self.player.jumping = False

        # Want to check if we need to scroll the screen
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)
                if mob.rect.top >= HEIGHT:
                    mob.kill()

            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                # Remove the platforms if they go off the screen
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

        # Check for collision with powerups:
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.player.vel.y   = -BOOST_POWER
                self.player.jumping = False
                self.boost_sound.play()

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
            Platform(self, random.randrange(0, WIDTH - width),
                         random.randrange(-75, -30))

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
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        # Drawing the game loop to the screen
        self.screen.fill(BGCOLOUR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # After drawing everything, we flip the display
        pg.display.flip()

    def show_start_screen(self):
        # Include music:
        pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.wav'))
        pg.mixer.music.play(loops=-1)
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
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        # Music for the screen
        pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.wav'))
        pg.mixer.music.play(loops=-1)
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
        pg.mixer.music.fadeout(500)

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
