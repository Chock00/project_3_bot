# t.me/TheMainSystemAgainstSusliks_bot
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
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)
TIMER = 5
reply_keyboard = [['/dice54к', '/timer']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def check_password(name, pw):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.name == name).first()
    if user:
        return str(hash(pw)) ==  str(user.hashed_password)
    return False


async def echo(update, context):
    text = str(update.message.text).split()
    if len(text) == 2 and check_password(text[0], text[1]):
        await update.message.reply_text('Добро пожаловать в систему, ' + text[0])
    else:
        await update.message.reply_text('Неверный логин или пароль')

async def start(update, context):
    await update.message.reply_text(
        '''Главная секретная система армии сопротивления против сусликов. Для пользования системой, пожалуйста, войдите в нее.
        Введите своё имя и пароль через пробел''',
        reply_markup=markup
    )


async def see_all_info(update, context):
    t = str(str(dt.datetime.now()).split(' ')[-1])
    await update.message.reply_text(t)



async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


def main():
    application = Application.builder().token('6807284847:AAEzbdth50Pm_FHUiMA4Or3hBwTxnpoSE38').build()
    text_handler = MessageHandler(filters.TEXT, echo)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("close", close_keyboard))
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()


