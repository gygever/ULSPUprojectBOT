## generate keyboard here
from telebot import types

def chois_buttons():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bt1 = types.KeyboardButton('на сегодня')
    bt2 = types.KeyboardButton('на эту неделю')
    bt3 = types.KeyboardButton('на завтра')
    bt4 = types.KeyboardButton('на следующую неделю')
    markup.add(bt1, bt2, bt3, bt4)
    return markup