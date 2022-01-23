import bisect
import math
import random
from queue import PriorityQueue

import Tile


# TODO enemy can spawn on mountains

class Zombie:

    def __init__(self, pos, screen, field):
        self.field = field
        self.pos = pos
        self.screen = screen
        self.color = (0, 0, 255)
        self.radius = self.field.hex_size / 2.3  # base this on hex_size of Tiles

        self.current_tile = None
        self.align_enemy(self.pos)

    def display(self):
        self.screen.stroke_size(0)
        self.screen.stroke(self.color)
        self.screen.circle(self.pos[0], self.pos[1], self.radius, self.color)

    def update(self):
        pass

    def align_enemy(self, point):
        self.current_tile = self.field.get_tile_from_point(point)
        self.pos = self.current_tile.get_center()

    def a_star_test(self, target_tile):
        frontier = PriorityQueue()
        frontier.put(self.current_tile)
        came_from = dict()
        cost_so_far = dict()
        came_from[self.current_tile] = None
        cost_so_far[self.current_tile] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == target_tile:
                break

            neighbours = current.get_neighbours()
            random.shuffle(neighbours)

            for next_tile in neighbours:
                # calculate (travel-dist) cost score g-score
                if next_tile.is_walkable():
                    new_cost = cost_so_far[current] + (1 / next_tile.is_walkable()) * 2
                elif next_tile.has_structure():
                    new_cost = cost_so_far[current] + 10  # temp
                else:
                    continue

                if next_tile not in cost_so_far or new_cost < cost_so_far[next_tile]:
                    next_tile.highlight((255, 255, 0, 50))
                    cost_so_far[next_tile] = new_cost
                    priority = new_cost + self.manhattan_distance(target_tile, next_tile)  # g-score + f-score
                    frontier.put(next_tile, priority)
                    came_from[next_tile] = current

        # print(f"{came_from = }, {cost_so_far[target_tile]}")

        if target_tile not in came_from.keys():
            return

        current = target_tile
        path = []
        while current != self.current_tile:
            path.insert(0, current)
            current = came_from[current]

        # print(f"{path}")

        for tile in path:
            tile.highlight((255, 0, 0, 50))

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
                    next_tile.highlight((255, 255, 0, 50))
                    cost_so_far[next_tile] = new_cost
                    priority = new_cost + self.manhattan_distance(target_tile, next_tile)  # g-score + f-score
                    bisect.insort(frontier, Node(next_tile, -priority))
                    came_from[next_tile] = current_tile

        if target_tile in cost_so_far:
            print(f"{came_from = }, {cost_so_far[target_tile]}")

        if target_tile not in came_from.keys():
            return

        current_tile = target_tile
        path = []
        while current_tile != self.current_tile:
            path.insert(0, current_tile)
            current_tile = came_from[current_tile]

        # print(f"{path}")

        for tile in path:
            tile.highlight((255, 0, 0, 50))

    def manhattan_distance(self, startTile, endTile):
        return abs(startTile.get_center()[0] - endTile.get_center()[0]) + abs(startTile.get_center()[1] - endTile.get_center()[1])
        # return math.dist(startTile.get_center(), endTile.get_center())


class Node:
    def __init__(self, tile: Tile, priority):
        self.tile = tile
        self.priority = priority

    def __lt__(self, other):
        return self.priority > other.priority

    def get_tile(self) -> Tile:
        return self.tile
