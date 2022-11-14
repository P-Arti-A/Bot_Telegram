#########################################################
# INITIALIZATION VARIABLES

from cgitb import text
import logging as log
import telebot
from telebot import types
import sqlite3
from random import randint, random
from config import TOKEN, direct, directhandler
from Keyboard import keyboard
import math as mt

class ud:   #UserData Class
    def __init__(self, message, user_login = None, user_password = None):
        self.ms = message
        self.id = message.chat.id #User identifier
        self.fn = message.from_user.first_name #First username
        self.lg = message.from_user.username #User nickname 
        self.pw = user_password
        self.tx = message.text
        self.pl = None

class bd:
    def __init__(self, mes = '') -> None:
        self.mes_id = mes.message_id
        self.mes_now = mes
        self.last_mes = None
        self.bet = 1
        self.last_bet = 1
        self.bet_mes = None
        self.last_bet_mes = None
        self.ch = 0.15
        self.pb = 0
        self.mes_value = None
        self.last_mes_value = None
# class statemachin:
#     def __init__(self, state = ''):
#         self.action = 'action'
#         self.registrate = 'registrate'
#         statenow = state
    # def state (state: str):
        

    # def namesbutt(butt_name):
    #     bname = {'casino': "🎰 Казино!", 'bone': "🎲 Кости!", 'my_cas': "Самодельное казино!", 'back': "◀️ Назад"}.get(butt_name)
    #     return bname

    # def keyboard(*args):
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    #     markup.add(*args)
    #     return markup

    # def handler (func):
    #     bot.register_next_step_handler(message, func)

bot = telebot.TeleBot(TOKEN)

db = sqlite3.connect ('CasinoDataTelegram.db', check_same_thread=False)  # DataBase
cdb = db.cursor()                       # Cursor of DB

                                        # Create table
cdb.execute ("""CREATE TABLE IF NOT EXISTS users (
    login TEXT (30),
    password TEXT (16),
    cash BIGINT (15)                          
)""")

db.commit()

#########################################################
# BASIC PROGRAM

log.basicConfig(filename=direct, format='%(levelname)s %(asctime)s - %(message)s', level=log.INFO, encoding='utf-8', datefmt='%m/%d/%Y %H:%M:%S')

@bot.message_handler(commands=['start'])
def welcome (message):
    log.info(f'ID:{ud(message).id}, {ud(message).fn}({ud(message).lg}), исп. команду: {message.text}')
    markup = keyboard.mark(keyboard.button("Казино"), keyboard.button("Кости"), keyboard.button("Моё казино"))

    bot.send_message(ud(message).id, f"Добро пожаловать, {ud(message).fn}!\nЯ - *{bot.get_me().first_name}*, бот созданный чтобы быть подопытным кроликом.",
    parse_mode='markdown', reply_markup = markup)

@bot.message_handler(commands=['notification'])
def notification(message):
    log.info(f'ID:{ud(message).id}, {ud(message).fn}({ud(message).lg}), исп. команду: {message.text}')
    markup = keyboard.mark(keyboard.button("Назад"))
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

@bot.callback_query_handler(func = lambda call: call.data in ['-10', '-', 'bet', '+', '+10'])
def callback_inline(call):
    global user
    global databot
    if call.message:
        if call.data == '-10': 
            databot.bet -= 10
            if databot.bet < 1: databot.bet = 1
        elif call.data == '-': 
            databot.bet -= 1
            if databot.bet < 1: databot.bet = 1
        elif call.data == 'bet': 
            if cash_check (user.lg): return
            match user.pl:
                case 'random':
                    randomid(user.ms)
                case 'slot':
                    slot_machin(user.ms)
                case 'rulet':
                    markup = keyboard.inlinekeyboard()
                    databot.last_mes = bot.edit_message_text(chat_id = user.id, message_id = databot.last_mes.message_id, reply_markup=markup, 
                    text=f'Выберите число!')
                case _:
                    tprint (user.ms, 'Игра не выбрана!')
                    play (user.ms)
                    quit()
        elif call.data == '+': 
            databot.bet += 1
        elif call.data == '+10': 
            databot.bet += 10
    
        if call.data != 'bet' and databot.last_bet != databot.bet:
            markup = keyboard.markinline(keyboard.inlinebut('-10'), 
                                    keyboard.inlinebut('-'), 
                                    types.InlineKeyboardButton(f'{databot.bet}', callback_data='bet'),
                                    keyboard.inlinebut('+'), 
                                    keyboard.inlinebut('+10'), Row_width = 5)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = f'Ваша ставка равна = {databot.bet}', 
            reply_markup = markup) 
            databot.last_bet = databot.bet

