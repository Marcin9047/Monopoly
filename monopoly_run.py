from monopoly import Dices, Player, Area, Property, Squere, Special_Squere
from monopoly_logs import read_database

class Game:
    def __init__(self, players):
        self._active = True
        self._players = players

    def isactive(self):
        return self._active

    def shutdown(self):
        self._active = False

    def players(self):
        return self._players

def run_monopoly(database_file, players, init_money=3000):
    game_players = []
    for player in players:
        player = Player(init_money)
        game_players.append(player)
        read_database(database_file)
    game = Game(players)
    while game.isactive():
        for player in game_players:
            player.throw_dices()


def players():
    players = []
    while True:
        player = input()
        if not player:
            break
        players.append(player)
    return players

x = players()
run_monopoly("/home/marcin9047/Programowanie - dom/monopoly/database.json", x, 4000)