from distutils.log import INFO
import logging as log
from traceback import print_tb
import telebot
from telebot import types

TOKEN = '5608940006:AAF3ukW5_0QQY6wjuIGvAxjQ7_w1j1261GQ' # BOT TOKEN from @BotFather
direct = 'E:\Python\Telegram_bot\log.txt'
bot = telebot.TeleBot(TOKEN)

log.basicConfig(filename=direct, format='%(levelname)s %(asctime)s - %(message)s', level=log.INFO, encoding='utf-8', datefmt='%m/%d/%Y %I:%M:%S')

class ud:   #UserData Class
    def __init__(self, message):
        self.id = message.chat.id #User identifier
        self.fn = message.from_user.first_name #First username
        self.nn = message.from_user.username #User nickname 


@bot.message_handler(commands=['start'])
def welcome (message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    butt1 = types.KeyboardButton("🎰 Казино!")
    butt2 = types.KeyboardButton("🎲 Кости!")
    markup.add(butt1, butt2)

    bot.send_message(ud(message).id, f"Добро пожаловать, {ud(message).fn}!\nЯ - *{bot.get_me().first_name}*, бот созданный чтобы быть подопытным кроликом.",
    parse_mode='markdown', reply_markup = markup)

@bot.message_handler(commands=['notification'])
def notification(message):
    with open (direct, 'rt', encoding='utf-8') as f:
        text = f.readlines()
        table_t = []
        for t in text:
            t = t.split()
            if f'ID:{ud(message).id},' in t:
                t = t[1:3]+t[-4:]
                table_t.append (' '.join(t))
        text = '\n'.join(table_t[-10:])
    
    bot.send_message(ud(message).id, f'{ud(message).fn}, вот текушие результаты кручения в казино:\n{text}')



@bot.message_handler(content_types=['text'])
def message (message):
    if message.text == "🎰 Казино!":
        valuedice = bot.send_dice(message.chat.id, emoji='🎰')
        log.info(f'ID:{ud(message).id}, {ud(message).fn}({ud(message).nn}), в Казино = {valuedice.dice.value}')
    elif message.text == "🎲 Кости!":
        valuedice = bot.send_dice(message.chat.id)
        log.info(f'ID:{ud(message).id}, {ud(message).fn}({ud(message).nn}), в Кости = {valuedice.dice.value}')

# try:
bot.polling(none_stop = True)
# except:
#     print ('Время ожидания, превышено!')
#     quit()
