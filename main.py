# main file 
import telebot
from config.config import BOT_API_TOKEN
from utils.workjson import schedule, TomorrowRaspis, TodayRaspis
from utils.keyboard import ChoisButtons, DaysButtons, WeekButtons


bot = telebot.TeleBot(BOT_API_TOKEN)

MESS_MAX_LENGTH = 4096

@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, 'Введите преподавателя, расписание которого хотите посмотреть')
    bot.register_next_step_handler(msg, ChoiseDate)

def ChoiseDate(messge):
    global prname
    prname = messge.text
    msg = bot.send_message(messge.chat.id, 'Выберите временной промежуток', reply_markup=ChoisButtons())
    bot.register_next_step_handler(msg, ChoiseDate2)

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
        raspis = TodayRaspis(prname)
        for x in range(0, len(raspis), MESS_MAX_LENGTH):
            shraspis = raspis[x: x + MESS_MAX_LENGTH]
            bot.send_message(message.chat.id, shraspis, parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())
    elif msg == 'на завтра':
        raspis = TomorrowRaspis(prname)
        for x in range(0, len(raspis), MESS_MAX_LENGTH):
            shraspis = raspis[x: x + MESS_MAX_LENGTH]
            bot.send_message(message.chat.id, shraspis, parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())
    elif msg == 'ввести самому':
        msg = bot.send_message(message.chat.id, 'Введите день, на который хотите увидеть расписание в форме ДД.ММ.ГГ', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, prepod)


def ChoiseWeek(message):
    global prname
    msg = message.text
    if msg == 'на эту неделю':
        raspis = 'пока не работает'
        for x in range(0, len(raspis), MESS_MAX_LENGTH):
            shraspis = raspis[x: x + MESS_MAX_LENGTH]
            bot.send_message(message.chat.id, shraspis, parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove() )
    elif msg == 'на следующую неделю':
        raspis = "пока не работает"
        for x in range(0, len(raspis), MESS_MAX_LENGTH):
            shraspis = raspis[x: x + MESS_MAX_LENGTH]
            bot.send_message(message.chat.id, shraspis, parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())
    elif msg == 'ввести номер недели самому':
        bot.send_message(message.chat.id, 'пока не работает', reply_markup=telebot.types.ReplyKeyboardRemove())

def prepod(message):
    day = message.text
    raspis = schedule(prname, day)
    for x in range(0, len(raspis), MESS_MAX_LENGTH):
        shraspis = raspis[x: x + MESS_MAX_LENGTH]
        bot.send_message(message.chat.id, shraspis, parse_mode='Markdown')


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
