import telebot
from telebot import types
bot = telebot.TeleBot('6265221895:AAFWKmAl-pUHKueTzkUbMYUelTdm2owzcDU')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    btn2 = types.KeyboardButton("❓ Задать вопрос")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я тестовый бот ".format(message.from_user), reply_markup=markup)


@bot.message_handler(commands=['info'])
def info(message):
    mess = f'К сожалению, я пока что нихуя не умею, даи не очень быстро учусь :((((I(())I))))'
    bot.send_message(message.chat.id, mess)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if (message.chat.type == 'private'):
        if (message.text == '👋 Поздороваться'):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn3 = types.KeyboardButton("👋 Ебаться с питоном")
            btn4 = types.KeyboardButton("❓ Трахаться с SQL")
            markup.add(btn3, btn4)
            bot.send_message(message.chat.id, text="Что будем делать?, {0.first_name}! Я тестовый бот ".format(message.from_user), reply_markup=markup)

        if (message.text == '❓ Задать вопрос'):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn5 = types.KeyboardButton("Как правильно заходить в хату?")
            btn6 = types.KeyboardButton("Как правильно выходить из хаты?")
            markup.add(btn5, btn6)
            bot.send_message(message.chat.id, text="Я могу ответь на любые вопросы мироздания, {0.first_name}!".format(message.from_user), reply_markup=markup)

bot.polling(none_stop=True)
