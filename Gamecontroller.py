import pygame


class Gamecontroller:
	def __init__(self, screen, serial, game_end_func, timescale: int = 12, game_duration: int = 4):
		"""
		The gamecontroller manages miscellaneous functions like keeping track of time and the day/night cycle
		:param screen: pygame screen obj to blit to
		:param timescale: how quickly or slowly time progresses in the game (e.g. timescale=12 -> day lasts 12 ticks)
		:param game_duration: how long the game lasts (e.g. game_duration=4 -> game lasts 4 days)
		"""
		# make local variables for all objects
		self.screen = screen
		self.screen_size = self.screen.get_size()
		self.serial = serial

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

		# TODO: add zombie update function here

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

		#
		if (9 / 12) * self.timescale > self.day_night_time >= (6 / 12) * self.timescale:
			# TODO: add zombie spawning function here
			pass

		self.serial.updateDayNight(self.day_night_time)

	def update_sky(self):
		"""draw sky over the screen"""
		# change opacity so night gradually fades in
		self.sky.fill(self.sky_color)
		self.sky.set_alpha(self.sky_opacity)
		# blit overlay over whole screen
		self.screen.get_screen().blit(self.sky, (0, 0))

	def get_timescale(self) -> (int, int):
		"""returns timescale and game_duration"""
		return self.timescale, self.game_duration
