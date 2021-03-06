import math
import random

import pygame

from Data.Settings import Settings
from Field import Field
from Player import Player
from Screen import Screen
from Zombie import Zombie


class Gamecontroller:
	def __init__(self, screen: Screen, serial, game_end_func, zombies, zombie_death_func, field: Field, player: Player, timescale: int = 12, game_duration: int = 4):
		"""
		The gamecontroller manages miscellaneous functions like keeping track of time and the day/night cycle
		:param screen: pygame screen obj to blit to
		:param serial: serial object, so we can pass time updates to the LEDs
		:param game_end_func: we call this when the time is up / you are 'rescued'
		:param zombies: zombies array so we can update all of them when a tick occurs
		:param zombie_death_func: if a zombie is older than its lifespan, we can delete it from the array with this function
		:param field: to access and interface the tiles
		:param player: to spawn the zombies in a radius around the player
		:param timescale: how quickly or slowly time progresses in the game (e.g. timescale=12 -> day lasts 12 ticks)
		:param game_duration: how long the game lasts (e.g. game_duration=4 -> game lasts 4 days)
		"""
		# save the references to the objects as class members
		self.player = player
		self.screen = screen
		self.screen_size = self.screen.get_size()
		self.serial = serial
		self.field = field

		# counter variables
		self.game_time = 0
		self.game_day = 0
		self.day_night_time = 0  # always start game at beginning of day
		self.timescale = timescale

		self.game_duration = game_duration
		self.start_night = int(self.timescale / 2) - 1

		# assign external functions
		self.game_end_func = game_end_func

		# variables for skybox
		self.sky_color = (0, 0, 0)
		self.sky_opacity = 0
		self.sky = pygame.Surface(self.screen.get_size())

		self.zombies = zombies
		self.zombies_tiles = list()
		self.zombie_death_func = zombie_death_func

	def tick(self):
		"""
		Call this function to forward the time one tick (e.g. when player moved or did an action)
		"""
		self.game_time += 1
		if self.day_night_time >= self.timescale - 1:
			self.day_night_time = 0  # reset daytime
			self.game_day += 1
		else:
			self.day_night_time += 1  # increment time
		self.update_day_night()

		# check if game is done
		if self.game_day >= self.game_duration:
			self.game_end_func()

		# update the zombies
		self.zombies_tiles = []
		for zombie in self.zombies:
			if zombie.dead() is not True:
				# pass the zombies the reference to the list so they create a shared list of where they are, making them not walk on top of each other
				zombie.update_tick(self.zombies_tiles)
			else:
				self.zombie_death_func(zombie)

	def update_day_night(self):
		"""Manages the day/night cycle and sky color and opacity as well as zombie spawning"""

		if (5 / 12) * self.timescale > self.day_night_time:
			self.sky_opacity = 0
		elif (6 / 12) * self.timescale > self.day_night_time >= (5 / 12) * self.timescale:
			self.sky_opacity = 50
		elif (7 / 12) * self.timescale > self.day_night_time >= (6 / 12) * self.timescale:
			self.sky_opacity = 75
		elif (11 / 12) * self.timescale > self.day_night_time >= (7 / 12) * self.timescale:
			self.sky_opacity = 100
		elif self.day_night_time >= (11 / 12) * self.timescale:
			self.sky_opacity = 75

		# spawn zombies
		if (9 / 12) * self.timescale > self.day_night_time >= (6 / 12) * self.timescale:
			tile_list = self.field.get_land_tiles()
			for i in range(Settings.SPAWN_TRY_AMOUNT[self.game_day]):
				tile = tile_list[random.randint(0, len(tile_list)-1)]
				if Settings.MIN_SPAWN_DISTANCE < math.dist(self.player.get_player_position(), tile.get_center()) < Settings.MAX_SPAWN_DISTANCE and tile.is_walkable():
					self.zombies.append(Zombie(tile, self.screen, self.player))

		# send the new day/night-time to the LEDs
		self.serial.updateDayNight(int(self.day_night_time/(self.timescale / 12)))

	def update_sky(self):
		"""draw sky over the screen"""
		# change opacity so night gradually fades in
		self.sky.fill(self.sky_color)
		self.sky.set_alpha(self.sky_opacity)
		# blit overlay over whole screen
		self.screen.get_screen().blit(self.sky, (0, 0))

	def get_timescale(self) -> (int, int):
		return self.timescale, self.game_duration

	def get_score(self) -> int:
		return self.game_time
