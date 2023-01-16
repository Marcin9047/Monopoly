import pygame
from monopoly import Player, Property
import sys
from pygame.locals import *
from pygame.locals import Rect
from monopoly_exeptions import WrongInputError, ZeroThrowsError, NotEnoughtMoneyError


"""Colours"""
black = (0, 0, 0)
white = (255, 255, 255)
monopoly_txt = (60, 31, 129)
special = (174, 195, 222)
score = (93, 168, 116)
color = (212, 242, 221)
prop_color = (180, 174, 222)
deck_cen = (111, 155, 115)
button_color = (123, 129, 31)
pons_color = (216, 29, 29)
title_color = (60, 101, 64)


class Player_name_title:
    def __init__(self, background, color, top, font_size):
        self.font_size = font_size
        self.top = top
        self.background = background
        self.color = color

    def draw(self, player):
        font = pygame.font.Font(None, self.font_size)
        text = font.render(player.name(), 1, self.color)
        textpos = text.get_rect()
        textpos.centerx = self.background.get_rect().centerx
        textpos = textpos.move(0, self.top)
        self.background.blit(text, textpos)

    def clear(self):
        pygame.draw.rect(self.background, black, Rect(600, 20, 600, 50))
        pygame.draw.rect(self.background, color, Rect(600, 20, 600, 50))


