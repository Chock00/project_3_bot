# t.me/TheMainSystemAgainstSusliks_bot
import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from data import db_session
from data.users import User
from data.susliks import Suslik
import sqlite3
import requests
import math


db_session.global_init("db/base.db")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)
TIMER = 5
reply_keyboard = [['/add_suslik', '/add_user', '/see_one_info'], 
                  ['/see_all_info', '/change_info_sus', '/find_closest_sus']]
start_key = [['/autorize']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
markup_start = ReplyKeyboardMarkup(start_key, one_time_keyboard=False)


async def start(update, context):
    await update.message.reply_text(
        '''Главная секретная система армии сопротивления против сусликов. 
        Для использования системы, пожалуйста, введите свой пароль''', reply_markup=markup
    )  


async def autoriz(update, context):
    text = str(update.message.text)
    user_id = update.message.from_user.id
    name = update.message.from_user.username
    if check(user_id):
        await update.message.reply_text('Вы уже вошли в аккаунт', reply_markup=markup)  
    elif check_autorize(user_id, text):
        await update.message.reply_text('Добро пожаловать в систему, ' + name, reply_markup=markup)
    else:
        await update.message.reply_text('Неправильный пароль')


def check_autorize(user_id, pw):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id_tg == user_id).first()
    if user.check_password(pw):
        user.is_autorized = True
        db_sess.commit()
        return True
    return False
             

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
        for sus in db_sess.query(Suslik):
            line_1 = 'Имя: ' + sus.name + '\n'
            line_2 = 'Информация: ' + sus.information + '\n'
            line_3 = 'Местоположение: ' + sus.location + '\n'
            te = line_1 + line_2 + line_3
            await context.bot.send_photo(chat_id=update.message.chat_id, photo=sus.foto_bytes, caption=te)
    else:
        await update.message.reply_text('Доступ ограничен. Войдите в систему', reply_markup=markup_start)


async def change_info_sus(update, context):
    if check(update.message.from_user.id):
        await update.message.reply_text('Введите имя суслика, чей параметр вы хотите изменить')
        return 1
    else:
        await update.message.reply_text('Доступ ограничен. Войдите в систему', reply_markup=markup_start)


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
        await update.message.reply_text('Доступ ограничен. Войдите в систему', reply_markup=markup_start)


async def name_sus(update, context):
    await update.message.reply_text('Введите всю имеющуюся информацию о данном суслике')
    context.user_data['name'] = update.message.text
    return 3


async def location_sus(update, context):
    await update.message.reply_text('Введите город обитания суслика')
    context.user_data['info'] = update.message.text
    return 2


async def information_sus(update, context):
    await update.message.reply_text('Загрузите фотографию суслика')
    context.user_data['location'] = update.message.text
    return 4


async def foto_sus(update, context):
    await update.message.reply_text('Готово')
    new_file = await update.message.effective_attachment[-1].get_file()
    await new_file.download_to_drive("data/img/image.jpg")
    with open('data/img/image.jpg', mode='rb') as f:
        binary = sqlite3.Binary(f.read())
    add_sus(context.user_data['name'], context.user_data['info'], context.user_data['location'], binary)
    return ConversationHandler.END


async def add_user(update, context):
    if check(update.message.from_user.id):
        await update.message.reply_text('Введите id из telegram нового сотрудника')
        return 1
    else:
        await update.message.reply_text('Доступ ограничен. Войдите в систему', reply_markup=markup_start)


async def id_tg(update, context):
    await update.message.reply_text('Введите индивидуальный для него пароль')
    context.user_data['id_tg'] = update.message.text
    return 2


async def password(update, context):
    await update.message.reply_text('Готово')
    ad_user(context.user_data['id_tg'], update.message.text)
    return ConversationHandler.END


async def find_closest_sus(update, context):
    if check(update.message.from_user.id):
        await update.message.reply_text('Введите город, в котором вы сейчас находитесь')
        return 1
    else:
        await update.message.reply_text('Доступ ограничен. Войдите в систему', reply_markup=markup_start)


async def see_one_info(update, context):
    if check(update.message.from_user.id):
        await update.message.reply_text('Введите имя суслика, информацию о котором хотите узнать')
        return 1
    else:
        await update.message.reply_text('Доступ ограничен. Войдите в систему', reply_markup=markup_start)


