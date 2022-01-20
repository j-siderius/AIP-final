import pygame
from Screen import Screen
from Field import Field
from Player import Player
import time


class program:

    def __init__(self):
        # self.screen = Screen(584, 592, self.loop, title="Test Terrain")
        self.screen = Screen(0, 0, self.loop, title="Test Terrain", mouse_pressed_func=self.mouse_pressed)

        self.field = Field(self.screen, hex_width=4 * 11, field_size=(self.screen.get_size()))
        self.player = Player(self.screen, field_size=(self.screen.get_size()), field=self.field)  # need to implement hex calculation in class

        self.screen.start()

    def loop(self):
        self.field.display(self.screen)
        self.player.update()
        self.player.display()

        self.screen.toggle_stroke(False)
        self.screen.rect(5, 5, 100, 20, (255))
        self.screen.text_font(20)
        self.screen.text_color(0)
        self.screen.text(5, 5, f"{self.screen.get_frameRate():.2f}", False)

    def mouse_pressed(self, button):
        self.player.mouse_pressed(self.screen.get_mouse_pos(), button)


if __name__ == '__main__':
    program()
