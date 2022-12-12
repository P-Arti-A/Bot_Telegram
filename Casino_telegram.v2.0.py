#########################################################
# INITIALIZATION VARIABLES

import logging as log
import telebot
from telebot import types
import sqlite3
from random import randint, random
from config import TOKEN, direct, directhandler
from Keyboard import keyboard
import math as mt

class ud:   #UserData Class
    def __init__(self, message):
        self.id = message.chat.id #User identifier
        self.fn = message.from_user.first_name #First username
        self.lg = message.from_user.username #User nickname
class wordbook:
    def __init__(self, tupledata) -> None:
        self.lg = tupledata[0] #User nickname 
        self.pw = tupledata[1] #User password
        self.st = tupledata[2] #State machin
        self.fn = tupledata[3] #First username
        self.id = tupledata[4] #User identifier
        self.ch = tupledata[5] #User cash
class wordbook_bot:
    def __init__(self, tupledata) -> None:
        self.lg = tupledata[0] #User nickname 
        self.mes_id = tupledata[1]
        self.last_mes_id = tupledata[2]
        self.bet = tupledata[3]
        self.last_bet = tupledata[4]
        self.bet_mes_id = tupledata[5]
        self.last_bet_mes_id = tupledata[6]
        self.ch = tupledata[7]
        self.pb = tupledata[8]
        self.mes_value = tupledata[9]
        self.last_mes_value = tupledata[10]
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

bot = telebot.TeleBot(TOKEN)

db = sqlite3.connect ('CasinoDataTelegram.db', check_same_thread=False)  # DataBase
cdb = db.cursor()                       # Cursor of DB

                                        # Create table
cdb.execute ("""CREATE TABLE IF NOT EXISTS bot (
    user_chat_id BIGINT,
    message_id BIGINT,
    last_message_id BIGINT,
    bet BIGINT,
    last_bet BIGINT,
    bet_message_id BIGINT,
    last_bet_message_id BIGINT,
    chance REAL,
    prob BIGINT,
    message_value TEXT,
    last_message_value TEXT                          
)""")
db.commit()

cdb.execute ("""CREATE TABLE IF NOT EXISTS users (
    login TEXT,
    password TEXT, 
    password_state TEXT, 
    user_first_name TEXT, 
    user_chat_id BIGINT, 
    cash BIGINT
)""")
db.commit()

#########################################################
# BASIC PROGRAM

log.basicConfig(filename=direct, format='%(asctime)s - %(message)s', level=log.CRITICAL, encoding='utf-8', datefmt='%m/%d/%Y %H:%M:%S')

@bot.message_handler(commands=['start'])
def welcome (message):
    log.critical(f'ID:{ud(message).id}, {ud(message).fn}({ud(message).lg}), исп. команду: {message.text}')
    markup = keyboard.mark(keyboard.button("Казино"), keyboard.button("Кости"), keyboard.button("Моё казино"))

    bot.send_message(ud(message).id, f"Добро пожаловать, {ud(message).fn}!\n*{bot.get_me().first_name}* это бот, который поможет заменить вам реальные игровые автоматы, и весело провести время!",
    parse_mode='markdown', reply_markup = markup)

@bot.message_handler(commands=['notification'])
def notification(message):
    log.critical(f'ID:{ud(message).id}, {ud(message).fn}({ud(message).lg}), исп. команду: {message.text}')
    markup = keyboard.mark(keyboard.button("Назад"))
    with open (direct, 'rt', encoding='utf-8') as f:
        text = f.readlines()
        table_t = []
        for t in text:
            t = t.split()
            if f'ID:{ud(message).id},' in t and "Выпало" in t:
                t = t[1:3]+t[6:]
                table_t.append (' '.join(t))
        text = '\n'.join(table_t[-10:])
    
    bot.send_message(ud(message).id, f'{ud(message).fn}, вот текушие результаты кручения в казино:\n{text}', reply_markup = markup)

