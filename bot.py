import logging as log
import Casino_telegram as cas
import telebot
from telebot import types
from config import TOKEN, direct

bot = telebot.TeleBot(TOKEN)


log.basicConfig(filename=direct, format='%(levelname)s %(asctime)s - %(message)s', level=log.INFO, encoding='utf-8', datefmt='%m/%d/%Y %H:%M:%S')

class ud:   #UserData Class
    def __init__(self, message, user_login = None, user_password = None):
        self.id = message.chat.id #User identifier
        self.fn = message.from_user.first_name #First username
        self.nn = message.from_user.username #User nickname 
        self.lg = user_login
        self.pw = user_password
    def namesbutt(butt_name):
        bname = {'casino': "🎰 Казино!", 'bone': "🎲 Кости!", 'my_cas': "Самодельное казино!", 'back': "◀️ Назад"}.get(butt_name)
        return bname
    def keyboard(*args):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(*args)
        return markup

@bot.message_handler(commands=['start'])
def welcome (message):
    butt1 = types.KeyboardButton(ud.namesbutt('casino'))
    butt2 = types.KeyboardButton(ud.namesbutt('bone'))
    butt3 = types.KeyboardButton(ud.namesbutt('my_cas'))
    markup = ud.keyboard(butt1, butt2, butt3)

    bot.send_message(ud(message).id, f"Добро пожаловать, {ud(message).fn}!\nЯ - *{bot.get_me().first_name}*, бот созданный чтобы быть подопытным кроликом.",
    parse_mode='markdown', reply_markup = markup)

@bot.message_handler(commands=['notification'])
def notification(message):
    butt1 = types.KeyboardButton(ud.namesbutt('back'))
    markup = ud.keyboard(butt1)
    with open (direct, 'rt', encoding='utf-8') as f:
        text = f.readlines()
        table_t = []
        for t in text:
            t = t.split()
            if f'ID:{ud(message).id},' in t:
                t = t[1:3]+t[-4:]
                table_t.append (' '.join(t))
        text = '\n'.join(table_t[-10:])
    
    bot.send_message(ud(message).id, f'{ud(message).fn}, вот текушие результаты кручения в казино:\n{text}', reply_markup = markup)



@bot.message_handler(content_types=['text'])
def message (message):
    if message.text == ud.namesbutt('casino'):
        valuedice = bot.send_dice(message.chat.id, emoji='🎰')
        log.info(f'ID:{ud(message).id}, {ud(message).fn}({ud(message).nn}), в Казино = {valuedice.dice.value}')
    elif message.text == ud.namesbutt('bone'):
        valuedice = bot.send_dice(message.chat.id)
        log.info(f'ID:{ud(message).id}, {ud(message).fn}({ud(message).nn}), в Кости = {valuedice.dice.value}')
    elif message.text == ud.namesbutt('my_cas'):
        bot.send_message (ud(message).id, 'Запуск самодельного Казино!')
        cas.main (message)
    elif message.text == ud.namesbutt('back'):
        welcome(message)

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling(none_stop = True)
# print ('Время ожидания, превышено!')
#     quit()
