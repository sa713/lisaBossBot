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
config.read("lisabotconfig.ini")

bot_token = config([Botconfig][bot_token])
chat_id = config([Botconfig][chat_id_prom]) #ПРОМ
#chat_id = config([Botconfig][chat_id_ift]) #ИФТ
bot = telebot.TeleBot(bot_token)
master_id = config([Botconfig][master_id])

def start(bot, update):
    if update.message.from_user.username == master_id:
        bot.sendMessage(chat_id=update.message.chat_id, text="Приветствую тебя, Мастер!")
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Только Мастер может запускать бота.")

def plus(bot, update):
    if update.message.from_user.username == master_id:
        bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEBUcxfWoTWE9_fH2LLHiePekrjcTQD8wACIQMAApKYGQABS3-P5xR5J7gbBA')
        try:
            mariadb_connection = mariadb.connect(user='tlgbotuser', password='tlgbotpass', database='tg_bots')
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
        bot.sendMessage(chat_id=update.message.chat_id, text="Только Мастер может управлять рейтингом.")

def minus(bot, update):
    if update.message.from_user.username == master_id:
        bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEBUcpfWoRaQ1xlcZrCW-9ww9j0X03e4gACGwMAApKYGQABXKvAZtGGe6sbBA')

        try:
            mariadb_connection = mariadb.connect(user='tlgbotuser', password='tlgbotpass', database='tg_bots')
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
        bot.sendMessage(chat_id=update.message.chat_id, text="Только Мастер может управлять рейтингом.")

def rating(bot, update):
    bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEBUc5fWoUdCrBoM0HJV6euckYYXLzPTwACDwMAApKYGQABO29Om3RWbfQbBA')
    try:
        mariadb_connection = mariadb.connect(user='tlgbotuser', password='tlgbotpass', database='tg_bots')
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

def status(bot, update):
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