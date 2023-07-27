from monopoly_logs import Database
from monopoly_player import Player
from pygame_file import main
from monopoly_exeptions import NotEnoughtMoneyError

prop = "monopoly/database.json"
spc = "monopoly/Special_cards_database.json"
database = Database(prop, spc)
squares = database.sort_database()


class Game:
    def __init__(self, players, database):
        self._active = True
        self._players = players
        self._database = database

    def get_position(self, i):
        return self._database[i]

    def isactive(self):
        return self._active

    def database(self):
        return self._database

    def shutdown(self):
        self._active = False

    def players(self):
        return self._players

    def play(self):
        inter = main(self.players(), self.database())
        inter.draw()
        while self.isactive():
            for player in self.players():
                if player.isactive():
                    inter.draw()
                    while player.ready_to_play():
                        inter.active_sqr = inter.database[player.position()]
                        inter.active_sqr.set_active()
                        inter.draw()
                        inter.draw_title(player)
                        inter.add_button(("Rzuć kośćmi", None))
                        inter.do_action(player)
                        inter.last_sqr.set_inactive()
                        inter.active_sqr.set_active()
                        inter.draw()
                        if inter.active_sqr.type() != "property":
                            unsolved = True
                            while unsolved:
                                try:
                                    inter.add_button(("Wykonaj", inter.active_sqr))
                                    inter.do_action(player)
                                    inter.active_sqr.do_action(player)
                                    unsolved = False
                                except NotEnoughtMoneyError:
                                    inter.draw()
                                    inter.do_action(player, True)
                        elif inter.active_sqr.type() == "property":
                            owner = inter.active_sqr.owner()
                            if owner is not None and owner != player:
                                unsolved = True
                                while unsolved:
                                    inter.draw()
                                    try:
                                        inter.add_button(("Zapłać", inter.active_sqr))
                                        inter.do_action(player)
                                        unsolved = False
                                    except NotEnoughtMoneyError:
                                        inter.draw()
                                        inter.do_action(player, True)
                        inter.draw()
                        inter.draw_title(player)
                        inter.do_action(player)
                        inter.active_sqr.set_inactive()
                    player.subtract_pause()
                    if player.pause() == 0:
                        player.add_throws()
                else:
                    self._players.remove(player)
            if len(self.players()) == 1:
                for player in self.players():
                    print(f'{player.name()} is a winner')


def players():
    players = []
    while True:
        player = input("Wprowadź nazwę gracza: ")
        if not player:
            break
        player_cls = Player(player, 1500)
        players.append(player_cls)
    return players


x = players()
game = Game(x, squares)
game.play()
