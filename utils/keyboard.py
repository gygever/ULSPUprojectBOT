## generate keyboard here
from telebot import types

def chois_buttons():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    bt1 = types.KeyboardButton('на день')
    bt2 = types.KeyboardButton('на неделю')
    markup.add(bt1, bt2)
    return markup

def days_buttons():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    bt1 = types.KeyboardButton('на сегодня')
    bt2 = types.KeyboardButton('на завтра')
    bt3 = types.KeyboardButton('ввести самому')
    markup.add(bt1, bt2, bt3)
    return markup

def week_buttons():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    bt1 = types.KeyboardButton('на эту неделю')
    bt2 = types.KeyboardButton('на следующую неделю')
    bt3 = types.KeyboardButton('ввести номер недели самому')
    markup.add(bt1, bt2, bt3)
    return markup