import telebot
from telebot import types
from config import TOKEN, direct

class keyboard:
    def mark(*args: tuple, One_time_keyboard: bool = False, Row_width: int = 3):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = One_time_keyboard, row_width = Row_width)
        markup.add (*args)
        return markup

    def markinline (*args: tuple, Row_width: int = 3):
        markup = types.InlineKeyboardMarkup(row_width = Row_width)
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
        "+10": types.InlineKeyboardButton("+10", callback_data='+10')
        }.get(key)
        return butt

# keyboard.mark(keyboard.button('Да'))
# bname = {'casino': "🎰 Казино!", 'bone': "🎲 Кости!", 'my_cas': "Самодельное казино!", 'back': "◀️ Назад"}.get(butt_name)
# 1. РандоМит\n2. Однорукий Бандит\n3. Рулетка