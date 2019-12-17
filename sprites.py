# This is the sprite classes for the platform Game

# Import packages
import pygame as     pg
from   random import choice, randrange

# Import files
from constants import *

# Shortcuts:
vec = pg.math.Vector2

class Spritesheet:
    # A class to let us slice up the spritesheet to get the
    # graphics we want.
    # Here we load and parse the spritesheet
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, w, h):
        # To extract the specific chunck of the spreadsheet
        image = pg.Surface((w, h))
        image.blit(self.spritesheet, (0, 0), (x, y, w, h))
        # Need to resize the images:
        image = pg.transform.scale(image, (w // 2, h // 2))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        # Initialize a pygame sprite:
        pg.sprite.Sprite.__init__(self, self.groups)
        # Want the player to know about the game
        self.game  = game
        # Variables for the different images:
        self.walking       = False
        self.jumping       = False
        self.current_frame = 0 # For animation frames, e.g. walking
        self.last_update   = 0 # What time we made the last change
        # Group all the images in a new method:
        self.load_images()
        # Create a simple sprite:
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT - 100)

        # Position, velocity and acceleration
        self.pos = vec(40, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        # Load the images for the player sprite:
        # The standing frames:
        self.standing_frames = [self.game.spritesheet.get_image(*BUNNY_READY),
                                self.game.spritesheet.get_image(*BUNNY_STAND)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        # The walking right frames:
        self.walk_frames_r   = [self.game.spritesheet.get_image(*BUNNY_WALK1),
                                self.game.spritesheet.get_image(*BUNNY_WALK2)]
        # The walking left frames:
        self.walk_frames_l   = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))

        # The jump frame
        self.jump_frame      = self.game.spritesheet.get_image(*BUNNY_JUMP)
        self.jump_frame.set_colorkey(BLACK)

    def jump(self):
        # Only want to jump if we are standing on a platform
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y   = -JUMP_HEIGHT

    def jump_cut(self):
        # Shorter jump
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAVITY)
        # Check what keys are pressed:
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACCELERATION
        if keys[pg.K_RIGHT]:
            self.acc.x =  PLAYER_ACCELERATION

        # Adjust the sprite placement according to the speed
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + (0.5 * self.acc)

        # Wrap around the sides of the screen
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2


        self.rect.midbottom = self.pos

    def animate(self):
        # Will handle what frame we want to use.
        # Find out what time in the game we are at:
        now = pg.time.get_ticks()
        # Find out if we are walking
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        # Need to know if we want to show the standing animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update   = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom             = self.rect.bottom
                self.image         = self.standing_frames[self.current_frame]
                self.rect          = self.image.get_rect()
                self.rect.bottom   = bottom
        # Show the walk animation
        if self.walking:
            if now - self.last_update > 180:
                self.last_update   = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom             = self.rect.bottom
                if self.vel.x > 0:
                    self.image     = self.walk_frames_r[self.current_frame]
                else:
                    self.image     = self.walk_frames_l[self.current_frame]
                self.rect          = self.image.get_rect()
                self.rect.bottom   = bottom

        # Set our mask:
        self.mask = pg.mask.from_surface(self.image)

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms
        # Want to define the size and position everytime we define a new
        # platform
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game   = game
        images      = [self.game.spritesheet.get_image(*PLAT_LARGE),
                        self.game.spritesheet.get_image(*PLAT_SMALL)]
        self.image  = choice(images)
        self.image.set_colorkey(BLACK)
        self.rect   = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange(100) < POW_SPAWN_PCT:
            Pow(self.game, self)

class Pow(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = POW_LAYER
        # The two groups we want to add the powerup sprite to.
        self.groups = game.all_sprites, game.powerups
        # Needs to know the platform on which we want the powerup to spawn
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game   = game
        self.plat   = plat
        self.type   = choice(['boost'])
        self.image  = self.game.spritesheet.get_image(*POW_BOOST)
        self.image.set_colorkey(BLACK)
        self.rect         = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom  = self.plat.rect.top - 5

    def update(self):
        # If the platform moves, so will the platform
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()

class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = MOB_LAYER
        # The two groups we want to add the powerup sprite to.
        self.groups = game.all_sprites, game.mobs
        # Needs to know the platform on which we want the powerup to spawn
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game       = game
        self.image_up   = self.game.spritesheet.get_image(*MOB_FLY_UP)
        self.image_up.set_colorkey(BLACK)
        self.image_down = self.game.spritesheet.get_image(*MOB_FLY_DOWN)
        self.image_down.set_colorkey(BLACK)
        self.image      = self.image_up
        self.rect       = self.image.get_rect()
        # Spawn on a random side, outside the screen
        self.rect.centerx  = choice([-100, WIDTH+100])
        self.vx            = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1

        self.rect.y = randrange(HEIGHT / 2)
        self.vy     = 0
        self.dy     = 0.5 # To adjust the acceleration

    def update(self):
        self.rect.x += self.vx
        self.vy     += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            # Moving upwards:
            self.image = self.image_up
        else:
            self.image = self.image_down

        self.rect        = self.image.get_rect()
        self.mask        = pg.mask.from_surface(self.image)
        self.rect.center = center
        self.rect.y     += self.vy
        if self.rect.left > WIDTH+100 or self.rect.right < -100:
            self.kill()


class Cloud(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = CLOUD_LAY
        self.groups = game.all_sprites, game.clouds
        # Initialize a pygame sprite:
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = choice(self.game.cloud_images)
        self.image.set_colorkey(BLACK)
        self.rect   = self.image.get_rect()
        scale       = randrange(50, 101) / 100
        self.image  = pg.transform.scale(self.image, ((int(self.rect.width*scale), int(self.rect.height*scale))))
        self.rect.x = randrange(WIDTH - self.rect.width)
        self.rect.y = randrange(-500, -50)

    def update(self):
        if self.rect.top > HEIGHT * 2:
            self.kill()
