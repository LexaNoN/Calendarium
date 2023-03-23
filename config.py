import logging
from dc import *
from gettext import gettext as _


class Config:
    logger_lvl = logging.DEBUG

    class TG:
        debug = False
        admins = [
            666147669, # @lexanon - Лёша
        ]
        bot_token = ''  #

    class DB:
        debug = False
        # host = 'db'
        if debug:
            host = 'localhost'
            port = 3306
            user = ''
            password = ''
            database = ''
        else:
            host = 'https://lexanon.me'
            port = 0
            user = ''
            password = ''
            database = ''
