import pygame

from Data.TilesData import Resources
from Screen import Screen


class Overlay:
    def __init__(self, screen: Screen, controller, player):
        """
        The overlay class manages the tutorial overlay, the end screen and the inventory and health UI
        :param screen: main screen class so we can render stuff on screen
        :param controller: controller class so we can get the timescale of the game
        """
        self.screen: Screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()[0], self.screen.get_size()[1]
        self.player = player

        self.start = True
        self.end = False

        # the place relative place on the screen the continue text is
        self.continue_height_scale = 3.34

        self.score: int = -1
        self.timescale, self.game_duration = controller.get_timescale()

        # initializing all screen images and resizing them to fit screen
        self.won_screen = pygame.image.load("Data/Images/won.png").convert_alpha()
        self.won_screen, self.won_rect = self.scale_image(self.won_screen)

        self.lost_screen = pygame.image.load("Data/Images/lost.png").convert_alpha()
        self.lost_screen, self.lost_rect = self.scale_image(self.lost_screen)

        self.tut0 = pygame.image.load("Data/Images/tutorial0.png").convert_alpha()
        self.tut0, self.tut0_rect = self.scale_image(self.tut0)

        self.tut1 = pygame.image.load("Data/Images/tutorial1.png").convert_alpha()
        self.tut1, self.tut1_rect = self.scale_image(self.tut1)

        self.tut2 = pygame.image.load("Data/Images/tutorial2.png").convert_alpha()
        self.tut2, self.tut2_rect = self.scale_image(self.tut2)

        self.tut3 = pygame.image.load("Data/Images/tutorial3.png").convert_alpha()
        self.tut3, self.tut3_rect = self.scale_image(self.tut3)

        self.tutorial_slide = 0

        # initialize UI sprites
        self.heart_full = pygame.image.load("Data/Sprites/UI/ui_heart_full.png").convert_alpha()
        self.heart_full, temp = self.scale_image(self.heart_full, int(self.screen_width * 0.02))
        self.heart_empty = pygame.image.load("Data/Sprites/UI/ui_heart_empty.png").convert_alpha()
        self.heart_empty, temp = self.scale_image(self.heart_empty, int(self.screen_width * 0.02))
        self.log = pygame.image.load("Data/Sprites/UI/log.png").convert_alpha()
        self.log, temp = self.scale_image(self.log, int(self.screen_width * 0.015))

        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((150, 150, 150))
        self.background.set_alpha(75)

        # initializing fonts
        self.regular_font = pygame.font.Font("Data/Fonts/Athelas-Regular.ttf", 40)
        self.small_font = pygame.font.Font("Data/Fonts/Athelas-Regular.ttf", 24)
        self.bold_font = pygame.font.Font("Data/Fonts/Athelas-Bold.ttf", 40)

    def display(self):
        """
        displays start and end screens if we have the correct game state, as well as UI elements
        """

        player_menu_left = self.screen_width - 30 - (self.heart_full.get_width() * 5)
        # display health bar
        health = self.player.get_health()
        for i in range(4):
            if i > health - 1:
                self.screen.get_screen().blit(self.heart_empty, (player_menu_left + (self.heart_full.get_width() * i), 30))
            else:
                self.screen.get_screen().blit(self.heart_full,(player_menu_left + (self.heart_full.get_width() * i), 30))

        # display inventory
        inventory = self.player.get_resources()
        woods = inventory[Resources.wood]
        self.screen.get_screen().blit(self.log, (player_menu_left, 80))
        self.screen.set_font(self.regular_font)
        self.screen.text(player_menu_left + (self.heart_full.get_width() * 1), 75 - self.log.get_height()/2, woods, centered=False)

        # display start and end screen
        if self.start:
            self.start_screen()
        elif self.end:
            self.end_screen()

    def start_screen(self):
        """
        Shows the current tutorial overlay
        """
        # fill the background with a light hue/mist
        self.background.fill((150, 150, 150))
        self.background.set_alpha(75)
        self.screen.get_screen().blit(self.background, (0, 0))

        if self.tutorial_slide == 0:
            # show the tutorial image on the screen
            self.screen.get_screen().blit(self.tut0, self.tut0_rect.topleft)

            # show the continue text
            self.screen.set_font(self.small_font)
            self.screen.text(self.screen_width / 2, (self.screen_height / 5) * self.continue_height_scale,
                             "Press [left] or [z] to continue")
        elif self.tutorial_slide == 1:
            # show the tutorial image on the screen
            self.screen.get_screen().blit(self.tut1, self.tut1_rect.topleft)

            # show the continue text
            self.screen.set_font(self.small_font)
            self.screen.text(self.screen_width / 2, (self.screen_height / 5) * self.continue_height_scale,
                             "Press [left] or [z] to continue")
        elif self.tutorial_slide == 2:
            self.screen.get_screen().blit(self.tut2, self.tut2_rect.topleft)

            self.screen.set_font(self.small_font)
            self.screen.text(self.screen_width / 2, (self.screen_height / 5) * self.continue_height_scale,
                             "Press [left] or [z] to continue")
        else:
            self.screen.get_screen().blit(self.tut3, self.tut3_rect.topleft)

            self.screen.set_font(self.small_font)
            self.screen.text(self.screen_width / 2, (self.screen_height / 5) * self.continue_height_scale,
                             "Press [left] or [z] to start")

    def end_screen(self):
        """
        Show the end screen overlay, depending on the win/lose state
        """
        self.screen.get_screen().blit(self.background, (0, 0))

        if self.score < self.game_duration * self.timescale:  # if you lost it shows you the lose screen overlay
            self.screen.get_screen().blit(self.lost_screen, self.lost_rect.topleft)
        else:  # show the win screen overlay
            self.screen.get_screen().blit(self.won_screen, self.won_rect.topleft)

        # add the played duration to the screen
        self.screen.set_font(self.bold_font)
        self.screen.text(self.screen_width / 2, (self.screen_height / 5) * 2.8, f"You survived {self.score} hours")
        self.screen.set_font(self.small_font)
        self.screen.text(self.screen_width / 2, (self.screen_height / 5) * 3, "(Press [esc] to quit)")

    def update_end(self, score: int = -1):
        """
        Set the end, win/lose state
        :param score: The amount of 'hours' you survived
        """
        self.end = True
        self.score = score

    def update_start(self):
        """
        show the next tutorial overlay or closes it
        """
        if self.tutorial_slide < 3:
            self.tutorial_slide += 1
        else:
            self.start = False
            self.background.set_alpha(0)
            self.screen.get_screen().blit(self.background, (0, 0))

    def scale_image(self, image: pygame.Surface, new_width: int = None) -> (pygame.Surface, pygame.Rect):
        """
        Resizes the images to fit the screen while keeping the aspect ratio the intact.
        And makes a rectangle of the image that is centered on the screen.
        :param image: The image that has to be resized
        :param new_width: Width to be resized to (can be left empty)
        :return: The resized image and the centered rectangle
        """
        width, height = image.get_size()
        screen_width, screen_height = self.screen.get_size()
        aspect_ratio = width / height

        if new_width is None:
            img_width = int(self.screen_width * 0.5)
        else:
            img_width = new_width
        img_height = int(img_width / aspect_ratio)
        img = pygame.transform.scale(image, (img_width, img_height))

        # get the rectangle bounding box and move it to be centered on the screen
        rect: pygame.Rect = img.get_rect()
        rect.center = (screen_width / 2, screen_height / 2)
        return img, rect
