import pygame
import sys
from pygame.locals import *
from monopoly_exeptions import WrongInputError, ZeroThrowsError, NotEnoughtMoneyError

class Button:
    def __init__(self, name, xval, yval, xsize, ysize, colour):
        self._name = name
        self.xval = xval
        self.yval = yval
        self.xsize = xsize
        self.ysize = ysize
        self.colour = colour

    def draw(self, surface):
        self._hitbox = Rect(self.xval, self.yval, self.xsize, self.ysize)
        pygame.draw.rect(surface, black, Rect(self.xval, self.yval, self.xsize, self.ysize), 4)
        pygame.draw.rect(surface, self.colour, Rect(self.xval + 2, self.yval + 2, self.xsize -4, self.ysize - 4))
        fontsize = (8 * self.ysize) // 10
        font = pygame.font.Font(None, fontsize)
        text = font.render(self.name(), 1, black)
        textpos = text.get_rect()
        textpos = textpos.move(self.xval + (self.xsize // 4) , self.yval + (self.ysize // 4))
        surface.blit(text, textpos)

    def name(self):
        return self._name

    def hitbox(self):
         return self._hitbox


"""Colours"""
black = (0, 0, 0)
white = (255, 255, 255)
monopoly_txt = (255, 153, 255)
special = (155, 155, 155)
score = (173, 186, 137)
color = (250, 235, 215)
prop_color= (210, 210, 210)
deck_cen = (80, 80, 80)

def player_name_clr(background):
    pygame.draw.rect(background, black, Rect(600, 20, 600, 50))
    pygame.draw.rect(background, color, Rect(600, 20, 600, 50))


def Player_name(player, background):
    font = pygame.font.Font(None, 50)
    player_name_clr(background)
    text = font.render(player.name(), 1, (169, 218, 184))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos = textpos.move(0, 20)
    background.blit(text, textpos)

def clear_score(background):
    pygame.draw.rect(background, score, Rect(1425, 200, 380, 650))


def Player_info(players, background):
        font = pygame.font.Font(None, 30)
        clear_score(background)
        for number, player in enumerate(players):
            move_dw = 50 * number
            if player.pause() != 0:
                line = f'{player.name()}:  {player.money()}    {player.pause()}'
            else:
                line = f'{player.name()}:  {player.money()}'
            text = font.render(line, 1, black)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos = textpos.move( 600, 200 + move_dw)
            background.blit(text, textpos)

def draw_card(background):
    pygame.draw.rect(background, black, Rect(174, 410, 250, 400), 4)

def main(players, database):
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption('Monopoly')
    # pygame.display.toggle_fullscreen()

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((color))
    

    pygame.draw.rect(background, black, Rect(560, 80, 800, 800), 4)
    pygame.draw.rect(background, prop_color, Rect(562, 82, 796, 796))
    pygame.draw.rect(background, deck_cen, Rect(662, 182, 596, 596))

    pygame.draw.rect(background, black, Rect(560, 776, 104, 104), 2)
    pygame.draw.rect(background, special, Rect(560 + 2, 776 + 2, 100, 100))
    move = 556 + 596 + 104
    pygame.draw.rect(background, black, Rect(move, 776, 104, 104), 2)
    pygame.draw.rect(background, special, Rect(move + 2, 776 + 2, 100, 100))
    move_up = 776 - 596 - 100
    pygame.draw.rect(background, black, Rect(560, move_up, 104, 104), 2)
    pygame.draw.rect(background, special, Rect(560 + 2, move_up + 2, 100, 100))
    pygame.draw.rect(background, black, Rect(move, move_up, 100, 104), 2)
    pygame.draw.rect(background, special, Rect(move + 2, move_up + 2, 100, 100))
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

    

    """Square names"""

    """corners"""
    font = pygame.font.Font(None, 20)
    
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
        textpos = textpos.move( 332 - move_txt, 805)
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
        textpos = textpos.move( -332, 790 - move_txt)
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
        textpos = textpos.move( -328 + move_txt, 145)
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
    
    

    """Score_tabel"""
    
    pygame.draw.rect(background, score, Rect(1420, 80, 400, 800))
    pygame.draw.rect(background, score, Rect(100, 80, 400, 800))
    pygame.draw.rect(background, black, Rect(1420, 80, 400, 800), 3)
    pygame.draw.rect(background, black, Rect(100, 80, 400, 800), 3)
    pygame.draw.rect(background, black, Rect(1420, 80, 400, 100), 3)
    pygame.draw.rect(background, black, Rect(100, 80, 400, 100), 3)

    """Players title"""
    font = pygame.font.Font(None, 50)
    text = font.render("Players", 1, black)
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos = textpos.move(650, 110)
    background.blit(text, textpos)

    """Action title"""
    font = pygame.font.Font(None, 50)
    text = font.render("Action", 1, black)
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos = textpos.move(-660, 110)
    background.blit(text, textpos)

    draw_card(background)
    """Game name"""
    
    font = pygame.font.Font(None, 90)
    text = font.render("Monopoly", 1, monopoly_txt)
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos = textpos.move(0, 430)
    background.blit(text, textpos)

    """Pons position"""
    xval = 1305
    yval = 820
    for number, player in enumerate(players):
        x = 0
        y = 0
        number = number + 1
        if number % 2 == 0:
            x = 1
        if number > 2:
            y = 1
        pygame.draw.rect(background, black, Rect(xval + (20 * x), yval + (20 * y), 14, 14), 2)
        pygame.draw.rect(background, score, Rect(xval + 2 + (20 * x), yval + 2 + (20 * y), 10, 10))

    """Pons move"""
    clock = pygame.time.Clock()
    FPS = 30
    
    bt = Button("Kup", 50, 400, 100, 20, white)
    bt.draw(background)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Event loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        for player in players:
            Player_name(player, background)
            Player_info(players, background)
            screen.blit(background, (0, 0))
            pygame.display.flip()
            while player.throws() != 0 and player.pause() == 0:
                Player_info(players, background)
                try:
                    player.throw_dices()
                    pos = player.position()
                    active_sqr = database[pos]
                    if active_sqr.type() == "special":
                        active_sqr.do_action(player)
                    elif active_sqr.type() == "property":
                        if active_sqr.owner() != None and active_sqr.owner() != player:
                            print(active_sqr.owner().name())
                            active_sqr.pay_rent(player)
                            if player.bankrut():
                                players.remove(player)
                        elif active_sqr.owner() != player:
                            print("Co chcesz zrobić?")
                            while True:
                                for event in pygame.event.get():
                                    if event.type == MOUSEBUTTONDOWN and bt.hitbox().collidepoint(pygame.mouse.get_pos()):
                                        try:
                                            active_sqr.buy(player)
                                            pygame.display.flip()
                                        except NotEnoughtMoneyError():
                                            print("Nie posiadasz wystarczających funduszy")
                        elif active_sqr.area().check_if_fully_occupied(player):
                            action = input("Możesz kupić domek, chcesz?: ")
                            if action == "Tak":
                                try:
                                    active_sqr.buy_house()
                                except NotEnoughtMoneyError():
                                    print("Nie posiadasz wystarczających funduszy")
                except:
                    break
            player.subtract_pause()
            if player.pause() == 0:
                player.add_throws()

        # screen.blit(background, (0, 0))
        # pygame.display.flip()



    
    


if __name__ == '__main__': main()

