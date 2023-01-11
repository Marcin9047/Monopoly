from monopoly import Dices, Player, Area, Property, Special_Squere
from monopoly_logs import sort_database
from monopoly_exeptions import WrongInputError, ZeroThrowsError, LessThanRequiredError, NotEnoughtMoneyError
from pygame_file import main

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
    money = init_money
    for one in players:
        player = Player(one, money)
        game_players.append(player)
    game = Game(players)
    while game.isactive():
        for player in game_players:
            while player.throws() != 0 and player.pause() == 0:
                try:
                    player.throw_dices()
                    pos = player.position()
                    active_sqr = squares[pos]
                    if active_sqr.type() == "special":
                        active_sqr.do_action(player)
                    elif active_sqr.type() == "property":
                        if active_sqr.owner() != None and active_sqr.owner() != player:
                            print(active_sqr.owner().name())
                            active_sqr.pay_rent(player)
                            if player.bankrut():
                                game_players.remove(player)
                        elif active_sqr.owner() != player:
                            action = input("Co chcesz zrobić?")
                            if action == "Kup":
                                try:
                                    active_sqr.buy(player)
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