@bot.callback_query_handler(func = lambda call: call.data in str(range(1, 37)) or ['1-12', '13-24', '25-36', 'Выбор'])
def callback_inline(call):
    global user
    global databot
    if call.message:
        if call.data == ' ': pass 
        elif call.data == 'Выбор': 
            try:
                if databot.last_mes is not None:
                    bot.delete_message(chat_id = user.id, message_id = databot.last_mes.message_id)
                    bot.delete_message(chat_id = user.id, message_id = databot.last_mes.message_id+1)
            except: pass
            databot = bd(tprint (user.ms, "Запускаем Рулетку"))
            bet_check (user.ms)
        elif call.data in str(range(1, 37)) or ['1-12', '13-24', '25-36']:
            databot.mes_value = call.data
            if databot.mes_value != databot.last_mes_value:
        # if call.data != 'bet' and databot.last_bet != databot.bet:
                markup = keyboard.inlinekeyboard()
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = f'Ваша ставка равна = {databot.mes_value}\nЕсли вы уверены,\nнажмите ещё раз', 
                reply_markup = markup) 
                databot.last_mes_value = databot.mes_value
            else: ruletka(user.ms)


@bot.message_handler(content_types=['text'])
def messaged (message):
    global user
    global databot
    try:
        if user.pw is None: pass
    except NameError:
        user = ud(message)
    try:
        if message.text not in ["🎰 Казино!","🎲 Кости!"]:
            log.info(f'ID:{user.id}, {user.fn}({user.lg}), написал: {message.text}')
        if message.text == "🎰 Казино!":
            valuedice = bot.send_dice(message.chat.id, emoji='🎰')
            log.info(f'ID:{user.id}, {user.fn}({user.lg}), в Казино = {valuedice.dice.value}')
        elif message.text == "🎲 Кости!":
            valuedice = bot.send_dice(message.chat.id)
            log.info(f'ID:{user.id}, {user.fn}({user.lg}), в Кости = {valuedice.dice.value}')
        elif message.text == "Самодельное казино!":
            cdb.execute (f"SELECT login FROM users WHERE login = '{user.lg}'")
            if user.pw is not None: 
                cdb.execute (f"SELECT password FROM users WHERE login = '{user.lg}'")
                user.pw = cdb.fetchone()[0]
                play (message)
            else:
                markup = keyboard.mark(keyboard.button("Вход"), keyboard.button("Регистрация"), keyboard.button("Назад"), One_time_keyboard = True, Row_width = 2)
                bot.send_message (user.id, 'Запуск самодельного Казино!', reply_markup=markup)
        elif message.text == "◀️ Назад":
            welcome(message)
        elif message.text == "Вход":   
            cdb.execute (f"SELECT login FROM users WHERE login = '{user.lg}'")
            if cdb.fetchone() is None:
                tprint (message, 'Вы ещё не зарегистрированы у нас!\n\nРегистрация!\nВведите Пароль')
                bot.register_next_step_handler(message, registrate)
            else:    
                tprint (message, 'Авторизация!\nВведите пароль')
                bot.register_next_step_handler(message, initialization)
        elif message.text == "Регистрация":
            cdb.execute (f"SELECT login FROM users WHERE login = '{user.lg}'")
            if cdb.fetchone() is not None:  
                tprint (message, 'Вы уже зарегистрированы\nЕсли вы забыли пароль, обратитесь в службу поддержки: @p_arti_a')
                return
            tprint (message, 'Регистрация!\nВведите Пароль')
            bot.register_next_step_handler(message, registrate)
        elif user.pw is not None and message.text in ["🎱 РандоМит", "🎰 Однорукий Бандит", "🎲 Рулетка"]:
            try:
                if databot.last_mes is not None:
                    bot.delete_message(chat_id = user.id, message_id = databot.last_mes.message_id)
                    bot.delete_message(chat_id = user.id, message_id = databot.last_mes.message_id-1)
            except: pass
            match message.text:
                case "🎱 РандоМит":
                    user.pl = 'random'
                    tprint (message, 'В данной игре может выпасть число от -20 до 20. В зависимости от выпавшего числа, ваша ставка будет умножена на это число делёное на 10.\nВыйгрыш = Ставка * Число / 10')
                    databot = bd(tprint (message, "Запускаем РандоМит"))
                case "🎰 Однорукий Бандит":
                    user.pl = 'slot'
                    table = {'💀':1, '🌑':2.5, '🌕':5, '⭐️':10, '🌈':25, '🔥':50, '💯':100, '💰':250} 
                    tprint (message, ''.join([f'{i}: {table[i]}X\n' for i in table]))
                    databot = bd(tprint (message, "Запускаем Однорукого Бандита"))
                case "🎲 Рулетка":
                    # tprint (user.ms, 'В разработке!')
                    # return
                    user.pl = 'rulet'
                    tprint (message, 'В начале, выбрети ставку, затем выберите число, которое по вашему мнению может выпасть в рулетке.\nЕсли вы угадаете, множители следующие:\nЗа конкретное число: 35Х\nЗа диапозон: 2,5Х')
                    databot = bd(tprint (message, "Запускаем Рулетку"))
            bet_check(message)
        else: tprint (message, "Нажмите /start для начала работы программы")
    except NameError as e:
        tprint (message, "Вы ещё не авторизировались!")
        log.error (e)


