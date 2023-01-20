from monopoly import Dices
from monopoly_exeptions import NotEnoughtMoneyError

class Player(Dices):
    """
    Class with parameteters of player in the game.
    """
    def __init__(self, name, money):
        """
        Inputs:
        name: string
        money: intiger
        """
        super().__init__()
        self._name = name
        self._properties = []
        self._cards = []
        self._money = money
        self._position = 0
        self._pause = 0
        self._isactive = True

    def set_pawn(self, pon):
        """
        Sets player pon
        input: Player_pon class object
        """
        self._pon = pon

    def pawn(self):
        return self._pon

    def properties(self):
        return self._properties

    def name(self):
        return self._name

    def add_property(self, prop):
        """ Iput is Property object
            Append the list of player's properties
            Used by method buy in Property class
        """
        self._properties.append(prop)

    def subtract_property(self, prop):
        """Removes property from player properties list
            Input: Property object
        """
        self._properties.remove(prop)

    def value_of_properties(self):
        """
        Returs sum of value of all of the player properties and houses
        Output: Intiger
        """
        sum = 0
        for property in self.properties():
            sum += property.price()
            sum += (property.houses() * property.check_house_cost())
        return sum

    def cards(self):
        return self._cards

    def set_cards(self, cards):
        self._cards = cards

    def add_card(self, card):
        self._cards.append(card)

    def subtract_card(self, card):
        new_cards = []
        for one_card in self.cards():
            if one_card != card:
                new_cards.append(one_card)
        self.set_cards(new_cards)

    def money(self):
        return self._money

    def set_money(self, value):
        self._money = value

    def add_money(self, value):
        """
        Adds value to the player money
        Input: intiger
        """
        self._money += value

    def subtract_money(self, value):
        """
        Subtract value from player money
        input: intiger
        If player got less than requiered raises
        NotEnoughtMoneyError
        """
        if self.check_debit(value):
            raise NotEnoughtMoneyError
        self._money -= value

    def check_debit(self, value):
        """
        Tests if it is possible to subtract qmmount from player money
        input: intiger
        """
        money_after = self.money() - value
        return money_after < 0

    def debit(self):
        """Returns true if player money < 0"""
        return self.money() < 0

    def position(self):
        return self._position

    def go_to(self, position):
        self._position = position

    def move_forward(self, value):
        """
        Moves player by value
        input: intiger
        """
        self._position += value
        if self.position() > 39:
            self.add_money(300)
            self._position -= 40

    def move_backward(self, value):
        """
        Moves player backward by set position
        input: intiger
        """
        self._position -= value
        if self.position() < 0:
            self._position = 40 + self.position()

    def pause(self):
        return self._pause

    def subtract_pause(self, value=1):
        """
        Subtract player pause when paused
        input: intiger | if None equals 1
        """
        self._pause -= value
        if self._pause < 0:
            self._pause = 0

    def set_pause(self, value):
        self._pause = value

    def isactive(self):
        return self._isactive

    def set_inactive(self):
        """
        The player is kicked out from the game.
        """
        self._isactive = False
