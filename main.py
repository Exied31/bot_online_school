import telebot
from config import TOKEN
from keyboards import get_main_menu, get_days_menu
from database import DBManager

# Подключаем базу данных
db = DBManager("school_data.db")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id, 
        "Привет! Я бот онлайн-школы. Нажми на кнопку ниже:",
        reply_markup=get_main_menu() 
    )

@bot.message_handler(content_types=['text'])
def handle_text(message):
    # Получаем список дней из базы сразу
    all_days = db.get_all_days()

    if message.text == "Расписание":
        # Показываем меню с днями
        bot.send_message(
            message.chat.id, 
            "На какой день ты хочешь узнать расписание?",
            reply_markup=get_days_menu(all_days)
        )

    elif message.text == "Назад":
        # Возвращаемся в главное меню
        bot.send_message(
            message.chat.id, 
            "Главное меню:", 
            reply_markup=get_main_menu()
        )

    elif message.text == "Все уроки":
        all_text = "📚 Полное расписание:\n\n"
        for day in all_days:
            info = db.get_day_schedule(day)
            all_text += f"**{day}**: {info}\n"
        bot.send_message(message.chat.id, all_text, parse_mode="Markdown")

    elif message.text in all_days:
        # Если нажали на конкретный день (например, "Понедельник")
        info = db.get_day_schedule(message.text)
        bot.send_message(message.chat.id, f"📅 {message.text}:\n{info}")

# Запуск бота
print("Бот запущен!")
bot.polling(none_stop=True)