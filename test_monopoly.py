import pytest
from monopoly import Square, Property, Area, Player
from monopoly import Dices, Special_Square
from monopoly_exeptions import WrongInputError, ZeroThrowsError
from monopoly_exeptions import ZeroHousesError, NotEnoughtMoneyError
from monopoly_exeptions import HousesNotEquallyError, HousesFullError

"""Tests for class Player"""


def test_player_init():
    player = Player("Marcin", 3000)
    assert len(player.properties()) == 0
    assert len(player.cards()) == 0
    assert player.money() == 3000
    assert player.position() == 0
    assert player.pause() == 0
    assert player.isactive() is True


def test_add_property():
    poland = Area("Poland")
    player = Player("Marcin", 3000)
    Warszawa = Property("Warszawa", 3, 230, 150, poland, None)
    player.add_property(Warszawa)
    assert player.properties() == [Warszawa]


def test_subtract_property():
    player = Player("Marcin", 3000)
    poland = Area("Poland")
    Warszawa = Property("Warszawa", 3, 230, 150, poland)
    Gdańsk = Property("Warszawa", 3, 230, 150, poland)
    Warszawa.buy(player)
    Gdańsk.buy(player)
    player.subtract_property(Warszawa)
    assert player.properties() == [Gdańsk]


def test_sum_of_value():
    poland = Area("Poland")
    Warszawa = Property("Warszawa", 3, 230, 150, poland, None)
    Gdańsk = Property("Gdańsk", 3, 230, 150, poland, None)
    player = Player("Marcin", 3000)
    player._properties = [Warszawa, Gdańsk]
    assert player.value_of_properties() == 460


def test_cards():
    player = Player("Marcin", 3000)
    assert len(player.cards()) == 0


def test_add_card():
    player = Player("Marcin", 3000)
    player.add_card("Key")
    assert player.cards() == ["Key"]


def test_subtract_card():
    player = Player("Marcin", 3000)
    player.add_card("Key")
    player.subtract_card("Key")
    assert len(player.cards()) == 0


def test_money():
    player = Player("Marcin", 3000)
    assert player.money() == 3000


def test_set_money():
    player = Player("Marcin", 3000)
    player.set_money(5000)
    assert player.money() == 5000


def test_add_money():
    player = Player("Marcin", 3000)
    player.add_money(2000)
    assert player.money() == 5000


def test_subtract_money():
    player = Player("Marcin", 3000)
    player.subtract_money(2000)
    assert player.money() == 1000


def test_debit():
    player = Player("Marcin", 3000)
    with pytest.raises(NotEnoughtMoneyError):
        player.subtract_money(4000)


def test_position_diff():
    player = Player("Marcin", 3000)
    assert player.position() == 0


def test_go_to():
    player = Player("Marcin", 3000)
    player.go_to(3)
    assert player.position() == 3


def test_move_forward():
    player = Player("Marcin", 3000)
    player.move_forward(4)
    assert player.position() == 4


def test_move_backward():
    player = Player("Marcin", 3000)
    player.go_to(3)
    player.move_backward(2)
    assert player.position() == 1


def test_pause():
    player = Player("Marcin", 3000)
    assert player.pause() == 0


def test_set_pouse():
    player = Player("Marcin", 3000)
    player.set_pause(2)
    assert player.pause() == 2


def test_isactive():
    player = Player("Marcin", 3000)
    assert player.isactive() is True


def test_set_inactive():
    player = Player("Marcin", 3000)
    player.set_inactive()
    assert player.isactive() is False


"""Tests for class Square """


def test_squere():
    """Test of squere class"""
    poland = Area("Poland")
    Warszawa = Property("Warszawa", 3, 230, 150, poland, "admin")
    assert Warszawa.type() == "property"
    assert Warszawa.position() == 3


"""Tests for class Property"""


def test_property_init():
    """Test of property class with all of the atributes writen"""
    poland = Area("Poland")
    admin = Player("admin", 4000)
    Warszawa = Property("Warszawa", 3, 230, 150, poland, admin, 5)
    assert Warszawa.position() == 3
    assert Warszawa.price() == 230
    assert Warszawa.rent() == 150
    assert Warszawa.area() == poland
    assert Warszawa.owner() == admin
    assert Warszawa.houses() == 5


def test_property_init_no_owner():
    """Test when owner and houses are not given.
    Program should give owner=None and houses=0"""
    poland = Area("Poland")
    Warszawa = Property("Warszawa", 3, 230, 150, poland)
    assert Warszawa.position() == 3
    assert Warszawa.price() == 230
    assert Warszawa.area() == poland
    assert Warszawa.owner() is None
    assert Warszawa.houses() == 0


