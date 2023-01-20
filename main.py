from monopoly_logs import Database
from monopoly import Player
from pygame_file import main
from monopoly_exeptions import NotEnoughtMoneyError

prop = "/home/marcin9047/Programowanie - dom/monopoly/database.json"
spc = "/home/marcin9047/Programowanie - dom/monopoly/Special_cards_database.json"
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
                        inter.draw()
                        inter.draw_title(player)
                        inter.add_button(("Rzuć kośćmi", None))
                        inter.do_action(player)
                        pos = player.position()
                        active_sqr = self.database()[pos]
                        if active_sqr.type() == "special":
                            unsolved = True
                            while unsolved:
                                try:
                                    active_sqr.do_action(player)
                                    unsolved = False
                                except NotEnoughtMoneyError:
                                    inter.do_action(player, True)
                        elif active_sqr.type() == "property":
                            owner = active_sqr.owner()
                            if owner is not None and owner != player:
                                print(active_sqr.owner().name())
                                inter.add_button(("Zapłać", active_sqr))
                        inter.draw()
                        inter.draw_title(player)
                        inter.do_action(player)
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
