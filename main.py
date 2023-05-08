# main file
import telebot
from config.config import BOT_API_TOKEN
from utils.workjson import tomorrow_raspis, today_raspis, teacher, this_week_schedule, next_week_schedule
from utils.keyboard import chois_buttons


bot = telebot.TeleBot(BOT_API_TOKEN)

MESS_MAX_LENGTH = 3000

def send_schedule(listRaspis, message):
    raspis = listRaspis[0]
    for x in range(1, len(listRaspis)):
        if len(raspis + listRaspis[x]) < MESS_MAX_LENGTH:
            raspis += listRaspis[x]
        else:
            bot.send_message(message.chat.id, raspis, parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())
            raspis = listRaspis[x]
    if raspis:
        bot.send_message(message.chat.id, raspis, parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())

@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, 'Введите преподавателя, расписание которого хотите посмотреть (Фамилия И.О.)')
    bot.register_next_step_handler(msg, choise_date)


def choise_date(messge):
    global prname
    prname = teacher(messge.text)
    if prname:
        msg = bot.send_message(messge.chat.id, 'Выберите временной промежуток', reply_markup=chois_buttons())
        bot.register_next_step_handler(msg, prepod_schedule)
    else:
        bot.send_message(messge.chat.id, 'На данного преподавателя нет расписания. Убедитесь, что правильно ввели фамилию и инициалы преподавателя.')


def prepod_schedule(message):
    global prname
    msg = message.text
    if msg == 'на сегодня':
        listRaspis = today_raspis(prname)
        send_schedule(listRaspis, message)
    elif msg == 'на завтра':
        listRaspis = tomorrow_raspis(prname)
        send_schedule(listRaspis, message)
    elif msg == 'на эту неделю':
        listRaspis = this_week_schedule(prname)
        send_schedule(listRaspis, message)
    elif msg == 'на следующую неделю':
        listRaspis = next_week_schedule(prname)
        send_schedule(listRaspis, message)

@bot.message_handler(commands=['help'])
def start(message):
    bot.send_message(message.chat.id, 'Help command')


## should be at the bottom, after all other function
@bot.message_handler(func=lambda messages: True)
def any_message(message):
    msg = "Cannot understand you. Please, enter '/help' or '/start' "
    bot.reply_to(message, msg)


## load next step handlers if needed here
if __name__ == "__main__":
    bot.infinity_polling()