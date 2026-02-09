from telebot import types

def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Расписание"), types.KeyboardButton("Все уроки"))
    return markup

def get_days_menu(days):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем кнопки для каждого дня из списка
    for day in days:
        markup.add(types.KeyboardButton(day))
    markup.add(types.KeyboardButton("Назад"))
    return markup