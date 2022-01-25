import pygame

from Screen import Screen


class Overlay:
    def __init__(self, screen: Screen, controller):
        self.screen: Screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()[0], self.screen.get_size()[1]

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

        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((150, 150, 150))
        self.background.set_alpha(75)

        # initializing fonts
        self.regular_font = pygame.font.Font("Data/Fonts/Athelas-Regular.ttf", 40)
        self.small_font = pygame.font.Font("Data/Fonts/Athelas-Regular.ttf", 24)
        self.bold_font = pygame.font.Font("Data/Fonts/Athelas-Bold.ttf", 40)

    def display(self):
        # TODO: add check to Input.py for tutorial and end of game
        if self.start:
            self.start_screen()
        elif self.end:
            self.end_screen()

    def start_screen(self):
        """
        Shows the current tutorial overlay
        """
        self.background.fill((150, 150, 150))
        self.background.set_alpha(75)
        self.screen.get_screen().blit(self.background, (0, 0))

        if self.tutorial_slide == 0:
            # show the tutorial image on the screen
            self.screen.get_screen().blit(self.tut0, self.tut0_rect.topleft)

            # show the continue text
            self.screen.set_font(self.small_font)
            self.screen.text(self.screen_width / 2, (self.screen_height / 5) * self.continue_height_scale, "Press [left] or [z] to continue")
        elif self.tutorial_slide == 1:
            # show the tutorial image on the screen
            self.screen.get_screen().blit(self.tut1, self.tut1_rect.topleft)

            # show the continue text
            self.screen.set_font(self.small_font)
            self.screen.text(self.screen_width / 2, (self.screen_height / 5) * self.continue_height_scale, "Press [left] or [z] to continue")
        elif self.tutorial_slide == 2:
            self.screen.get_screen().blit(self.tut2, self.tut2_rect.topleft)

            self.screen.set_font(self.small_font)
            self.screen.text(self.screen_width / 2, (self.screen_height / 5) * self.continue_height_scale, "Press [left] or [z] to continue")
        else:
            self.screen.get_screen().blit(self.tut3, self.tut3_rect.topleft)

            self.screen.set_font(self.small_font)
            self.screen.text(self.screen_width / 2, (self.screen_height / 5) * self.continue_height_scale, "Press [left] or [z] to start")

    def end_screen(self):
        """
        Show the end screen overlay, depending on the win/lose state
        """
        self.screen.get_screen().blit(self.background, (0, 0))

        if self.score < self.game_duration:  # if you lost it shows you the lose screen overlay
            self.screen.get_screen().blit(self.lost_screen, self.lost_rect.topleft)
        else:  # show the win screen overlay
            self.screen.get_screen().blit(self.won_screen, self.won_rect.topleft)

        self.screen.set_font(self.bold_font)
        self.screen.text(self.screen_width/2, (self.screen_height/5) * 2.8, f"You survived {self.score} hours")
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

    def scale_image(self, image: pygame.Surface) -> (pygame.Surface, pygame.Rect):
        """
        Resizes the images to fit the screen while keeping the aspect ratio the intact.
        And makes a rectangle of the image that is centered on the screen.
        :param image: The image that has to be resized
        :return: The resized image and the centered rectangle
        """
        width, height = image.get_size()
        screen_width, screen_height = self.screen.get_size()
        aspect_ratio = width / height

        img_width = int(self.screen_width * 0.5)
        img_height = int(img_width / aspect_ratio)
        img = pygame.transform.scale(image, (img_width, img_height))

        # get the rectangle bounding box and move it to be centered on the screen
        rect: pygame.Rect = img.get_rect()
        rect.center = (screen_width/2, screen_height/2)
        return img, rect