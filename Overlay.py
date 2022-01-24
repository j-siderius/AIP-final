import pygame


class Overlay:
    def __init__(self, screen):
        self.screen = screen
        screen_width, screen_height = self.screen.get_size()[0], self.screen.get_size()[1]
        img_width = int(screen_width * 0.6)  # based on images of 1920ximg_specific

        self.start = False
        self.end = False

        self.win_screen = pygame.image.load("Data/Images/win.png")
        img_height = int(self.win_screen.get_size()[1] * 0.6)
        # self.win_screen = pygame.transform.scale(self.win_screen, (img_width, img_height))


    def display(self):
        self.screen.get_screen().blit(self.win_screen, (0, 0))
        if self.start:
            pass
        elif self.end:
            pass

    def start_screen(self):
        pass

    def end_screen(self):
        pass

    def run_start(self):
        self.start = True

    def run_end(self):
        self.end = True

