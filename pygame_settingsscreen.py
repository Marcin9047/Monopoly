import pygame
from monopoly_player import Player
from monopoly_property import Property
from pygame.locals import *
from pygame.locals import Rect


blue = (66, 135, 245)
red = (153, 28, 28)
yellow = (184, 150, 48)
green = (88, 184, 48)
black = (0, 0, 0)
white = (255, 255, 255)
monopoly_txt = (60, 31, 129)
special = (174, 195, 222)
lighted_spec = (0, 195, 222)
score = (93, 168, 116)
color = (212, 242, 221)
prop_color = (180, 174, 222)
lighted_prop = (220, 174, 222)
deck_cen = (111, 155, 115)
button_color = (123, 129, 31)
pons_color = (216, 29, 29)
title_color = (60, 101, 64)


def draw_welcom_title(screen):
        fontsize = 75
        font = pygame.font.Font(None, fontsize)
        text = font.render("Welcome to Monopoly", 1, black)
        textpos = text.get_rect()
        textpos = textpos.move(35, 100)
        screen.backgr.blit(text, textpos)

def draw_please_select(screen):
        fontsize = 30
        font = pygame.font.Font(None, fontsize)
        text = font.render("Please select your game mode:", 1, black)
        textpos = text.get_rect()
        textpos = textpos.move(150, 180)
        screen.backgr.blit(text, textpos)

def draw_mods_names(screen):
        surf = screen.backgr
        fontsize = 60
        font = pygame.font.Font(None, fontsize)
        single = font.render("Singleplayer", 1, black)
        multi = font.render("Multiplayer", 1, black)
        team = font.render("Team battle", 1, black)

        textpos = single.get_rect()
        textpos = textpos.move(165, 325)
        screen.backgr.blit(single, textpos)
        pygame.draw.line(surf, black, [130, 370], [450, 370], 1)

        textpos = multi.get_rect()
        textpos = textpos.move(180, 525)
        screen.backgr.blit(multi, textpos)
        pygame.draw.line(surf, black, [130, 570], [450, 570], 1)

        textpos = team.get_rect()
        textpos = textpos.move(170, 725)
        screen.backgr.blit(team, textpos)
        pygame.draw.line(surf, black, [130, 770], [450, 770], 1)


def draw_mods(screen):
    surf = screen.backgr
    draw_welcom_title(screen)
    draw_please_select(screen)
    for i in range(3):
        mode_rec = Rect(50, 300 + 200 * i, 500, 100)
        pygame.draw.rect(surf, blue, mode_rec)
        pygame.draw.rect(surf, black, mode_rec, 2)
    draw_mods_names(screen)


class Setting_screen():
  
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 900))
        pygame.display.set_caption('Monopoly')
        self.backgr = pygame.Surface(self.screen.get_size())
        self.backgr = self.backgr.convert()
        self.backgr.fill((green))

    def draw(self):
        draw_mods(self)
        self.screen.blit(self.backgr, (0, 0))
        pygame.display.flip()


    def do_action(self, problem=False):
        buttons = 1
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    paused = False
                    # for button in self.action_table.buttons():
                        # button.activate(player, self)
                    # self.act_buttons = []

test2 = True
while test2:
    test = Setting_screen()
    test.draw()
    test.do_action()