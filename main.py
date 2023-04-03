# main file
import telebot
from config.config import BOT_API_TOKEN
from utils.workjson import schedule, tomorrow_raspis, today_raspis, teacher, this_week, this_week_schedule, next_week_schedule, my_week_schedule
from utils.keyboard import chois_buttons, week_buttons, days_buttons


bot = telebot.TeleBot(BOT_API_TOKEN)

MESS_MAX_LENGTH = 3000

@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, 'Введите преподавателя, расписание которого хотите посмотреть')
    bot.register_next_step_handler(msg, choise_date)


def choise_date(messge):
    global prname
    prname = teacher(messge.text)
    if prname:
        msg = bot.send_message(messge.chat.id, 'Выберите временной промежуток', reply_markup=chois_buttons())
        bot.register_next_step_handler(msg, choise_date2)
    else:
        bot.send_message(messge.chat.id, 'На данного преподавателя нет расписания. Убедитесь, что правильно ввели фамилию и инициалы преподавателя.')


def choise_date2(messge):
    msg = messge.text
    if msg =='на день':
        msg = bot.send_message(messge.chat.id, 'Выберите на какой день', reply_markup=days_buttons())
        bot.register_next_step_handler(msg, choise_day)
    elif msg == 'на неделю':
        msg = bot.send_message(messge.chat.id, 'Выберите на какую неделю', reply_markup=week_buttons())
        bot.register_next_step_handler(msg, choise_week)


def choise_day(message):
    global prname
    msg = message.text
    if msg == 'на сегодня':
        listRaspis = today_raspis(prname)
        raspis = listRaspis[0]
        for x in range(1, len(listRaspis)):
            if len(raspis + listRaspis[x]) < MESS_MAX_LENGTH:
                raspis += listRaspis[x]
            else:
                bot.send_message(message.chat.id, raspis, parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())
                raspis = listRaspis[x]
        if raspis:
            bot.send_message(message.chat.id, raspis, parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())
    elif msg == 'на завтра':
        listRaspis = tomorrow_raspis(prname)
        raspis = listRaspis[0]
        for x in range(1, len(listRaspis)):
            if len(raspis + listRaspis[x]) < MESS_MAX_LENGTH:
                raspis += listRaspis[x]
            else:
                bot.send_message(message.chat.id, raspis, parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())
                raspis = listRaspis[x]
        if raspis:
            bot.send_message(message.chat.id, raspis, parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())
    elif msg == 'ввести самому':
        msg = bot.send_message(message.chat.id, 'Введите день, на который хотите увидеть расписание в форме ДД.ММ.ГГ', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, prepod)


def prepod(message):
    day = message.text
    listRaspis = schedule(prname, day)
    raspis = listRaspis[0]
    for x in range(1, len(listRaspis)):
        if len(raspis + listRaspis[x]) < MESS_MAX_LENGTH:
            raspis += listRaspis[x]
        else:
            bot.send_message(message.chat.id, raspis, parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())
            raspis = listRaspis[x]
    if raspis:
        bot.send_message(message.chat.id, raspis, parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())


def choise_week(message):
    global prname
    msg = message.text
    if msg == 'на эту неделю':
        listRaspis = this_week_schedule(prname)
        raspis = listRaspis[0]
        for x in range(1, len(listRaspis)):
            if len(raspis + listRaspis[x]) < MESS_MAX_LENGTH:
                raspis += listRaspis[x]
            else:
                bot.send_message(message.chat.id, raspis, parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())
                raspis = listRaspis[x]
        if raspis:
            bot.send_message(message.chat.id, raspis, parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())
    elif msg == 'на следующую неделю':
        listRaspis=next_week_schedule(prname)
        raspis = listRaspis[0]
        for x in range(1, len(listRaspis)):
            if len(raspis + listRaspis[x]) < MESS_MAX_LENGTH:
                raspis += listRaspis[x]
            else:
                bot.send_message(message.chat.id, raspis, parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())
                raspis = listRaspis[x]
        if raspis:
            bot.send_message(message.chat.id, raspis, parse_mode='Markdown',reply_markup=telebot.types.ReplyKeyboardRemove())
    elif msg == 'ввести номер недели самому':
        message = bot.send_message(message.chat.id, f'Введите номер недели (сейчас идет {this_week()[1]} неделя)', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, castom_ween_schedule)


def castom_ween_schedule(message):
    listRaspis = my_week_schedule(prname, message.text)
    raspis = listRaspis[0]
    for x in range(1, len(listRaspis)):
        if len(raspis + listRaspis[x]) < MESS_MAX_LENGTH:
            raspis += listRaspis[x]
        else:
            bot.send_message(message.chat.id, raspis, parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())
            raspis = listRaspis[x]
    if raspis:
        bot.send_message(message.chat.id, raspis, parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())


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