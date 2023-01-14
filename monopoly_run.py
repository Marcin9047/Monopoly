from monopoly import Dices, Player, Area, Property, Special_Square
from monopoly_logs import sort_database
from monopoly_exeptions import WrongInputError, ZeroThrowsError, NotEnoughtMoneyError
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
                inter.draw()
                while player.ready_to_play():
                    player.throw_dices()
                    pos = player.position()
                    active_sqr = self.database()[pos]
                    if active_sqr.type() == "special":
                        try:
                            active_sqr.do_action(player)
                        except(NotEnoughtMoneyError):
                            print("Blisko bankructwa")
                    elif active_sqr.type() == "property":
                        if active_sqr.owner() is not None and active_sqr.owner() != player:
                            print(active_sqr.owner().name())
                            active_sqr.pay_rent(player)
                            if player.value_of_properties() + player.money() < 0:
                                self.players.remove(player)
                            else:
                                print("SPłać dług")
                        elif active_sqr.owner() != player:
                            print("Co chcesz zrobić")
                            try:
                                inter.do_action(player, active_sqr)
                                if player.value_of_properties() > 100:
                                    print("Udało się")
                                    inter.draw()
                            except(NotEnoughtMoneyError):
                                print("Nie posiadasz wystarczających funduszy")
                        elif active_sqr.area().check_if_fully_occupied(player):
                            action = input("Możesz kupić domek, chcesz?: ")
                            if action == "Tak":
                                try:
                                    active_sqr.buy_house()
                                except(NotEnoughtMoneyError):
                                    print("Nie posiadasz wystarczających funduszy")
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
game = Game(x, squares)
game.play()
# run_monopoly(x, 4000)