import telebot
from telebot import types

TOKEN = '5608940006:AAF3ukW5_0QQY6wjuIGvAxjQ7_w1j1261GQ' # BOT TOKEN from @BotFather

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome (message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    butt1 = types.KeyboardButton("🎰 Казино!")
    butt2 = types.KeyboardButton("🎲 Кости!")
    markup.add(butt1, butt2)

    bot.send_message(message.chat.id, f"Добро пожаловать, {message.from_user.first_name}!\nЯ - *{bot.get_me().first_name}*, бот созданный чтобы быть подопытным кроликом.",
    parse_mode='markdown', reply_markup = markup)


@bot.message_handler(content_types=['text'])
def message (message):
    if message.text == "🎰 Казино!":
        bot.send_dice(message.chat.id, emoji='🎰')
    elif message.text == "🎲 Кости!":
        bot.send_dice(message.chat.id)


bot.polling(none_stop = True)