@bot.callback_query_handler(func = lambda call: call.data in ['-10', '-', 'bet', '+', '+10'])
def callback_inline(call):
    userdata = wordbook(from_base(call.message, 'users'))
    botdata = wordbook_bot(from_base(call.message, 'bot'))
    if call.message:
        if call.data == '-10': 
            botdata.bet -= 10
            if botdata.bet < 1: botdata.bet = 1
        elif call.data == '-': 
            botdata.bet -= 1
            if botdata.bet < 1: botdata.bet = 1
        elif call.data == 'bet': 
            if userdata.ch < botdata.bet:
                bot.send_message (call.message.chat.id, "Ваша ставка больше вашего счёта!")
                return
            match userdata.st:
                case 'random':
                    base_save_bot (call.message, botdata)
                    randomid(call.message)
                    return
                case 'slot':
                    base_save_bot (call.message, botdata)
                    slot_machin(call.message)
                    return
                case 'rulet':
                    markup = keyboard.inlinekeyboard()
                    botdata.last_mes_id = bot.edit_message_text(chat_id = userdata.id, message_id = botdata.last_mes_id, reply_markup=markup, 
                    text=f'Выберите число!')
                case _:
                    base_save_bot (call.message, botdata)
                    tprint (call.message, 'Игра не выбрана!')
                    play (call.message)
                    quit()
        elif call.data == '+': 
            botdata.bet += 1
        elif call.data == '+10': 
            botdata.bet += 10
    
        if call.data != 'bet' and botdata.last_bet != botdata.bet:
            markup = keyboard.markinline(keyboard.inlinebut('-10'), 
                                    keyboard.inlinebut('-'), 
                                    types.InlineKeyboardButton(f'{botdata.bet}', callback_data='bet'),
                                    keyboard.inlinebut('+'), 
                                    keyboard.inlinebut('+10'), Row_width = 5)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = f'Ваша ставка равна = {botdata.bet}', 
            reply_markup = markup) 
            botdata.last_bet = botdata.bet
            base_save_bot (call.message, botdata)

@bot.callback_query_handler(func = lambda call: call.data in str(range(1, 37)) or ['1-12', '13-24', '25-36', 'Выбор'])
def callback_inline(call):
    userdata = wordbook(from_base(call.message, 'users'))
    botdata = wordbook_bot(from_base(call.message, 'bot'))
    if call.message:
        if call.data == ' ': pass 
        elif call.data == 'Выбор': 
            try:
                if botdata.last_mes_id != False:
                    bot.delete_message(chat_id = userdata.id, message_id = botdata.last_bet_mes_id )
            except: pass
            finally:
                    botdata.pb = 0
                    botdata.last_bet_mes_id = 0
            base_save_bot (call.message, botdata)
            bet_check (call.message)
            return
        elif call.data in str(range(1, 37)) or ['1-12', '13-24', '25-36']:
            botdata.mes_value = call.data
            if botdata.mes_value != botdata.last_mes_value:
                markup = keyboard.inlinekeyboard()
                botdata.last_mes_id = bot.edit_message_text(chat_id = userdata.id, message_id = botdata.mes_id, text = f'Ваша ставка равна = {botdata.mes_value}\nЕсли вы уверены,\nнажмите ещё раз', 
                reply_markup = markup).id
                botdata.last_mes_value = botdata.mes_value
            else: 
                ruletka(call.message)
                return
    base_save_bot (call.message, botdata)
    base_save_user (call.message, userdata)


