from monopoly import Dices, Player, Area, Property, Special_Square
from monopoly_logs import sort_database
from monopoly_exeptions import WrongInputError, ZeroThrowsError, LessThanRequiredError, NotEnoughtMoneyError
from pygame_file import main

prop = "/home/marcin9047/Programowanie - dom/monopoly/database.json"
spc = "/home/marcin9047/Programowanie - dom/monopoly/Special_cards_database.json"
squares = sort_database(prop, spc)


class Game:
    def __init__(self, players, database):
        self._active = True
        self._players = players
        self._database = database

    def get_position(self, i):
        return self._database[i]

    def isactive(self):
        return self._active

    def shutdown(self):
        self._active = False

    def players(self):
        return self._players

    def play(self):
        pass


def players():
    players = []
    while True:
        player = input()
        if not player:
            break
        player_cls = Player(player, 3000)
        players.append(player_cls)
    return players


x = players()
main(x, squares)
# run_monopoly(x, 4000)
