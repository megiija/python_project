import pygame
from pygame.locals import *
import sys
import time
import random

class typing_game:
    def __init__(self):
        pygame.init()

        self.w = 1250
        self.h = 750
        self.reset = True
        self.active = False
        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.time_end = 0
        self.accuracy = '0%'
        self.results = 'Time: 0   Accuracy: 0%    WPM: 0'
        self.wpm = 0
        self.end = False

        # colours
        self.HEAD_C = (208, 158, 255)
        self.TEXT_C = (240, 240, 240)
        self.RESULT_C = (255, 70, 70)

        self.open_img = pygame.image.load('typing_open.png')
        self.open_img = pygame.transform.scale(self.open_img, (self.w, self.h))
        self.bg = pygame.image.load('typing_bg.png')
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

    def get_sentence(self):
        f = open('phrases.csv').read()
        phrases = f.split('\n')
        phrase = random.choice(phrases)
        return phrase

    def show_results(self, screen):
        if not self.end:
            # calculate time
            self.time_end = time.time() - self.time_start
            # calculate accuracy
            count = 0
            for i, c in enumerate(self.word):
                try:
                    if self.input_text[i] == c:
                        count += 1
                except:
                    pass
            self.accuracy = count / len(self.word) * 100
            # Calculate words per minute
            self.wpm = len(self.input_text) * 60 / (5 * self.time_end)
            self.end = True
            print(self.time_end)

            self.results = 'Time:' + str(round(self.time_end)) + " secs Accuracy:" + str(
                round(self.accuracy)) + "%" + ' Wpm: ' + str(round(self.wpm))
            f = open('user.txt', 'r')
            user = f.read()
            f.close()
            save_file = (user + '.txt')
            f = open(save_file, "a+")
            f.write(self.results + '\n')
            f.close()

            # draw icon image
            self.time_img = pygame.image.load('reset.png')
            self.time_img = pygame.transform.scale(self.time_img, (150, 150))
            # screen.blit(self.time_img, (80,320))
            screen.blit(self.time_img, (self.w / 2 - 75, self.h - 160))
            self.paragraph_text(screen, "Reset", self.h - 100, 32, (255, 255, 255))

            print(self.results)
            pygame.display.update()

    def run(self):
        self.reset_game()

        self.running = True
        while self.running:
            clock = pygame.time.Clock()
            pygame.draw.rect(self.screen, self.HEAD_C, (110, 300, 1000, 150), 2)

            pygame.draw.rect(self.screen, (0, 0, 0), (112, 302, 996, 146))
            self.draw_text(self.screen, self.input_text, self.TEXT_C, (115, 305, 990, 130), 22, 'Nasa21-l23X.ttf')
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # position of input box
                    # 110, 300, 1000, 150
                    if 110 <= x <= 1110 and 300 <= y <= 450 and not self.active:
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time()
                    # position of reset box
                    if 550 <= x <= 700 and y >= 640 and self.end:
                        self.reset_game()
                    #position of menu button
                    if 20 <= x <= 220 and 20 <= y <= 95:
                        from subprocess import Popen
                        Popen(['python3', 'main.py'])
                        time.sleep(1)
                        sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.active:
                        self.show_results(self.screen)
                        print(self.results)
                        self.paragraph_text(self.screen, self.results, 500, 28, self.RESULT_C)
                        self.end = True

                    elif event.key == pygame.K_RETURN and not self.active:
                        pass

                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        try:
                            self.input_text += event.unicode
                            self.draw_text(self.screen, self.input_text, self.TEXT_C, (115, 305, 990, 130), 22,
                                           'Nasa21-l23X.ttf')
                            pygame.display.update()
                        except:
                            pass

            pygame.display.update()

        clock.tick(60)

    def reset_game(self):
        self.screen.blit(self.open_img, (0, 0))

        pygame.display.update()
        time.sleep(1)

        self.reset = False
        self.end = False

        self.input_text = 'Click to start typing.'
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0

        # Get random sentence
        self.word = self.get_sentence()
        if not self.word: self.reset_game()

        # drawing heading
        self.screen.blit(self.bg,(0,0))
        msg = "Typing Speed Test"
        self.draw_text(self.screen, msg, self.HEAD_C, (440, 50, 400, 100), 50, 'Nasa21-l23X.ttf')

        #MENU BUTTON
        self.menu_img = pygame.image.load('menubtn.png')
        self.screen.blit(self.menu_img, (20, 20))

        # draw the rectangle for input box
        pygame.draw.rect(self.screen, self.HEAD_C, (110, 300, 1000, 150), 2)

        # draw the sentence string
        self.draw_text(self.screen, self.word, self.TEXT_C, (110, 150, 1000, 400), 24, 'Nasa21-l23X.ttf')

        pygame.display.update()
