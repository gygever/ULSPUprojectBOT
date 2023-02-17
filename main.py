# main file 
import telebot
from config.config import BOT_API_TOKEN


bot = telebot.TeleBot(BOT_API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, 'Введите преподавателя, расписание которого хотите посмотреть')
    bot.register_next_step_handler(msg, prepod)

@bot.message_handler(commands=['help'])
def start(message):
    bot.send_message(message.chat.id, 'Help command')

def prepod(message):
    global prname
    prname=message.text
    bot.send_message(message.chat.id, 'расписание')



## should be at the bottom, after all other function
@bot.message_handler(func=lambda messages: True)
def any_message(message):
    msg = "Cannot understand you. Please, enter '/help' or '/start' "
    bot.reply_to(message, msg)



## load next step handlers if needed here
if __name__ == "__main__":
    bot.infinity_polling()
