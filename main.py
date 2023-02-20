# main file 
import telebot
from config.config import BOT_API_TOKEN
from utils.workjson import schedule


bot = telebot.TeleBot(BOT_API_TOKEN)

MESS_MAX_LENGTH = 4096

@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, 'Введите преподавателя, расписание которого хотите посмотреть')
    bot.register_next_step_handler(msg, prepod)


def prepod(message):
    global prname
    prname=message.text
    raspis=schedule(prname)
    for x in range(0, len(raspis), MESS_MAX_LENGTH):
        shraspis = raspis[x: x + MESS_MAX_LENGTH]
        bot.send_message(message.chat.id, shraspis)


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
