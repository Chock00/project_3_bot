# t.me/TheMainSystemAgainstSusliks_bot.
import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler
import datetime as dt
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from data import db_session

db_session.global_init("db/people.db")
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)
TIMER = 5
reply_keyboard = [['/dice54к', '/timer']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


async def echo(update, context):
    await update.message.reply_text('Я получил сообщение ' + update.message.text)

async def start(update, context):
    await update.message.reply_text(
        "Главная секретная система армии сопротивления против сусликов. Для пользования системой, пожалуйста, войдите в нее",
        reply_markup=markup
    )


async def time(update, context):
    t = str(str(dt.datetime.now()).split(' ')[-1])
    await update.message.reply_text(t)



async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


def main():
    application = Application.builder().token('7046686907:AAG34DBnOZhz9lvn4ozXHbVZ84_Lz4SWDK0').build()
    text_handler = MessageHandler(filters.TEXT, echo)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("time", time))
    application.add_handler(CommandHandler("close", close_keyboard))
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()


import sqlite3from PIL import Image
# открываем изображение
image = Image.open('example.jpg')
# преобразуем изображение в массив байтов
image_bytes = image.tobytes()
# подключаемся к базе данных 
SQLiteconnection = sqlite3.connect('database.sqlite')
cursor = connection.cursor()
# создаем таблицу для хранения изображений
cursor.execute('CREATE TABLE images (id INTEGER PRIMARY KEY AUTOINCREMENT, data BLOB)')
# сохраняем изображение в базе данных
cursor.execute('INSERT INTO images (data) VALUES (?)', (image_bytes,))connection.commit()
# закрываем соединение с базой данных
cursor.close()connection.close()