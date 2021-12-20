import pygame
from Screen import Screen
from Field import Field
import time

class program:

    def __init__(self):
        # self.screen = Screen(584, 592, self.loop, title="Test Terrain")
        self.screen = Screen(0, 0, self.loop, title="Test Terrain")

        self.field = Field(self.screen, field_pos=(0, 0), hex_width=4*16, field_size=(self.screen.get_size()))

        self.screen.start()

    def loop(self):
        # self.screen.background(0)
        self.field.display(self.screen)

        self.screen.toggle_stroke(False)
        self.screen.rect(5,5,100,20,(255))
        self.screen.text_font(20)
        self.screen.text_color(0)
        self.screen.text(5, 5, f"{self.screen.get_frameRate():.2f}", False)


if __name__ == '__main__':
    program()
