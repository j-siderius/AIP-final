import bisect
import math
import random
import pygame
import Tile
from Data.Settings import Settings
from Player import Player
from Screen import lerp, lerp_2D, Screen


class Zombie:
    """
    The Zombie class handles the actions of the zombie, the a* pathfinding, movement, attacking the player when it is in reach and attacking walls
    This class also draws the sprite and animation of the zombie

    :param tile: The starting tile of the zombie
    :param screen: Is used to draw the sprite on the screen and to get the time elapsed between frames
    :param player: Player is used by the zombie to attack
    """

    def __init__(self, tile, screen: Screen, player: Player):
        self.screen = screen
        self.player = player

        # walking
        self.walk_timer = 0
        self.is_walking = False
        self.target_tile: Tile = None
        self.current_tile = tile
        self.pos = tile.get_center()

        self.attack_damage = 1

        # pathfiding
        self.path = []
        if Settings.SHOW_PATH_FINDING:
            self.highlighted_path = []
        self.a_star(self.player.current_tile, [])

        self.health = random.randint(0, 15)
        self.health += len(self.path)

        # sprites
        self.idle_sprite = [[
            pygame.image.load("Data/Sprites/Zombie/chort_idle_anim_f0.png").convert_alpha(),
            pygame.image.load("Data/Sprites/Zombie/chort_idle_anim_f1.png").convert_alpha(),
            pygame.image.load("Data/Sprites/Zombie/chort_idle_anim_f2.png").convert_alpha(),
            pygame.image.load("Data/Sprites/Zombie/chort_idle_anim_f3.png").convert_alpha()
        ], [
            pygame.image.load("Data/Sprites/Zombie/chort_idle_anim_left_f0.png").convert_alpha(),
            pygame.image.load("Data/Sprites/Zombie/chort_idle_anim_left_f1.png").convert_alpha(),
            pygame.image.load("Data/Sprites/Zombie/chort_idle_anim_left_f2.png").convert_alpha(),
            pygame.image.load("Data/Sprites/Zombie/chort_idle_anim_left_f3.png").convert_alpha()
        ]]
        self.run_sprite = [[
            pygame.image.load("Data/Sprites/Zombie/chort_run_anim_f0.png").convert_alpha(),
            pygame.image.load("Data/Sprites/Zombie/chort_run_anim_f1.png").convert_alpha(),
            pygame.image.load("Data/Sprites/Zombie/chort_run_anim_f2.png").convert_alpha(),
            pygame.image.load("Data/Sprites/Zombie/chort_run_anim_f3.png").convert_alpha()
        ], [
            pygame.image.load("Data/Sprites/Zombie/chort_run_anim_left_f0.png").convert_alpha(),
            pygame.image.load("Data/Sprites/Zombie/chort_run_anim_left_f1.png").convert_alpha(),
            pygame.image.load("Data/Sprites/Zombie/chort_run_anim_left_f2.png").convert_alpha(),
            pygame.image.load("Data/Sprites/Zombie/chort_run_anim_left_f3.png").convert_alpha()
        ]]
        self.image = self.idle_sprite[1][0]
        self.rect = self.image.get_rect()
        self.look_direction = 1
        self.frame = random.randint(0, 3)
        self.timer: float = 0.0

    def display(self):
        """
        Draw the zombie sprite on the screen
        """

        # decide which frame of the animation should be shown
        self.timer += self.screen.get_elapsed_time()
        if self.timer > 0.10:
            self.timer: float = 0.0
            if self.frame < 3:
                self.frame += 1
            else:
                self.frame = 0

        # decide witch animation should be shown, walking or idle
        if self.is_walking:
            self.image = self.run_sprite[self.look_direction][self.frame]
        else:
            self.image = self.idle_sprite[self.look_direction][self.frame]

        self.screen.get_screen().blit(self.image, (self.pos[0] - 8, self.pos[1] - 16))

    def update(self):
        """
        Update the walking of the zombie
        """
        if self.is_walking:  # walking
            factor = 1 - self.walk_timer / Settings.PLAYER_WALKING_TIME  # how far along the walk the enemy is
            walkspeed = lerp(self.current_tile.is_walkable(), self.target_tile.is_walkable(), factor)   # walk speed on the current journey
            self.walk_timer -= self.screen.get_elapsed_time() * walkspeed

            # if the walk animation is done, move the player
            if self.walk_timer <= 0:
                self.is_walking = False
                self.align_enemy(self.target_tile)
                self.look_player()  # updating look direction
            else:  # if the walk animation isn't yet completed
                self.pos = lerp_2D(self.current_tile.get_center(), self.target_tile.get_center(), factor)

    def update_tick(self, zombies_tiles: list):
        """
        The update tick is called once the player does an action
        :param zombies_tiles: a reference to the list of tiles that the zombies updated before him already occupy
        """
        # lower the healht, as zombies die over time
        self.health -= 1
        self.a_star(self.player.current_tile, zombies_tiles)
        if len(self.path) > 0:  # if there is a path to the player move one stap closer
            self.move_zombie(self.path.pop(0))

    def dead(self) -> bool:
        """ Returns if the zombie is dead or alive"""
        return self.health <= 0

    def align_enemy(self, tile: Tile):
        """ aligns the enemy on the given tile"""
        self.current_tile = tile
        self.pos = self.current_tile.get_center()

    def look_player(self):
        """ make the enemy look at the player by flipping it sprite"""
        if self.pos[0] > self.player.get_player_position()[0]:
            self.look_direction = 1
        else:
            self.look_direction = 0

    def a_star(self, target_tile: Tile, zombies_tiles: list):
        """
        A star path finding, it uses the distance to the target and the costs of moving to the next tile
        to find the optimal path

        :param target_tile: The target tile the enemy wishes to array, the tile of the player
        :param zombies_tiles: The reference to the list of tiles currently occupy by other zombies
        """

        # set the start node at the current tile
        start_node: Node = Node(self.current_tile, 0, None)
        # the frontier is the unvisited tiles that have been explored and is sorted by priority
        frontier = list()
        frontier.append(start_node)

        # list of nodes the a* has visited, used to find the path at the end
        nodes = dict()
        nodes[self.current_tile] = start_node

        # the cost so far dict is the keeps tracks of the cost of the current optimal route till that tile
        cost_so_far = dict()
        cost_so_far[self.current_tile] = 0

        # if the show path finding is enabled, unhighlight the old highlighted tiles
        if Settings.SHOW_PATH_FINDING:
            for tile in self.highlighted_path:
                tile.unhighlight()
            self.highlighted_path.clear()

        while len(frontier) > 0:
            # get the current node and corresponding tile
            current_node: Node = frontier.pop(0)
            current_tile: Tile = current_node.get_tile()

            # if it is the wanted tile, then the AI is done
            if current_tile == target_tile:
                break

            # get the neighboring tiles and shuffle them
            neighbours = current_tile.get_neighbours().copy()
            random.shuffle(neighbours)

            for next_tile in neighbours:
                # calculate (travel-dist) cost score g-score
                if next_tile.is_walkable() and next_tile not in zombies_tiles:  # tiles that take longer to traverse have a higher cost
                    new_cost = cost_so_far[current_tile] + (1 / next_tile.is_walkable()) * Settings.MOVEMENT_COST_MULTIPLIER
                elif next_tile.has_structure():  # walls take longer to break so the cost will be higher
                    new_cost = cost_so_far[current_tile] + Settings.WALL_BREAK_TIME * Settings.MOVEMENT_COST_MULTIPLIER  # temp
                else: # else the tile is not walkable so skip it
                    continue

                if next_tile not in cost_so_far or new_cost < cost_so_far[next_tile]:
                    # save the new cost and calculate the new priority
                    cost_so_far[next_tile] = new_cost
                    priority = new_cost + self.manhattan_distance(target_tile, next_tile)  # g-score + f-score

                    # create a new node and sort it in the frontier and nodes list
                    new_node: Node = Node(next_tile, -priority, current_tile)
                    bisect.insort(frontier, new_node)
                    nodes[next_tile] = new_node

                    # show the AI path when enabled
                    if Settings.SHOW_PATH_FINDING:
                        self.highlighted_path.append(next_tile)
                        next_tile.unhighlight()
                        next_tile.highlight((255, 255, 0, 100))
                        next_tile.show_score(int(-priority))

        # if the target hasn't been found, so the enemy is on a island, end the function
        if target_tile not in nodes.keys():
            return

        # turn the nodes list into a path
        current_tile = target_tile
        self.path.clear()
        node_path = []

        # loop through the entire nodes tree backwards and build the path
        while current_tile != self.current_tile:
            self.path.insert(0, current_tile)
            node_path.insert(0, nodes[current_tile])
            current_tile = nodes[current_tile].get_came_from()

        # append it's future location to the reference list so the zombies around it know and won't try to walk on the same tile
        if len(self.path) > 0 and self.path[0].is_walkable():
            zombies_tiles.append(self.path[0])
        else:
            zombies_tiles.append(self.current_tile)

        # show the AI path if enabled in Settings.py
        if Settings.SHOW_PATH_FINDING:
            for node in node_path:
                node.get_tile().unhighlight()
                node.get_tile().highlight((255, 0, 0, 100))
                node.get_tile().show_score(int(node.priority))

    def manhattan_distance(self, startTile, endTile):
        """
        calculates an approximate distance to the player
        :param startTile: the start tile, from.
        :param endTile:  the end tile, until.
        """
        # return abs(startTile.get_center()[0] - endTile.get_center()[0]) + abs(startTile.get_center()[1] - endTile.get_center()[1])
        return math.dist(startTile.get_center(), endTile.get_center())

    def move_zombie(self, targetTile: Tile):
        """Moves the zombie to the clicked tile (if valid move)"""
        if targetTile.is_wall: # if the next move is through a wall, attack the wall
            targetTile.attack_wall(self.attack_damage)
        # if the next move is the player, attack the player
        elif self.player.current_tile == targetTile or self.player.current_tile == self.current_tile or self.player.target_tile == targetTile:
            self.player.attack_player(self.attack_damage)
        # if the next move is walkable tile, walk there
        elif targetTile.is_walkable():
            self.target_tile = targetTile
            self.is_walking = True
            self.walk_timer = Settings.PLAYER_WALKING_TIME

    def get_next_tile(self):
        """ get the tile the zombie will be on in the next turn"""
        next_tile: Tile
        if len(self.path) > 0:
            next_tile = self.path[0]
        else:
            next_tile = self.current_tile

        if not next_tile.is_walkable:
            return self.current_tile
        return next_tile


class Node:
    """
    The node class, this class is used in the A* to bind a tile and priority together so they can be sorted
    :param tile: the tile bound to this node
    :param priority: the priority of the tile
    :param came_from: the tile that is before this tile on the path
    """
    def __init__(self, tile: Tile, priority, came_from):
        self.tile = tile
        self.priority = priority
        self.came_from = came_from

    # sorts the nodes based on priority
    def __lt__(self, other):
        return self.priority > other.priority

    def get_tile(self) -> Tile:
        return self.tile

    def get_came_from(self) -> Tile:
        return self.came_from