# print ('Время ожидания, превышено!')
#     quit()

#########################################################
# FUNCSION
# @bot.message_handler(commands=['start', 'notification'])

def comeback (message):
    log.info(f'ID:{ud(message).id}, {ud(message).fn}({ud(message).lg}), написал: {message.text}')
    if message.text in ['/start', '/notification', '◀️ Назад']:
        welcome(message)
        return True

#########################################################

def tprint (message, text, Reply_markup: str = None):
    log.info(f'ID:{ud(message).id}, {ud(message).fn}({ud(message).lg}), вывел на экран: {text}')
    return bot.send_message(ud(message).id, text, reply_markup=Reply_markup)

#########################################################

def registrate (message):
    global user
    if comeback(message):  return
    user = ud(message)
    try:
        user.pw = user.tx
    except ValueError:
        tprint (message, 'Вы ввели неизвестные символы!\n Возвращаю вас в главное меню.')
        welcome(message)
    match user.pw:
        case '':
            tprint (message, 'Вы не ввели данные!')
            bot.register_next_step_handler(message, registrate)
            return
        case user.pw if len(user.pw) < 4:
            tprint (message, "Вы ввели меньше 4 символов!")
            bot.register_next_step_handler(message, registrate)
            return
    cdb.execute (f'INSERT INTO users VALUES (?, ?, ?)', (user.lg, user.pw, 100))
    db.commit()
    tprint (message, f'Вы зарегистрировались, {user.fn}\nВаш баланс: 100')
    play(message)

#########################################################

def initialization(message):
    global user
    if comeback(message):  return
    user = ud(message)
    try:
        user.pw = user.tx
    except ValueError:
        tprint (message, 'Вы ввели неизвестные символы!\n Возвращаю вас в главное меню.')
        welcome(message)
    match user.pw:
        case '':
            tprint (message, 'Вы не ввели данные!')
            bot.register_next_step_handler(message, initialization)
            return
        case user.pw if len(user.pw) < 4:
            tprint (message, "Вы ввели меньше 4 символов!")
            bot.register_next_step_handler(message, initialization)
            return
    cdb.execute (f"SELECT login FROM users WHERE login = '{user.lg}' AND password = '{user.pw}'")
    if cdb.fetchone() is None:
        tprint (message, f'Некорректные данные, повторите попытку\nВведите пароль')
        bot.register_next_step_handler(message, initialization)
        return
    else: 
        tprint (message, f'Вы успешно авторизировались {user.fn}')
        play(message)

#########################################################

