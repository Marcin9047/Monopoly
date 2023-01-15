from monopoly_exeptions import WrongInputError, ZeroThrowsError, NotOwnerOfEveryError
from monopoly_exeptions import ZeroHousesError, NotEnoughtMoneyError
from monopoly_exeptions import HousesNotEquallyError, HousesFullError
from random import randint


def pos(int):
    from monopoly_run import squares
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

    def dice_throw(self)
        """Generates two random intigers"""
        x = randint(1, 6)
        y = randint(1, 6)
        return [x, y]


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

    def set_pon(self, pon):
        """
        Sets player pon
        input: Player_pon class object
        """
        self._pon = pon

    def pon(self):
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
        """Removes property from player properties list>
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
        return self._money < 0

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
            self._position -= 40
        self.pon().move()

    def move_backward(self, value):
        """
        Moves player backward by set position
        input: intiger
        """
        self._position -= value
        if self.position() < 0:
            self._position = 40 + self.position()
        self.pon().move()

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


class Property(Square):
    """Class with the parameters of property on the board
    Super class: Square
    Methods to: pay rent, buy/sell, increase/decrease rent, buy/sell houses,
    set pladge and set house cost
    """
    def __init__(self, name, position, price, rent, area, owner=None, houses=0):
        """
        name: string
        position: intiger
        price: intiger
        rent: intiger
        area: Area class object
        owner=None: Player class object
        houses=None: intiger

        Gives type:"property" and position to Area class
        adds property to area and sets house cost
        """
        super().__init__("property", position)
        self._name = name
        self._price = price
        self._rent = rent
        self._area = area
        self._owner = owner
        self._houses = houses
        self._pledge = False
        self._area.add_property(self)
        self.set_house_cost()

    def name(self):
        return self._name

    def position(self):
        return self._position

    def price(self):
        return self._price

    def increase_rent(self, rent):
        self._rent += rent

    def decrease_rent(self, rent):
        self._rent -= rent

    def rent(self):
        return self._rent

    def pay_rent(self, player):
        """
        Pays rent of the property to the owner or just 
        subtract money if property is pladged
        input: Player class object
        reaises NotEnoughtMoneyError if player is unable to pay
        """
        value = self.rent()
        if player.check_debit(value):
            raise NotEnoughtMoneyError
        player.subtract_money(value)
        if self.pledge() is False:
            self.owner().add_money(value)

    def area(self):
        return self._area

    def set_owner(self, owner):
        self._owner = owner

    def owner(self):
        return self._owner

    def set_pledge(self, value=True):
        """Sets player pladge by given value
        value=True: True/False
        if value same as pladge raises WrongInputError
        If value == True gives half of the property price to the player
        if value == False subtract same money from owner
        """
        if self.pledge() == value:
            raise WrongInputError
        else:
            pld_money = self.price() // 2
            if value:
                self.owner().add_money(pld_money)
                self._pledge = True
            else:
                self.owner().subtract_money(pld_money)
                self._pledge = True

    def pledge(self):
        return self._pledge

    def set_house_cost(self):
        """Sets house cost base on the side of the board"""
        side = (self.position() // 10) + 1
        self._house_cost = 100 * side

    def check_house_cost(self):
        return self._house_cost

    def buy_house(self):
        """Method to buy house ona property if player is an owner of every property in area
            if not: rases NotOwnerOfEveryError
            if houses on property equal 4: property is full
            raises HousesFullError
            raises NotEnoughtMoneyError if player cant afford to buy a house
        """
        if not self.area().check_if_fully_occupied(self.owner()):
            raise NotOwnerOfEveryError
        if self.houses() == 4:
            raise HousesFullError
        cost = self.check_house_cost()
        if self.owner().check_debit(cost):
            raise NotEnoughtMoneyError
        for property in self.area().area_properties():
            if property.houses() < self.houses():
                raise HousesNotEquallyError
        self._houses += 1
        increase = (5 * self.rent()) // 10
        if self.houses() <= 2:
            self.owner().subtract_money(cost)
            self.increase_rent(increase)
        else:
            self.owner().subtract_money(2 * cost)
            self.increase_rent(2 * increase)

    def sell_house(self):
        """Method to sell house on property.
        Raises ZeroHousesError if there is already no houses on property
        """
        if self._houses == 0:
            raise ZeroHousesError
        else:
            self._houses -= 1
            self.owner().add_money(self.check_house_cost())

    def houses(self):
        return self._houses

    def sell(self):
        """Method to sell property"""
        owner = self.owner()
        owner.add_money(self.price())
        self.set_owner(None)
        owner.subtract_property(self)

    def buy(self, player):
        """Method to buy property
        input: Player class object
        raises NotEnoughtMoneyError if player can afford to buy this property
        """
        if player.check_debit(self.price()):
            raise NotEnoughtMoneyError
        self.set_owner(player)
        player.subtract_money(self.price())
        player.add_property(self)

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
        if self.name() == "Start":
            player.add_money(300)
        if self.name() == "Lotnisko":
            pass
        if self.name() == "Podatek":
            player.subtract_money(200)
        if self.name() == "Zarobek":
            player.add_money(300)
