# t.me/TheMainSystemAgainstSusliks_bot.
import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler
import datetime as dt
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)
TIMER = 5
reply_keyboard = [['/dice', '/timer']]
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

async def date(update, context):
    d = str(dt.date.today())
    await update.message.reply_text(d)

async def set_timer(update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.effective_message.chat_id
    # Добавляем задачу в очередь
    # и останавливаем предыдущую (если она была)
    t = context.args[0]
    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_once(task, int(t), chat_id=chat_id, name=str(chat_id), data=int(t))
    text = 'Вернусь через ' + t + ' с.!'
    if job_removed:
        text += ' Старая задача удалена.'
    await update.effective_message.reply_text(text)


def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

async def task(context):
    """Выводит сообщение"""
    await context.bot.send_message(context.job.chat_id, text=f'КУКУ! ' + str(context.job.data) + 'c. прошли!')


async def unset(update, context):
    """Удаляет задачу, если пользователь передумал"""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    await update.message.reply_text(text)


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
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("unset", unset))
    application.add_handler(CommandHandler("date", date))
    application.add_handler(CommandHandler("close", close_keyboard))
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
