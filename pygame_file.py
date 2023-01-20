import pygame
from monopoly_player import Player
from monopoly_property import Property
from pygame.locals import *
from pygame.locals import Rect
from monopoly_exeptions import WrongInputError, ZeroThrowsError, NotEnoughtMoneyError


"""Colours"""
blue = (66, 135, 245)
red = (153, 28, 28)
yellow = (184, 150, 48)
green = (88, 184, 48)
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
    def __init__(self, backgr, color, sizex, sizey,
                 xcord, ycord, title_hight, font, name):
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
    def __init__(self, players, backgr, color, sizex, sizey,
                 xcord, ycord, title_hight, font):
        super().__init__(backgr, color, sizex, sizey, xcord, ycord,
                         title_hight, font, "Players")
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
            y_cord = self.ycord + self.title_hight + 50 + move_dw
            textpos = textpos.move(self.xcord + 50, y_cord)
            self.background.blit(text, textpos)


class Action(Side_Table):
    def __init__(self, backgr, data, color, sizex,
                 sizey, xcord, ycord, title_hight, font):
        super().__init__(backgr, color, sizex, sizey,
                         xcord, ycord, title_hight, font, "Action")
        self.data = data
        self._buttons = []

    def add_button(self, button):
        self._buttons.append(button)

    def buttons(self):
        return self._buttons


