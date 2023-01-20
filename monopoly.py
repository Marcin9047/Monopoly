from monopoly_exeptions import *
from random import randint


def pos(int):
    from main import squares
    return squares[int]


class Dices:
    """
    Class for the players dices.
    check_dublets: test if throw is dublet
    set_zero_dublets: sets player dublets to 0
    ready_to_play : return true if player got throws and player pause equal 0
    dice_throw: generate 2 random numbers (1-6) | returns two int
    throw_dices: moves player by random number if possible
    """
    def __init__(self):
        self._throws = 1
        self._dublets = 0

    def check_dublet(self, throw1, throw2):
        """Checks of value on both dices is the same
        input: intigers
        """
        if throw1 == throw2:
            self._dublets += 1
            self.add_throws()
        return throw1 == throw2

    def dublets(self):
        return self._dublets

    def set_zero_dublets(self):
        self._dublets = 0

    def throws(self):
        return self._throws

    def add_throws(self, throws=1):
        self._throws += throws

    def set_zero_throws(self):
        self._throws = 0

    def ready_to_play(self):
        """Return true if player got throws and his pause if equal 0"""
        return self.throws() != 0 and self.pause() == 0

    def throw_dices(self):
        """
        If player ready to play moves him by the generated number,
        For 3 dublet in a player goes to prison
        else raises ZeroThrowsError
        """
        if self.ready_to_play():
            self._throws -= 1
            x, y = self.dice_throw()
            if self.dublets() != 3:
                self.move_forward(x + y)
            else:
                pos(30).do_action(self)
            self.set_zero_dublets()
        else:
            raise ZeroThrowsError
        return x, y

    def dice_throw(self):
        """Generates two random intigers"""
        x = randint(1, 6)
        y = randint(1, 6)
        return [x, y]


class Square:
    """Super class for every position on the board.
        Methods: type, position
    """
    def __init__(self, type, position):
        """
        Sets the pyte of a square and its position on the map.
        type: string
        position: intiger
        """
        self._type = type
        self._position = position

    def type(self):
        return self._type

    def position(self):
        return self._position


class Area:
    """
    Class with the informations about area color,
    properties and name
    """
    def __init__(self, name):
        """
        name: string
        """
        self._name = name
        self._list_of_properties = []

    def set_colour(self, colour):
        """input: rgb value of color"""
        self._colour = colour

    def colour(self):
        return self._colour

    def add_property(self, property):
        self._list_of_properties.append(property)

    def name(self):
        return self._name

    def check_if_fully_occupied(self, player):
        """
        Checks if player has all of the properties in Area
        input: Player class object
        """
        for property in self.area_properties():
            if property.owner() != player:
                return False
        return True

    def area_properties(self):
        return self._list_of_properties


class Special_Square(Square):
    def __init__(self, name, position, value=None):
        """name: string
        position: intiger
        value=None: intiger

        For the area class gives:
        type: "special" and position
        """
        super().__init__("special", position)
        if value:
            self._value = value
        self._name = name

    def name(self):
        return self._name

    def value(self):
        return self._value

    def do_action(self, player, pos=None):
        """Does action of a special square on a player
        player: Player class object
        pos=None: position on the board
        """

        if self.name() == "Idziesz do więzienia":
            player.set_pause(3)
        if self.name() == "Lotnisko":
            pass
        if self.name() == "Podatek":
            player.subtract_money(200)
        if self.name() == "Zarobek":
            player.add_money(300)