class Side_Table:
    def __init__(self, backgr, color, sizex, sizey, xcord, ycord, title_hight, font, name):
        self.background = backgr
        self.sizex = sizex
        self.sizey = sizey
        self.xcord = xcord
        self.ycord = ycord
        self.color = color
        self.title_hight = title_hight
        self.title_font = font
        self._name = name

    def name(self):
        return self._name

    def clear_score(background):
        pygame.draw.rect(background, score, Rect(1425, 200, 380, 650))

    def draw(self):
        left = self.xcord
        top = self.ycord
        sizex = self.sizex
        sizey = self.sizey
        tl_hgh = self.title_hight
        title = Rect(left, top, sizex, tl_hgh)
        main = Rect(left, top, sizex, sizey)
        self.set_hitbox(main)
        pygame.draw.rect(self.background, self.color, main)
        pygame.draw.rect(self.background, black, main, 3)
        pygame.draw.rect(self.background, black, title, 3)
        self.draw_title()

    def draw_title(self):
        fontsize = self.title_font
        name = self.name()
        font = pygame.font.Font(None, fontsize)
        text = font.render(name, 1, black)
        textpos = text.get_rect()
        x = self.xcord + (self.sizex // 3)
        y = self.ycord + (self.title_hight // 2) - (fontsize // 2)
        textpos = textpos.move(x, y)
        self.background.blit(text, textpos)

    def set_hitbox(self, rect):
        self._hitbox = rect

    def hitbox(self):
        return self._hitbox


class Score(Side_Table):
    def __init__(self, players, backgr, color, sizex, sizey, xcord, ycord, title_hight, font):
        super().__init__(backgr, color, sizex, sizey, xcord, ycord, title_hight, font, "Players")
        self.players = players

    def line(self, player):
        name = player.name()
        money = player.money()
        pause = player.pause()
        if pause != 0:
            line = f'{name}:  {money}    {pause}'
        else:
            line = f'{name}:  {money}'
        return line

    def draw_text(self):
        font = pygame.font.Font(None, 30)
        for number, player in enumerate(self.players):
            move_dw = 50 * number
            line = self.line(player)
            text = font.render(line, 1, black)
            textpos = text.get_rect()
            textpos = textpos.move(self.xcord + 50, self.ycord + self.title_hight + 50 + move_dw)
            self.background.blit(text, textpos)


class Action(Side_Table):
    def __init__(self, backgr, data, color, sizex, sizey, xcord, ycord, title_hight, font):
        super().__init__(backgr, color, sizex, sizey, xcord, ycord, title_hight, font, "Action")
        self.data = data
        self._buttons = []

    def add_button(self, button):
        self._buttons.append(button)

    def buttons(self):
        return self._buttons

    def draw_action(self, player):
        position = self.data[player.position()]
        pygame.draw.rect(self.background, black, Rect(174, 410, 250, 400), 4)


class Button(Action):
    def __init__(self, name, surf, table, xval, yval, xsize, ysize, colour):
        self.surface = surf
        self._name = name
        self.xval = xval
        self.yval = yval
        self.xsize = xsize
        self.ysize = ysize
        self.colour = colour
        self.table = table
        self.table.add_button(self)

    def name(self):
        return self._name

    def draw(self):
        surf = self.surface
        x = self.xval
        y = self.yval
        xsize = self.xsize
        ysize = self.ysize
        self._hitbox = Rect(x, y, xsize, ysize)
        pygame.draw.rect(surf, black, Rect(x, y, xsize, ysize), 4)
        xsize -= 4
        ysize -= 4
        pygame.draw.rect(surf, self.colour, Rect(x + 2, y + 2, xsize, ysize))
        fontsize = (8 * self.ysize) // 10
        font = pygame.font.Font(None, fontsize)
        text = font.render(self.name(), 1, black)
        textpos = text.get_rect()
        textpos = textpos.move(x + (self.xsize // 4), y + (self.ysize // 4))
        surf.blit(text, textpos)

    def activate(self, property, player):
        x = self.xval
        y = self.yval
        xsize = self.xsize
        ysize = self.ysize
        cur = pygame.mouse.get_pos()
        if x + xsize > cur[0] > x and y + ysize > cur[1] > y:
            if self.name() == "Kup":
                property.buy(player)
            if self.name() == "Sprzedaj":
                pass
            if self.name() == "Zastaw":
                pass
            if self.name() == "Kup domek":
                pass
            if self.name() == "Sprzedaj domek":
                pass


class Board:
    def __init__(self, background, color_out, color_in, size, cent_size, xcord, ycord, font_size):
        self.background = background
        self.size = size
        self.xcord = xcord
        self.ycord = ycord
        self.color_out = color_out
        self.color_in = color_in
        self.center_size = cent_size
        self.font_size = font_size
        self.corner_size = (self.size - self.center_size) // 2
        self.pons = []

    def add_pon(self, pon):
        self.pons.append(pon)

    def draw_pons(self):
        for pon in self.pons:
            pon.draw()

    def find_start_pon_position(self):
        for number, pon in enumerate(self.pons):
            x = 0
            y = 0
            number = number + 1
            if number % 2 == 0:
                x = 1
            if number > 2:
                y = 1
            pon.x_start += (20 * x)
            pon.y_start += (20 * y)

    def draw(self):
        surf = self.background
        left = self.xcord
        top = self.ycord
        size = self.size
        cent = self.center_size
        color_out = self.color_out
        color_in = self.color_in
        move = (size - cent) // 2
        pygame.draw.rect(surf, black, Rect(left, top, size, size), 4)
        pygame.draw.rect(surf, color_out, Rect(left + 2, top + 2, size - 4, size - 4))
        pygame.draw.rect(surf, color_in, Rect(left + move, top + move, cent, cent))
        pygame.draw.rect(surf, black, Rect(left + move - 2, top + move - 2, cent + 4, cent + 4), 4)
        self.draw_name()

    def draw_name(self):
        font = pygame.font.Font(None, self.font_size)
        text = font.render("Monopoly", 1, monopoly_txt)
        textpos = text.get_rect()
        textpos.centerx = self.background.get_rect().centerx
        y = self.ycord + (self.size // 2) - (self.font_size // 2)
        textpos = textpos.move(0, y)
        self.background.blit(text, textpos)

    def draw_corner(self, number, color):
        x, y = self.corner_cords(number)
        surf = self.background
        corner_size = (self.size - self.center_size + 4) // 2
        pygame.draw.rect(surf, color, Rect(x + 2, y + 2, corner_size - 2, corner_size - 2))
        pygame.draw.rect(surf, black, Rect(x, y, corner_size, corner_size), 2)

    def corner_cords(self, number):
        """Define cords of the chosen corner"""
        x = self.xcord
        y = self.ycord
        corner_size = (self.size - self.center_size) // 2
        move = self.center_size + corner_size - 2
        if number == 4:
            x += move
        if number == 2:
            y += move
        if number == 1:
            x += move
            y += move
        return x, y

    def draw_cards(self, database):
        background = self.background
        move = 556 + 596 + 104
        move_up = 776 - 596 - 100
        """Poziome rzędy"""
        for i in range(1, 10):
            move_blk = i * 66
            if database[10 - i].type() == "special":
                pygame.draw.rect(background, special, Rect(596 + move_blk, 776, 68, 104))
            pygame.draw.rect(background, black, Rect(596 + move_blk, 776, 68, 104), 2)
            if database[i + 20].type() == "special":
                pygame.draw.rect(background, special, Rect(596 + move_blk, move_up, 68, 104))
            pygame.draw.rect(background, black, Rect(596 + move_blk, move_up, 68, 104), 2)

        """Pionowe rzędy"""
        for i in range(1, 10):
            move_blk = i * 66
            if database[20 - i].type() == "special":
                pygame.draw.rect(background, special, Rect(560, move_up + 36 + move_blk, 104, 68))
            pygame.draw.rect(background, black, Rect(560, move_up + 36 + move_blk, 104, 68), 2)
            if database[i + 30].type() == "special":
                pygame.draw.rect(background, special, Rect(move, move_up + 36 + move_blk, 104, 68))
            pygame.draw.rect(background, black, Rect(move, move_up + 36 + move_blk, 104, 68), 2)


class player_pon(Board):
    def __init__(self, board, colour, owner):
        self.x_start = 1305
        self.y_start = 820
        self.board = board
        self._colour = colour
        self._owner = owner
        owner.set_pon(self)
        board.add_pon(self)
        self.board.find_start_pon_position()
        self.x = self.x_start
        self.y = self.y_start

    def colour(self):
        return self._colour

    def owner(self):
        return self._owner

    def draw(self):
        pygame.draw.rect(self.board.background, black, Rect(self.x, self.y, 14, 14), 2)
        pygame.draw.rect(self.board.background, self.colour(), Rect(self.x + 2, self.y + 2, 10, 10))

    def move(self):
        pos = self.owner().position()
        corner = self.board.corner_size
        if pos // 10 == 0:
            self.x = self.x_start - pos * self.board.center_size // 9
            self.y = self.y_start
        elif pos // 10 == 1:
            move = pos - 10
            self.x = self.x_start - self.board.center_size - corner
            self.y = self.y_start - move * self.board.center_size // 9
        elif pos // 10 == 2:
            move = pos - 20
            self.x = self.x_start - self.board.center_size - corner + pos * self.board.center_size // 9
            self.y = self.y_start - self.board.center_size - corner
        elif pos // 10 == 3:
            self.x = self.x_start
            self.y = self.y_start - self.board.center_size - corner + pos * self.board.center_size // 9

        


# xval = 1305
#         yval = 820
#         for number, player in enumerate(self.players):
#             x = 0
#             y = 0
#             number = number + 1
#             if number % 2 == 0:
#                 x = 1
#             if number > 2:
#                 y = 1
#             pygame.draw.rect(self.background, black, Rect(xval + (20 * x), yval + (20 * y), 14, 14), 2)
#             pygame.draw.rect(self.background, score, Rect(xval + 2 + (20 * x), yval + 2 + (20 * y), 10, 10))

class Positions:
    def __init__(self, surf, data, fontsize):
        self.surf = surf
        self.data = data
        self.fontsize = fontsize

    def draw(self):
        background = self.surf
        database = self.data
        font = pygame.font.Font(None, self.fontsize)
        for i in range(4):
            sqr = database[10 * i]
            text = font.render(sqr.name(), 1, black)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            text = pygame.transform.rotate(text, 45)
            text = pygame.transform.rotate(text, -90 * i)
            textpos = textpos.move(360, 825)
            if i == 1 or i == 2:
                textpos = textpos.move(-728, 0)
            if i == 2 or i == 3:
                textpos = textpos.move(0, -742)
            background.blit(text, textpos)

        """0 - 10"""
        font = pygame.font.Font(None, 15)
        for i in range(1, 10):
            move_txt = i * 66
            line = database[i].name()
            if database[i].type() == "property":
                pygame.draw.rect(background, black, Rect(1256 - move_txt, 776,  68, 25,), 2)
                pygame.draw.rect(background, database[i].area().colour(), Rect(1258 - move_txt, 778, 64, 21))
            text = font.render(line, 1, black)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos = textpos.move(332 - move_txt, 805)
            background.blit(text, textpos)

        """10 - 20"""
        for i in range(1, 10):
            move_txt = i * 66
            line = database[i + 10].name()
            if database[i + 10].type() == "property":
                pygame.draw.rect(background, black, Rect(639, 776 - move_txt, 25, 68), 2)
                pygame.draw.rect(background, database[i + 10].area().colour(), Rect(641, 778 - move_txt, 21, 64))
            text = font.render(line, 1, black)
            text = pygame.transform.rotate(text, 270)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos = textpos.move(-332, 790 - move_txt)
            background.blit(text, textpos)

        """20 - 30"""
        for i in range(1, 10):
            move_txt = i * 66
            line = database[i + 20].name()
            if database[i + 20].type() == "property":
                pygame.draw.rect(background, black, Rect(596 + move_txt, 159,  68, 25,), 2)
                pygame.draw.rect(background, database[i + 20].area().colour(), Rect(598 + move_txt, 161, 64, 21))
            text = font.render(line, 1, black)
            text = pygame.transform.rotate(text, 180)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos = textpos.move(-328 + move_txt, 145)
            background.blit(text, textpos)

        """30 - 40"""
        for i in range(1, 10):
            move_txt = i * 66
            line = database[i + 30].name()
            if database[i + 30].type() == "property":
                pygame.draw.rect(background, black, Rect(1256, 116 + move_txt, 25, 68), 2)
                pygame.draw.rect(background, database[i + 30].area().colour(), Rect(1258, 118 + move_txt, 21, 64))
            text = font.render(line, 1, black)
            text = pygame.transform.rotate(text, 90)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos = textpos.move(332, 125 + move_txt)
            background.blit(text, textpos)


class main():
    def __init__(self, players, database):
        self.players = players
        self.database = database
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption('Monopoly')
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((color))
        self.title = Player_name_title(self.background, title_color, 20, 70)
        self.board = Board(self.background, prop_color, deck_cen, 800, 596, 560, 80, 70)
        for player in self.players:
            pon = player_pon(self.board, pons_color, player)

    def clear(self):
        self.background.fill((color))

    def draw(self):
        self.clear()
        self.action_table = Action(self.background, "data", score, 400, 800, 100, 80, 100, 50)
        self.action_table.draw()
        self.board.draw()
        self.board.draw_corner(1, white)
        self.board.draw_corner(2, white)
        self.board.draw_corner(3, white)
        self.board.draw_corner(4, white)
        self.board.draw_cards(self.database)
        position = Positions(self.background, self.database, 20)
        position.draw()
        self.score_table = Score(self.players, self.background, score, 400, 800, 1420, 80, 100, 50)
        self.score_table.draw()
        self.score_table.draw_text()
        self.board.draw_pons()
        pygame.display.flip()

    def draw_buttons(self, player):
        self.buttons(player)
        for number, button in enumerate(self.act_buttons):
            move = 60 * number
            bt = Button(button, self.background, self.action_table, 150 + move, 220, 50, 20, button_color)
            bt.draw()
            self.screen.blit(self.background, (0, 0))
            pygame.display.flip()

    def draw_title(self, player):
        self.title.draw(player)
        pygame.display.flip()

    def buttons(self, player):
        list_of_buttons = []
        database = self.database
        active_sqr = database[player.position()]
        if player.debit():
            if player.value_of_properties() + player.money() < 0:
                player.set_inactive()
            else:
                list_of_buttons.append("Sprzedaj")
                list_of_buttons.append("Zastaw")
                list_of_buttons.append("Sprzedaj domek")
        elif active_sqr.type() == "property":
            if active_sqr.owner() == player:
                if active_sqr.area().check_if_fully_occupied(player):
                    if not player.check_debit(active_sqr.check_house_cost()):
                        list_of_buttons.append("Kup domek")
            if not active_sqr.owner():
                if not player.check_debit(active_sqr.price()):
                    list_of_buttons.append("Kup")
                    list_of_buttons.append("Pomiń")
        self.act_buttons = list_of_buttons

    def do_action(self, player, property):
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    paused = False
                    for button in self.action_table.buttons():
                        button.activate(property, player)
        pygame.display.flip()
    