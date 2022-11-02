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


class ud:   #UserData Class
    def __init__(self, message, user_login = None, user_password = None):
        self.ms = message
        self.id = message.chat.id #User identifier
        self.fn = message.from_user.first_name #First username
        self.un = message.from_user.username #User nickname 
        self.lg = user_login
        self.pw = user_password
        self.tx = message.text

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

db = sqlite3.connect ('Telegram_bot/CasinoDataTelegram.db', check_same_thread=False)  # DataBase
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
    log.info(f'ID:{ud(message).id}, {ud(message).fn}({ud(message).un}), исп. команду: {message.text}')
    markup = keyboard.mark(keyboard.button("Казино"), keyboard.button("Кости"), keyboard.button("Моё казино"))

    bot.send_message(ud(message).id, f"Добро пожаловать, {ud(message).fn}!\nЯ - *{bot.get_me().first_name}*, бот созданный чтобы быть подопытным кроликом.",
    parse_mode='markdown', reply_markup = markup)

@bot.message_handler(commands=['notification'])
def notification(message):
    log.info(f'ID:{ud(message).id}, {ud(message).fn}({ud(message).un}), исп. команду: {message.text}')
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

# def statemachin (message):
#     if message.text == "":


@bot.message_handler(content_types=['text'])
def messaged (message):
    if message.text not in ["🎰 Казино!","🎲 Кости!"]:
        log.info(f'ID:{ud(message).id}, {ud(message).fn}({ud(message).un}), написал: {message.text}')
    if message.text == "🎰 Казино!":
        valuedice = bot.send_dice(message.chat.id, emoji='🎰')
        log.info(f'ID:{ud(message).id}, {ud(message).fn}({ud(message).un}), в Казино = {valuedice.dice.value}')
    elif message.text == "🎲 Кости!":
        valuedice = bot.send_dice(message.chat.id)
        log.info(f'ID:{ud(message).id}, {ud(message).fn}({ud(message).un}), в Кости = {valuedice.dice.value}')
    elif message.text == "Самодельное казино!":
        markup = keyboard.mark(keyboard.button("Вход"), keyboard.button("Регистрация"), keyboard.button("Назад"), One_time_keyboard = True, Row_width = 2)
        bot.send_message (ud(message).id, 'Запуск самодельного Казино!', reply_markup=markup)
        # tprint (message, 'Авторизация:\nЛогин:')

    elif message.text == "◀️ Назад":
        welcome(message)
    elif message.text == "Вход":   
        tprint (message, 'Авторизация!\nВведите данные.\nЛогин;Пароль')
        bot.register_next_step_handler(message, initialization)
    elif message.text == "Регистрация":
        tprint (message, 'Регистрация!\nВведите данные.\nЛогин;Пароль')
        bot.register_next_step_handler(message, registrate)
    
    


# print ('Время ожидания, превышено!')
#     quit()

#########################################################
# FUNCSION
# @bot.message_handler(commands=['start', 'notification'])

def comeback (message):
    log.info(f'ID:{ud(message).id}, {ud(message).fn}({ud(message).un}), написал: {message.text}')
    if message.text in ['/start', '/notification', '◀️ Назад']:
        welcome(message)
        return True

def tprint (message, text):
    log.info(f'ID:{ud(message).id}, {ud(message).fn}({ud(message).un}), вывел на экран: {text}')
    return bot.send_message(ud(message).id, text)


def registrate (message):
    if comeback(message):  return
    user = ud(message)
    try:
        user.lg, user.pw = user.tx.split(';')
    except ValueError:
        tprint (message, 'Вы не указали разделитель!')
        exit()
    if '' in [user.lg, user.pw] :
        tprint (message, 'Вы не ввели данные!')
        bot.register_next_step_handler(message, registrate)
        exit()
    cdb.execute (f'INSERT INTO users VALUES (?, ?, ?)', (user.lg, user.pw, 100))
    db.commit()
    tprint (message, f'Вы зарегистрировались, {user.lg} {user.pw}\nВаш баланс: 100')

def password(message):
    global user
    if message.text == '':
        tprint (message, 'Вы не ввели пароль!')
        bot.register_next_step_handler(message, password)
    else:
        cdb.execute (f"SELECT password FROM users WHERE login = '{message.text}'")
        if cdb.fetchone () is None:
            user = ud(message, user.lg, message.text)
            # cdb.execute (f"INSERT INTO users VALUES (?, ?, ?)", (user.lg, user.pw, 100))
            tprint (message, f'{user.lg}, вы успешно зарегистрировались!')

prob = 0 # Пробные попытки авторизации в функции initialization которая объявлена глобальной

