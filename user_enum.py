import enum


class SizeDishes ( enum.Enum ):
    XS = "маленький"
    S = "нормальный"
    L = "большой"


class MenuCategories ( enum.Enum ):
    PIZZA = "пицца"
    SUSHI = "суши"
    DRINK = "напиток"


class TypesPay ( enum.Enum ):
    CASH = "наличка"
    CARD = "карта"


class States ( enum.Enum ):
    INIT = 0
    HELLO = 1
    MENU = 2
    ADD = 3
    CHANGE = 4
    DELETE = 5
    SIZE = 6
    CHECK = 7
    CHOISE = 8
    COMPLETION = 9


def get_value_enum(obj, name):
    for k in obj:
        if k.value == name:
            return k
