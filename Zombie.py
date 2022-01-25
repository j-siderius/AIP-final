import bisect
import math
import random
from queue import PriorityQueue
import Tile
from Data.settings import Settings

from Field import Field
from Player import Player
from Screen import lerp, lerp_2D, Screen


class Zombie:

    def __init__(self, tile, screen: Screen, field: Field, player: Player, zombies_tiles: list):
        self.field = field
        # self.pos = pos
        self.screen = screen
        self.color = (0, 0, 255)
        self.radius = self.field.hex_size / 2.3  # base this on hex_size of Tiles

        # walking
        self.walk_timer = 0
        self.is_walking = False
        self.target_tile: Tile = None

        # self.current_tile = self.field.get_tile_from_point(pos)  # TODO change tho start tile
        self.current_tile = tile
        self.pos = tile.get_center()

        self.path = []
        self.align_enemy(self.current_tile)

        self.player = player
        self.a_star(self.player.current_tile, zombies_tiles)

        self.health = random.randint(0, 15)
        self.health += len(self.path)

    def display(self):
        self.screen.stroke_size(0)
        self.screen.stroke(self.color)
        self.screen.circle(self.pos[0], self.pos[1], self.radius, self.color)

    def update(self):
        if self.is_walking:  # walking
            factor = 1 - self.walk_timer / Settings.PLAYER_WALKING_TIME
            walkspeed = lerp(self.current_tile.is_walkable(), self.target_tile.is_walkable(), factor)
            self.walk_timer -= self.screen.get_elapsed_time() * walkspeed
            if self.walk_timer <= 0:
                self.is_walking = False
                self.align_enemy(self.target_tile)
            else:
                self.pos = lerp_2D(self.current_tile.get_center(), self.target_tile.get_center(), factor)

    def update_tick(self, zombies_tiles: list):
        self.health -= 1
        self.a_star(self.player.current_tile, zombies_tiles)
        if len(self.path) > 0:
            self.move_zombie(self.path.pop(0))

    def dead(self) -> bool:
        return self.health <= 0

    def align_enemy(self, tile: Tile):
        self.current_tile = tile
        self.pos = self.current_tile.get_center()

    def a_star(self, target_tile: Tile, zombies_tiles: list):
        start_node: Node = Node(self.current_tile, 0, None)

        frontier = list()
        frontier.append(start_node)
        nodes = dict()
        nodes[self.current_tile] = start_node
        cost_so_far = dict()
        cost_so_far[self.current_tile] = 0

        while len(frontier) > 0:
            current_node: Node = frontier.pop(0)
            current_tile: Tile = current_node.get_tile()

            if current_tile == target_tile:
                break

            neighbours = current_tile.get_neighbours().copy()
            random.shuffle(neighbours)

            for next_tile in neighbours:
                # calculate (travel-dist) cost score g-score
                if next_tile.is_walkable() and next_tile not in zombies_tiles:
                    new_cost = cost_so_far[current_tile] + (1 / next_tile.is_walkable()) * Settings.MOVEMENT_COST_MULTIPLIER
                elif next_tile.has_structure():
                    new_cost = cost_so_far[current_tile] + Settings.WALL_BREAK_TIME * Settings.MOVEMENT_COST_MULTIPLIER  # temp
                else:
                    continue

                if next_tile not in cost_so_far or new_cost < cost_so_far[next_tile]:
                    cost_so_far[next_tile] = new_cost
                    priority = new_cost + self.manhattan_distance(target_tile, next_tile)  # g-score + f-score
                    new_node: Node = Node(next_tile, -priority, current_tile)
                    bisect.insort(frontier, new_node)
                    nodes[next_tile] = new_node

                    # show the AI path
                    # next_tile.unhighlight()
                    # next_tile.highlight((255, 255, 0, 100))
                    # next_tile.show_score(int(-priority))

        if target_tile not in nodes.keys():
            return

        current_tile = target_tile
        self.path.clear()
        node_path = []
        while current_tile != self.current_tile:
            self.path.insert(0, current_tile)
            node_path.insert(0, nodes[current_tile])
            current_tile = nodes[current_tile].get_came_from()

        if len(self.path) > 0 and self.path[0].is_walkable():
            zombies_tiles.append(self.path[0])
        else:
            print("hoi")
            zombies_tiles.append(self.current_tile)

        # debugging and showing the AI path
        # for node in node_path:
        #     node.get_tile().unhighlight()
        #     node.get_tile().highlight((255, 0, 0, 100))
        #     node.get_tile().show_score(int(node.priority))

    def manhattan_distance(self, startTile, endTile):
        # return abs(startTile.get_center()[0] - endTile.get_center()[0]) + abs(startTile.get_center()[1] - endTile.get_center()[1])
        return math.dist(startTile.get_center(), endTile.get_center())

    def move_zombie(self, targetTile):
        """Moves the player to the clicked tile (if valid move)"""
        if targetTile.is_wall:
            # TODO: damage wall
            pass
        elif self.player.current_tile == targetTile:
            # TODO: subtract -1 health from player
            pass
        elif targetTile.is_walkable():
            self.target_tile = targetTile
            self.is_walking = True
            self.walk_timer = Settings.PLAYER_WALKING_TIME

    def get_next_tile(self):
        next_tile: Tile
        if len(self.path) > 0:
            next_tile = self.path[0]
        else:
            next_tile = self.current_tile

        if not next_tile.is_walkable:
            return self.current_tile
        return next_tile


class Node:
    def __init__(self, tile: Tile, priority, came_from):
        self.tile = tile
        self.priority = priority
        self.came_from = came_from

    def __lt__(self, other):
        return self.priority > other.priority

    def get_tile(self) -> Tile:
        return self.tile

    def get_came_from(self) -> Tile:
        return self.came_from