def initialization(message):
    global prob
    if comeback(message):  return
    if prob == 3:
        tprint (message, 'Вы не смогли войти!')
        quit ()
    user = ud(message)
    # if '/' in [user.tx.split()]:
    #     tprint (message, 'Повторите команду')
    #     exit()
    try:
        user.lg, user.pw = user.tx.split(';')
    except ValueError:
        tprint (message, 'Вы не указали разделитель!')
        bot.register_next_step_handler(message, initialization)
        return
    cdb.execute (f"SELECT login FROM users WHERE login = '{user.lg}' AND password = '{user.pw}'")
    if cdb.fetchone() is None:
        tprint (message, f'Некорректные данные, у вас осталось {3 - prob} попыток\nПовторите попытку\nЛогин;Пароль')
        prob += 1
        bot.register_next_step_handler(message, initialization)
        return
    else: 
        tprint (message, f'Вы успешно авторизировались {user.lg}')
        # if input_set () in ['Y', 'y', 'У', 'у']:
            # while True:
            #     login = input_set ('Login (>30 символов): ')
            #     if len(login) > 30: 
            #         tprint (message, 'Введеное кол-во символов превышает лимит')
            #         continue
            #     password = input_set ('Password (>16 символов): ')
            #     if len(password) > 16: 
            #         tprint (message, 'Введеное кол-во символов превышает лимит')
            #         continue
            #     registrate(login, password)
            #     tprint (message, "Вы успешно зарегистрировались!\n")
            # play()
            # quit ()
        # else:   tprint (message, "Для продолжения, нужно зарегистрироваться!"), quit()
    # user_pas = input_set ('Password: ')
    # cdb.execute (f"SELECT login, password FROM users WHERE login = '{user_login}' AND password = '{user_pas}'")
    # if cdb.fetchone() is None:
    #     if probs == 0:
    #         tprint (message, "К сожалению, вы заблокированы.")
    #         quit()
    #     else:
    #         tprint (f'Неверный пароль! У вас осталось {probs} попыток')
    #     probs -= 1
    # else:
    #     return (user_login, user_pas)

#########################################################

# #########################################################
    
# def show_user(user): 
#     for value in cdb.execute (f"SELECT * FROM users WHERE login = '{user}'"):
#         tprint (value)

# #########################################################
    
# def show_all_user(): 
#     for value in cdb.execute (f"SELECT * FROM users"):
#         tprint (value)

# #########################################################


# def prob_init (user_login):
#     cdb.execute (f"SELECT * FROM users WHERE login = '{user_login}'")
#     if cdb.fetchone () is None: return tprint (message, "Не найден данный логин!"), quit()
#     else: return user_login

# #########################################################

# def delete (user_login):
#     prob_init (user_login)
#     cdb.execute (f"DELETE FROM users WHERE login = '{user_login}'")
#     db.commit()
#     tprint (message, "Пользователь удалён!")
#     initialization()

# #########################################################

# def zeroing (user_login):
#     prob_init (user_login)
#     cdb.execute (f"UPDATE users SET cash = 0 WHERE login = '{user_login}'")
#     db.commit()
#     tprint (message, "Ваш баланс = 0!")

# #########################################################

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
    
# #########################################################

# def bet_check (user_login):
#     prob_init (user_login)
#     cdb.execute (f"SELECT  cash from users WHERE login = '{user_login}'")
#     cash = cdb.fetchone()[0]
#     try:
#         bet = input_set('\nВаша ставка: ')
#         if bet in ['quit', 'continue', 'break', 'выход', 'выйти', 'дальше']:
#             main_table (user_login)
#             play(user_login)
#             quit()
#         if abs(int(bet)) > cash:
#             return tprint (message, "Ставка слишком большая!")
#         return abs(int(bet))
#     except ValueError: 
#         tprint (message, 'Введите цифры!')
#         return

# #########################################################
# def input_set(text):
#     if text in ['setings', 'seting', 'settings', 'setting']:
#         setings()
#         quit()
#     elif text == "": 
#         tprint (message, "Вы не ввели никаких данных!")
#         input_set ()
#     else: return text

# #########################################################
# def play(user_login):
    
#     tprint (message, '\nВ какую игру сыграем?\n1. РандоМит\n2. Однорукий Бандит\n3. Рулетка')
#     # try:
#     #     result = int(input_set('1/2/3: '))
#     #     if result == 1:  randomid (user_login)
#     #     if result == 2:  slot_machin (user_login)
#     #     if result == 3:  ruletka (user_login)
#     # except ValueError:
#     #     tprint (message, 'Введите цифры!') 
#     #     play()
#     # else: 
#     #     main_table(user_login)
#     #     tprint (message, 'Приходите ещё!\n')
#     quit()

# #########################################################

