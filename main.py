import pygame
from Screen import Screen
from Field import Field
from Player import Player
from Serial import Serial
import time
from Input import Input


class program:

    def __init__(self):
        # self.screen = Screen(584, 592, self.loop, title="Test Terrain")
        self.screen = Screen(0, 0, self.loop, title="Test Terrain", mouse_pressed_func=self.mouse_pressed, mouse_moved_func=self.mouse_moved)

        self.field = Field(self.screen, hex_width=4 * 11, field_size=(self.screen.get_size()))
        self.player = Player(self.screen, field_size=(self.screen.get_size()), field=self.field)  # need to implement hex calculation in class
        self.serial = Serial('COM14', controller_moved_func=self.controller_moved, controller_pressed_func=self.controller_pressed)  # COM14 is PC, /dev/cu.wchusbserial1410 is MAC
        self.input = Input(self.player)

        self.screen.start()

    def loop(self):
        self.field.display(self.screen)
        self.player.update()
        self.player.display()
        self.serial.update()

        self.screen.toggle_stroke(False)
        self.screen.rect(5, 5, 100, 20, (255))
        self.screen.text_font(20)
        self.screen.text_color(0)
        self.screen.text(5, 5, f"{self.screen.get_frameRate():.2f}", False)

    def mouse_moved(self):
        self.input.process_mouse_movement(self.screen.get_mouse_pos())

    def mouse_pressed(self, button):
        self.input.process_mouse_button(button)

    def controller_moved(self, position):
        self.input.process_nunchuck_movement(position)

    def controller_pressed(self, buttons):
        self.input.process_nunchuck_button(buttons)


if __name__ == '__main__':
    program()