@bot.message_handler(content_types=['text'])
def messaged (message):
    try:
        userdata = wordbook(from_base(message, 'users'))
        botdata = wordbook_bot(from_base(message, 'bot'))
    except NameError: 
        cdb.execute (f'INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)', (message.from_user.username, None, True, message.from_user.first_name, message.chat.id, 0))
        cdb.execute (f'INSERT INTO bot VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (message.from_user.id, 0, 0, 1, 1, 0, 0, 0.15, 0, 0, 0))
        db.commit()
        userdata = wordbook(from_base(message, 'users'))
        botdata = wordbook_bot(from_base(message, 'bot'))
    try:
        if message.text not in ["🎰 Казино!","🎲 Кости!"]:
            log.critical(f'ID:{userdata.id}, {userdata.fn}({userdata.lg}), написал: {message.text}')
        if message.text == "🎰 Казино!":
            valuedice = bot.send_dice(message.chat.id, emoji='🎰')
            log.critical(f'ID:{userdata.id}, {userdata.fn}({userdata.lg}), в Казино = {valuedice.dice.value}')
        elif message.text == "🎲 Кости!":
            valuedice = bot.send_dice(message.chat.id)
            log.critical(f'ID:{userdata.id}, {userdata.fn}({userdata.lg}), в Кости = {valuedice.dice.value}')
        elif message.text == "Самодельное казино!":
            if userdata.pw is not None: 
                play (message)
            else:
                markup = keyboard.mark(keyboard.button("Вход"), keyboard.button("Регистрация"), keyboard.button("Назад"), Row_width = 2)
                bot.send_message (userdata.id, 'Запуск самодельного Казино!', reply_markup=markup)
        elif message.text == "◀️ Назад":
            welcome(message)
        elif message.text == "Вход":   
            cdb.execute (f"SELECT password FROM users WHERE user_chat_id = '{userdata.id}'")
            if cdb.fetchone()[0] is None:
                tprint (message, 'Вы ещё не зарегистрированы у нас!\n\nРегистрация!\nВведите Пароль')
                bot.register_next_step_handler(message, registrate)
            else:    
                tprint (message, 'Авторизация!\nВведите пароль')
                bot.register_next_step_handler(message, initialization)
        elif message.text == "Регистрация":
            cdb.execute (f"SELECT password FROM users WHERE user_chat_id = '{userdata.id}'")
            if cdb.fetchone()[0] is not None:  
                tprint (message, 'Вы уже зарегистрированы\nЕсли вы забыли пароль, обратитесь в службу поддержки: @p_arti_a')
                return
            tprint (message, 'Регистрация!\nВведите Пароль')
            bot.register_next_step_handler(message, registrate)
        elif userdata.pw is not None and message.text in ["🎱 РандоМит", "🎰 Однорукий Бандит", "🎲 Рулетка"]:
            botdata = wordbook_bot(from_base(message, 'bot'))
            try:
                if botdata.last_mes_id != False:
                    bot.delete_message(chat_id = userdata.id, message_id = botdata.last_mes_id)
                    bot.delete_message(chat_id = userdata.id, message_id = botdata.last_mes_id - 1)
                    bot.delete_message(chat_id = userdata.id, message_id = botdata.last_bet_mes_id)
            except: pass
            finally: 
                    botdata.last_mes_id = 0
                    botdata.last_bet_mes_id = 0
                    botdata.last_mes_value = 0
                    base_save_bot (message, botdata)
            match message.text:
                case "🎱 РандоМит":
                    userdata.st, botdata.pb = 'random', 0
                    tprint (message, 'В данной игре может выпасть число от -20 до 20. В зависимости от выпавшего числа, ваша ставка будет умножена на это число делёное на 10.\nВыйгрыш = Ставка * Число / 10')
                    botdata.mes_id = tprint (message, "Запускаем РандоМит").id
                    base_save_bot (message, botdata)
                    base_save_user (message, userdata)
                case "🎰 Однорукий Бандит":
                    userdata.st, botdata.pb = 'slot', 0
                    table = {'💀':1, '🌑':2.5, '🌕':5, '⭐️':10, '🌈':25, '🔥':50, '💯':100, '💰':250} 
                    tprint (message, ''.join([f'{i}: {table[i]}X\n' for i in table]))
                    botdata.mes_id = tprint (message, "Запускаем Однорукого Бандита").id
                    base_save_bot (message, botdata)
                    base_save_user (message, userdata)
                case "🎲 Рулетка":
                    userdata.st, botdata.pb = 'rulet', 0
                    tprint (message, 'В начале, выбрети ставку, затем выберите число, которое по вашему мнению может выпасть в рулетке.\nЕсли вы угадаете, множители следующие:\nЗа конкретное число: 35Х\nЗа диапозон: 2,5Х')
                    botdata.mes_id = tprint (message, "Запускаем Рулетку").id
                    base_save_bot (message, botdata)
                    base_save_user (message, userdata)
            bet_check(message)
            return
        else: tprint (message, "Нажмите /start для начала работы программы")
    except NameError as e:
        tprint (message, "Вы ещё не авторизировались!")
        log.error (e)


#########################################################
# FUNCSION

def from_base (message, table):
    cdb.execute (f"SELECT * FROM {table} WHERE user_chat_id = '{message.chat.id}'")
    data = cdb.fetchone ()
    if data is None: raise (NameError)
    else:   return data

def base_save_user (message, userdata_save):
    tuple_ = (userdata_save.pw, 
            userdata_save.st, 
            userdata_save.fn, 
            userdata_save.lg, 
            userdata_save.ch)
    cdb.execute (f"""UPDATE users SET password = ?, 
                                    password_state = ?, 
                                    user_first_name = ?, 
                                    login = ?, 
                                    cash = ?  
                                    WHERE user_chat_id = '{message.chat.id}'""", tuple_)
    db.commit()

def base_save_bot (message, botdata_save):
    tuple_ = (botdata_save.mes_id, 
            botdata_save.last_mes_id, 
            botdata_save.bet, 
            botdata_save.last_bet, 
            botdata_save.bet_mes_id,
            botdata_save.last_bet_mes_id,
            botdata_save.ch,
            botdata_save.pb,
            botdata_save.mes_value,
            botdata_save.last_mes_value)
    cdb.execute (f"""UPDATE bot SET message_id = ?,
                                    last_message_id = ?,
                                    bet = ?,
                                    last_bet = ?,
                                    bet_message_id = ?,
                                    last_bet_message_id = ?,
                                    chance = ?,
                                    prob = ?,
                                    message_value = ?,
                                    last_message_value = ?
                                    WHERE user_chat_id = '{message.chat.id}'""", tuple_) 
    db.commit()

#########################################################

def comeback (message):
    userdata = wordbook(from_base(message, 'users'))
    log.critical(f'ID:{ud(message).id}, {ud(message).fn}({ud(message).lg}), написал: {message.text}')
    if message.text in ['/start', '/notification', '◀️ Назад']:
        welcome(message)
        return True
    elif message.text == 'Регистрация':
        tprint (message, 'Регистрация!\nВведите Пароль')
        bot.register_next_step_handler(message, registrate)
        return True
    elif message.text == 'Вход':  
        cdb.execute (f"SELECT password FROM users WHERE user_chat_id = '{userdata.id}'")
        if cdb.fetchone()[0] is None:
            tprint (message, 'Вы ещё не зарегистрированы у нас!\n\nРегистрация!\nВведите Пароль')
            bot.register_next_step_handler(message, registrate)
        else:    
            tprint (message, 'Авторизация!\nВведите пароль')
            bot.register_next_step_handler(message, initialization)
        return True


#########################################################

def tprint (message, text, Reply_markup: str = None):
    userdata = wordbook(from_base(message, 'users'))
    log.critical(f'ID:{userdata.id}, {userdata.fn}({userdata.lg}), вывел на экран: {text}')
    return bot.send_message(message.chat.id , text, reply_markup=Reply_markup)

#########################################################

def registrate (message):
    if comeback(message):  return
    userdata = wordbook(from_base(message, 'users'))
    try:
        userdata.pw = message.text
    except ValueError:
        tprint (message, 'Вы ввели неизвестные символы!\n Возвращаю вас в главное меню.')
        welcome(message)
    match userdata.pw:
        case '':
            tprint (message, 'Вы не ввели данные!')
            bot.register_next_step_handler(message, registrate)
            return
        case userdata.pw if len(userdata.pw) < 4:
            tprint (message, "Вы ввели меньше 4 символов!")
            bot.register_next_step_handler(message, registrate)
            return
    userdata.ch = 100
    base_save_user (message, userdata)
    tprint (message, f'Вы зарегистрировались, {userdata.fn}\nВаш баланс: 100')
    play(message)

#########################################################

def initialization(message):
    if comeback(message):  return
    userdata = wordbook(from_base(message, 'users'))
    try:
        userdata.pw = message.text
    except ValueError:
        tprint (message, 'Вы ввели неизвестные символы!\n Возвращаю вас в главное меню.')
        welcome(message)
    match userdata.pw:
        case '':
            tprint (message, 'Вы не ввели данные!')
            bot.register_next_step_handler(message, initialization)
            return
        case userdata.pw if len(userdata.pw) < 4:
            tprint (message, "Вы ввели меньше 4 символов!")
            bot.register_next_step_handler(message, initialization)
            return
    cdb.execute (f"SELECT user_chat_id FROM users WHERE user_chat_id = '{userdata.id}' AND password = '{userdata.pw}'")
    if cdb.fetchone() is None:
        tprint (message, f'Некорректные данные, повторите попытку\nВведите пароль')
        bot.register_next_step_handler(message, initialization)
        return
    else:
        base_save_user(message, userdata)
        tprint (message, f'Вы успешно авторизировались {userdata.fn}')
        play(message)

#########################################################

def play(message):
    userdata = wordbook(from_base(message, 'users'))
    markup = keyboard.mark(keyboard.button('РандоМит'), keyboard.button('Бандит'), keyboard.button('Рулетка'), keyboard.button('Назад'), Row_width = 2)
    tprint (message, f'\nВ какую игру сыграем?\n1. РандоМит\n2. Однорукий Бандит\n3. Рулетка\nВаш баланс равен: {userdata.ch}', Reply_markup = markup)
    bot.register_next_step_handler(message, messaged)
    return

#########################################################

def bet_check(message):
    botdata = wordbook_bot(from_base(message, 'bot'))
    userdata = wordbook(from_base(message, 'users'))
    markup = keyboard.markinline(keyboard.inlinebut('-10'), 
                                keyboard.inlinebut('-'), 
                                types.InlineKeyboardButton(f'{botdata.bet}', callback_data='bet'),
                                keyboard.inlinebut('+'), 
                                keyboard.inlinebut('+10'), Row_width = 5)
    if botdata.pb == 0:
        botdata.pb += 1
        botdata.last_mes_id = bot.edit_message_text(chat_id = userdata.id, message_id = botdata.mes_id, reply_markup=markup, 
        text=f'Ваша ставка равна = {botdata.bet}').id
    else: pass
    base_save_bot (message, botdata)           

def randomid (message):
    botdata = wordbook_bot(from_base(message, 'bot'))
    userdata = wordbook(from_base(message, 'users'))
    fortune = randint (-20, 20)
    bet_new = (fortune * int(botdata.bet) / 10).real    # Метод .real это класс для предоставления вещественныз чисел. На выходе получаем float
    userdata.ch += round (bet_new, 2)
    if botdata.last_bet_mes_id == False:    
        botdata.last_bet_mes_id = tprint (message, f'Выпало число\nВы\nТеперь ваш баланс равен: ').id 
    if fortune >= 0: 
        botdata.bet_mes_id = bot.edit_message_text(chat_id = userdata.id, message_id = botdata.last_bet_mes_id, text=f"Выпало число {fortune}\n✅Вы выйграли: {round(bet_new,2)}\nТеперь ваш баланс равен: {userdata.ch:.1f}").id
    elif fortune < 0:
        botdata.bet_mes_id = bot.edit_message_text(chat_id = userdata.id, message_id = botdata.last_bet_mes_id, text=f"Выпало число {fortune}\n❌Вы проиграли\nТеперь ваш баланс равен: {userdata.ch:.1f}").id
    botdata.last_bet_mes_id = botdata.bet_mes_id
    log.critical(f'ID:{userdata.id}, {userdata.fn} ({userdata.lg}), Выпало число {fortune}, баланс равен: {userdata.ch:.1f}')
    if userdata.ch <= 0: zeroing(message)
    else:
        cdb.execute (f"UPDATE users SET cash = {userdata.ch:.1f} WHERE user_chat_id = '{userdata.id}'")
        db.commit()
    base_save_bot (message, botdata)
    base_save_user (message, userdata)
    bet_check(message)


########################################################

def slot_machin (message):
    botdata = wordbook_bot(from_base(message, 'bot'))
    userdata = wordbook(from_base(message, 'users'))
    bet_new = botdata.bet
    table = {'💀':1, '🌑':2.5, '🌕':5, '⭐️':10, '🌈':25, '🔥':50, '💯':100, '💰':250} 
    simbol = [i for i in table.keys ()]
    chance = []
    if botdata.last_bet_mes_id == False:
        botdata.last_bet_mes_id = tprint (message, f'\n\n\nВаш баланс = ').id
    chance.append (simbol[int (mt.log(random(), 0.5) % 8)])
    while len(chance)<3:
        if random () < botdata.ch:  chance.append (chance[0])
        else: chance.append (simbol[int (mt.log(random(), 0.5) % 8)])
    if chance [0] == chance [1]: 
        if chance [1] == chance [2]: 
            bet_new *= table.get (chance [-1])
            userdata.ch += bet_new
            botdata.bet_mes_id = bot.edit_message_text(chat_id = userdata.id, message_id = botdata.last_bet_mes_id, text=f'Выпало {" ".join (chance)}\n✅Вы выйграли! = {bet_new}\nВаш баланс = {userdata.ch:.1f}').id
            botdata.ch = 0.15
        else: 
            userdata.ch -= bet_new
            botdata.bet_mes_id = bot.edit_message_text(chat_id = userdata.id, message_id = botdata.last_bet_mes_id, text=f'Выпало {" ".join (chance)}\n❌Почти! Вы проиграли\nВаш баланс = {userdata.ch:.1f}').id
            botdata.ch += 0.05
    else: 
        userdata.ch -= bet_new
        botdata.bet_mes_id = bot.edit_message_text(chat_id = userdata.id, message_id = botdata.last_bet_mes_id, text=f'Выпало {" ".join (chance)}\n❌Пройгрыш!\nВаш баланс = {userdata.ch:.1f}').id
        botdata.ch += 0.05
    if userdata.ch <= 0: zeroing(message)
    else:
        botdata.last_bet_mes_id = botdata.bet_mes_id
        base_save_user (message, userdata)
    log.critical(f'ID:{userdata.id}, {userdata.fn}({userdata.lg}), Выпало {" ".join (chance)}, ставка {bet_new}, баланс = {userdata.ch:.1f}')
    base_save_bot (message, botdata)
    bet_check(message)

########################################################

def ruletka(message):
    botdata = wordbook_bot(from_base(message, 'bot'))
    userdata = wordbook(from_base(message, 'users'))
    if botdata.mes_value.find ('-') != -1:
        chance = [int (f) for f in botdata.mes_value.split ('-')]
        chance = range (chance[0], chance[-1]+1)
    else: chance = int (botdata.mes_value)
    bet = botdata.bet
    rulet = randint (1, 36) 
    # Проверяем выпавшее число со ставкой
    result = 0
    if botdata.last_bet_mes_id == False: botdata.last_bet_mes_id = tprint (message, 'Ваша ставка').id
    if isinstance (chance, int):    
        if rulet == chance:
            result = bet * 35
            userdata.ch += result
            botdata.bet_mes_id = bot.edit_message_text(chat_id = userdata.id, message_id = botdata.last_bet_mes_id, text=f'Выпало число {rulet}\n✅Поздравляем! Вы выйграли: {result:.1f}\nВаш баланс = {userdata.ch:.1f}').id
        else:
            result -= bet
            userdata.ch += result
            botdata.bet_mes_id = bot.edit_message_text(chat_id = userdata.id, message_id = botdata.last_bet_mes_id, text=f'Выпало число {rulet}\n❌Вы проиграли\nВаш баланс = {userdata.ch:.1f}').id
    else:
        if rulet in chance:
            result = bet * 2.5
            userdata.ch += result
            botdata.bet_mes_id = bot.edit_message_text(chat_id = userdata.id, message_id = botdata.last_bet_mes_id, text=f'Выпало число {rulet}\n✅Поздравляем! Вы выйграли: {result:.1f}\nВаш баланс = {userdata.ch:.1f}').id
        else:
            result -= bet
            userdata.ch += result
            botdata.bet_mes_id = bot.edit_message_text(chat_id = userdata.id, message_id = botdata.last_bet_mes_id, text=f'Выпало число {rulet}\n❌Вы проиграли\nВаш баланс = {userdata.ch:.1f}').id
    botdata.last_bet_mes_id = botdata.bet_mes_id
    if userdata.ch <= 0: zeroing(message)
    else:
        base_save_user (message, userdata)
    log.critical(f'ID:{userdata.id}, {userdata.fn}({userdata.lg}), Выпало число {rulet}, ставили на {botdata.mes_value}, баланс = {userdata.ch:.1f}')
    base_save_bot (message, botdata)
    bet_check (message)
    
#########################################################

def zeroing (message):
    userdata = wordbook(from_base(message, 'users'))
    cdb.execute (f"UPDATE users SET cash = 0 WHERE user_chat_id = '{userdata.id}'")
    db.commit()
    tprint (message, "У вас закончились средства! Обраитесь в службу поддержки: @p_arti_a")
    base_save_user(message, userdata)
    welcome(message)

#########################################################
# MAIN PROGRAM

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
try:
    bot.infinity_polling()
except:
    pass

#########################################################