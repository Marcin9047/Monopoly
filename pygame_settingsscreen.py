import pygame
from monopoly_player import Player
from monopoly_property import Property
from pygame.locals import *
from pygame.locals import Rect
from shapely.geometry import Point, Polygon


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

pawns = [blue, red, yellow, green, black, white]

class Add_player():
    def __init__(self, screen, mode):
        self.surf = screen.backgr
        self.scr = screen.screen
        self.mode = mode
        self.new_pos = 200

    def draw_new(self):
        player_rec = Rect(50, self.new_pos, 500, 100)
        pygame.draw.rect(self.surf, yellow, player_rec)
        pygame.draw.rect(self.surf, black, player_rec, 2)
        self.new_pos = self.new_pos + 200
        self.scr.blit(self.surf, (0, 0))
        pygame.display.flip()

    def players_list(self):
        self.surf.fill((255, 255, 255))
        pygame.display.flip()
        self.done_button = Rect(50, 600, 300, 100)
        pygame.draw.rect(self.surf, black, self.done_button)
        self.scr.blit(self.surf, (0, 0))
        pygame.display.flip()

        self.all_done = False
        self.down = 0
        self.act_colors = pawns

        self.players = []
        self.pawns = []

        while self.all_done is False:
            self.pawns_inx = 0
            self.draw_add()
            self.down += 1
        return self.players, self.pawns



    def draw_add(self):
        
        not_done = True
                # basic font for user typed
        screen = self.scr
        surf = self.surf
        base_font = pygame.font.Font(None, 32)
        user_text = ''
        
        # create rectangle
        input_rect = pygame.Rect(200, 200 + 200 * self.down, 140, 32)
        ok_rect = pygame.Rect(500, 200 + 200 * self.down, 30, 30)
        color_rect = pygame.Rect(400, 200 + 200 * self.down, 30, 30)


        right_size = ((435, 200 + 200 * self.down), (435, 226 + 200 * self.down), (455, 213 + 200 * self.down))
        left_size = ((395, 200 + 200 * self.down), (395, 226 + 200 * self.down), (375, 213 + 200 * self.down))
        right_arrow = Polygon([(435, 200 + 200 * self.down), (435, 226 + 200 * self.down), (455, 213 + 200 * self.down)])
        left_arrow = Polygon([(395, 200 + 200 * self.down), (395, 226 + 200 * self.down), (375, 213 + 200 * self.down)])
        

        
        
        # color_active stores color(lightskyblue3) which
        # gets active when input box is clicked by user
        color_active = pygame.Color('lightskyblue3')
        
        # color_passive store color(chartreuse4) which is
        # color of input box.
        color_passive = pygame.Color('chartreuse4')
        color = color_passive
        
        active = False
        screen.fill((255, 255, 255))

        while not_done:
            player_color = self.act_colors[self.pawns_inx]
            for event in pygame.event.get():
        
            # if user types QUIT then the screen will close
                if event.type == pygame.QUIT:
                    pygame.quit()
        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(not_done)
                    if input_rect.collidepoint(event.pos):
                        active = True
                    elif ok_rect.collidepoint(event.pos):
                        not_done = False
                        active = False
                        user = Player(user_text, 1500)
                        self.players.append(user)
                        self.pawns.append(player_color)
                        colors = []
                        for i in self.act_colors:
                            if i != self.act_colors[self.pawns_inx]:
                                colors.append(i)
                        self.act_colors = colors
                        print(user)
                        print(not_done)
                    elif self.done_button.collidepoint(event.pos):
                        not_done = False
                        self.all_done = True
                        pygame.quit()
                    elif left_arrow.contains(Point(event.pos)):
                        if self.pawns_inx == 0:
                            self.pawns_inx = len(self.act_colors) - 1
                        else:
                            self.pawns_inx -= 1
                        print("Wyszło")
                    elif right_arrow.contains(Point(event.pos)):
                        if self.pawns_inx == len(self.act_colors) - 1:
                            self.pawns_inx = 0
                        else:
                            self.pawns_inx += 1
                        print("Wyszło2")

                    else:
                        active = False
        
                if event.type == pygame.KEYDOWN and active:
        
                    # Check for backspace
                    if event.key == pygame.K_BACKSPACE:
        
                        # get text input from 0 to -1 i.e. end.
                        user_text = user_text[:-1]
        
                    # Unicode standard is used for string
                    # formation
                    elif len(user_text) < 10:
                        user_text += event.unicode
            
            # it will set background color of screen
            if self.all_done is not True:
                screen.fill((255, 255, 255)) 
                if active:
                    color = color_active
                else:
                    color = color_passive
                    
                # draw rectangle and argument passed which should
                # be on screen
                pygame.draw.rect(surf, color, input_rect)
                pygame.draw.rect(surf, color, ok_rect)
                pygame.draw.rect(surf, player_color, color_rect)

                
                pygame.draw.polygon(self.surf, black, right_size)
                pygame.draw.polygon(self.surf, black, left_size)
                

                text_surface = base_font.render(user_text, True, black)
                
                # render at position stated in arguments
                surf.blit(text_surface, (input_rect.x+5, input_rect.y+5))
                screen.blit(surf, (0, 0))
                
                # # set width of textfield so that text cannot get
                # # outside of user's text input
                # input_rect.w = max(100, text_surface.get_width()+10)
                
                # display.flip() will update only a portion of the
                # screen to updated, not full area
                pygame.display.flip()
                
            


