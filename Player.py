import random

class Player:

    def __init__(self, screen, field_size, field, hex_amount):
        self.screen = screen
        self.field = field

        self.screen_size = field_size

        # assign starting position to a viable tile
        self.find_starting_tile(int(hex_amount[0]/2), int(hex_amount[1]/2))

        self.radius = (field_size[0] / hex_amount[0]) / 2.3  # base this on hex_size of Tiles

        self.color = (255, 0, 0)

    def display(self):
        # stroke is globally enabled in the Screen class, maybe make it disablable per draw :)
        # TODO: see if stroke can be individually disabled
        self.screen.circle(self.x, self.y, self.radius, self.color)

    def update_player(self):
        pass

    def player_input(self, keyPresses):
        pass

    def move_player(self):
        pass

    # employ walking algorithm to find suitable starting tile
    def find_starting_tile(self, tileX, tileY):
        tile = self.field.get_tile(tileX, tileY)
        if tile.is_walkable() != 1:
            # TODO: implement marching algorithm / queued list search
            try_tile = tile.bordering_tiles[random.randint(0, len(tile.bordering_tiles)-1)]
            self.find_starting_tile(try_tile.x, try_tile.y)
        else:
            # assign player position to the found grass tile
            print(f"Starting tile found: ({tileX},{tileY})")
            print(tile.is_walkable())
            hex_size = self.field.get_hex_size()
            # TODO: fix spacing / placement of player
            self.x = (tileX * hex_size)
            self.y = (tileY * hex_size)
