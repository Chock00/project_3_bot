# t.me/TheMainSystemAgainstSusliks_bot
import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from data import db_session
from data.users import User
from data.susliks import Suslik
import sqlite3


db_session.global_init("db/base.db")
user_1 = User()
user_1.id_tg = "1711108797"
user_1.is_autorized = False
user_1.set_password('pw')
db_sess = db_session.create_session()
db_sess.add(user_1)
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
reply_keyboard = [['/see_all_info', '/change_info_sus'], 
                  ['/add_suslik', '/add_user']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def check_autorize(user_id, pw):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id_tg == user_id).first()
    if  bool(user and user.check_password(pw)) is True:
        user.is_autorized = True
        return True
    return False


async def autoriz(update, context):
    text = str(update.message.text)
    user_id = update.message.from_user.id
    name = update.message.from_user.username
    if check_autorize(text, user_id):
        await update.message.reply_text('Добро пожаловать в систему, ' + name)
    else:
        await update.message.reply_text('Неверный пароль')

async def start(update, context):
    await update.message.reply_text(
        '''Главная секретная система армии сопротивления против сусликов. 
        Для использования системы, пожалуйста, введите свой пароль''',
        reply_markup=markup
    )


async def autorize(update, context):
    await update.message.reply_text(
        '''Введите свой пароль''',)


def check(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id_tg == user_id).first()
    return bool(user and user.is_autorized)


async def ok(update, context):
    await update.message.reply_text("Что ещё хотите сделать?", reply_markup=markup)
    return ConversationHandler.END


async def see_all_info(update, context):
    if check(update.message.from_user.id):
        db_sess = db_session.create_session()
        all_lines = []
        for sus in db_sess.query(Suslik):
            line_1 = 'Имя: ' + sus.name + '\n'
            line_2 = 'Информация: ' + sus.information + '\n'
            foto = sus.foto_bytes
            line_3 = 'Фото: '
            line_4 = '***********' + '\n'
            all_lines.append(line_1, line_2, line_3, line_4)
        await update.message.reply_text(all_lines)
    else:
        await update.message.reply_text('Доступ ограничен. Войдите в систему')


async def change_info_sus(update, context):
    if check(update.message.from_user.id):
        await update.message.reply_text('Введите имя суслика, чей параметр вы хотите изменить')
        return 1
    else:
        await update.message.reply_text('Доступ ограничен. Войдите в систему')


async def name(update, context):
    await update.message.reply_text('Введите название параметра, который вы хотите изменить')
    context.user_data['name'] = update.message.text
    return 2


async def what(update, context):
    await update.message.reply_text('Введите новое значение параметра')
    context.user_data['what'] = update.message.text
    return 3


async def new(update, context):
    await update.message.reply_text('Готово')
    change_sus(context.user_data['name'], context.user_data['what'], update.message.text)
    return ConversationHandler.END


async def add_suslik(update, context):
    if check(update.message.from_user.id):
        await update.message.reply_text('Введите имя нового суслика')
        return 1
    else:
        await update.message.reply_text('Доступ ограничен. Войдите в систему')

async def name_sus(update, context):
    await update.message.reply_text('Введите всю имеющуюся информацию о данном суслике')
    context.user_data['name'] = update.message.text
    return 2


async def information_sus(update, context):
    await update.message.reply_text('Загрузите фотографию суслика')
    context.user_data['info'] = update.message.text
    return 3


async def foto_sus(update, context):
    await update.message.reply_text('Готово')
    add_sus(context.user_data['name'], context.user_data['info'], update.message.text)
    return ConversationHandler.END


async def add_user(update, context):
    if check(update.message.from_user.id):
        await update.message.reply_text('Введите id из telegram нового сотрудника')
        return 1
    else:
        await update.message.reply_text('Доступ ограничен. Войдите в систему')


async def id_tg(update, context):
    await update.message.reply_text('Введите индивидуальный для него пароль')
    context.user_data['id_tg'] = update.message.text
    return 2


async def password(update, context):
    await update.message.reply_text('Готово')
    ad_user(context.user_data['id_tg'], update.message.text)
    return ConversationHandler.END


def change_sus(name, what, new):
    db_sess = db_session.create_session()
    sus = db_sess.query(Suslik).filter(Suslik.name == name).first()
    if what == 'name':
        sus.name = new
    elif what == 'information':
        sus.information = new
    else:
        sus.foto_bytes = new
    db_sess.commit()


def add_sus(name, info, foto):
    db_sess = db_session.create_session()
    sus = Suslik()
    sus.name = name
    sus.information = info
    sus.foto_bytes = foto
    db_sess.add(sus)
    db_sess.commit()


def ad_user(id_tg, password):
    db_sess = db_session.create_session()
    user = User()
    user.id_tg = id_tg
    user.set_password(password)
    db_sess.add(user)
    db_sess.commit()


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


conv_handler_1 = ConversationHandler(
        entry_points=[CommandHandler('add_suslik', add_suslik)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, name_sus)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, information_sus)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, foto_sus)]
        },
        fallbacks=[CommandHandler('ok', ok)]
    )
conv_handler_2 = ConversationHandler(
        entry_points=[CommandHandler('add_user', add_user)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, id_tg)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, password)]
        },
        fallbacks=[CommandHandler('ok', ok)]
    )
conv_handler_3 = ConversationHandler(
        entry_points=[CommandHandler('change_info_sus', change_info_sus)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, what)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, new)]
        },
        fallbacks=[CommandHandler('ok', ok)]
    )
def main():
    application = Application.builder().token('6807284847:AAEzbdth50Pm_FHUiMA4Or3hBwTxnpoSE38').build()
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, autoriz)
    application.add_handler(conv_handler_1)
    application.add_handler(conv_handler_2)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("see", see_all_info))
    application.add_handler(CommandHandler("close", close_keyboard))
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
