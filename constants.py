# This file contains all the constants we will use in the
# platform game that we are developing.

# Game-screen:
WIDTH       = 480
HEIGHT      = 600
FPS         =  60
TITLE       = "Platform Jumping"
FONT_NAME   = 'arial'
HS_FILE     = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"

# Colours:
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
BLUE      = (  0,   0, 255)
YELLOW    = (255, 255,   0)
LIGHTBLUE = (  0, 155, 155)
BGCOLOUR  = LIGHTBLUE

# Player
PLAYER_ACCELERATION =  0.5
PLAYER_FRICTION     = -0.12
PLAYER_GRAVITY      =  0.8
JUMP_HEIGHT         =  20

# Starting platforms:
PLATFORM_LIST = [(0, HEIGHT-50),
            (WIDTH / 2 - 50, HEIGHT * 3 / 4 - 50),
            (125, HEIGHT - 350),
            (350, 200),
            (175, 100)]

# SPRITES:
BUNNY_READY = [614, 1063, 120, 191]
BUNNY_STAND = [690,  406, 120, 201]
BUNNY_WALK1 = [678,  860, 120, 201]
BUNNY_WALK2 = [692, 1458, 120, 207]
BUNNY_JUMP  = [382,  763, 150, 181]
BUNNY_HURT  = [382,  946, 150, 174]

# PLATFORMS:
PLAT_LARGE         = [  0,  288, 380,  94]
PLAT_SMALL         = [213, 1662, 201, 100]
PLAT_LARGE_DAMAGED = [  0,  384, 380,  94]
PLAT_SMALL_DAMAGED = [382,  204, 200, 100]
