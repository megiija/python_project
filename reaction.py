import pygame
from pygame.locals import *
import sys
import time
import random


class reaction_game:
    def __init__(self):
        pygame.init()

        self.w = 1250
        self.h = 750
        self.time_start = 0
        self.react_time = 0
        self.average = 0
        self.reset = True
        self.active = False
        self.end = False

        self.HEAD_C = (208, 158, 255)
        self.TEXT_C = (240, 240, 240)
        self.RESULT_C = (255, 70, 70)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)

        self.open_img = pygame.image.load('reaction_open.png')
        self.open_img = pygame.transform.scale(self.open_img, (self.w, self.h))
        self.bg = pygame.image.load('react_bg.png')
        self.bg = pygame.transform.scale(self.bg, (self.w, self.h))

        self.screen = pygame.display.set_mode([self.w, self.h])

    def paragraph_text(self, screen, msg, y, fsize, colour):
        font = pygame.font.Font('Nasa21-l23X.ttf', fsize)
        text = font.render(msg, 1, colour)
        text_rect = text.get_rect(center=(self.w / 2, y))
        screen.blit(text, text_rect)
        pygame.display.update()

    def draw_text(self, screen, text, color, rect, fsize, font):
        aa = False
        font = pygame.font.Font(font, fsize)
        rect = Rect(rect)
        y = rect.top
        lineSpacing = -2
        fontHeight = font.size("Tg")[1]

        while text:
            i = 1
            # determine if the row of text will be outside our area
            if y + fontHeight > rect.bottom:
                break
            # determine maximum width of line
            while font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1
            # if we've wrapped the text, then adjust the wrap to the last word
            if i < len(text):
                i = text.rfind(" ", 0, i) + 1
            # render the line and blit it to the surface
            image = font.render(text[:i], aa, color)
            screen.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing
            # remove the text we just blitted
            text = text[i:]

        return text

    def results(self):
        pass

    def run(self):
        self.screen.blit(self.open_img, (0, 0))
        pygame.display.update()
        time.sleep(1)

        self.time_start = 0
        self.react_time = 0

        pygame.display.update()
        count = 0
        game_state = 'start'

        self.running = True
        while self.running:
            clock = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()

                if event.type == MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # position of menu button
                    if 20 <= x <= 220 and 20 <= y <= 95:
                        from subprocess import Popen
                        Popen(['python3', 'main.py'])
                        time.sleep(1)
                        sys.exit()

                if count <= 5 and event.type == pygame.KEYDOWN:
                    if game_state == 'start':
                        self.average = 0
                        self.react_time = 0
                        game_state = 'wait'
                        self.time_start = clock + random.randint(1000, 4000)

                    if game_state == 'wait':
                        self.time_start = clock + random.randint(1000, 4000)

                    if game_state == "wait_for_reaction":
                        game_state = "wait"
                        self.react_time = (clock - self.time_start) / 1000
                        self.time_start = clock + random.randint(1000, 4000)
                        count += 1
                        self.average = (self.average * (count - 1) + self.react_time) / count

                if count > 5:
                    game_state = 'start'
                    f = open('user.txt', 'r')
                    user = f.read()
                    f.close()
                    save_file = (user + '.txt')
                    f = open(save_file, "a+")
                    f.write(str(self.average) + '\n')
                    f.close()
                    count = 0

            if game_state == 'wait':
                if clock >= self.time_start:
                    game_state = "wait_for_reaction"

            self.screen.blit(self.bg, (0, 0))
            center = self.screen.get_rect().center
            self.draw_text(self.screen, ("Reaction time: " + str(self.react_time)), self.HEAD_C, (50, 650, 400, 100),
                           32,
                           'Nasa21-l23X.ttf')
            self.draw_text(self.screen, ("Average Reaction time: " + str(self.average)), self.HEAD_C,
                           (350, 650, 1000, 100), 32, 'Nasa21-l23X.ttf')

            # MENU BUTTON
            self.menu_img = pygame.image.load('menubtn.png')
            self.screen.blit(self.menu_img, (20, 20))

            if game_state == 'start':
                self.draw_text(self.screen, "Reaction Time Test", self.HEAD_C, (430, 50, 400, 100), 50,
                               'Nasa21-l23X.ttf')
                self.draw_text(self.screen, "When the red box turns green, click as quickly as you can.", self.TEXT_C,
                               (150, 150, 1000, 100), 32, 'Nasa21-l23X.ttf')
                self.draw_text(self.screen, "Clicking too early will reset the timer.", self.TEXT_C,
                               (150, 200, 1000, 100), 32, 'Nasa21-l23X.ttf')
                self.draw_text(self.screen, "PRESS ANY KEY TO BEGIN", self.TEXT_C,
                               (150, 250, 1000, 100), 32, 'Nasa21-l23X.ttf')

            if game_state == 'wait':
                pygame.draw.rect(self.screen, self.red, (375, 100, 500, 500))
                self.draw_text(self.screen, 'wait...', self.TEXT_C, (575, 300, 400, 100), 46,
                               'Nasa21-l23X.ttf')

            if game_state == 'wait_for_reaction':
                pygame.draw.rect(self.screen, self.green, (375, 100, 500, 500))
                self.draw_text(self.screen, 'press any key!', (0, 0, 0), (500, 300, 400, 100), 46,
                               'Nasa21-l23X.ttf')

            pygame.display.flip()

    def reset_game(self):
        self.screen.blit(self.open_img, (0, 0))

        pygame.display.update()
        time.sleep(1)

        self.reset = False
        self.end = False
        self.time_start = 0
        self.react_time = 0

        # drawing heading
        self.screen.blit(self.bg, (0, 0))
        self.draw_text(self.screen, "Reaction Time Test", self.HEAD_C, (430, 50, 400, 100), 50, 'Nasa21-l23X.ttf')

        pygame.display.update()
