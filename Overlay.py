import pygame


class Overlay:
    def __init__(self, screen, controller):
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()[0], self.screen.get_size()[1]
        img_width = int(self.screen_width * 0.5)  # based on images of 1920ximg_specific
        self.img_pos = (int(self.screen_width/4), int(self.screen_height/5))

        self.start = True
        self.end = False

        self.score: int = -1
        self.timescale, self.game_duration = controller.get_timescale()

        # initializing all screen images and resizing them to fit screen
        self.won_screen = pygame.image.load("Data/Images/won.png").convert_alpha()
        img_height = int(self.won_screen.get_size()[1] * 0.6)
        self.win_screen = pygame.transform.scale(self.won_screen, (img_width, img_height))

        self.lost_screen = pygame.image.load("Data/Images/lost.png").convert_alpha()
        img_height = int(self.lost_screen.get_size()[1] * 0.6)
        self.lost_screen = pygame.transform.scale(self.lost_screen, (img_width, img_height))

        self.tut0 = pygame.image.load("Data/Images/tutorial0.png").convert_alpha()
        img_height = int(self.tut0.get_size()[1] * 0.6)
        self.tut0 = pygame.transform.scale(self.tut0, (img_width, img_height))

        self.tut1 = pygame.image.load("Data/Images/tutorial1.png").convert_alpha()
        img_height = int(self.tut1.get_size()[1] * 0.6)
        self.tut1 = pygame.transform.scale(self.tut1, (img_width, img_height))

        self.tut2 = pygame.image.load("Data/Images/tutorial2.png").convert_alpha()
        img_height = int(self.tut2.get_size()[1] * 0.6)
        self.tut2 = pygame.transform.scale(self.tut2, (img_width, img_height))

        self.tut3 = pygame.image.load("Data/Images/tutorial3.png").convert_alpha()
        img_height = int(self.tut3.get_size()[1] * 0.6)
        self.tut3 = pygame.transform.scale(self.tut3, (img_width, img_height))

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
        self.background.fill((150, 150, 150))
        self.background.set_alpha(75)
        self.screen.get_screen().blit(self.background, (0, 0))

        if self.tutorial_slide == 0:
            self.screen.get_screen().blit(self.tut0, (self.img_pos[0], self.img_pos[1]))

            self.screen.set_font(self.small_font)
            self.screen.text(self.screen_width / 2, (self.screen_height / 5) * 3.2, "Press [left] or [z] to continue")
        elif self.tutorial_slide == 1:
            self.screen.get_screen().blit(self.tut1, (self.img_pos[0], self.img_pos[1]))

            self.screen.set_font(self.small_font)
            self.screen.text(self.screen_width / 2, (self.screen_height / 5) * 3.2, "Press [left] or [z] to continue")
        elif self.tutorial_slide == 2:
            self.screen.get_screen().blit(self.tut2, (self.img_pos[0], self.img_pos[1]))

            self.screen.set_font(self.small_font)
            self.screen.text(self.screen_width / 2, (self.screen_height / 5) * 3.2, "Press [left] or [z] to continue")
        else:
            self.screen.get_screen().blit(self.tut3, (self.img_pos[0], self.img_pos[1]))

            self.screen.set_font(self.small_font)
            self.screen.text(self.screen_width / 2, (self.screen_height / 5) * 3.2, "Press [left] or [z] to start")

    def end_screen(self):
        self.screen.get_screen().blit(self.background, (0, 0))

        if self.score < self.game_duration:
            self.screen.get_screen().blit(self.lost_screen, (self.img_pos[0], self.img_pos[1]))
        else:
            self.screen.get_screen().blit(self.won_screen, (self.img_pos[0], self.img_pos[1]))

        self.screen.set_font(self.bold_font)
        self.screen.text(self.screen_width/2, (self.screen_height/5) * 2.8, f"You survived {self.score} hours")
        self.screen.set_font(self.small_font)
        self.screen.text(self.screen_width / 2, (self.screen_height / 5) * 3, "(Press [left] or [z] to quit)")

    def update_end(self, score: int = -1):
        self.end = True
        self.score = score

    def update_start(self):
        if self.tutorial_slide < 3:
            self.tutorial_slide += 1
        else:
            self.start = False
            self.background.set_alpha(0)
            self.screen.get_screen().blit(self.background, (0, 0))

