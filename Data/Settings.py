from enum import Enum

# a place to store settings and constants, might make a separate JSON file to actual store settings


class Settings:
    # Overall
    SERIAL_PORT = 'COM3'
    GAME_DURATION = 4       # The amount of days the user needs to survive for
    TIMESCALE = 24          # The amount of ticks (player actions) in a day (has to be a multiple of 12)

    # Debug
    SHOW_FPS = True
    SHOW_PATH_FINDING = False
    SHOW_SPAWN_AREA = False

    # spawning
    MIN_SPAWN_DISTANCE = 200
    MAX_SPAWN_DISTANCE = 500
    SPAWN_TRY_AMOUNT = [1, 1, 2, 2, 3, 3]

    # AI
    MOVEMENT_COST_MULTIPLIER = 25
    WALL_BREAK_TIME = 3  # it takes ten turns to break a wall

    # player
    PLAYER_WALKING_TIME = 0.25
    WOODEN_WALL_COST = 2

    # tile highlight
    HIGHLIGHT_COLOR = (255, 100)
    HIGHLIGHT_COLOR_SELECTED = (255, 140, 0, 200)
    HIGHLIGHT_COLOR_ACTION = (65, 105, 225, 150)

    # terrain generation
    WATER_DROP_OFF_SCALING = 1


class MouseButton:
    left: int = 1
    scroll: int = 2
    right: int = 3
    scroll_up: int = 4
    scroll_down: int = 5
