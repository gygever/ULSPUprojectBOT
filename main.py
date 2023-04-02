# main file
import telebot
from config.config import BOT_API_TOKEN
from utils.workjson import schedule, TomorrowRaspis, TodayRaspis, teacher, ThisWeek, ThisWeekSchedule, NextWeekSchedule, MyWeekSchedule
from utils.keyboard import ChoisButtons, DaysButtons, WeekButtons


bot = telebot.TeleBot(BOT_API_TOKEN)

MESS_MAX_LENGTH = 3000

@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, 'Введите преподавателя, расписание которого хотите посмотреть')
    bot.register_next_step_handler(msg, ChoiseDate)


def ChoiseDate(messge):
    global prname
    prname = teacher(messge.text)
    if prname:
        msg = bot.send_message(messge.chat.id, 'Выберите временной промежуток', reply_markup=ChoisButtons())
        bot.register_next_step_handler(msg, ChoiseDate2)
    else:
        bot.send_message(messge.chat.id, 'На данного преподавателя нет расписания. Убедитесь, что правильно ввели фамилию и инициалы преподавателя.')


def ChoiseDate2(messge):
    msg = messge.text
    if msg =='на день':
        msg = bot.send_message(messge.chat.id, 'Выберите на какой день', reply_markup=DaysButtons())
        bot.register_next_step_handler(msg, ChoiseDay)
    elif msg == 'на неделю':
        msg = bot.send_message(messge.chat.id, 'Выберите на какую неделю', reply_markup=WeekButtons())
        bot.register_next_step_handler(msg, ChoiseWeek)


def ChoiseDay(message):
    global prname
    msg = message.text
    if msg == 'на сегодня':
        listRaspis = TodayRaspis(prname)
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
        listRaspis = TomorrowRaspis(prname)
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


def ChoiseWeek(message):
    global prname
    msg = message.text
    if msg == 'на эту неделю':
        listRaspis = ThisWeekSchedule(prname)
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
        listRaspis=NextWeekSchedule(prname)
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
        message = bot.send_message(message.chat.id, f'Введите номер недели (сейчас идет {ThisWeek()[1]} неделя)', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, CastomWeenSchedule)


def CastomWeenSchedule(message):
    listRaspis = MyWeekSchedule(prname, message.text)
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