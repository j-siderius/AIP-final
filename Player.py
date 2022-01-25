import random
import pygame
import math
import time

import Tile
from Field import Field
from Data.Settings import Settings
from Data.TilesData import Resources
from Screen import lerp, lerp_2D


class Player:

    def __init__(self, screen,  serial_update_health, field_size, field: Field, game_end_func, time_ticker_func=None):
        self.screen = screen
        self.field = field
        hex_amount = field.field_size
        self.field_size = field_size
        self.time_ticker = time_ticker_func
        self.serial_update_health = serial_update_health
        self.game_end_func = game_end_func

        self.health = 4

        self.x, self.y = None, None  # pos on the world map
        self.current_tile: Tile = None
        self.radius = self.field.hex_size / 2.3  # base this on hex_size of Tiles
        # assign starting position to a viable tile
        self.find_starting_tile(int(hex_amount[0] / 2), int(hex_amount[1] / 2))
        # is_highlight the next moves
        self.current_tile.highlight_neighbours()

        # walking
        self.is_walking = False
        self.walk_timer = 0
        self.from_tile = self.current_tile
        self.target_tile = None

        # mining and building
        # self.last_mouse_down_time = 0
        self.doing_an_action = False
        self.inventory = {Resources.wood: 100}  # dict()

        self.color = (255, 0, 0)

        self.idle_sprite = [[
            pygame.image.load("Data/Sprites/Player/elf_m_idle_anim_f0.png").convert_alpha(),
            pygame.image.load("Data/Sprites/Player/elf_m_idle_anim_f1.png").convert_alpha(),
            pygame.image.load("Data/Sprites/Player/elf_m_idle_anim_f2.png").convert_alpha(),
            pygame.image.load("Data/Sprites/Player/elf_m_idle_anim_f3.png").convert_alpha()
        ], [
            pygame.image.load("Data/Sprites/Player/elf_m_idle_anim_left_f0.png").convert_alpha(),
            pygame.image.load("Data/Sprites/Player/elf_m_idle_anim_left_f1.png").convert_alpha(),
            pygame.image.load("Data/Sprites/Player/elf_m_idle_anim_left_f2.png").convert_alpha(),
            pygame.image.load("Data/Sprites/Player/elf_m_idle_anim_left_f3.png").convert_alpha()
        ]]
        self.run_sprite = [[
            pygame.image.load("Data/Sprites/Player/elf_m_run_anim_f0.png").convert_alpha(),
            pygame.image.load("Data/Sprites/Player/elf_m_run_anim_f1.png").convert_alpha(),
            pygame.image.load("Data/Sprites/Player/elf_m_run_anim_f2.png").convert_alpha(),
            pygame.image.load("Data/Sprites/Player/elf_m_run_anim_f3.png").convert_alpha()
        ], [
            pygame.image.load("Data/Sprites/Player/elf_m_run_anim_left_f0.png").convert_alpha(),
            pygame.image.load("Data/Sprites/Player/elf_m_run_anim_left_f1.png").convert_alpha(),
            pygame.image.load("Data/Sprites/Player/elf_m_run_anim_left_f2.png").convert_alpha(),
            pygame.image.load("Data/Sprites/Player/elf_m_run_anim_left_f3.png").convert_alpha()
        ]]
        self.image = self.idle_sprite[1][0]
        self.rect = self.image.get_rect()
        self.look_direction = 1
        self.frame = 0
        self.timer: float = 0.0

    def display(self):
        self.timer += self.screen.get_elapsed_time()
        if self.timer > 0.10:
            self.timer: float = 0.0
            if self.frame < 3:
                self.frame += 1
            else:
                self.frame = 0

        if self.is_walking:
            self.image = self.run_sprite[self.look_direction][self.frame]
        else:
            self.image = self.idle_sprite[self.look_direction][self.frame]

        self.screen.get_screen().blit(self.image, (self.x-8, self.y-18))

        # inventory menu
        menu_txt = ["Inventory: "]
        for key, value in self.inventory.items():
            menu_txt.append(f"{key}: {value}")

        self.screen.text_font(25)
        width, height = self.screen.get_size()
        self.screen.text_array(width - 110, 20, menu_txt, 255, background_color=0)

    def update(self):
        if self.is_walking:  # walking
            factor = 1 - self.walk_timer / Settings.PLAYER_WALKING_TIME
            walkspeed = lerp(self.from_tile.is_walkable(), self.target_tile.is_walkable(), factor)
            self.walk_timer -= self.screen.get_elapsed_time() * walkspeed
            if self.walk_timer <= 0:
                self.is_walking = False
                self.align_player(self.target_tile)
                self.from_tile = self.current_tile

                # is_highlight the next moves
                self.current_tile.highlight_neighbours()
            else:
                self.x, self.y = lerp_2D(self.from_tile.get_center(), self.target_tile.get_center(), factor)

    def move_player(self, target_tile: Tile):
        """Moves the player to the clicked tile (if valid move)"""
        if self.is_walking or self.doing_an_action:
            return

        neighbours = self.current_tile.get_neighbours()
        for neighbour in neighbours:
            if neighbour == target_tile and target_tile.is_walkable():
                # TODO: implement tick rate with something like nextTile = this.tile
                self.time_ticker()
                self.current_tile.unhighlight_neighbours()
                self.is_walking = True
                self.walk_timer = Settings.PLAYER_WALKING_TIME
                self.target_tile = neighbour

    def mine_build(self, pressed_tile):
        """Performs the player action on the clicked tile (mine, build, destroy)"""
        if self.is_walking or self.doing_an_action:
            return

        # resource mining
        if pressed_tile.has_resources():  # if the tile has resources
            self.start_action()
            pressed_tile.action_mine_resource(self.end_action)

        # building
        elif pressed_tile.can_build():
            # wooden wall
            if self.inventory[Resources.wood] >= Settings.WOODEN_WALL_COST:
                self.start_action()
                pressed_tile.action_build_wall(self.end_action)
                self.inventory[Resources.wood] -= Settings.WOODEN_WALL_COST

        # destroying buildings
        elif pressed_tile.has_structure():
            self.start_action()
            pressed_tile.action_destroy_structure(self.end_action)

    # employ walking algorithm to find suitable starting tile
    def find_starting_tile(self, tileX, tileY):
        tile = self.field.get_tile(tileX, tileY)
        if tile.is_walkable() != 1:
            try_tile = tile.get_neighbours()[random.randint(0, len(tile.get_neighbours()) - 1)]
            self.find_starting_tile(try_tile.x, try_tile.y)
        else:
            # assign player position to the found grass tile
            print(f"Starting tile found: ({tileX},{tileY})")
            self.align_player(tile)

    def align_player(self, tile: Tile):
        self.current_tile = tile
        self.x, self.y = tile.get_center()

    # called when the player starts an action, not called when the player moves
    def start_action(self):
        self.time_ticker()
        # implementation ^ Work In Progress
        self.doing_an_action = True

    def end_action(self, gained_resource, amount):
        if gained_resource is not None:  # if a resource was gained in the action
            if gained_resource in self.inventory:  # if the user already has a resource then just add it.
                self.inventory[gained_resource] += amount
            else:  # if the user doesn't than add the resource to the inventory
                self.inventory[gained_resource] = amount

        # set doing an action to false so the user can start another action
        self.doing_an_action = False

    def get_player_position(self):
        return self.x, self.y

    def get_current_tile(self):
        return self.current_tile

    def set_look_direction(self, direction: str):
        if direction == "left": self.look_direction = 0
        elif direction == "right": self.look_direction = 1

    def attack_player(self, damage):
        self.health -= damage
        self.serial_update_health(self.health)
        if self.health <= 0:
            self.game_end_func()
