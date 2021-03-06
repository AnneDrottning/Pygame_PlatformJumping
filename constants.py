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
CLOUD_LAY = 0

# Player
PLAYER_ACCELERATION =  0.5
PLAYER_FRICTION     = -0.12
PLAYER_GRAVITY      =  0.8
JUMP_HEIGHT         = 20
PLAYER_LAYER        =  2

# Powerup properties:
BOOST_POWER        = 60
POW_SPAWN_PCT      =  5
POW_LAYER          =  1
BUBBLE_POWER       = 70

# Mob properties:
MOB_SPAWN_FREQ     = 5000 # in time
MOB_LAYER          =    2

# Starting platforms:
PLATFORM_LIST = [(0, HEIGHT - 60),
            (WIDTH / 2 - 50, HEIGHT * 3 / 4 - 50),
            (125, HEIGHT - 350),
            (350, 200),
            (175, 100)]
PLATFORM_LAYER = 1

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

# POWERUPS:
POW_BOOST          = [820, 1805,  71,  70]
POW_BUBBLE         = [826,  134,  71,  70]
BUBBLE_CIRCLE      = [  0, 1662, 211, 215]

# ITEMS:
COIN_GOLD          = [698, 1931, 84, 84]
GOLD_POINTS        = 100
GOLD_PCT           =   1
COIN_SILVER        = [584,  406, 84, 84]
SILVER_POINTS      =  50
SILVER_PCT         =   5
COIN_BRONZE        = [707,  296, 84, 84]
BRONZE_POINTS      =  20
BRONZE_PCT         =  10

# MOBS:
MOB_SPIKE          = [814, 1417,  90, 155]
MOB_FLY_UP         = [566,  510, 122, 139]
MOB_FLY_DOWN       = [568, 1534, 122, 135]