class Button(Action):
    def __init__(self, name, property, surf, table, xval, yval, xsize, ysize, colour):
        self.property = property
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
        if self.property:
            text = font.render(f"{self.name()}: {self.property.name()}", 1, black)
        else:
            text = font.render(self.name(), 1, black)
        textpos = text.get_rect()
        textpos = textpos.move(x + (self.xsize // 4), y + (self.ysize // 4))
        surf.blit(text, textpos)

    def activate(self, player):
        property = self.property
        x = self.xval
        y = self.yval
        xsize = self.xsize
        ysize = self.ysize
        cur = pygame.mouse.get_pos()
        if x + xsize > cur[0] > x and y + ysize > cur[1] > y:
            name = self.name()
            if name == "Rzuć kośćmi":
                x, y = player.throw_dices()
                fontsize = (8 * self.ysize) // 10
                font = pygame.font.Font(None, fontsize)
                line = f'{x}  {y}'
                text = font.render(line, 1, black)
                textpos = text.get_rect()
                textpos = textpos.move(x + self.xsize + 20, y + self.ysize + 20)
                surf = self.surface
                surf.blit(text, textpos)
            if name == "Kup":
                try:
                    property.buy(player)
                except:
                    pass
            if name == "Sprzedaj":
                try:
                    property.sell()
                except:
                    pass
            if name == "Zapłać":
                    property.pay_rent(player)
            if name == "Zastaw":
                try:
                    property.set_pledge()
                except:
                    pass
            if name == "Cofnij zastaw":
                try:
                    property.set_pledge(False)
                except:
                    pass
            if name == "Kup domek":
                try:
                    property.buy_house()
                except:
                    pass
            if name == "Sprzedaj domek":
                try:
                    property.sell_house()
                except:
                    pass


class Board:
    def __init__(self, background, color_out, color_in, size,
                 cent_size, xcord, ycord, font_size):
        self.background = background
        self.size = size
        self.xcord = xcord
        self.ycord = ycord
        self.color_out = color_out
        self.color_in = color_in
        self.center_size = cent_size
        self.font_size = font_size
        self.corner_size = (self.size - self.center_size) // 2
        self.pawns = []

    def add_pawn(self, pawn):
        self.pawns.append(pawn)

    def draw_pawns(self):
        for pawn in self.pawns:
            pawn.draw()

    def find_start_pawn_position(self):
        for number, pon in enumerate(self.pawns):
            number += 1
            if number % 2 == 0:
                pon.x_start += 20
            if number > 2:
                pon.y_start += 20

    def draw(self):
        surf = self.background
        left = self.xcord
        top = self.ycord
        size = self.size
        cent = self.center_size
        color_out = self.color_out
        color_in = self.color_in
        move = (size - cent) // 2
        black_rec = Rect(left, top, size, size)
        out_rec = Rect(left + 2, top + 2, size - 4, size - 4)
        in_rect = Rect(left + move, top + move, cent, cent)
        sec_blk_rec = Rect(left + move - 2, top + move - 2, cent + 4, cent + 4)
        pygame.draw.rect(surf, black, black_rec, 4)
        pygame.draw.rect(surf, color_out, out_rec)
        pygame.draw.rect(surf, color_in, in_rect)
        pygame.draw.rect(surf, black, sec_blk_rec, 4)
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
        color_rec = Rect(x + 2, y + 2, corner_size - 2, corner_size - 2)
        black_rec = Rect(x, y, corner_size, corner_size)
        pygame.draw.rect(surf, color, color_rec)
        pygame.draw.rect(surf, black, black_rec, 2)

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
            rec = Rect(596 + move_blk, 776, 68, 104)
            rec2 = Rect(596 + move_blk, move_up, 68, 104)
            if database[10 - i].type() == "special":
                pygame.draw.rect(background, special, rec)
            pygame.draw.rect(background, black, rec, 2)
            if database[i + 20].type() == "special":
                pygame.draw.rect(background, special, rec2)
            pygame.draw.rect(background, black, rec2, 2)

        """Pionowe rzędy"""
        for i in range(1, 10):
            move_blk = i * 66
            if database[20 - i].type() == "special":
                pygame.draw.rect(background, special,
                                 Rect(560, move_up + 36 + move_blk, 104, 68))
            pygame.draw.rect(background, black,
                             Rect(560, move_up + 36 + move_blk, 104, 68), 2)
            if database[i + 30].type() == "special":
                pygame.draw.rect(background, special,
                                 Rect(move, move_up + 36 + move_blk, 104, 68))
            pygame.draw.rect(background, black,
                             Rect(move, move_up + 36 + move_blk, 104, 68), 2)


class player_pawn(Board):
    def __init__(self, board, colour, owner):
        self.x_start = board.xcord + board.size - 55
        self.y_start = board.ycord + board.size - 55
        self.board = board
        self._colour = colour
        self._owner = owner
        owner.set_pawn(self)
        board.add_pawn(self)
        self.board.find_start_pawn_position()
        self.x = self.x_start
        self.y = self.y_start

    def colour(self):
        return self._colour

    def owner(self):
        return self._owner

    def draw(self):
        self.move()
        black_rect = Rect(self.x, self.y, 14, 14)
        color_rect = Rect(self.x + 2, self.y + 2, 10, 10)
        pygame.draw.rect(self.board.background, black, black_rect, 2)
        pygame.draw.rect(self.board.background, self.colour(), color_rect)

    def move(self):
        pos = self.owner().position()
        x_for_1side = 2 * self.board.xcord - self.x_start + self.board.size
        y_for_2side = 2 * self.board.ycord - self.y_start + self.board.size
        if pos // 10 == 0 and pos != 0:
            self.x = self.x_start - 20 - (pos * self.board.center_size // 9)
            self.y = self.y_start
        elif pos // 10 == 1:
            pos_diff = pos - 10
            self.x = 2 * self.board.xcord - self.x_start + self.board.size
            self.y = self.y_start - pos_diff * self.board.center_size // 9
        if pos // 10 == 2:
            pos_diff = pos % 20
            move = (pos_diff * self.board.center_size // 9)
            self.x = x_for_1side + move
            self.y = 2 * self.board.ycord - self.y_start + self.board.size
        elif pos // 10 == 3:
            if pos == 30:
                pos += 1
            pos_diff = pos % 30
            move = (pos_diff * self.board.center_size // 9)
            self.x = self.x_start
            self.y = y_for_2side + move


class Positions:
    def __init__(self, surf, data, fontsize):
        self.surf = surf
        self.data = data
        self.fontsize = fontsize

    def draw(self):
        surf = self.surf
        database = self.data
        font = pygame.font.Font(None, self.fontsize)
        for i in range(4):
            sqr = database[10 * i]
            text = font.render(sqr.name(), 1, black)
            textpos = text.get_rect()
            textpos.centerx = surf.get_rect().centerx
            text = pygame.transform.rotate(text, 45)
            text = pygame.transform.rotate(text, -90 * i)
            textpos = textpos.move(360, 825)
            if i == 1 or i == 2:
                textpos = textpos.move(-728, 0)
            if i == 2 or i == 3:
                textpos = textpos.move(0, -742)
            surf.blit(text, textpos)

        """0 - 10"""
        font = pygame.font.Font(None, 15)
        for i in range(1, 10):
            move_txt = i * 66
            line = database[i].name()
            if database[i].type() == "property":
                black_re = Rect(1256 - move_txt, 776, 68, 25,)
                inside_re = Rect(1258 - move_txt, 778, 64, 21)
                pygame.draw.rect(surf, black, black_re, 2)
                pygame.draw.rect(surf, database[i].area().colour(), inside_re)
                property = database[i]
                if property.owner():
                    houses = property.houses()
                    if property.houses() != 0:
                        line2 = f"{property.owner().name()}: {houses}"
                    else:
                        line2 = database[i].owner().name()
                    text2 = font.render(line2, 1, black)
                    textpos = text2.get_rect()
                    textpos.centerx = surf.get_rect().centerx
                    textpos = textpos.move(332 - move_txt, 835)
                    surf.blit(text2, textpos)
                    line3 = f"Czynsz: {property.rent()}"
                else:
                    line3 = f"Cena: {property.price()}"
                text3 = font.render(line3, 1, black)
                textpos = text3.get_rect()
                textpos.centerx = surf.get_rect().centerx
                textpos = textpos.move(332 - move_txt, 855)
                surf.blit(text3, textpos)
            text = font.render(line, 1, black)
            textpos = text.get_rect()
            textpos.centerx = surf.get_rect().centerx
            textpos = textpos.move(332 - move_txt, 805)
            surf.blit(text, textpos)

        """10 - 20"""
        for i in range(1, 10):
            move_txt = i * 66
            line = database[i + 10].name()
            if database[i + 10].type() == "property":
                black_rec = Rect(639, 776 - move_txt, 25, 68)
                color = Rect(641, 778 - move_txt, 21, 64)
                pygame.draw.rect(surf, black, black_rec, 2)
                pygame.draw.rect(surf, database[i + 10].area().colour(), color)
                property = database[i + 10]
                if property.owner():
                    houses = property.houses()
                    if property.houses() != 0:
                        line2 = f"{property.owner().name()}: {houses}"
                    else:
                        line2 = property.owner().name()
                    text2 = font.render(line2, 1, black)
                    text2 = pygame.transform.rotate(text2, 270)
                    textpos = text2.get_rect()
                    textpos.centerx = surf.get_rect().centerx
                    textpos = textpos.move(-362, 790 - move_txt)
                    surf.blit(text2, textpos)
                    line3 = f"Rent: {property.rent()}"
                else:
                    line3 = f"Price: {property.price()}"
                text3 = font.render(line3, 1, black)
                text3 = pygame.transform.rotate(text3, 270)
                textpos = text3.get_rect()
                textpos.centerx = surf.get_rect().centerx
                textpos = textpos.move(-382, 790 - move_txt)
                surf.blit(text3, textpos)
            text = font.render(line, 1, black)
            text = pygame.transform.rotate(text, 270)
            textpos = text.get_rect()
            textpos.centerx = surf.get_rect().centerx
            textpos = textpos.move(-332, 790 - move_txt)
            surf.blit(text, textpos)

        """20 - 30"""
        for i in range(1, 10):
            move_txt = i * 66
            line = database[i + 20].name()
            if database[i + 20].type() == "property":
                black_rec = Rect(596 + move_txt, 159,  68, 25,)
                inside_rec = Rect(598 + move_txt, 161, 64, 21)
                pygame.draw.rect(surf, black, black_rec, 2)
                pygame.draw.rect(surf, database[i + 20].area().colour(),
                                 inside_rec)
                property = database[i + 20]
                if property.owner():
                    houses = property.houses()
                    if property.houses() != 0:
                        line2 = f"{property.owner().name()}: {houses}"
                    else:
                        line2 = property.owner().name()
                    text2 = font.render(line2, 1, black)
                    text2 = pygame.transform.rotate(text2, 180)
                    textpos = text2.get_rect()
                    textpos.centerx = surf.get_rect().centerx
                    textpos = textpos.move(-328 + move_txt, 115)
                    surf.blit(text2, textpos)
                    line3 = f"Rent: {property.rent()}"
                else:
                    line3 = f"Price: {property.price()}"
                text3 = font.render(line3, 1, black)
                text3 = pygame.transform.rotate(text3, 180)
                textpos = text3.get_rect()
                textpos.centerx = surf.get_rect().centerx
                textpos = textpos.move(-328 + move_txt, 95)
                surf.blit(text3, textpos)
            text = font.render(line, 1, black)
            text = pygame.transform.rotate(text, 180)
            textpos = text.get_rect()
            textpos.centerx = surf.get_rect().centerx
            textpos = textpos.move(-328 + move_txt, 145)
            surf.blit(text, textpos)

        """30 - 40"""
        for i in range(1, 10):
            move_txt = i * 66
            line = database[i + 30].name()
            if database[i + 30].type() == "property":
                black_rec = Rect(1256, 116 + move_txt, 25, 68)
                inside_rec = Rect(1258, 118 + move_txt, 21, 64)
                rect_color = database[i + 30].area().colour()
                pygame.draw.rect(surf, black, black_rec, 2)
                pygame.draw.rect(surf, rect_color, inside_rec)
                property = database[i + 30]
                if property.owner():
                    houses = property.houses()
                    if property.houses() != 0:
                        line2 = f"{property.owner().name()}: {houses}"
                    else:
                        line2 = property.owner().name()
                    text2 = font.render(line2, 1, black)
                    text2 = pygame.transform.rotate(text2, 90)
                    textpos = text2.get_rect()
                    textpos.centerx = surf.get_rect().centerx
                    textpos = textpos.move(362, 125 + move_txt)
                    surf.blit(text2, textpos)
                    line3 = f"Rent: {property.rent()}"
                else:
                    line3 = f"Price: {property.price()}"
                text3 = font.render(line3, 1, black)
                text3 = pygame.transform.rotate(text3, 90)
                textpos = text3.get_rect()
                textpos.centerx = surf.get_rect().centerx
                textpos = textpos.move(382, 125 + move_txt)
                surf.blit(text3, textpos)
            text = font.render(line, 1, black)
            text = pygame.transform.rotate(text, 90)
            textpos = text.get_rect()
            textpos.centerx = surf.get_rect().centerx
            textpos = textpos.move(332, 125 + move_txt)
            surf.blit(text, textpos)


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
        back = self.background
        self.title = Player_name_title(back, title_color, 20, 70)
        self.board = Board(back, prop_color, deck_cen, 800, 596, 560, 80, 70)
        self.act_buttons = []
        pawns_colors = [red, blue, yellow, green]
        for number, player in enumerate(self.players):
            pawn_color = pawns_colors[number]
            pawn = player_pawn(self.board, pawn_color, player)

    def add_button(self, name):
        self.act_buttons.append(name)

    def clear(self):
        self.background.fill((color))
        self.act_buttons = []

    def draw(self):
        self.clear()
        self.action_table = Action(self.background, "data", score, 400, 800,
                                   100, 80, 100, 50)
        self.action_table.draw()
        self.board.draw()
        self.board.draw_corner(1, white)
        self.board.draw_corner(2, white)
        self.board.draw_corner(3, white)
        self.board.draw_corner(4, white)
        self.board.draw_cards(self.database)
        position = Positions(self.background, self.database, 20)
        position.draw()
        srf = self.background
        score_tb = Score(self.players, srf, score, 400, 800, 1420, 80, 100, 50)
        self.score_table = score_tb
        self.score_table.draw()
        self.score_table.draw_text()
        self.board.draw_pawns()
        pygame.display.flip()

    def draw_buttons(self, player, problem):
        self.buttons(player, problem)
        if len(self.act_buttons) != 0:
            for number, button in enumerate(self.act_buttons):
                name, property = button
                move = 30 * number
                bt = Button(name, property, self.background, self.action_table,
                            150, 220 + move, 300, 20, button_color)
                bt.draw()
                self.screen.blit(self.background, (0, 0))
                pygame.display.flip()

    def draw_title(self, player):
        self.title.draw(player)
        pygame.display.flip()

    def buttons(self, player, problem):
        list_of_buttons = []
        database = self.database
        active_sqr = database[player.position()]
        if problem:
            if not len(player.properties()) == 0:
                for property in player.properties():
                    if property.houses() != 0:
                        list_of_buttons.append(("Sprzedaj domek", property))
                    else:
                        list_of_buttons.append(("Sprzedaj", property))
                        if not property.pledge():
                            list_of_buttons.append(("Zastaw", property))
            else:
                player.set_inactive()
        elif active_sqr.type() == "property":
            if active_sqr.owner() == player:
                if active_sqr.pledge():
                    list_of_buttons.append(("Cofnij zastaw", property))
                else:
                    if active_sqr.area().check_if_fully_occupied(player):
                        if not player.check_debit(active_sqr.check_house_cost()):
                            list_of_buttons.append(("Kup domek", active_sqr))
            if not active_sqr.owner():
                if not player.check_debit(active_sqr.price()):
                    list_of_buttons.append(("Kup", active_sqr))
                list_of_buttons.append(("Pomiń", None))
        self.act_buttons.extend(list_of_buttons)

    def do_action(self, player, problem=False):
        self.draw_buttons(player, problem)
        buttons = self.act_buttons
        paused = True
        while paused and len(buttons) != 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    paused = False
                    for button in self.action_table.buttons():
                        button.activate(player)
                    self.act_buttons = []
        pygame.display.flip()
