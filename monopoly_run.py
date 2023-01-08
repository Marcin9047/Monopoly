from monopoly import Dices, Player, Area, Property, Squere, Special_Squere
from monopoly_logs import sort_database

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

def run_monopoly(database_file, file, players, init_money=3000):
    game_players = []
    for one in players:
        player = Player(one, init_money)
        game_players.append(player)
    squares = sort_database(database_file, file)
    game = Game(players)
    while game.isactive():
        for player in game_players:
            while player.throws() != 0:
                player.throw_dices()
                pos = player.position()
                active_sqr = squares[pos]
                if active_sqr.type() == "special":
                    print("special")
                if active_sqr.type() == "property":
                    print("Property")
            player.add_throws()
        


def players():
    players = []
    while True:
        player = input()
        if not player:
            break
        players.append(player)
    return players

x = players()
run_monopoly("/home/marcin9047/Programowanie - dom/monopoly/database.json", "/home/marcin9047/Programowanie - dom/monopoly/Special_cards_database.json", x, 4000)