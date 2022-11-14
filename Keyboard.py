import telebot
from telebot import types
from config import TOKEN, direct

class keyboard:
    def mark(*args: tuple,  One_time_keyboard: bool = False, Row_width: int = 3):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = One_time_keyboard, row_width = Row_width, )
        markup.add (*args)
        return markup

    def markinline (*args: tuple, Row_width: int = 3):
        markup = types.InlineKeyboardMarkup(row_width = Row_width, )
        markup.add (*args)
        return markup

    def button (key):
        butt = {
        "Да": types.KeyboardButton('Да'),
        "Нет": types.KeyboardButton('Нет'),
        "Казино": types.KeyboardButton("🎰 Казино!"),
        "Кости": types.KeyboardButton("🎲 Кости!"),
        "Моё казино": types.KeyboardButton("Самодельное казино!"),
        "Назад": types.KeyboardButton("◀️ Назад"),
        "Вход": types.KeyboardButton("Вход"),
        "Регистрация": types.KeyboardButton("Регистрация"),
        "РандоМит": types.KeyboardButton("🎱 РандоМит"),
        "Бандит": types.KeyboardButton("🎰 Однорукий Бандит"),
        "Рулетка": types.KeyboardButton("🎲 Рулетка"),
        "-": types.KeyboardButton("-"),
        "+": types.KeyboardButton("+"),
        "-10": types.KeyboardButton("-10"),
        "+10": types.KeyboardButton("+10")
        }.get(key)
        return butt

    def inlinebut (key):
        butt = {
        "-10": types.InlineKeyboardButton("-10", callback_data='-10'),
        "-": types.InlineKeyboardButton("-", callback_data='-'),
        "+": types.InlineKeyboardButton("+", callback_data='+'),
        "+10": types.InlineKeyboardButton("+10", callback_data='+10'),
        }.get(key)
        return butt

    def inlinekeyboard():
        markup = types.InlineKeyboardMarkup(row_width = 6)
        markup.add (
        types.InlineKeyboardButton("1", callback_data='1'),
        types.InlineKeyboardButton("2", callback_data='2'),
        types.InlineKeyboardButton("3", callback_data='3'),
        types.InlineKeyboardButton("4", callback_data='4'),
        types.InlineKeyboardButton("5", callback_data='5'),
        types.InlineKeyboardButton("6", callback_data='6'),
        types.InlineKeyboardButton("7", callback_data='7'),
        types.InlineKeyboardButton("8", callback_data='8'),
        types.InlineKeyboardButton("9", callback_data='9'),
        types.InlineKeyboardButton("10", callback_data='10'),
        types.InlineKeyboardButton("11", callback_data='11'),
        types.InlineKeyboardButton("12", callback_data='12'),
        types.InlineKeyboardButton("13", callback_data='13'),
        types.InlineKeyboardButton("14", callback_data='14'),
        types.InlineKeyboardButton("15", callback_data='15'),
        types.InlineKeyboardButton("16", callback_data='16'),
        types.InlineKeyboardButton("17", callback_data='17'),
        types.InlineKeyboardButton("18", callback_data='18'),
        types.InlineKeyboardButton("19", callback_data='19'),
        types.InlineKeyboardButton("20", callback_data='20'),
        types.InlineKeyboardButton("21", callback_data='21'),
        types.InlineKeyboardButton("22", callback_data='22'),
        types.InlineKeyboardButton("23", callback_data='23'),
        types.InlineKeyboardButton("24", callback_data='24'),
        types.InlineKeyboardButton("25", callback_data='25'),
        types.InlineKeyboardButton("26", callback_data='26'),
        types.InlineKeyboardButton("27", callback_data='27'),
        types.InlineKeyboardButton("28", callback_data='28'),
        types.InlineKeyboardButton("29", callback_data='29'),
        types.InlineKeyboardButton("30", callback_data='30'),
        types.InlineKeyboardButton("31", callback_data='31'),
        types.InlineKeyboardButton("32", callback_data='32'),
        types.InlineKeyboardButton("33", callback_data='33'),
        types.InlineKeyboardButton("34", callback_data='34'),
        types.InlineKeyboardButton("35", callback_data='35'),
        types.InlineKeyboardButton("36", callback_data='36'),
        types.InlineKeyboardButton("1-12", callback_data='1-12'),
        types.InlineKeyboardButton("13-24", callback_data='13-24'),
        types.InlineKeyboardButton("25-36", callback_data='25-36'),
        types.InlineKeyboardButton("Ставка", callback_data='Выбор'))
        return markup

# keyboard.mark(keyboard.button('Да'))
# bname = {'casino': "🎰 Казино!", 'bone': "🎲 Кости!", 'my_cas': "Самодельное казино!", 'back': "◀️ Назад"}.get(butt_name)
# 1. РандоМит\n2. Однорукий Бандит\n3. Рулетка