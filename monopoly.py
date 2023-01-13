from monopoly_exeptions import WrongInputError, ZeroThrowsError
from monopoly_exeptions import ZeroHousesError, NotEnoughtMoneyError
from monopoly_exeptions import HousesNotEquallyError, HousesFullError
from random import randint


def pos(int):
    from monopoly_run import squares
    return squares[int]


class Dices:
    def __init__(self):
        self._throws = 1
        self._dublets = 0

    def check_dublet(self, throw1, throw2):
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

    def throw_dices(self):
        if self._throws != 0 and self.pause() == 0:
            self._throws -= 1
            x, y = self.dice_throw()
            if self.dublets() != 3:
                self.move_forward(x + y)
            else:
                pos(30).do_action(self)
            self.set_zero_dublets()
        else:
            raise ZeroThrowsError

    def dice_throw(self):
        x = randint(1, 6)
        y = randint(1, 6)
        return [x, y]


class Player(Dices):
    def __init__(self, name, money):
        super().__init__()
        self._name = name
        self._properties = []
        self._cards = []
        self._money = money
        self._position = 0
        self._pause = 0
        self._isactive = True

    def set_pon(self, pon):
        self._pon = pon

    def pon(self):
        return self._pon

    def properties(self):
        return self._properties

    def name(self):
        return self._name

    def add_property(self, prop):
        self._properties.append(prop)

    def subtract_property(self, prop):
        self._properties.remove(prop)

    def value_of_properties(self):
        sum = 0
        for property in self.properties():
            sum += property.price()
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
        self._money += value

    def subtract_money(self, value):
        if self.check_debit(value):
            raise NotEnoughtMoneyError
        self._money -= value

    def check_debit(self, value):
        money_after = self.money() - value
        return money_after < 0

    def debit(self):
        return self._money < 0

    def position(self):
        return self._position

    def go_to(self, position):
        self._position = position

    def move_forward(self, value):
        self._position += value
        if self.position() > 39:
            self._position -= 40

    def move_backward(self, value):
        self._position -= value
        if self.position() < 0:
            self._position = 40 + self.position()

    def pause(self):
        return self._pause

    def subtract_pause(self, value=1):
        self._pause -= value
        if self._pause < 0:
            self._pause = 0

    def set_pause(self, value):
        self._pause = value

    def isactive(self):
        return self._isactive

    def set_inactive(self):
        self._isactive = False


class Square:
    def __init__(self, type, position):
        self._type = type
        self._position = position

    def type(self):
        return self._type

    def position(self):
        return self._position


class Property(Square):
    def __init__(self, name, position, price, rent, area, owner=None, houses=0):
        super().__init__("property", position)
        self._name = name
        self._price = price
        self._rent = rent
        self._area = area
        self._owner = owner
        self._houses = houses
        self._pledge = False
        self._area.add_property(self)
        self._house_cost = self.house_cost()

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

    def house_cost(self):
        side = (self.position() // 10) + 1
        return 100 * side

    def check_house_cost(self):
        return self._house_cost

    def buy_house(self):
        if self.houses == 4:
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
        if self._houses == 0:
            raise ZeroHousesError
        else:
            self._houses -= 1
            self.owner().add_money(self.house_cost())

    def houses(self):
        return self._houses

    def sell(self):
        owner = self.owner()
        owner.add_money(self.price())
        self.set_owner(None)
        owner.subtract_property(self)

    def buy(self, player):
        if player.check_debit(self.price()):
            raise NotEnoughtMoneyError
        self.set_owner(player)
        player.subtract_money(self.price())
        player.add_property(self)

    def __str__(self):
        return "test"


class Area:
    def __init__(self, name):
        self._name = name
        self._list_of_properties = []

    def set_colour(self, colour):
        self._colour = colour

    def colour(self):
        return self._colour

    def add_property(self, property):
        self._list_of_properties.append(property)

    def name(self):
        return self._name

    def check_if_fully_occupied(self, player):
        for property in self.area_properties():
            if property.owner() != player:
                return False
        return True

    def area_properties(self):
        return self._list_of_properties


class Special_Square(Square):
    def __init__(self, name, position, value=None):
        super().__init__("special", position)
        if value:
            self._value = value
        self._name = name

    def name(self):
        return self._name

    def value(self):
        return self._value

    def do_action(self, player, pos=None):
        if self.name() == "Idziesz do więzienia":
            player.set_pause(3)
        if self.name() == "Start":
            player.add_money(300)
        if self.name() == "Lotnisko":
            pass
        if self.name() == "Podatek":
            player.subtract_money(300)
        if self.name() == "Zarobek":
            player.add_money(300)
