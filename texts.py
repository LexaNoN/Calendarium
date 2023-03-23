from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
to_menu = 'Перейти в головне меню'


class Text:
    to_menu = to_menu
    err = 'Перекидаю вас в головне меню'

    class Start:  # start
        text = 'Стартовый текст '


        class kb:
            continue_bttn = 'Продовжити'

        keyboard = ReplyKeyboardMarkup([[KeyboardButton(kb.continue_bttn)]], resize_keyboard=True)



    class Menu:  # menu
        text = 'Оберіть, будь ласка, один з розділів меню, щоб отримати більше інформації'

        class kb:
            info = 'Про компанію'
            drugs = 'Ознайомитися з препаратами'
            question = 'Поставити запитання компанії'
            korisne = 'Корисна інформація'
            rubrikator = 'Рубрикатор по боту'
            rassilka = '(A) Розсилка'

        keyboard = ReplyKeyboardMarkup([
            [KeyboardButton(kb.info), KeyboardButton(kb.question)],
            [KeyboardButton(kb.drugs)]],
            resize_keyboard=True,
            one_time_keyboard=True)

        keyboard_admin = ReplyKeyboardMarkup([
            [KeyboardButton(kb.info), KeyboardButton(kb.drugs)],
            [KeyboardButton(kb.question), KeyboardButton(kb.korisne)],
            [KeyboardButton(kb.rubrikator), KeyboardButton(kb.rassilka)]], resize_keyboard=True,
            one_time_keyboard=True)

