class ZeroThrowsError(Exception):
    """Raise when player have no throws"""
    pass


class WrongInputError(Exception):
    """Raised if input is wrong"""
    pass


class ZeroHousesError(Exception):
    """Raised when there is 0 houses on property"""
    pass


class NotEnoughtMoneyError(Exception):
    """Raised when player doesn't have enought money"""
    pass


class HousesFullError(Exception):
    """Raised when there is 5 houses on a place"""
    pass


class HousesNotEquallyError(Exception):
    """Raised when player try to buy houses not equaly on area"""
    pass


class NotOwnerOfEveryError(Exception):
    """Raised when player is not owner of every area property"""
    pass