def play(message):
    markup = keyboard.mark(keyboard.button('РандоМит'), keyboard.button('Бандит'), keyboard.button('Рулетка'), keyboard.button('Назад'), One_time_keyboard = True, Row_width = 2)
    tprint (message, '\nВ какую игру сыграем?\n1. РандоМит\n2. Однорукий Бандит\n3. Рулетка', Reply_markup = markup)
    bot.register_next_step_handler(message, messaged)
    return

#########################################################

def bet_check(message):
    global databot
    # match user.pl:
        # case 'random':
    markup = keyboard.markinline(keyboard.inlinebut('-10'), 
                                keyboard.inlinebut('-'), 
                                types.InlineKeyboardButton(f'{databot.bet}', callback_data='bet'),
                                keyboard.inlinebut('+'), 
                                keyboard.inlinebut('+10'), Row_width = 5)
    if databot.bet == 1 and databot.pb == 0:
        databot.last_mes = bot.edit_message_text(chat_id = user.id, message_id = databot.mes_now.message_id, reply_markup=markup, 
        text=f'Ваша ставка равна = 1')
        databot.pb += 1
    else: pass
        # case 'rulet':
        #     markup = keyboard.inlinekeyboard()
        #     databot.last_mes = bot.edit_message_text(chat_id = user.id, message_id = databot.mes_now.message_id, reply_markup=markup, 
        #     text=f'Сделайте вашу ставку')
            
# if databot.last_bet != databot.bet:
#     databot.last_mes = bot.edit_message_text(chat_id = user.id, message_id = databot.mes_now.message_id, reply_markup=markup, 
#     text=f'Ваша ставка равна = {databot.bet}')
            

def randomid (message):
    global databot
    cdb.execute (f"SELECT cash from users WHERE login = '{user.lg}'")
    cash = cdb.fetchone()[0]
    # tprint (ud.ms, '\nЕсли наигрались пишите "выход/quit" для выхода')
    fortune = randint (-20, 20)
    bet_new = (fortune * int(databot.bet) / 10).real    # Метод .real это класс для предоставления вещественныз чисел. На выходе получаем float
    cash += round (bet_new, 2)
    if databot.last_bet_mes is None:    
        databot.last_bet_mes = tprint (message, f'Выпало число\nВы\nТеперь ваш баланс равен: ') 
    # if databot.last_bet_mes is None:
        # if fortune >= 0: 
        #     databot.bet_mes = tprint (message, f"Выпало число {fortune}\nВы выйграли: {round(bet_new,2)} ✅\nТеперь ваш баланс равен: {cash:.1f}")
        # elif fortune < 0:
        #     databot.bet_mes = tprint (message, f"Выпало число {fortune}\nВы проиграли: {round(bet_new,2)} ❌\nТеперь ваш баланс равен: {cash:.1f}")
    # else:
    if fortune >= 0: 
        databot.bet_mes = bot.edit_message_text(chat_id = user.id, message_id = databot.last_bet_mes.message_id, text=f"Выпало число {fortune}\n✅Вы выйграли: {round(bet_new,2)}\nТеперь ваш баланс равен: {cash:.1f}")
    elif fortune < 0:
        databot.bet_mes = bot.edit_message_text(chat_id = user.id, message_id = databot.last_bet_mes.message_id, text=f"Выпало число {fortune}\n❌Вы проиграли\nТеперь ваш баланс равен: {cash:.1f}")
    databot.last_bet_mes = databot.bet_mes
    log.info(f'ID:{ud(message).id}, {ud(message).fn}({ud(message).lg}), {databot.last_bet_mes.text}')
    if cash <= 0: zeroing(user.lg)
    else:
        cdb.execute (f"UPDATE users SET cash = {cash:.1f} WHERE login = '{user.lg}'")
        db.commit()
    bet_check(message)


########################################################

