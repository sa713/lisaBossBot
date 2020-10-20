#!/usr/bin/python
# -*- coding: utf-8 -*-

import configparser
import datetime
import requests
import telebot
import mysql.connector as mariadb
from mysql.connector import Error
from telebot import types
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram.ext import Filters, MessageHandler

config = configparser.ConfigParser()
config.read('configbot.conf')

bot_token = config.get('botconfig','bot_token')
chat_id = config.get('botconfig','chat_id_prom') #ПРОМ
#chat_id = config.get('botconfig','chat_id_ift') #ИФТ
master_id = config.get('botconfig','master_id')
db_user = config.get('botconfig','db_user')
db_password = config.get('botconfig','db_password')
db_database = config.get('botconfig','db_database')

webhook_host = config.get('botconfig','webhook_host')
webhook_port = config.get('botconfig','webhook_port')
webhook_listen = config.get('botconfig','webhook_listen')

webhook_ssl_cert = './webhook_cert.pem'
webhook_ssl_priv = './webhook_priv.key'

webhook_url_base = "https://%s:%s" % (webhook_host, webhook_port)
webhook_url_path = "/%s/" % (bot_token)

bot = telebot.TeleBot(bot_token)

app = web.Application()

def start(update, context):
    if update.message.from_user.username == master_id:
        bot.send_message(chat_id=update.message.chat_id, text="Приветствую тебя, Мастер!")
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Только Мастер может запускать бота.")

def plus(update, context):
    if update.message.from_user.username == master_id:
        bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEBUcxfWoTWE9_fH2LLHiePekrjcTQD8wACIQMAApKYGQABS3-P5xR5J7gbBA')
        try:
            mariadb_connection = mariadb.connect(user=db_user, password=db_password, database=db_database)
            sql_select_rating = "SELECT a FROM lisarating;"
            cursor = mariadb_connection.cursor()

            cursor.execute(sql_select_rating)
            rating_lisa = cursor.fetchall()

            for row in rating_lisa:
                sql_update_rating = "UPDATE lisarating SET a = a + 1"
                text_rating = "Текущий рейтинг " + str(row[0]+1)

            cursor.execute(sql_update_rating)
            mariadb_connection.commit()

            bot.send_message(chat_id, text_rating)
        except Exception as e:
            print(e)

        finally:
            if (mariadb_connection.is_connected()):
                mariadb_connection.close()

        else:
        bot.send_message(chat_id=update.message.chat_id, text="Только Мастер может управлять рейтингом.")

def minus(update, context):
    if update.message.from_user.username == master_id:
        bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEBUcpfWoRaQ1xlcZrCW-9ww9j0X03e4gACGwMAApKYGQABXKvAZtGGe6sbBA')

        try:
            mariadb_connection = mariadb.connect(user=db_user, password=db_password, database=db_database)
            sql_select_rating = "SELECT a FROM lisarating;"
            cursor = mariadb_connection.cursor()

            cursor.execute(sql_select_rating)
            rating_lisa = cursor.fetchall()

            for row in rating_lisa:
                sql_update_rating = "UPDATE lisarating SET a = a - 1"
                text_rating = "Текущий рейтинг " + str(row[0]-1)

            cursor.execute(sql_update_rating)
            mariadb_connection.commit()

            bot.send_message(chat_id, text_rating)

        except Exception as e:
            print(e)

        finally:
            if(mariadb_connection.is_connected()):
                mariadb_connection.close()
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Только Мастер может управлять рейтингом.")

def rating(update, context):
    bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEBUc5fWoUdCrBoM0HJV6euckYYXLzPTwACDwMAApKYGQABO29Om3RWbfQbBA')
    try:
        mariadb_connection = mariadb.connect(user=db_user, password=db_password, database=db_database)
        sql_select_rating = "SELECT a FROM lisarating;"
        cursor = mariadb_connection.cursor()

        cursor.execute(sql_select_rating)
        rating_lisa = cursor.fetchall()

        for row in rating_lisa:
            text_rating = "Текущий рейтинг " + str(row[0])

        bot.send_message(chat_id, text_rating)

    except Exception as e:
        print(e)

    finally:
        if(mariadb_connection.is_connected()):
            mariadb_connection.close()

def status(update, context):
    now = datetime.datetime.now()
    day = datetime.datetime.today().isoweekday()
    try:
        if day < 6 and now.hour > 7 and now.hour < 18:
            text_status = "Рабочее время. Лиза – госпожа. Подчинись ей."
        else:
            text_status = "Нерабочее время. Лиза подчиняется."

        bot.send_message(chat_id, text_status)

    except Exception as e:
        print(e)

updater = Updater(token=bot_token)

start_handler = CommandHandler('start', start)
plus_handler = CommandHandler('plus', plus)
minus_handler = CommandHandler('minus', minus)
rating_handler = CommandHandler('rating', rating)
status_handler = CommandHandler('status', status)

updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(plus_handler)
updater.dispatcher.add_handler(minus_handler)
updater.dispatcher.add_handler(rating_handler)
updater.dispatcher.add_handler(status_handler)
updater.start_polling()

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(webhook_ssl_cert, webhook_ssl_priv)

web.run_app(
    app,
    host=webhook_listen,
    port=webhook_port,
    ssl_context=context,
)