def test_increase_rent():
    poland = Area("Poland")
    Warszawa = Property("Warszawa", 3, 230, 150, poland)
    Warszawa.increase_rent(150)
    assert Warszawa.rent() == 300


def test_decrease_rent():
    poland = Area("Poland")
    Warszawa = Property("Warszawa", 3, 230, 150, poland)
    Warszawa.decrease_rent(50)
    assert Warszawa.rent() == 100


def test_pay_rent():
    owner = Player("Janek", 400)
    player = Player("Marcin", 300)
    poland = Area("Poland")
    Warszawa = Property("Warszawa", 3, 230, 150, poland, owner)
    Warszawa.pay_rent(player)
    assert player.money() == 150
    assert owner.money() == 550


def test_set_owner():
    poland = Area("Poland")
    Warszawa = Property("Warszawa", 3, 230, 150, poland)
    player = Player("Marcin", 300)
    Warszawa.set_owner(player)
    assert Warszawa.owner() == player


def test_pledge():
    poland = Area("Poland")
    Warszawa = Property("Warszawa", 3, 230, 150, poland)
    assert Warszawa.pledge() is False


def test_set_pledge():
    poland = Area("Poland")
    player = Player("admin", 4000)
    Warszawa = Property("Warszawa", 3, 230, 150, poland, player)
    Warszawa.set_pledge(True)
    assert Warszawa.pledge() is True


def test_buy_house():
    poland = Area("Poland")
    player = Player("admin", 4000)
    Warszawa = Property("Warszawa", 3, 230, 150, poland, player)
    Warszawa.buy(player)
    Warszawa.buy_house()
    assert Warszawa.houses() == 1


def test_sell_houses():
    poland = Area("Poland")
    Warszawa = Property("Warszawa", 3, 230, 150, poland)
    player = Player("admin", 4000)
    Warszawa.buy(player)
    Warszawa.buy_house()
    Warszawa.sell_house()
    assert Warszawa.houses() == 0


def test_buy_property():
    poland = Area("Poland")
    Warszawa = Property("Warszawa", 3, 230, 150, poland)
    player = Player("Marcin", 300)
    Warszawa.buy(player)
    assert Warszawa.owner() == player
    assert player.money() == 70


def test_sell_property():
    poland = Area("Poland")
    Warszawa = Property("Warszawa", 3, 230, 150, poland)
    player = Player("Marcin", 300)
    Warszawa.buy(player)
    Warszawa.sell()
    assert Warszawa.owner() is None
    assert player.money() == 300


"""Tests for class Area"""


def test_area_init():
    area = Area("Poland")
    Warszawa = Property("Warszawa", 3, 230, 150, area)
    Gdańsk = Property("Gdańsk", 2, 200, 150, area)
    assert area.area_properties() == [Warszawa, Gdańsk]


def test_check_if_fully_occupied():
    poland = Area("Poland")
    Warszawa = Property("Warszawa", 3, 230, 150, poland)
    Gdańsk = Property("Gdańsk", 2, 200, 150, poland)
    player = Player("Player", 4000)
    assert poland.check_if_fully_occupied(player) is False
    Gdańsk.buy(player)
    Warszawa.buy(player)
    assert poland.check_if_fully_occupied(player) is True


"""Tests for class Dices"""


def test_dice_init():
    player = Player("Marcin", 300)
    assert player.throws() == 1
    assert player.dublets() == 0


def test_check_dublet():
    player = Player("Marcin", 300)
    player.check_dublet(3, 3)
    assert player.dublets() == 1
    assert player.throws() == 2


def test_add_throws():
    player = Player("Marcin", 300)
    player.add_throws(3)
    assert player.throws() == 4


def test_set_zero_throws():
    player = Player("Marcin", 300)
    player.add_throws(3)
    player.set_zero_throws()
    assert player.throws() == 0


def test_dice_throw():
    """test if randint returns two intiger numbers"""
    dice = Dices()
    throw = dice.dice_throw()
    assert len(throw) == 2
    for number in throw:
        assert isinstance(number, int)


def test_throw_dices():
    player = Player("Marcin", 300)
    player.throw_dices()
    assert player.position() != 0


"""Tests for class Special_squere"""


def test_specia_square_init():
    prison = Special_Square("prision", 7)
    start = Special_Square("Start", 15)
    assert prison.position() == 7
    assert start.position() == 15


def test_do_Start_action():
    start = Special_Square("Start", 15)
    player = Player("Marcin", 300)
    start.do_action(player)
    assert player.money() == 600
