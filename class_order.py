from user_enum import *


class Order:
    def __init__(self, name):
        self.name = name
        self.count = 1
        self.size = SizeDishes.S

    def create_all_order(self):
        temp_str = [x.value for x in MenuCategories if x == self.name][0].title()
        temp_str_2 = [x.value for x in SizeDishes if x == self.size][0]
        return f'\n{temp_str}. Количество - {self.count}.\nРазмер - {temp_str_2}'