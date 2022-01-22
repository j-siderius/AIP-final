import pygame


class Gamecontroller:
	def __init__(self, screen, serial, timescale=12):
		"""
		The gamecontroller manages miscellaneous functions like keeping track of time and the day/night cycle
		:param screen: pygame screen obj to blit to
		:param timescale: how quickly or slowly time progresses in the game (e.g. timescale=12 -> day lasts 12 ticks)
		"""
		self.screen = screen
		self.screen_size = self.screen.get_size()
		self.serial = serial

		self.game_time = 0
		self.day_night_time = 1  # always start game at beginning of day
		self.timescale = int(timescale)
		if self.timescale < 12:
			self.timescale = 12
		self.start_night = int(self.timescale / 2) - 1

		self.sky_color = (0, 0, 0)
		self.sky_opacity = 0
		self.sky = pygame.Surface(self.screen.get_size())

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

		# TODO: add zombie update function here

	def update_day_night(self):
		"""Manages the day/night cycle and sky color and opacity"""

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

		self.serial.updateDayNight(int((self.day_night_time / self.timescale) * 11))

	def update_sky(self):
		"""draw sky over the screen"""

		self.sky.fill(self.sky_color)
		self.sky.set_alpha(self.sky_opacity)
		# blit overlay over whole screen
		self.screen.get_screen().blit(self.sky, (0, 0))
		# TODO: enable blit when water tiles are fixed
