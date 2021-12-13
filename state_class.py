from transitions import Machine

from classOrder import *
from user_enum import *


class OrderBot(object):
    def __init__(self):
        self.order = []
        self.type_pay = TypesPay.CARD
        self.temp_str = ''
        self.cur_dish = ''
        self.success = True

    def start(self):
        self.order = []
        self.type_pay = TypesPay.CARD
        self.temp_str = ''
        self.cur_dish = ''
        self.success = True

    def say_hello(self):
        """ Приветствие """

        self.temp_str = "Здравствуйте. Что вы хотите заказать?"

    def view_menu(self):
        """ Вывод позиций из меню """
        msg_1 = '\n' + 'Введите /add и позицию'
        msg_2 = '\n' + 'Пример: /add пицца'
        temp_str = "\n".join([i.value for i in MenuCategories])
        self.temp_str = f'Меню:\n{temp_str}\n{msg_1}{msg_2}'

    def set_dish(self, dish):
        """Сохранение типа блюд"""

        self.cur_dish = dish
        is_add = False
        for i in self.order:
            if i.name == dish:
                i.count += 1
                is_add = True
        if not is_add:
            self.order.append ( Order ( dish ) )

    def view_size(self):
        """ Вывод позиций из меню """

        msg_1 = '\n' + 'Введите /add и размер'
        msg_2 = '\n' + 'Пример: /add маленький'
        temp_str = "\n".join([i.value for i in SizeDishes])
        self.temp_str = f'Какой размер?\n \n{temp_str} \n \n{msg_1} {msg_2}'

    def set_size(self, size):
        """ Установка размера блюда"""

        if size:
            for i in self.order:
                if i.name == self.cur_dish:
                    i.size = size
                    break
            else:
                self.temp_str = f'Не поняла размер. Текущий размер {SizeDishes.s}'

    def view_pay(self):
        """ Вывод типа оплаты"""

        temp_str = "\n".join([i.value for i in TypesPay])
        msg_1 = '\n' + 'Введите /pay и тип оплаты'
        msg_2 = '\n' + 'Пример: /pay наличка'
        self.temp_str = f'Тип оплаты:\n{temp_str} \n{msg_1} {msg_2}'

    def set_pay(self, pay):
        """Установка типа оплаты"""

        if pay:
            self.type_pay = [x.value for x in TypesPay if x == pay][0]

    def delete_dish(self, str_info):
        """Удаление блюда"""
        arr_msg = str_info.split ( " " )
        if len(arr_msg) != 3:
            self.success = False
        else:
            dish = arr_msg[0]
            size = arr_msg[1]
            count = arr_msg[2]

            for i in self.order:
                if i.name.value == dish:
                    if i.size.value == size:
                        temp_str = i.create_all_order ()
                        if i.count == int(count):
                            self.order.remove(i)
                            self.temp_str = f"Удалено: {temp_str}"
                            self.success = True
                            break
                        else:
                            i.count -= 1
                            self.temp_str = f"Изменено количество: {temp_str}"
                            self.success = True
                            break
            if not self.success:
                self.temp_str = "Такой позиции нет."

    def view_order(self):
        """ Вывод заказа"""
        msg_1 = '\n' + 'Введите /check и да или нет'
        msg_2 = '\n' + 'Пример: /check да'
        str = ''

        if not self.order:
            str = "Вы ничего не заказали"
        else:

            for i in self.order:
                str = f'{i.create_all_order()} {str}\n'

        self.temp_str = f'Ваш заказ:\n{str} \n{msg_1} {msg_2}'

    def view_order_delete(self):
        """ Вывод заказа"""

        if not self.order:
            self.temp_str = "Вы ничего не заказали"
        else:
            str = ''
            for i in self.order:
                str = f'{i.create_all_order()} {str}\n'
                msg_1 = '\n' + 'Введите /del и блюдо, размер и количество , чтобы удалить или нет'
                msg_2 = '\n\n' + 'Пример: /del нет'
                msg_3 = '\n' + 'Пример: /del пицца маленький 1'
            self.temp_str = f'Ваш заказ:\n{str} \n{msg_1} {msg_2} {msg_3}'

    def view_next_step(self):
        """ Вывод меню редактирования"""
        msg_1 = '\n' + 'Введите /change и удалить или добавить'
        msg_2 = '\n' + 'Пример: /change удалить'
        self.temp_str = f'удалить или добавить? \n{msg_1} {msg_2}'

    def goodbye(self):
        """ Вывод итоговой фразы"""

        self.temp_str = "До свидания! Спасибо за заказ."


def state_bot_create():
    order_bot = OrderBot()
    types = [i.name for i in States]
    machine = Machine(order_bot, types, initial=States.INIT, ignore_invalid_triggers=True)
    machine.add_transition('first', States.INIT,  States.HELLO, before='say_hello')
    machine.add_transition ( 'first', "*", States.HELLO, before='say_hello' )

    machine.add_transition('next', States.HELLO, States.MENU, before='view_menu')
    machine.add_transition ('set', States.MENU, States.MENU, before='set_dish')
    machine.add_transition('next', States.MENU, States.SIZE, after='view_size')
    machine.add_transition ('set', States.SIZE, States.SIZE, before='set_size')
    machine.add_transition ('next', States.SIZE, States.CHECK, before='view_pay')
    machine.add_transition ('set', States.CHECK, States.CHECK, before='set_pay')
    machine.add_transition ( 'next', States.CHECK, States.COMPLETION, before='view_order' )
    machine.add_transition ('next', States.COMPLETION, None, after='goodbye')
    machine.add_transition ('change', States.COMPLETION, States.CHOISE, after='view_next_step')
    machine.add_transition ('delete', States.CHOISE, States.DELETE, after='view_order_delete')
    machine.add_transition ('show', States.DELETE, States.DELETE, after='view_order_delete')
    machine.add_transition ('prev', States.CHOISE, States.MENU, after='view_menu')
    machine.add_transition('delete', States.DELETE, States.DELETE, after='delete_dish')
    machine.add_transition('add', States.DELETE, States.MENU, after='view_menu')
    machine.add_transition('next', States.DELETE, States.COMPLETION, after='view_order')
    machine.add_transition ('stop', "*", States.COMPLETION, after='goodbye')

    return order_bot


