import pygame
from Screen import Screen
from Field import Field
import time


class program:

    def __init__(self):
        # self.screen = Screen(584, 592, self.loop, title="Test Terrain")
        self.screen = Screen(0, 0, self.loop, title="Test Terrain")

        self.field = Field(self.screen, field_pos=(0, 0), hex_width=4*12, field_size=(self.screen.get_size()), hex_amount=(80, 0))

        self.screen.start()

    def loop(self):
        self.screen.background(139, 69, 19)
        self.field.display(self.screen)


if __name__ == '__main__':
    program()