def slot_machin (message):
    global databot
    cdb.execute (f"SELECT cash from users WHERE login = '{user.lg}'")
    cash = cdb.fetchone()[0]
    bet_new = databot.bet
    table = {'💀':1, '🌑':2.5, '🌕':5, '⭐️':10, '🌈':25, '🔥':50, '💯':100, '💰':250} 
    simbol = [i for i in table.keys ()]
    chance = []
    if databot.last_bet_mes is None:
        databot.last_bet_mes = tprint (message, f'\n\n\nВаш баланс = ')
    chance.append (simbol[int (mt.log(random(), 0.5) % 8)])
    while len(chance)<3:
        if random () < databot.ch:  chance.append (chance[0])
        else: chance.append (simbol[int (mt.log(random(), 0.5) % 8)])
    if chance [0] == chance [1]: 
        if chance [1] == chance [2]: 
            bet_new *= table.get (chance [-1])
            cash += bet_new
            databot.bet_mes = bot.edit_message_text(chat_id = user.id, message_id = databot.last_bet_mes.message_id, text=f'{" ".join (chance)}\n✅Вы выйграли! = {bet_new}\nВаш баланс = {cash:.1f}')
            databot.ch = 0.15
        else: 
            cash -= bet_new
            databot.bet_mes = bot.edit_message_text(chat_id = user.id, message_id = databot.last_bet_mes.message_id, text=f'{" ".join (chance)}\n❌Почти! Вы проиграли\nВаш баланс = {cash:.1f}')
            databot.ch += 0.05
    else: 
        cash -= bet_new
        databot.bet_mes = bot.edit_message_text(chat_id = user.id, message_id = databot.last_bet_mes.message_id, text=f'{" ".join (chance)}\n❌Пройгрыш!\nВаш баланс = {cash:.1f}')
        databot.ch += 0.05
    if cash <= 0: zeroing(user.lg)
    else:
        cdb.execute (f"UPDATE users SET cash = {cash:.1f} WHERE login = '{user.lg}'")
        db.commit()
    databot.last_bet_mes = databot.bet_mes
    log.info(f'ID:{ud(message).id}, {ud(message).fn}({ud(message).lg}), {databot.last_bet_mes.text}')
    bet_check(message)

########################################################

def ruletka(message):
    if databot.mes_value.find ('-') != -1:
        chance = [int (f) for f in databot.mes_value.split ('-')]
        chance = range (chance[0], chance[-1]+1)
    else: chance = int (databot.mes_value)
    bet = databot.bet
    cdb.execute (f"SELECT cash from users WHERE login = '{user.lg}'")
    cash = cdb.fetchone()[0]
    rulet = randint (1, 36) 
    # Проверяем выпавшее число со ставкой
    result = 0
    if databot.last_bet_mes is None: databot.last_bet_mes = tprint (message, 'Ваша ставка')
    # elif databot.last_bet_mes.text == databot.bet_mes.text: return
    if isinstance (chance, int):    
        if rulet == chance:
            result = bet * 35
            cash += result
            databot.bet_mes = bot.edit_message_text(chat_id = user.id, message_id = databot.last_bet_mes.message_id, text=f'Выпало число {rulet}\n✅Поздравляем! Вы выйграли: {result:.1f}\nВаш баланс = {cash}')
        else:
            result -= bet
            cash += result
            databot.bet_mes = bot.edit_message_text(chat_id = user.id, message_id = databot.last_bet_mes.message_id, text=f'Выпало число {rulet}\n❌Вы проиграли\nВаш баланс = {cash}')
    else:
        if rulet in chance:
            result = bet * 2.5
            cash += result
            databot.bet_mes = bot.edit_message_text(chat_id = user.id, message_id = databot.last_bet_mes.message_id, text=f'Выпало число {rulet}\n✅Поздравляем! Вы выйграли: {result:.1f}\nВаш баланс = {cash}')
        else:
            result -= bet
            cash += result
            databot.bet_mes = bot.edit_message_text(chat_id = user.id, message_id = databot.last_bet_mes.message_id, text=f'Выпало число {rulet}\n❌Вы проиграли\nВаш баланс = {cash}')
    databot.last_bet_mes = databot.bet_mes
    cdb.execute (f"UPDATE users SET cash = {cash:.1f} WHERE login = '{user.lg}'")
    db.commit()
    log.info(f'ID:{ud(message).id}, {ud(message).fn}({ud(message).lg}), {databot.last_bet_mes.text}')
    bet_check (message)
    

# #########################################################

