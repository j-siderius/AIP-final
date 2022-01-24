import bisect
import math
import random
from queue import PriorityQueue
import Tile
from Data.settings import Settings


# TODO enemy can spawn on mountains
from Screen import lerp, lerp_2D


class Zombie:

    def __init__(self, pos, screen, field, player):
        self.field = field
        self.pos = pos
        self.screen = screen
        self.color = (0, 0, 255)
        self.radius = self.field.hex_size / 2.3  # base this on hex_size of Tiles

        # walking
        self.walk_timer = 0
        self.is_walking = False
        self.target_tile: Tile = None

        self.current_tile = self.field.get_tile_from_point(pos)  # TODO change tho start tile
        self.path = []
        self.align_enemy(self.current_tile)

        self.player = player
        self.a_star(self.player.current_tile)

        self.health = random.randint(0, 15)
        print(len(self.path))
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

    def update_tick(self):
        self.health -= 1
        self.a_star(self.player.current_tile)
        if len(self.path) > 0:
            self.move_zombie(self.path.pop(0))

    def dead(self) -> bool:
        return self.health <= 0

    def align_enemy(self, point):
        self.current_tile = self.field.get_tile_from_point(point)
        self.pos = self.current_tile.get_center()

    def a_star(self, target_tile):
        frontier = list()
        frontier.append(Node(self.current_tile, 0))  # self.current_tile)
        came_from = dict()
        cost_so_far = dict()
        came_from[self.current_tile] = None
        cost_so_far[self.current_tile] = 0

        while len(frontier) > 0:
            current_node: Node = frontier.pop(0)
            current_tile: Tile = current_node.get_tile()
            print(current_node)

            if current_tile == target_tile:
                break

            neighbours = current_tile.get_neighbours()
            random.shuffle(neighbours)

            for next_tile in neighbours:
                # calculate (travel-dist) cost score g-score
                if next_tile.is_walkable():
                    new_cost = cost_so_far[current_tile] + (1 / next_tile.is_walkable()) * 2
                elif next_tile.has_structure():
                    new_cost = cost_so_far[current_tile] + 10  # temp
                else:
                    continue

                if next_tile not in cost_so_far or new_cost < cost_so_far[next_tile]:
                    # next_tile.highlight((255, 255, 0, 50))
                    cost_so_far[next_tile] = new_cost
                    priority = new_cost + self.manhattan_distance(target_tile, next_tile)  # g-score + f-score
                    bisect.insort(frontier, Node(next_tile, -priority))
                    came_from[next_tile] = current_tile

        if target_tile in cost_so_far:
            print(f"{came_from = }, {cost_so_far[target_tile]}")

        if target_tile not in came_from.keys():
            return

        current_tile = target_tile
        self.path = []
        while current_tile != self.current_tile:
            self.path.insert(0, current_tile)
            current_tile = came_from[current_tile]

        # for tile in self.path:
        #     tile.highlight((255, 0, 0, 50))

    def manhattan_distance(self, startTile, endTile):
        return abs(startTile.get_center()[0] - endTile.get_center()[0]) + abs(startTile.get_center()[1] - endTile.get_center()[1])
        # return math.dist(startTile.get_center(), endTile.get_center())

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


class Node:
    def __init__(self, tile: Tile, priority):
        self.tile = tile
        self.priority = priority

    def __lt__(self, other):
        return self.priority > other.priority

    def get_tile(self) -> Tile:
        return self.tile
