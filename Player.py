import random
from Field import Field
import helper


class Player:

    def __init__(self, screen, field_size, field: Field):
        self.screen = screen
        self.field = field
        hex_amount = field.field_size

        self.field_size = field_size

        self.x, self.y = None, None
        self.xPos, self.yPos = 0, 0
        self.radius = self.field.hex_size / 2.3  # base this on hex_size of Tiles
        # assign starting position to a viable tile
        self.find_starting_tile(int(hex_amount[0] / 2), int(hex_amount[1] / 2))
        print(f"{hex_amount[0]/2 = } {hex_amount[1]/2 = }")

        self.color = (255, 0, 0)

    def display(self):
        self.screen.stroke_size(0)
        self.screen.stroke(self.color)
        self.screen.circle(self.x, self.y, self.radius, self.color)

    def update(self):
        self.player_input(self.screen.get_mouse_pos(), self.screen.get_mouse_pressed(), self.screen.get_pressed_keys())
        pass

    def player_input(self, mousePos, mousePressed, keyPresses):
        if mousePressed[0]:
            pressedTile = self.field.get_current_mouse_tile()
            self.move_player(pressedTile.x, pressedTile.y)

    def move_player(self, targetTileX, targetTileY):
        neighbours = self.field.get_tile(self.xPos, self.yPos).bordering_tiles
        for neighbour in neighbours:
            if (neighbour.x, neighbour.y) == (targetTileX, targetTileY) and self.field.get_tile(targetTileX, targetTileY).walkable:
                # TODO: implement tick rate with something like nextTile = this.tile
                self.align_player(targetTileX, targetTileY)

    # employ walking algorithm to find suitable starting tile
    def find_starting_tile(self, tileX, tileY):
        tile = self.field.get_tile(tileX, tileY)
        if tile.is_walkable() != 1:
            try_tile = tile.bordering_tiles[random.randint(0, len(tile.bordering_tiles) - 1)]
            self.find_starting_tile(try_tile.x, try_tile.y)
        else:
            # assign player position to the found grass tile
            print(f"Starting tile found: ({tileX},{tileY})")
            hex_size = self.field.get_hex_size()
            self.align_player(tileX, tileY)

    def align_player(self, x, y):
        # points are arranged in the following manner: [0]=bottom-right, [1]=bottom-left, [2]=middle-left,
        # [3]=top-left, [4]=top-right, [5]=middle-right
        self.xPos = x
        self.yPos = y
        self.x, self.y = self.field.get_tile(x,y).get_center()
        # self.x = self.field.get_tile(x, y).get_points()[4][0] - (self.field.get_hex_width() / 3)
        # self.y = self.field.get_tile(x, y).get_points()[2][1]