# def randomid (user_login):
#     prob_init(user_login)
#     tprint (ud.ms, '\nКА-ЗИ-НО!\nРандоМит')
#     while True:
#         cdb.execute (f"SELECT cash from users WHERE login = '{user_login}'")
#         cash = cdb.fetchone()[0]
#         tprint (ud.ms, '\nНаигрались? Пишите "выход/quit" для выхода')
#         bet = bet_check(user_login)
#         if bet is None: continue
#         fortune = randint (-20, 20)
#         bet_new = (fortune * int(bet) / 10).real
#         cash += round (bet_new, 2)
#         if fortune >= 0: 
#             tprint (f"Выпало число {fortune}\nВы выйграли: {round(bet_new,2)}")
#         elif fortune < 0:
#             tprint (f"Выпало число {fortune}\nВы проиграли: {round(bet_new,2)}")
#         if cash < 0: zeroing(user_login)
#         else:
#             cdb.execute (f"UPDATE users SET cash = {cash:.1f} WHERE login = '{user_login}'")
#             db.commit()
#             tprint (f"\nТеперь ваш баланс равен: {cash:.1f}")

# #########################################################

# def slot_machin (user_login):
#     while True:
#         prob_init (user_login)
#         tprint (message, '\nНаигрались? Пишите "выход/quit" для выхода')
#         bet = bet_check (user_login)
#         if bet is None: continue
#         cdb.execute (f"SELECT cash from users WHERE login = '{user_login}'")
#         cash = cdb.fetchone()[0]
#         table = {'Ѿ':20, 'Ѽ':10, 'Ѻ':5, 'Ѭ':2.5, 'Ѫ':1, 'Ѧ':0.5, 'Ӕ':0.25, 'Ҩ':0.1}
#         simbol = [i for i in table.keys ()]
#         chance = []
#         random_chance = 7
#         for i in table:
#             tprint (f'{i}: {table[i]}X', end='       ')
#         for i in range (random_chance):
#             if random () > i * 0.1 + 0.25: random_chance -= 1 
#         chance.append (simbol [random_chance])
#         while len(chance)<3:
#             if random () > 0.5:  chance.append (chance[0])
#             else: chance.append (simbol[randint(0,7)])
#         if chance [0] == chance [1]: 
#             if chance [1] == chance [2]: 
#                 bet *= table.get (chance [-1])
#                 tprint (message, " ".join (chance), "Вы выйграли! ", bet)
#             else: 
#                 tprint (message, " ".join (chance), "Почти! Вы проиграли: ", bet)
#                 bet -= bet*2
#         else: 
#             tprint (message, " ".join (chance), "Пройгрыш! Вы проиграли: ", bet)
#             bet -= bet*2
#         cdb.execute (f"UPDATE users SET cash = {cash+bet} WHERE login = '{user_login}'")
#         db.commit()
#         show_user (user_login)
#         # chance = set(simbol)
#         # print (simbol,chance)

# #########################################################

# def ruletka(user_login):
#     # prob_init(user_login)
#     table_rulet = [i for i in range(1, 37)]
#     table_rulet.extend (['1-12', '13-24', '25-36'])
#     while True:
#         tprint (message, '\nНаигрались? Пишите "выход/quit" для выхода')
#         bet = bet_check (user_login)
#         if bet is None: continue
#         # Выведение в терминал стола рулетки
#         tprint (message, 'Выберите куда поставить вашу ставку:\n')
#         for i in range (1,37):
#             if i < 9:
#                 tprint (i, end='   ')
#             else: tprint (i, end='  ')
#             if i % 3 == 0: print()
#         tprint (message, " ".join (table_rulet [-3:]))
#         # Проверяем выбор игрока на корректные значения
#         while True:
#             try:
#                 number = input_set()
#                 if number in table_rulet [-3:]:
#                     break
#                 elif number not in table_rulet:
#                     tprint (message, 'Вы введи некорректный номер!')
#                     continue
#                 number = abs(int(number))
#                 break
#             except ValueError:
#                 tprint (message, 'Вы введи некорректный номер!')
#                 continue
#         # Выводим число выпавшее на рулетке
#         cdb.execute (f"SELECT cash from users WHERE login = '{user_login}'")
#         cash = cdb.fetchone()[0]
#         tprint (message, 'Выпало число: ') 
#         rulet = randint (1, 36)
#         tprint (rulet)
#         # Проверяем выпавшее число со ставкой
#         result = 0
#         if isinstance (number, int): 
#             if rulet == number:
#                 result = bet * 35
#                 print(f'Поздравляем! Вы выйграли: {result}')
#             else:
#                 result -= bet
#                 print(f'Вы проиграли {result}')
#         else:
#             number = number.split ('-')
#             if int(number[0]) <= rulet <= int(number[1]):
#                 result = bet * 2.5
#                 print(f'Поздравляем! Вы выйграли: {result}')
#             else:
#                 result -= bet
#                 print(f'Вы проиграли {result}')
#         cdb.execute (f"UPDATE users SET cash = {cash+result} WHERE login = '{user_login}'")
#         db.commit()
#         tprint (f'Ваш баланс: {cash+result}')
    

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
bot.polling(none_stop = True)
#########################################################