# def setings (): 
#     tprint (message, '''Настройки содержат в себе следующие меню:
#     'regis' - Регистрация, 
#     'random' - Играть в казино,
#     'table' - Главное меню,
#     'plays' - Начало программы,
#     'zero' - Обнуление,
#     'delet' - Удаление,
#     'allshow' - Показать всех игроков,
#     'quit' - Выйти из программы,
#     'show' - Показать информацию об игроке,
#     'cashup' - Пополнение баланса у игрока,
#     'probin' - Проверка логина на существование,
#     'slotmach' - "Однорукий бандит"
#     'betcheck' - Проверка ставки у конкретного пользователя,
#     'rulet' - Рулетка''')
#     word = input()

#     sets = {'regis': registrate ,
#             'random': randomid ,
#             'table': main_table,
#             'plays': play,
#             'zero': zeroing ,
#             'delet': delete,
#             'allshow': show_all_user,
#             'quit': quit,
#             'show': show_user,
#             'cashup': cash_up,
#             'probin': prob_init,
#             'betcheck': bet_check,
#             'slotmach': slot_machin,
#             'rulet': ruletka}.get (word, "Ошибка, не правильно написана функция!")
#     if word in ['regis', 'plays', 'allshow', 'quit']:
#         if word == 'regis':    return sets(input ('Log in: '), input ('Password: '))
#         else:   return sets() 
#     elif word in ['rulet', 'slotmach', 'random', 'table', 'plays', 'zero', 'delet', 'show', 'cashup', 'probin', 'betcheck']: return sets(input ('Log in: '))
#     return setings()

# #########################################################

# def prob_init (message):
#     cdb.execute (f"SELECT * FROM users WHERE login = '{user.lg}'")
#     if cdb.fetchone () is None: return tprint (message, "Не найден данный логин!")
#     else: True
    
# #########################################################
    
# def show_user(user): 
#     for value in cdb.execute (f"SELECT * FROM users WHERE login = '{user}'"):
#         tprint (value)

# #########################################################
    
# def show_all_user(): 
#     for value in cdb.execute (f"SELECT * FROM users"):
#         tprint (value)


# #########################################################

# def delete (user_login):
#     prob_init (user_login)
#     cdb.execute (f"DELETE FROM users WHERE login = '{user_login}'")
#     db.commit()
#     tprint (message, "Пользователь удалён!")
#     initialization()

#########################################################

def zeroing (user_login):
    cdb.execute (f"UPDATE users SET cash = 0 WHERE login = '{user_login}'")
    db.commit()
    tprint (user.ms, "У вас закончились средства! Обраитесь в службу поддержки: @p_arti_a")
    welcome(user.ms)

#########################################################

# def main_table(user_login):
#     prob_init (user_login)
#     cdb.execute (f"SELECT * from users WHERE login = '{user_login}'")
#     cash = cdb.fetchone()[-1]
#     # print ('\nВы успешно авторизировались!')
#     tprint (f'{user_login}, Ваш баланс: {cash}')

# #########################################################

# def cash_up(user_login):
#     prob_init (user_login)
#     new_cash = int(input_set('Введите сумму пополнения: '))
#     cdb.execute (f"SELECT cash FROM users WHERE login = '{user_login}'")
#     cash = cdb.fetchone()[0]
#     cdb.execute (f"UPDATE users SET cash = {cash + new_cash} WHERE login = '{user_login}'")
#     db.commit()
#     tprint (f'{user_login}, Ваш баланс пополнен и равен: {cash + new_cash}')
    
#########################################################

def cash_check (user_login):
    cdb.execute (f"SELECT  cash from users WHERE login = '{user_login}'")
    cash = cdb.fetchone()[0]
    if cash < databot.bet:
        tprint (user.ms, "Ваша ставка больше вашего счёта!")
        # welcome(user.ms)
        return True
    else: False

#########################################################
# def input_set(text):
#     if text in ['setings', 'seting', 'settings', 'setting']:
#         setings()
#         quit()
#     elif text == "": 
#         tprint (message, "Вы не ввели никаких данных!")
#         input_set ()
#     else: return text


#########################################################
# MAIN PROGRAM

# @bot.message_handler(content_types=['text'])
# def main():
    # user = ud(mes)
    # bot.register_next_step_handler(user.ms, initialization)

#     # try:
#     play(message)
#     # finally:
#     #     cdb.close()
#     #     db.close()


# if __name__ == '__main__':
bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.infinity_polling()
#########################################################