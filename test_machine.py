import pytest

from state_class import state_bot_create
from user_enum import *


class TestMachine:
    def test_add_one_dish(self):
        '''Добавление одной позиции'''

        bot = state_bot_create ()
        bot.first ()
        bot.next ()
        bot.set ( get_value_enum ( MenuCategories, 'пицца' ) )
        bot.next ()
        bot.set ( get_value_enum ( SizeDishes, 'маленький' ) )
        bot.next ()
        bot.set ( get_value_enum ( TypesPay, 'карта' ) )
        bot.next ()
        bot.next ()
        assert (bot.temp_str == "До свидания! Спасибо за заказ.")

    def test_add_two_dish(self):
        '''Добавление двух позиций'''

        bot = state_bot_create ()
        bot.first ()
        bot.next ()
        bot.set ( get_value_enum ( MenuCategories, 'пицца' ) )
        bot.next ()
        bot.set ( get_value_enum ( SizeDishes, 'маленький' ) )
        bot.next ()
        bot.set ( get_value_enum ( TypesPay, 'карта' ) )
        bot.next ()
        bot.change ()
        bot.prev ()
        bot.set ( get_value_enum ( MenuCategories, 'суши' ) )
        bot.next ()
        bot.set ( get_value_enum ( SizeDishes, 'маленький' ) )
        bot.next ()
        bot.set ( get_value_enum ( TypesPay, 'карта' ) )
        bot.change ()
        bot.next ()
        bot.next ()
        bot.next ()
        assert (bot.temp_str == "До свидания! Спасибо за заказ.")

    def test_del_one_dish(self):
        '''Удаление одной позиции'''

        bot = state_bot_create ()
        bot.first ()
        bot.next ()
        bot.set ( get_value_enum ( MenuCategories, 'пицца' ) )
        bot.next ()
        bot.set ( get_value_enum ( SizeDishes, 'маленький' ) )
        bot.next ()
        bot.set ( get_value_enum ( TypesPay, 'карта' ) )
        bot.next ()
        bot.change ()
        bot.prev ()
        bot.set ( get_value_enum ( MenuCategories, 'суши' ) )
        bot.next ()
        bot.set ( get_value_enum ( SizeDishes, 'маленький' ) )
        bot.next ()
        bot.set ( get_value_enum ( TypesPay, 'карта' ) )
        bot.next ()
        bot.change ()
        bot.delete ()
        bot.delete ( 'суши маленький 1' )
        bot.next ()
        assert (("Суши" in bot.temp_str) == False)



