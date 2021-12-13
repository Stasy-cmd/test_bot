import logging
import sys
import time

import telebot

from settings import API_KEY
from state_class import *

bot = telebot.TeleBot ( __name__ )
global order_bot
order_bot = state_bot_create ()


@bot.route ( '/start' )
def start_step(message):
    global order_bot
    chat_dest = message['chat']['id']
    order_bot.start ()
    order_bot.first ()
    msg = order_bot.temp_str
    order_bot.next ()
    msg = msg + '\n\n' + order_bot.temp_str
    bot.send_message ( chat_dest, msg )


@bot.route ( '/add' )
def add_step(message):
    global order_bot
    chat_dest = message['chat']['id']
    msg = message['text'].strip ( "/add" ).strip ( " " )

    ret_msg = ''
    if order_bot.state == 'MENU':
        value = get_value_enum ( MenuCategories, msg )
        if value:
            order_bot.set ( value )
            order_bot.next ()
        else:
            ret_msg = "Нет такого блюда \n \n"
            order_bot.menu ()
    elif order_bot.state == 'SIZE':
        value = get_value_enum ( SizeDishes, msg )
        if value:
            order_bot.set ( value )
            order_bot.next ()
    else:
        order_bot.first ()

    ret_msg = f'{ret_msg}{order_bot.temp_str}'
    bot.send_message ( chat_dest, ret_msg )


@bot.route ( '/pay' )
def step_pay(message):
    global order_bot
    chat_dest = message['chat']['id']
    msg = message['text'].strip ( "/pay" ).strip ( " " )
    value = get_value_enum ( TypesPay, msg )
    if value:
        order_bot.set ( value )
        order_bot.next ()

    bot.send_message ( chat_dest, order_bot.temp_str )


@bot.route ( '/check' )
def step_chek(message):
    global order_bot
    chat_dest = message['chat']['id']
    msg = message['text'].strip ( "/chek" ).strip ( " " ).lower ()
    if msg == "да":
        order_bot.next ()
    else:
        order_bot.change ()
    bot.send_message ( chat_dest, order_bot.temp_str )


@bot.route ( '/change' )
def step_change(message):
    global order_bot
    chat_dest = message['chat']['id']
    msg = message['text'].strip ( "/change" ).strip ( " " ).lower ()
    if msg == "удалить":
        order_bot.delete ()
    else:
        order_bot.prev ()
    bot.send_message ( chat_dest, order_bot.temp_str )


@bot.route ( '/del' )
def step_delete(message):
    global order_bot
    chat_dest = message['chat']['id']
    msg = message['text'].strip ( "/del" ).strip ( " " ).lower ()
    if msg == "нет":
        order_bot.next ()
    else:
        order_bot.delete ( msg )
    if order_bot.success:
        order_bot.next ()
    else:
        bot.send_message ( chat_dest, order_bot.temp_str )
        order_bot.show ()

    bot.send_message ( chat_dest, order_bot.temp_str )


@bot.route ( '/stop' )
def stop_step(message):
    global order_bot
    chat_dest = message['chat']['id']
    order_bot.stop ()
    bot.send_message ( chat_dest, order_bot.temp_str )


def start_api():
    global order_bot
    bot.config['api_key'] = API_KEY
    while True:
        try:
            bot.poll ()
        except:
            logging.error ( 'error: {}'.format ( sys.exc_info ()[0] ) )
            time.sleep ( 2 )
            order_bot = state_bot_create ()
            order_bot.first ()


start_api ()
