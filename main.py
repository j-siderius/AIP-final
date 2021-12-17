import pygame
from Screen import Screen
from Field import Field
import time


class program:

    def __init__(self):
        # self.screen = Screen(584, 592, self.loop, title="Test Terrain")
        self.screen = Screen(0, 0, self.loop, title="Test Terrain")

        self.field = Field(self.screen, field_pos=(0, 0), hex_width='auto', field_size=(self.screen.get_size()), hex_amount=(75, 0))

        self.screen.start()

    def loop(self):
        self.screen.background(139, 69, 19)
        self.field.display()


if __name__ == '__main__':
    program()
