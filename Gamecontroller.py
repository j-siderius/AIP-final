import math
import random

import pygame

from Data.settings import Settings
from Field import Field
from Player import Player
from Screen import Screen
from Zombie import Zombie


class Gamecontroller:
	def __init__(self, screen: Screen, serial, zombies, zombie_death_func, field: Field, player: Player, timescale=12):
		"""
		The gamecontroller manages miscellaneous functions like keeping track of time and the day/night cycle
		:param screen: pygame screen obj to blit to
		:param timescale: how quickly or slowly time progresses in the game (e.g. timescale=12 -> day lasts 12 ticks)
		"""
		self.player = player
		self.screen = screen
		self.screen_size = self.screen.get_size()
		self.serial = serial
		self.field = field

		self.game_time = 0
		self.day_night_time = 0  # always start game at beginning of day
		self.timescale = int(timescale)
		if self.timescale < 12:
			self.timescale = 12
		self.start_night = int(self.timescale / 2) - 1

		self.sky_color = (0, 0, 0)
		self.sky_opacity = 0
		self.sky = pygame.Surface(self.screen.get_size())

		self.zombies = zombies
		# self.zombies_tiles = [zombie.current_tile for zombie in self.zombies]
		self.zombies_tiles = [zombie.get_next_tile() for zombie in self.zombies]
		# self.zombies_tiles = list()
		self.zombie_death_func = zombie_death_func

	def tick(self):
		"""
		Call this function to forward the time one tick (e.g. when player moved or did an action)
		"""
		self.game_time += 1
		if self.day_night_time >= self.timescale - 1:
			self.day_night_time = 0  # reset daytime
		else:
			self.day_night_time += 1  # increment time
		self.update_day_night()

		self.zombies_tiles = []
		for zombie in self.zombies:
			if zombie.dead() is not True:
				# pass the zombies the reference to the list so they create a shared list of where they are, making them not walk on top of each other
				zombie.update_tick(self.zombies_tiles)
			else:
				self.zombie_death_func(zombie)


	def update_day_night(self):
		"""Manages the day/night cycle and sky color and opacity as well as zombie spawning"""

		if self.day_night_time < (1/12) * self.timescale:
			self.sky_opacity = 50
		elif (5 / 12) * self.timescale > self.day_night_time >= (1 / 12) * self.timescale:
			self.sky_opacity = 0
		elif (6 / 12) * self.timescale > self.day_night_time >= (5 / 12) * self.timescale:
			self.sky_opacity = 50
		elif (7 / 12) * self.timescale > self.day_night_time >= (6 / 12) * self.timescale:
			self.sky_opacity = 75
		elif (11 / 12) * self.timescale > self.day_night_time >= (7 / 12) * self.timescale:
			self.sky_opacity = 100
		elif self.day_night_time >= (11 / 12) * self.timescale:
			self.sky_opacity = 75

		if (9 / 12) * self.timescale > self.day_night_time >= (6 / 12) * self.timescale:
			# TODO: add zombie spawning function here
			tile_list = self.field.get_land_tiles()
			for i in range(5):
				tile = tile_list[random.randint(0, len(tile_list))]
				if Settings.MIN_SPAWN_DISTANCE < math.dist(self.player.get_player_position(), tile.get_center()) < Settings.MAX_SPAWN_DISTANCE and tile.is_walkable():
					self.zombies.append(Zombie(tile, self.screen, self.field, self.player, []))
					break

		self.serial.updateDayNight(int((self.day_night_time / self.timescale) * 11))

	def update_sky(self):
		"""draw sky over the screen"""

		self.sky.fill(self.sky_color)
		self.sky.set_alpha(self.sky_opacity)
		# blit overlay over whole screen
		self.screen.get_screen().blit(self.sky, (0, 0))
