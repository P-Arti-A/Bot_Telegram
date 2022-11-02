import telebot
from telebot import types
from config import TOKEN, direct

class keyboard:
    def mark(*args: tuple, One_time_keyboard: bool = False, Row_width: int = 3):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = One_time_keyboard, row_width = Row_width)
        markup.add (*args)
        return markup

    def button (key, value=None):
        butt = {
        "Да": types.KeyboardButton('Да'),
        "Нет": types.KeyboardButton('Нет'),
        "Казино": types.KeyboardButton("🎰 Казино!"),
        "Кости": types.KeyboardButton("🎲 Кости!"),
        "Моё казино": types.KeyboardButton("Самодельное казино!"),
        "Назад": types.KeyboardButton("◀️ Назад"),
        "Вход": types.KeyboardButton("Вход"),
        "Регистрация": types.KeyboardButton("Регистрация")
        }.setdefault(key, value)
        return butt

# keyboard.mark(keyboard.button('Да'))
# bname = {'casino': "🎰 Казино!", 'bone': "🎲 Кости!", 'my_cas': "Самодельное казино!", 'back': "◀️ Назад"}.get(butt_name)