class Mode_screen():
    def __init__(self, screen):
        self.surf = screen.backgr
        self._mode_buttons = []

    def buttons(self):
        return self._mode_buttons

    def draw_welcom_title(self):
            fontsize = 75
            font = pygame.font.Font(None, fontsize)
            text = font.render("Welcome to Monopoly", 1, black)
            textpos = text.get_rect()
            textpos = textpos.move(35, 100)
            self.surf.blit(text, textpos)

    def draw_please_select(self):
            fontsize = 30
            font = pygame.font.Font(None, fontsize)
            text = font.render("Please select your game mode:", 1, black)
            textpos = text.get_rect()
            textpos = textpos.move(150, 180)
            self.surf.blit(text, textpos)

    def draw_mods_names(self):
            surf = self.surf
            fontsize = 60
            font = pygame.font.Font(None, fontsize)
            single = font.render("Singleplayer", 1, black)
            multi = font.render("Multiplayer", 1, black)
            team = font.render("Team battle", 1, black)

            textpos = single.get_rect()
            textpos = textpos.move(165, 325)
            surf.blit(single, textpos)
            pygame.draw.line(surf, black, [130, 370], [450, 370], 1)

            textpos = multi.get_rect()
            textpos = textpos.move(180, 525)
            surf.blit(multi, textpos)
            pygame.draw.line(surf, black, [130, 570], [450, 570], 1)

            textpos = team.get_rect()
            textpos = textpos.move(170, 725)
            surf.blit(team, textpos)
            pygame.draw.line(surf, black, [130, 770], [450, 770], 1)


    def draw_mods(self):
        surf = self.surf
        self.draw_welcom_title()
        self.draw_please_select()
        for i in range(3):
            mode_rec = Rect(50, 300 + 200 * i, 500, 100)
            self._mode_buttons.append(mode_rec)
            pygame.draw.rect(surf, blue, mode_rec)
            pygame.draw.rect(surf, black, mode_rec, 2)
        self.draw_mods_names()


class Setting_screen():
  
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 900))
        pygame.display.set_caption('Monopoly')
        self.backgr = pygame.Surface(self.screen.get_size())
        self.backgr = self.backgr.convert()
        self.backgr.fill((green))

    def draw(self):
        self.mods = Mode_screen(self)
        self.player_tab = Add_player(self, "multiplayer")
        self.mods.draw_mods()
        self.screen.blit(self.backgr, (0, 0))
        pygame.display.flip()
        self.do_action()


    def do_action(self, problem=False):
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    for button in self.mods.buttons():
                        if button.collidepoint(event.pos):
                            paused = False

# test2 = True

# test = Setting_screen()
# test3 = Mode_screen(test)
# test3.draw_mods()
# test.draw()
# test.backgr.fill((color))
# test.screen.blit(test.backgr, (0, 0))
# pygame.display.flip()
# test.player_tab.players_list()
# # test.player_tab.draw_new()
# # test.player_tab.draw_new()
# print("zupa")
# test.do_action()