import datetime
import json
import logging
from time import sleep

import mysql
import mysql.connector as mc

import dc
from config import Config
from dc import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
# logging.disable(logging.DEBUG)
logger = logging.getLogger('db')


class DB:
    def __init__(self):
        self.conn = self.connect()
        self.conn.autocommit = True
        self.DBCreator: DBCreator = DBCreator(self)
        self.User: User = User(self)

    @staticmethod
    def connect():
        try:
            return mc.connect(
                host=Config.DB.host,
                user=Config.DB.user,
                password=Config.DB.password,
                database=Config.DB.database,
            )
        except mysql.connector.errors.ProgrammingError:
            conn = mc.connect(  # if no database
                host=Config.DB.host,
                user=Config.DB.user,
                password=Config.DB.password,
                database='mysql')
            cursor = conn.cursor()
            cursor.execute(f'CREATE DATABASE {Config.DB.database}')
            conn.commit()
            conn.close()
            return mc.connect(
                host=Config.DB.host,
                user=Config.DB.user,
                password=Config.DB.password,
                database=Config.DB.database)
        except mysql.connector.errors.DatabaseError as e:
            logger.fatal('Database error: ' + e.msg + ', sleeping 120 seconds and exit')
            sleep(120)
            exit(1)
        except Exception as e:
            logger.fatal(f'Database err: {e}, sleeping 120 seconds and exit')
            sleep(120)
            exit(1)

    def get_cursor(self):
        try:
            self.conn.ping(reconnect=True, attempts=3, delay=5)  # check if connection is alive
        except mysql.connector.Error:
            # reconnect your cursor as you did in __init__ or wherever
            try:
                self.conn.close()
            except Exception:
                pass
            self.conn = self.connect()
        self.conn.autocommit = True
        return self.conn.cursor()


class DBCreator:
    def __init__(self, db: DB):
        self.db = db

    def create_db(self):
        cur = self.db.get_cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB.database}")
        self.db.conn.commit()
        cur.close()

    def create_tables(self):
        cur = self.db.get_cursor()
        # create table points with fields id, point, address, and schedule for week
        cur.execute(""" 
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            permission INT DEFAULT 2,
            id_telegram BIGINT UNIQUE,
            nickname TEXT,
            date_reg DATETIME DEFAULT CURRENT_TIMESTAMP
            )""")
        self.db.conn.commit()
        cur.close()


class User:
    def __init__(self, db: DB):
        self.db = db

    @staticmethod
    def transform(data) -> dc.User:
        if data:
            user = dc.User(id=data[0], permission=data[1], id_telegram=data[2], nickname=data[3], posada=data[4],
                            date_reg=data[5])
            return user

    def create(self, user: dc.User):
        cur = self.db.get_cursor()
        cur.execute("""
                INSERT INTO users (id_telegram) VALUES (%s) 
                ON DUPLICATE KEY UPDATE id_telegram = %s""",
                        [user.id_telegra]
                        )
        self.db.conn.commit()
        return True

    def get_by_id(self, id: int) -> dc.User:
        cur = self.db.get_cursor()
        cur.execute("SELECT * FROM users WHERE id = %s", [id])
        return self.transform(cur.fetchone())

    def get_by_tg_id(self, id_tg: int) -> dc.User:
        cur = self.db.get_cursor()
        cur.execute("SELECT * FROM users WHERE id_telegram = %s", [id_tg])
        return self.transform(cur.fetchone())

    def update(self, user_id: int, user: User):
        cur = self.db.get_cursor()
        cur.execute("""
        UPDATE users SET pib = %s, region = %s, address = %s, name_mereja = %s, name_apteka = %s, posada = %s, 
        phone_work = %s, phone_personal = %s, reg = 1 WHERE id = %s""",
                    [user.pib, user.region, user.address, user.name_mereja, user.name_apteka, user.posada,
                     user.phone_work, user.phone_personal, user_id])
        self.db.conn.commit()

    def update_permission(self, user_id: int, permission: int):
        cur = self.db.get_cursor()
        cur.execute("""
        UPDATE users SET permission = %s WHERE id_telegram = %s""",
                    [permission, user_id])
        self.db.conn.commit()



if __name__ == '__main__':
    db = DB()
    db.DBCreator.create_db()
    db.DBCreator.create_tables()
