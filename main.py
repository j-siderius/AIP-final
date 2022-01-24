import pygame

from Data.settings import MouseButton
from Zombie import Zombie
from Screen import Screen
from Field import Field
from Player import Player
from Serial import Serial
from Input import Input
from Gamecontroller import Gamecontroller


class Program:

    def __init__(self):
        self.screen = Screen(0, 0, self.loop, title="HexZomb", mouse_pressed_func=self.mouse_pressed, mouse_moved_func=self.mouse_moved, fps_func=self.print_avg_fps, key_pressed_func=self.key_pressed)

        self.field = Field(self.screen, hex_width=4 * 11, field_size=(self.screen.get_size()))
        self.player = Player(self.screen, field_size=(self.screen.get_size()), field=self.field, time_ticker_func=self.tick_timer)
        self.serial = Serial('COM3', controller_moved_func=self.controller_moved, controller_pressed_func=self.controller_pressed)  # COM14 is PC, /dev/cu.wchusbserial1410 is MAC # and com3 voor Frank
        self.input = Input(self.player)
        self.zombies = []
        self.controller = Gamecontroller(self.screen, self.serial, self.zombies, zombie_death_func=self.zombie_death)

        self.fps = []

        self.screen.set_serial_func(self.serial.update)
        self.screen.start()

    def loop(self):
        self.field.render(self.screen)
        self.player.update()
        self.player.display()

        for zombie in self.zombies:
            zombie.update()
            zombie.display()

        # fps counter
        self.screen.toggle_stroke(False)
        self.screen.rect(5, 5, 100, 20, (255))
        self.screen.text_font(20)
        self.screen.text_color(0)
        self.screen.text(5, 5, f"{self.screen.get_frameRate():.2f}", False)
        self.fps.append(self.screen.get_frameRate())

        self.controller.update_sky()

    def mouse_moved(self):
        self.input.process_mouse_movement(self.screen.get_mouse_pos())

    def mouse_pressed(self, button):
        self.input.process_mouse_button(button)
        if button == MouseButton.scroll:
            self.zombies.append(Zombie(self.screen.get_mouse_pos(), self.screen, self.field, self.player, []))
            # self.zombies[len(self.zombies) - 1].a_star(self.player.current_tile)

    def controller_moved(self, position):
        self.input.process_nunchuck_movement(position)

    def controller_pressed(self, buttons):
        self.input.process_nunchuck_button(buttons)

    def tick_timer(self):
        self.controller.tick()

    def zombie_death(self, zombie):
        self.zombies.remove(zombie)

    def print_avg_fps(self):
        print(f"average fps={sum(self.fps)/len(self.fps)}")
        print(f"lowest fps={min(self.fps)}")

    # for testing without mouse
    def key_pressed(self, keys):
        self.zombies.append(Zombie(self.screen.get_mouse_pos(), self.screen, self.field, self.player, []))


if __name__ == '__main__':
    Program()
