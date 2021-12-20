# todo
#  - alphas :)
#       + text
#  - rotation to rectangles, like dashed line
#  - correct logging
#  - a lot
#  - sleep
# -

"""
 NOTE: Strokes don't support alpha
"""

import math
import pygame
from pygame import gfxdraw as draw
from enum import Enum
import time
import numpy as np


class Screen:
    def __init__(self, width: int, height: int, loopFunction, frameRate=60, title=None, key_pressed_func=None, key_hold_func=None,
                 mouse_pressed_func=None, mouse_dragged_func=None, mouse_released_func=None):
        # setup screen
        pygame.init()
        if width == height == 0:
            self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((width, height))
        if title: Screen.set_title(title)

        # input variables 
        self.window_width = width
        self.window_height = height
        self.frameRate = frameRate
        "  - functions"
        self.loopFunction = loopFunction
        self.key_pressed_func = key_pressed_func
        self.key_hold_func = key_hold_func
        self.mouse_pressed_func = mouse_pressed_func
        self.mouse_released_func = mouse_released_func
        self.mouse_dragged_func = mouse_dragged_func


        # other variables
        self.run = True
        self.txt_font = pygame.font.SysFont('arial', 40)  # pygame.font.SysFont('Comic Sans MS', 30)
        self.old_time = time.perf_counter()
        self.elapsed_time = 0
        "  - draw shitzle"
        self.current_color = (0, 0, 0, 255)
        self.current_stroke_color = (0, 0, 0, 255)
        self.current_stroke_thickness = 5
        self.stroke_active = True
        self.filled = True
        "  --text "
        self.current_text_color = (0, 0, 0)
        self.current_text_stroke_color = (0, 0, 0)
        self.current_text_stroke_thickness = 2
        self.text_stroke_active = False

    # the loop function that redraws every frame
    def loop(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.K_ESCAPE in self.get_pressed_keys() or pygame.KSCAN_ESCAPE in self.get_pressed_keys():
                    self.run = False
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    self.key_pressed()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_pressed(event.button)
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_released(event.button)

            self.elapsed_time = time.perf_counter() - self.old_time

            # main loop
            if self.elapsed_time > 1 / self.frameRate:
                self.old_time = time.perf_counter()
                if self.mouse_dragged_func: self.key_hold()
                if self.mouse_dragged_func: self.mouse_dragged()

                # call the loop function
                self.loopFunction()

                pygame.display.flip()  # to_be_updated_rects) # has to be changed for optimalization.

    # starts the loop
    def start(self):
        self.loop()
        # stops the loop and so often the program aswell

    def stop(self):
        self.run = False

    # events
    def key_pressed(self):
        # keypressed, the function is called and the active keys are given. the key can be found using pygame.KSCAN_W
        if self.key_pressed_func is not None:
            active_keys = self.get_pressed_keys()

            self.key_pressed_func(active_keys)

    def key_hold(self):
        if self.key_hold_func is not None:
            active_keys = self.get_pressed_keys()
            if len(active_keys) > 0:
                self.key_hold_func(active_keys)

    def mouse_pressed(self, button):  # 3 == right button, 1 == left button, 2 scroll button
        if self.mouse_pressed_func is not None: self.mouse_pressed_func(button)

    def mouse_released(self, button):
        if self.mouse_released_func is not None: self.mouse_released_func(button)

    def mouse_dragged(self):
        if self.get_mouse_pressed()[0]:
            self.mouse_dragged_func(self.get_mouse_pos())


    # settings
    def setframeRate(self, frameRate):
        self.frameRate = frameRate

    # getters
    def get_screen(self):
        return self.screen

    def get_frameRate(self):
        return 1.0 / self.elapsed_time

    def get_wanted_frameRate(self):
        return self.frameRate

    def get_delta_time(self):
        return self.get_wanted_frameRate() / self.get_frameRate()

    def get_width(self):
        w, h = self.get_size()
        return w

    def get_height(self):
        w, h = self.get_size()
        return h

    def get_size(self):
        return self.screen.get_size()

    def get_mouse_pressed(self):
        return pygame.mouse.get_pressed()

    def get_mouse_pos(self):
        return pygame.mouse.get_pos()

    def get_pressed_keys(self):
        pressed_keys = pygame.key.get_pressed()
        active_keys = set(())

        for key_constant, pressed in enumerate(pressed_keys):
            if pressed:
                active_keys.add(key_constant)
        return active_keys

    def get_text_size(self, text, font=None):
        if not font == None:
            text_width, text_height = font.size(text)
        else:
            text_width, text_height = self.txt_font.size(text)
        return (text_width, text_height)

    def new_font(self, size, font='arial'):
        return pygame.font.SysFont(font, size)

    def get_available_fonts(self):
        return pygame.font.get_fonts()

    # setters
    def color(self, r=-1, g=-1, b=-1):
        # if just 1 value is entered make the r,g and b the same. so 255 -> (255,255,255) = white
        if b == -1:
            print("!!!!!  ----- NOT ENOUGH ARGUMENTS GIVEN FOR 'COLOR' -----  !!!!!")
            return

        if (g == -1):
            g = r
            b = r
        color = (r, g, b)
        if r == -1:
            self.filled = False
        else:
            self.current_color = color
        self.filled = True

    def color(self, color):
        self.current_color = self.drawColor(color)
        self.filled = True

    def stroke(self, color):
        '''
         Currently alpha is just partialy supported for strokes
        '''
        color = format_color(color)
        if color == None: return
        self.current_stroke_color = format_color(color)
        self.stroke_active = True

    def stroke_size(self, thickness):
        self.current_stroke_thickness = thickness

    def toggle_stroke(self, stroke_active):
        self.stroke_active = stroke_active

    def toggle_fill(self, filled):
        self.filled = filled

    def text_font(self, size, font='arial'):
        self.txt_font = pygame.font.SysFont(font, size)

    def set_font(self, font):  # probably make fonts en shit more easily :)
        self.txt_font = font

    def text_color(self, color):
        self.current_text_color = format_color(color)

    def text_stroke(self, color, thickness=None):
        self.current_text_stroke_color = format_color(color)
        self.text_stroke_active = True
        if thickness: self.current_text_stroke_thickness = thickness

    def toggle_text_stroke(self, active):
        self.text_stroke_active = active

    def set_title(title):
        pygame.display.set_caption(title)

    # drawing
    def circle(self, x, y, radius=20, color=None, surface=None):
        if surface == None: surface = self.get_screen()
        if color:
            filled = True
        else:
            filled = False
        color = self.drawColor(color)
        radius = int(radius)
        if radius < 0: return

        # it's done this way, because alpha's are in this case on just one color and this is a lot faster
        draw_surface = pygame.Surface((radius * 2, radius * 2))
        alpha = color[3]
        draw_color = format_color_3(color)
        color_key = opposite_color(draw_color)
        draw_surface.fill(color_key)
        draw_surface.set_colorkey(color_key)

        if self.filled or filled:
            draw.filled_circle(draw_surface, int(radius), int(radius), int(radius), draw_color)
            draw_surface.set_alpha(alpha)
            surface.blit(draw_surface, pygame.Rect(int(x) - radius, int(y) - radius, radius * 2, radius * 2))
        if self.stroke_active: draw.aacircle(surface, int(x), int(y), int(radius),
                                             self.current_stroke_color)  # not changable thickness!!

    def rect(self, x, y, w=20, h=20, color=None, border_radius=1, border_top_left_radius=-1, border_top_right_radius=-1,
             border_bottom_left_radius=-1, border_bottom_right_radius=-1, surface=None):
        if surface is None: surface = self.get_screen()
        if color:
            filled = True
        else:
            filled = False
        color = self.drawColor(color)

        # it's done this way, because alpha's are in this case on just one color and this is a lot faster
        draw_surface = pygame.Surface((w, h))
        alpha = color[3]
        draw_color = format_color_3(color)

        # if self.filled or color[0] == -1: pygame.draw.rect(surface, color, pygame.Rect(x,y, w, h))
        if self.filled or filled:
            if border_radius > 1:
                pygame.draw.rect(surface, color, pygame.Rect(x, y, w, h), border_radius=border_radius, border_top_right_radius=border_top_right_radius
                                 , border_bottom_left_radius=border_bottom_left_radius, border_top_left_radius=border_top_left_radius,
                                 border_bottom_right_radius=border_bottom_right_radius)
            else:
                pygame.Surface.fill(draw_surface, draw_color, pygame.Rect(0, 0, w, h))  # should be a bit faster
                draw_surface.set_alpha(alpha)
                surface.blit(draw_surface, pygame.Rect(x, y, w, h))
        if self.stroke_active:
            pygame.draw.rect(surface, self.current_stroke_color, pygame.Rect(x, y, w, h), self.current_stroke_thickness, border_radius=border_radius,
                             border_top_right_radius=border_top_right_radius, border_bottom_left_radius=border_bottom_left_radius,
                             border_top_left_radius=border_top_left_radius, border_bottom_right_radius=border_bottom_right_radius)

    def text(self, x, y, txt, centered=True, color=None, font=None, surface=None, antialiasing=True):
        if font is None: font = self.txt_font
        if surface is None: surface = self.get_screen()
        color = format_color(color)
        if color is None: color = self.current_text_color

        try:
            txt = str(txt)
        except:
            print("!!!!!  ----- the text in text() can't be converted to string -----  !!!!!")

        if self.text_stroke_active:
            outlineSurf = self.txt_font.render(txt, antialiasing, self.current_text_stroke_color)
            offsets = [(ox, oy)
                       for ox in range(-self.current_text_stroke_thickness, 2 * self.current_text_stroke_thickness,
                                       int(self.current_text_stroke_thickness / 2) if int(
                                           self.current_text_stroke_thickness / 2) > 0 else self.current_text_stroke_thickness)
                       for oy in range(-self.current_text_stroke_thickness, 2 * self.current_text_stroke_thickness,
                                       int(self.current_text_stroke_thickness / 2) if int(
                                           self.current_text_stroke_thickness / 2) > 0 else self.current_text_stroke_thickness)
                       if ox != 0 or ox != 0]
            for ox, oy in offsets:
                px, py = x, y
                surface.blit(outlineSurf, outlineSurf.get_rect(center=(px + ox, py + oy)))
            innerText = self.txt_font.render(txt, antialiasing, color).convert_alpha()
            textRect = innerText.get_rect()
            if centered:
                center = textRect.center
            else:
                center = [0, 0]
            surface.blit(innerText, (x - center[0], y - center[1]))
        else:
            textSurf = self.txt_font.render(txt, antialiasing, color)
            textRect = textSurf.get_rect()
            if centered:
                center = textRect.center
            else:
                center = [0, 0]
            surface.blit(textSurf, (x - center[0], y - center[1]))

    def text_array(self, x, y, txt_array, color=None, font=None, surface=None,
                   antialias=True):  # not updated anymore!!!!
        if font == None: font = self.txt_font
        if surface == None: surface = self.get_screen()
        color = self.drawColor(color)

        try:
            for txt in txt_array:
                txt = str(txt)
        except:
            print("!!!!!  ----- the text in text() can't be converted to string -----  !!!!!")

        for txt in txt_array[::-1]:
            text_width, text_height = font.size(txt)
            x_ = x - text_width / 2
            y -= text_height / 2
            textsurface = font.render(txt, antialias, color)
            surface.blit(textsurface, (x_, y))
            y -= text_height / 2

    def background(self, r, g=-1, b=-1, surface=None):
        if surface == None: surface = self.get_screen()

        if (g == -1):
            g = r
            b = r
        if b == -1:
            print("!!!!!  ----- NOT ENOUGH ARGUMENTS GIVEN FOR 'BACKGROUND' -----  !!!!!")
            return
        surface.fill((r, g, b))

    def dashed_line(self, startPos, endPos, width, step=25, color=None, surface=None):
        if surface == None: surface = self.get_screen()
        if color:
            filled = True
        else:
            filled = False
        color = self.drawColor(color)
        drawpos = [startPos[0], startPos[1]]

        # make a column surface with the dashed line
        height = int(math.dist(startPos, endPos))
        line_surface = pygame.Surface([width, height], pygame.SRCALPHA, 32)
        line_surface.set_alpha(color[3])

        for i in range(0, height, step):
            if float(i) % float(step * 2) == 0:
                if self.filled or filled:
                    pygame.Surface.fill(line_surface, format_color_3(color), pygame.Rect(0, i, width, step))

                if self.stroke_active: pygame.draw.rect(line_surface, self.current_stroke_color,
                                                        pygame.Rect(0, i, width, step), self.current_stroke_thickness,
                                                        1)

        # rotate it
        vector = np.array([endPos[0] - startPos[0], endPos[1] - startPos[1]])
        angle = np.angle(vector[0] + vector[1] * 1j, True)
        if angle < 0: angle += 360

        line_surface = pygame.transform.rotate(line_surface, -angle + 90)

        if 90 < angle <= 270:
            drawpos[0] += math.cos(angle * math.pi / 180) * height
        if 180 < angle <= 360:
            drawpos[1] += math.sin(angle * math.pi / 180) * height

        "- center it"
        drawpos[1] += -abs(math.cos(angle * math.pi / 180)) * width / 2
        drawpos[0] += -abs(math.sin(angle * math.pi / 180)) * width / 2

        # add it to the screen
        surface.blit(line_surface, drawpos)

    def outline_circle(self, x, y, radius, thickness=5, color=None, surface=None):
        if surface == None: surface = self.get_screen()
        color = self.drawColor(color)
        radius = int(radius)
        if radius < 0: return

        draw_surface = pygame.Surface((radius * 2, radius * 2))
        alpha = color[3]
        draw_color = format_color_3(color)
        color_key = opposite_color(draw_color)
        draw_surface.fill(color_key)
        draw_surface.set_colorkey(color_key)

        draw.filled_circle(draw_surface, int(radius), int(radius), int(radius), draw_color)
        draw.filled_circle(draw_surface, int(radius), int(radius), int(radius) - thickness, color_key)
        draw_surface.set_alpha(alpha)

        surface.blit(draw_surface, pygame.Rect(int(x) - radius, int(y) - radius, radius * 2 + 1, radius * 2))

    def polygon(self, points, color=None, stroke_active=True, stroke_color=None, stroke_tickness=None,
                surface=None):  # stroke is work in progress !!!!!
        if surface == None: surface = self.get_screen()
        if color:
            filled = True
        else:
            filled = False
        color = self.drawColor(color)

        # stroke setup
        stroke_active_overwrite = stroke_active

        if stroke_color or stroke_tickness:
            stroke_active = True
        stroke_color = format_color(stroke_color)
        if stroke_color is None:
            stroke_color = self.current_stroke_color
        if stroke_tickness is None:
            stroke_tickness = self.current_stroke_thickness

        # calc the width and height of the polygon
        pointsX = []
        pointsY = []
        for point in points:
            pointsX.append(point[0])
            pointsY.append(point[1])
        width = int(max(pointsX) - min(pointsX))
        height = int(max(pointsY) - min(pointsY))
        x = min(pointsX)
        y = min(pointsY)

        pos = []
        for point in points:
            pos.append((point[0] - x, point[1] - y))

        # alpha
        draw_surface = pygame.Surface((width, height))
        alpha = color[3]
        draw_color = format_color_3(color)
        color_key = opposite_color(draw_color)
        draw_surface.fill(color_key)
        draw_surface.set_colorkey(color_key)

        # stroke
        stroke_surface = pygame.Surface((width, height))
        stroke_cutout = pygame.Surface((width, height))

        stroke_alpha = stroke_color[3]
        draw_stroke_color = format_color_3(self.current_stroke_color)
        stroke_color_key = opposite_color(draw_stroke_color)

        stroke_surface.fill(stroke_color_key)
        stroke_surface.set_colorkey(stroke_color_key)
        stroke_cutout.fill(draw_stroke_color)
        stroke_cutout.set_colorkey(draw_stroke_color)

        if (self.stroke_active or stroke_active) and stroke_active_overwrite:
            # outline
            draw.filled_polygon(stroke_surface, pos, draw_stroke_color)
            draw.aapolygon(stroke_surface, pos, draw_stroke_color)
            stroke_surface.set_alpha(stroke_alpha)
            scaled_stroke_surface = pygame.transform.scale(stroke_surface, (
                width + int(stroke_tickness) * 2, height + int(stroke_tickness) * 2))

            # cutout
            draw.filled_polygon(stroke_cutout, pos, stroke_color_key)
            # combine
            scaled_stroke_surface.blit(stroke_cutout,
                                       pygame.Rect(int(stroke_tickness), int(stroke_tickness), width, height))
            # draw to screen
            surface.blit(scaled_stroke_surface, pygame.Rect(x - int(stroke_tickness), y - int(stroke_tickness),
                                                            width + int(stroke_tickness) * 2,
                                                            height + int(stroke_tickness) * 2))

        if self.filled or filled:
            draw.filled_polygon(draw_surface, pos, draw_color)
            draw.aapolygon(draw_surface, pos, draw_color)
            draw_surface.set_alpha(alpha)
            surface.blit(draw_surface, pygame.Rect(x, y, width, height))

    def aapolygon(self, points, color=None, stroke_color=None, surface=None):
        """
        a antialised and cleaner version of the normal polygon, but *doesn't work with alpha*\n
        :param points: a list of points/corners of the polygon
        :param color: the color of the fill of the polygon
        :param stroke_color: the 1px line around the polygon
        :param surface: the surface to draw to, if left empty it is the surface of the called screen
        """

        if surface is None: surface = self.get_screen()
        if color:
            filled = True
        else:
            filled = False
        color = self.drawColor(color)
        stroke_color = format_color(stroke_color)
        if stroke_color is None: stroke_color = color

        # alpha
        draw_color = format_color_3(color)

        if self.filled or filled:
            draw.filled_polygon(surface, points, draw_color)
            draw.aapolygon(surface, points, stroke_color)

    def shape(self, pos, radius, pointsAmount, color=None, stroke_active=True, stroke_color=None, stroke_tickness=None,
              surface=None):
        self.polygon([(radius * math.cos(2 / pointsAmount * math.pi * T) + pos[0],
                       radius * math.sin(2 / pointsAmount * math.pi * T) + pos[1]) for T in range(0, pointsAmount)],
                     color, stroke_active=stroke_active, stroke_color=stroke_color, stroke_tickness=stroke_tickness,
                     surface=surface)

    # extra thingies for drawing
    def drawColor(self, color):
        # if no color is selected use the current color
        if color == None: color = self.current_color

        # if just 1 value is entered make the r,g and b the same. so 255 -> (255,255,255) = white
        try:
            if (len(color) == 1):
                color = (color[0], color[0], color[0])
            elif (len(color) == 2):
                color = (color[0], color[0], color[0], color[1])
        except:  # if it isn't a tuple
            color = (color, color, color)

        if color[0] == -1: self.filled = False  # old, still possible, but just old, tho it is faster. so you dcan use it ;)

        if len(color) < 4:
            color = (color[0], color[1], color[2], 255)

        return color


# enums
class MouseButton(Enum):
    left = 1
    scroll = 2
    right = 3
    scroll_up = 4
    scroll_down = 5


def format_color(color):
    '''
     formates color to the (r,g,b,a) format
    '''
    # if no color is selected use the current color
    if color == None: return None
    # if just 1 value is entered make the r,g and b the same. so 255 -> (255,255,255) = white
    try:
        if (len(color) == 1):
            color = (color[0], color[0], color[0])
        elif (len(color) == 2):
            color = (color[0], color[0], color[0], color[1])
    except:  # if it isn't a tuple
        color = int(color)
        color = (color, color, color)

    if len(color) < 4:
        color = (color[0], color[1], color[2], 255)
    return color


def format_color_3(color):
    '''
     Formates color to the (r,g,b) format,
     By doing so removing the alpha
    '''
    # if no color is selected use the current color
    if color == None: return None
    # if just 1 value is entered make the r,g and b the same. so 255 -> (255,255,255) = white
    try:
        if (len(color) == 1):
            color = (color[0], color[0], color[0])
        elif (len(color) == 2):
            color = (color[0], color[0], color[0], color[1])
    except:  # if it isn't a tuple
        color = (color, color, color)

    if len(color) == 4:
        color = (color[0], color[1], color[2])
    return color


def opposite_color(color):
    """
    Returns the opposite color.\n
    Usefull for color keying.
    """
    if len(color) <= 2: color = format_color(color)
    if len(color) == 3:
        return (255 - color[0], 255 - color[1], 255 - color[2])
    elif len(color) == 4:
        return (255 - color[0], 255 - color[1], 255 - color[2], color[3])


def lerp_2D(vector1, vector2, factor):
    """
     return the vector inbetween the two 2D vectors. \n
     when the factor is 0 it will be vector1, when it's 1 it is vector2
    """
    if factor > 1:
        factor = 1
    elif factor < 0:
        factor = 0

    if not len(vector1) == 2 or not len(vector2) == 2:
        print(" FOR LERP_2D() 2D vectors have to be enterd")
        return None

    return np.array(
        [(vector2[0] - vector1[0]) * factor + vector1[0], (vector2[1] - vector1[1]) * factor + vector1[1]])

def lerp_color(color1, color2, factor):
    """
     return the color inbetween the two colors. \n
     when the factor is 0 it will be color1, when it's 1 it is color2
    """
    if factor > 1:
        factor = 1
    elif factor < 0:
        factor = 0

    color1 = format_color(color1)
    color2 = format_color(color2)

    r = (color2[0] - color1[0]) * factor + color1[0]
    g = (color2[1] - color1[1]) * factor + color1[1]
    b = (color2[2] - color1[2]) * factor + color1[2]
    a = (color2[3] - color1[3]) * factor + color1[3]

    return format_color((r, g, b, a))