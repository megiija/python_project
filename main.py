from pygame_menu import Theme
from reaction import reaction_game
from typing_redone import typing_game
import pygame_menu
import pygame
import sys

pygame.init()

w = 1250
h = 750

# colours
HEAD_C = (140, 50, 175)
TEXT_C = (240, 240, 240)

surface = pygame.display.set_mode((w, h))

font = pygame_menu.font.FONT_NEVIS
myTheme = Theme(background_color=(208, 158, 255),
                title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE,
                widget_font=font, widget_font_size=42,
                title_font=font, title_font_size=50,
                title_background_color=(0, 0, 0))


def user_select():
    username = menu.get_input_data()
    user = username['username'].lower()
    f = open('user.txt', 'w+')
    f.write(user)
    f.close()


def menu_typing():
    user_select()
    typing_game().run()
    sys.exit()


def menu_reaction():
    user_select()
    reaction_game().run()
    sys.exit()


menu = pygame_menu.Menu('Welcome', 1250, 750, theme=myTheme)

menu.add.text_input('User :', default='Guest', textinput_id='username')
menu.add.button('Typing Test', menu_typing)
menu.add.button('Reaction Time Test', menu_reaction)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)
