# t.me/TheMainSystemAgainstSusliks_bot.
import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler
import datetime as dt
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from data import db_session
from data.users import User
from data.susliks import Suslik
import sqlite3

db_session.global_init("db/base.db")
user_1 = User()
user_1.name = "Mega_cap"
user_1.job = "capitan"
user_1.hashed_password = str(hash('mega_secret_password'))
db_sess = db_session.create_session()
db_sess.add(user_1)
db_sess.commit()

user_2 = User()
user_2.name = "Less_mega_cap"
user_2.job = "Assistant"
user_2.hashed_password = str(hash('less_mega_secret_password'))
db_sess = db_session.create_session()
db_sess.add(user_2)
db_sess.commit()

suslik_1 = Suslik()
suslik_1.name = "Mega_sus"
suslik_1.information = "The most dangerous suslik"
with open('data/img/mega_sus.jpg', mode='rb') as f:
    binary = sqlite3.Binary(f.read())
suslik_1.foto_bytes = binary
db_sess = db_session.create_session()
db_sess.add(suslik_1)
db_sess.commit()

suslik_2 = Suslik()
suslik_2.name = "Susi"
suslik_2.information = "Common_suslik_1"
with open('data/img/common_sus.jpg', mode='rb') as f:
    binary = sqlite3.Binary(f.read())
suslik_2.foto_bytes = binary
db_sess = db_session.create_session()
db_sess.add(suslik_2)
db_sess.commit()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)
TIMER = 5
reply_keyboard = [['/dice54к', '/timer']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def check_password(pw):
    pass



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


