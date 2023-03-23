import threading
from time import sleep

from telegram import ReplyKeyboardMarkup, KeyboardButton, Update, ParseMode, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
import logging

# ---------
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import dc
from dc import *
from database import DB
from config import Config
from texts import Text

# ---------

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logging.getLogger('telegram.bot').setLevel('ERROR')
logger = logging.getLogger(__name__)
logger.info('Folder "parrent" is: ' + parent)
db = DB()
cache = []


def start(update: Update, context: CallbackContext) -> None:  # /start
    get = db.User.get_by_tg_id(update.effective_user.id)
    if get is None:
        db.User.create(update.effective_user.id)

    context.user_data['status'] = 'start'
    context.user_data['rassilka'] = None

    def a(id):
        sleep(5)
        context.bot.send_message(chat_id=id,
                               caption=Text.Start.text, reply_markup=Text.Start.keyboard,
                               parse_mode=ParseMode.MARKDOWN)


def button(update: Update, context: CallbackContext) -> None:  # Inline button
    query = update.callback_query

    text = query.data
    user = db.User.get_by_tg_id(update.effective_user.id)
    status: str = context.user_data.get('status')
    if status is None:
        context.user_data['status'] = 'start'
    print(query)

    if text.startswith('ban_'):
        user_id = query.data.split('_')[1]
        query.message.reply_text(text=f'Користувач {user_id} був '
                                     f'заблокований модератором {update.effective_user.username}',
                                    reply_markup=InlineKeyboardMarkup(
                                    [[InlineKeyboardButton('❎ Розбанити ❎',
                                                           callback_data=f'unban_{user_id}')]]))
    elif text.startswith('navch_test_'):
        query.message.reply_text(Text.Rassilka.text_navch_test4)
        context.user_data['status'] = f'navch_test_{text.split("_")[2]}'  # Сохранение позиции пользователя
    else:
        query.answer(text='Помилка обробки кнопки', show_alert=True)

    try:
        query.answer()
    except Exception:
        pass


def message(update: Update, context: CallbackContext) -> None:  # on message
    text = update.message.text
    user = db.User.get_by_id(update.effective_user.id)

    status: str = context.user_data.get('status')
    if not status:
        context.user_data['status'] = 'start'
        status: str = context.user_data.get('status')
        # update.message.reply_text(Text.err)
        # start(update, context)
        # return

    if text == Text.to_menu:
        start(update, context)
    elif text == Text.Menu.kb.info:
        context.user_data['status'] = 'info'
        update.message.reply_text(Text.Info.text1_tg, reply_markup=Text.Info.keyboard1,
                                  parse_mode=ParseMode.MARKDOWN_V2)
    elif status == 'anketa_9':
        context.user_data['status'] = 'anketa_finnal'
        db.User.update(user.id, context.user_data['anketa'])
        update.message.reply_text(Text.Anketa.finnal,
                                  parse_mode=ParseMode.MARKDOWN)
        start(update, context)


def get_admin_permissions(update: Update, context: CallbackContext) -> None:
    user = db.User.get_by_tg_id(update.effective_user.id)
    if user:
        if user.permission == dc.Permissons.ADMIN:
            db.User.update_permission(update.effective_user.id, dc.Permissons.USER.value)
            update.message.reply_text('Видав права користувача')
        else:
            db.User.update_permission(update.effective_user.id, dc.Permissons.ADMIN.value)
            update.message.reply_text('Видав права адміністратора')
        start(update, context)
    else:
        update.message.reply_text('Ви не зареєстровані')


def reciveFile(update: Update, context: CallbackContext) -> None:
    if update.message.document.file_name.endswith('.xlsx'):
        file = update.message.document
        file_id = file.file_id
        file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '_' + file.file_name
        a = context.bot.get_file(file_id)
        a.download(rf"{parent}/static/rassilka/{file_name}")
        #  wb = load_workbook(rf"{parent}/static/rassilka/{file_name}")




def main() -> None:
    updater = Updater(Config.TG.bot_token, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('credits', credits))
    updater.dispatcher.add_handler(CommandHandler('admin', get_admin_permissions))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(MessageHandler(Filters.document, reciveFile))
    updater.dispatcher.add_handler(MessageHandler(Filters.all, message))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