async def name_one(update, context):
    name = update.message.text
    db_sess = db_session.create_session()
    sus = db_sess.query(Suslik).filter(Suslik.name == name).first()
    if sus:
        line_1 = 'Имя: ' + sus.name + '\n'
        line_2 = 'Информация: ' + sus.information + '\n'
        line_3 = 'Местоположение:' + sus.location + '\n'
        te = line_1 + line_2 + line_3
        await context.bot.send_photo(chat_id=update.message.chat_id, photo=sus.foto_bytes, caption=te)
    else:
        await update.message.reply_text('Такого суслика в базе нет')
    return ConversationHandler.END


async def city_user(update, context):
    city = update.message.text
    text = find_closest(city)
    db_sess = db_session.create_session()
    sus = db_sess.query(Suslik).filter(Suslik.id == int(text)).first()
    l1 = 'Имя: ' + sus.name + '\n'
    l2 = 'Местоположение: ' + sus.location
    await update.message.reply_text(l1 + l2)
    return ConversationHandler.END


def change_sus(name, what, new):
    db_sess = db_session.create_session()
    sus = db_sess.query(Suslik).filter(Suslik.name == name).first()
    if sus is None:
        return 'Суслика с таким именем нет в базе'
    name = ['имя', 'name']
    info = ['информация', 'info', 'information']
    loc = ['локация', 'местоположение', 'location', 'месторасположение']
    foto = ['фото', 'фотография', 'foto', 'foto_bytes']
    if what.lower() in name:
        sus.name = new
    elif what.lower() in info:
        sus.information = new
    elif what.lower() in loc:
        sus.location = new
    elif what.lower() in foto:
        sus.foto_bytes = new
    else:
        return 'Такого параметра у суслика нет'
    db_sess.commit()
    return 'Готово'


def add_sus(name, info, loca, foto):
    db_sess = db_session.create_session()
    sus = Suslik()
    sus.name = name
    sus.information = info
    sus.location = loca
    sus.foto_bytes = foto
    db_sess.add(sus)
    db_sess.commit()


def ad_user(id_tg, password):
    db_sess = db_session.create_session()
    user = User()
    user.id_tg = id_tg
    user.is_autorized = False
    user.set_password(password)
    db_sess.add(user)
    db_sess.commit()


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000 # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    distance = math.sqrt(dx * dx + dy * dy)
    return distance


def len_trip(us, sus):
    g1 = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=" + us + "&format=json"
    g2 = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=" + sus + "&format=json"
    r1 = requests.get(g1)
    r2 = requests.get(g2)
    if r1 and r2 and r1.json()["response"]["GeoObjectCollection"]["featureMember"] and r2.json()["response"]["GeoObjectCollection"]["featureMember"]:
        t1 = r1.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        c_home = [float(i) for i in t1["Point"]["pos"].split()]
        t2 = r2.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        c_school = [float(i) for i in t2["Point"]["pos"].split()]
        return lonlat_distance(c_home, c_school)
    else:
        return "Ошибка выполнения запроса"


def find_closest(city):
    db_sess = db_session.create_session()
    al = []
    for sus in db_sess.query(Suslik):
        trip = len_trip(city, sus.location)
        if trip != str(trip):
            al.append((trip, sus.id))
    al.sort(key=lambda s: s[0])
    return al[0][1]


conv_handler_1 = ConversationHandler(
        entry_points=[CommandHandler('add_suslik', add_suslik)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, name_sus)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, information_sus)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, location_sus)],
            4: [MessageHandler(~filters.COMMAND, foto_sus)]
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
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, new)]
        },
        fallbacks=[CommandHandler('ok', ok)]
    )
conv_handler_4 = ConversationHandler(
        entry_points=[CommandHandler('find_closest_sus', find_closest_sus)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, city_user)]
        },
        fallbacks=[CommandHandler('ok', ok)]
    )
conv_handler_5 = ConversationHandler(
        entry_points=[CommandHandler('see_one_info', see_one_info)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, name_one)]
        },
        fallbacks=[CommandHandler('ok', ok)]
    )


def main():
    application = Application.builder().token('6807284847:AAEzbdth50Pm_FHUiMA4Or3hBwTxnpoSE38').build()
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, autoriz)
    application.add_handler(conv_handler_1)
    application.add_handler(conv_handler_2)
    application.add_handler(conv_handler_3)
    application.add_handler(conv_handler_4)
    application.add_handler(conv_handler_5)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("see_all_info", see_all_info))
    application.add_handler(CommandHandler("autorize", autorize))
    application.add_handler(CommandHandler("close", close_keyboard))
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
