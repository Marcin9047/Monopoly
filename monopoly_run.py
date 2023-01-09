from monopoly import Dices, Player, Area, Property, Special_Squere
from monopoly_logs import sort_database

squares = sort_database("/home/marcin9047/Programowanie - dom/monopoly/database.json", "/home/marcin9047/Programowanie - dom/monopoly/Special_cards_database.json")

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

def run_monopoly(players, init_money=3000):
    game_players = []
    for one in players:
        player = Player(one, init_money)
        game_players.append(player)
    game = Game(players)
    while game.isactive():
        for player in game_players:
            while player.throws() != 0:
                try:
                    player.throw_dices()
                    pos = player.position()
                    active_sqr = squares[pos]
                    if active_sqr.type() == "special":
                        active_sqr.do_action()
                    elif active_sqr.type() == "property":
                        print(active_sqr.owner())
                        if active_sqr.owner() != None and active_sqr.owner() != player:
                            active_sqr.pay_rent(player)
                            if player.bankrut():
                                game_players.remove(player)
                        elif active_sqr.owner() != player:
                            action = input("Co chcesz zrobić?")
                            if action == "Kup":
                                active_sqr.buy(player)
                except:
                    break
            player.subtract_pause()
            if player.pause() == 0:
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
run_monopoly(x, 4000)