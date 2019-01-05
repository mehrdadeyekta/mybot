#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple Bot to reply to Telegram messages.
This is built on the API wrapper, see echobot2.py to see the same example built
on the telegram.ext bot framework.
This program is dedicated to the public domain under the CC0 license.
"""
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import psycopg2 as db
import sys
import random
import configparser

DB_HOST = '127.0.0.1'
DB_DATABASE = ''
DB_USERNAME = ''
DB_PASSWORD = ''
BOT_TOKEN = ''
ADMIN_USER_ID = 0

conn = db.connect(host=DB_HOST, database=DB_DATABASE, user=DB_USERNAME, password=DB_PASSWORD)
cursor = conn.cursor()
update_id = None

config = configparser.RawConfigParser()
configFilePath = 'config.txt'
config.read(configFilePath)

DB_HOST = '127.0.0.1'
DB_DATABASE = config.get("CONFIG", "DB_DATABASE")
DB_USERNAME = config.get("CONFIG", "DB_USERNAME")
DB_PASSWORD = config.get("CONFIG", "DB_PASSWORD")
BOT_TOKEN = config.get("CONFIG", "BOT_TOKEN")
ADMIN_USER_ID = config.get("CONFIG", "ADMIN_USER_ID")


def main():
    """Run the bot."""
    global update_id
    
    # Telegram Bot Authorization Token
    bot = telegram.Bot(BOT_TOKEN)

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            handle_msg(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def handle_msg(bot):
    """Echo the message the user sent."""
    global update_id
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):

        update_id = update.update_id + 1

        if update.message:  # your bot can receive updates without messages
            cursor.execute("select  user_id from users where user_id='" + str(update.message.from_user['id']) + "';")
            if cursor.rowcount == 0:
                rand_id = 0
                while True:
                    rand_id = str(random.randint(1000,9999))
                    cursor.execute("select  * from users where user_anon_id='" + rand_id + "';")
                    if cursor.rowcount == 0:
                        break
                fname = str(update.message.from_user['first_name'].encode("utf-8")) if update.message.from_user['first_name'] else 'None'
                lname = str(update.message.from_user['last_name'].encode("utf-8")) if update.message.from_user['last_name'] else 'None'
                cursor.execute("insert into users (username, user_id, first_name, last_name, user_anon_id) values (" +\
                                                                                             "'" + str(update.message.from_user['username']) + "', " +\
                                                                                             "'" + str(update.message.from_user['id']) + "', " +\
                                                                                             "'" + fname + "', " +\
                                                                                             "'" + lname + "', " +\
                                                                                             "'" + rand_id + "');")
                cursor.execute("commit;")
                update.message.reply_text("\xd8\xb3\xd9\x84\xd8\xa7\xd9\x85\x21\x0a\x0a\xd8\xa8\xd9\x87\x20\xd8\xa8\xd8\xa7\xd8\xaa\x20\xd9\xbe\xdb\x8c\xd8\xa7\xd9\x85\x20\xd9\x86\xd8\xa7\xd8\xb4\xd9\x86\xd8\xa7\xd8\xb3\x20\xd8\xae\xd9\x88\xd8\xb4\x20\xd8\xa2\xd9\x85\xd8\xaf\xdb\x8c\xd8\xaf\x2e\x20\xd8\xa2\xdb\x8c\xe2\x80\x8c\xd8\xaf\xdb\x8c\x20\xd8\xb4\xd9\x85\xd8\xa7\x20\xd8\xa8\xd8\xb1\xd8\xa7\xdb\x8c\x20\xd8\xa7\xdb\x8c\xd9\x86\xda\xa9\xd9\x87\x20\xd8\xaf\xdb\x8c\xda\xaf\xd8\xb1\xd8\xa7\xd9\x86\x20\xd8\xa8\xd8\xaa\xd9\x88\xd8\xa7\xd9\x86\xd9\x86\xd8\xaf\x20\xd8\xa8\xd9\x87\x20\xd8\xb4\xd9\x85\xd8\xa7\x20\xd9\xbe\xdb\x8c\xd8\xa7\xd9\x85\x20\xd9\x86\xd8\xa7\xd8\xb4\xd9\x86\xd8\xa7\xd8\xb3\x20\xd8\xa7\xd8\xb1\xd8\xb3\xd8\xa7\xd9\x84\x20\xda\xa9\xd9\x86\xd9\x86\xd8\xaf\x20\xd8\xa8\xd8\xb1\xd8\xa7\xd8\xa8\xd8\xb1\x20\xd8\xa7\xd8\xb3\xd8\xaa\x20\xd8\xa8\xd8\xa7\x3a\x20" + rand_id + "\x0a\x0a\x0a\xd8\xaf\xd8\xb1\xd8\xae\xd9\x88\xd8\xa7\xd8\xb3\xd8\xaa\x20\xd8\xb1\xd8\xa7\xd9\x87\xd9\x86\xd9\x85\xd8\xa7\x20\xd8\xa8\xd8\xa7\x0a\x2f\x68\x65\x6c\x70")
            else:
                pass

            # Reply to the message
            if update.message.text:
                text = str(update.message.text.encode("utf-8"))
                if text == "/help":
                    update.message.reply_text("\x2f\x6e\x65\x77\x20\x20\x20\x20\x20\x20\x20\x20\x20\x3d\x3d\x3e\x20\x20\x20\xd8\xa7\xd8\xb1\xd8\xb3\xd8\xa7\xd9\x84\x20\xd9\xbe\xdb\x8c\xd8\xa7\xd9\x85\x20\xd9\x86\xd8\xa7\xd8\xb4\xd9\x86\xd8\xa7\xd8\xb3\x20\xd8\xa8\xd9\x87\x20\xda\xa9\xd8\xa7\xd8\xb1\xd8\xa8\xd8\xb1\x20\xd8\xac\xd8\xaf\xdb\x8c\xd8\xaf\x0a\x2f\x67\x65\x74\x5f\x69\x64\x20\x20\x20\x20\x20\x20\x3d\x3d\x3e\x20\x20\x20\xd8\xaf\xd8\xb1\xdb\x8c\xd8\xa7\xd9\x81\xd8\xaa\x20\xd8\xa2\xdb\x8c\xe2\x80\x8c\xd8\xaf\xdb\x8c\x20\xd8\xae\xd9\x88\xd8\xaf\x0a\x2f\x63\x68\x61\x6e\x67\x65\x5f\x69\x64\x20\x20\x20\x3d\x3d\x3e\x20\x20\x20\xd8\xaa\xd8\xba\xdb\x8c\xdb\x8c\xd8\xb1\x20\xda\xa9\xd8\xaf\x20\xd9\x86\xd8\xa7\xd8\xb4\xd9\x86\xd8\xa7\xd8\xb3\x20\xd8\xae\xd9\x88\xd8\xaf")

                elif text == "/change_id":
                    while True:
                        rand_id = str(random.randint(1000,9999))
                        cursor.execute("select  * from users where user_anon_id='" + rand_id + "';")
                        if cursor.rowcount == 0:
                            cursor.execute("update users set user_anon_id='" + rand_id + "' where user_id='" + str(update.message.from_user['id']) + "';")
                            cursor.execute("commit;")
                            update.message.reply_text("\xd8\xa2\xdb\x8c\xe2\x80\x8c\xd8\xaf\xdb\x8c\x20\xd8\xac\xd8\xaf\xdb\x8c\xd8\xaf\x20\xd8\xb4\xd9\x85\xd8\xa7\x20\xd8\xa8\xd8\xb1\xd8\xa7\xd8\xa8\xd8\xb1\x20\xd8\xa7\xd8\xb3\xd8\xaa\x20\xd8\xa8\xd8\xa7\x20 " + rand_id) 
                            break

                elif text == "/get_id":
                    cursor.execute("select user_anon_id from users where user_id='" + str(update.message.from_user['id']) + "';")
                    update.message.reply_text(cursor.fetchall()[0][0])

                elif text == "/new":
                    cursor.execute("select last_chat from users where user_id='" + str(update.message.from_user['id']) + "';")
                    current_target = cursor.fetchall()[0][0]
                    if current_target == None:
                        update.message.reply_text("\xd8\xa2\xdb\x8c\xe2\x80\x8c\xd8\xaf\xdb\x8c\x20\xda\xa9\xd8\xa7\xd8\xb1\xd8\xa8\xd8\xb1\x20\xd9\x85\xd9\x88\xd8\xb1\xd8\xaf\x20\xd9\x86\xd8\xb8\xd8\xb1\x20\xd8\xb1\xd8\xa7\x20\xd9\x88\xd8\xa7\xd8\xb1\xd8\xaf\x20\xda\xa9\xd9\x86\xdb\x8c\xd8\xaf\x20\x28\xd8\xa8\xd8\xa7\x20\xd8\xa7\xd8\xb9\xd8\xaf\xd8\xa7\xd8\xaf\x20\xd8\xa7\xd9\x86\xda\xaf\xd9\x84\xdb\x8c\xd8\xb3\xdb\x8c\x29")
                    else:
                        update.message.reply_text("\xd8\xa2\xd8\xae\xd8\xb1\xdb\x8c\xd9\x86\x20\xd9\xbe\xdb\x8c\xd8\xa7\xd9\x85\xe2\x80\x8c\xd9\x87\xd8\xa7\xdb\x8c\x20\xd8\xb4\xd9\x85\xd8\xa7\x20\xd8\xa8\xd9\x87\x20\xda\xa9\xd8\xa7\xd8\xb1\xd8\xa8\xd8\xb1\x20\xd8\xa8\xd8\xa7\x20\xd8\xa2\xdb\x8c\xe2\x80\x8c\xd8\xaf\xdb\x8c\x20" + str(current_target) + "\x20\xd8\xa7\xd8\xb1\xd8\xb3\xd8\xa7\xd9\x84\x20\xd9\x85\xdb\x8c\xe2\x80\x8c\xd8\xb4\xd9\x88\xd9\x86\xd8\xaf\x2e\x20\xd8\xaf\xd8\xb1\x20\xd8\xb5\xd9\x88\xd8\xb1\xd8\xaa\x20\xd8\xaa\xd9\x85\xd8\xa7\xdb\x8c\xd9\x84\x20\xd8\xa8\xd9\x87\x20\xd8\xaa\xd8\xba\xdb\x8c\xdb\x8c\xd8\xb1\x20\xd8\xa2\xdb\x8c\xe2\x80\x8c\xd8\xaf\xdb\x8c\x20\xda\xa9\xd8\xa7\xd8\xb1\xd8\xa8\xd8\xb1\x20\xd8\xac\xd8\xaf\xdb\x8c\xd8\xaf\x20\xd8\xb1\xd8\xa7\x20\xd9\x88\xd8\xa7\xd8\xb1\xd8\xaf\x20\xda\xa9\xd9\x86\xdb\x8c\xd8\xaf\x2e")

                elif text.replace("/","").isdigit() and len(text.replace("/","")) == 4:
                    cursor.execute("update users set last_chat='" + text.replace("/","") + "' where user_id='" + str(update.message.from_user['id']) + "';")
                    cursor.execute("commit;")
                    update.message.reply_text("\xd8\xa7\xd8\xb2\x20\xd8\xa7\xdb\x8c\xd9\x86\x20\xd8\xa8\xd9\x87\x20\xd8\xa8\xd8\xb9\xd8\xaf\x20\xd9\xbe\xdb\x8c\xd8\xa7\xd9\x85\xe2\x80\x8c\xd9\x87\xd8\xa7\xdb\x8c\x20\xd8\xa8\xd8\xb9\xd8\xaf\xdb\x8c\x20\xd8\xb4\xd9\x85\xd8\xa7\x20\xd8\xa8\xd9\x87\x20\xda\xa9\xd8\xa7\xd8\xb1\xd8\xa8\xd8\xb1\x20\xd9\x85\xd9\x88\xd8\xb1\xd8\xaf\x20\xd9\x86\xd8\xb8\xd8\xb1\x20\xd8\xa7\xd8\xb1\xd8\xb3\xd8\xa7\xd9\x84\x20\xd9\x85\xdb\x8c\xe2\x80\x8c\xd8\xb4\xd9\x88\xd8\xaf\x2e\x20\xd9\x85\xda\xaf\xd8\xb1\x20\xd8\xa7\xdb\x8c\xd9\x86\x20\xda\xa9\xd9\x87\x20\xd8\xa8\xd8\xa7\x20\x0a\x2f\x6e\x65\x77\x0a\xda\xa9\xd8\xa7\xd8\xb1\xd8\xa8\xd8\xb1\x20\xd8\xac\xd8\xaf\xdb\x8c\xd8\xaf\xdb\x8c\x20\xd8\xa8\xd8\xb1\xd8\xa7\xdb\x8c\x20\xd8\xaf\xd8\xb1\xdb\x8c\xd8\xa7\xd9\x81\xd8\xaa\x20\xd9\xbe\xdb\x8c\xd8\xa7\xd9\x85\x20\xd8\xaa\xd8\xb9\xd8\xb1\xdb\x8c\xd9\x81\x20\xda\xa9\xd9\x86\xdb\x8c\xd8\xaf\x2e")

                else:
                    cursor.execute("select user_anon_id from users where user_id='" + str(update.message.from_user['id']) + "';")
                    uid = cursor.fetchall()[0][0]
                    cursor.execute("select last_chat from users where user_id='" + str(update.message.from_user['id']) + "';")
                    target = cursor.fetchall()[0][0]
                    if target:
                        cursor.execute("select user_id from users where user_anon_id='" + str(target) + "';")
                        if cursor.rowcount == 0:
                            update.message.reply_text("\xda\xa9\xd8\xaf\x20\xd9\x88\xd8\xa7\xd8\xb1\xd8\xaf\x20\xd8\xb4\xd8\xaf\xd9\x87\x20\xd9\x88\xd8\xac\xd9\x88\xd8\xaf\x20\xd9\x86\xd8\xaf\xd8\xa7\xd8\xb1\xd8\xaf\x2e\x20\xd9\x85\xd9\x85\xda\xa9\xd9\x86\x20\xd8\xa7\xd8\xb3\xd8\xaa\x20\xda\xa9\xd8\xa7\xd8\xb1\xd8\xa8\xd8\xb1\x20\xda\xa9\xd8\xaf\x20\xd9\xbe\xdb\x8c\xd8\xa7\xd9\x85\x20\xd9\x86\xd8\xa7\xd8\xb4\xd9\x86\xd8\xa7\xd8\xb3\x20\xd8\xae\xd9\x88\xd8\xaf\x20\xd8\xb1\xd8\xa7\x20\xd8\xaa\xd8\xba\xdb\x8c\xdb\x8c\xd8\xb1\x20\xd8\xaf\xd8\xa7\xd8\xaf\xd9\x87\x20\xd8\xa8\xd8\xa7\xd8\xb4\xd8\xaf\x2e\x20\xd9\x85\xd8\xac\xd8\xaf\xd8\xaf\xd8\xa7\x20\xd8\xa8\xd8\xb1\xd8\xb1\xd8\xb3\xdb\x8c\x20\xd9\x86\xd9\x85\xd8\xa7\xdb\x8c\xdb\x8c\xd8\xaf\x2e")
                        else:
                            target_id = cursor.fetchall()[0][0]
                            msg = "From /" + str(uid) + ":\n\n" + str(text)
                            bot.sendMessage(target_id, msg)
                            bot.sendMessage(ADMIN_USER_ID, str(update.message.from_user['id']) + "==>" + str(target_id) + " :: " + str(text))
                    else:
                        update.message.reply_text("\xd8\xb4\xd9\x85\xd8\xa7\x20\xda\xa9\xd8\xa7\xd8\xb1\xd8\xa8\xd8\xb1\xdb\x8c\x20\xd8\xb1\xd8\xa7\x20\xd8\xa8\xd8\xb1\xd8\xa7\xdb\x8c\x20\xd8\xa7\xd8\xb1\xd8\xb3\xd8\xa7\xd9\x84\x20\xd9\xbe\xdb\x8c\xd8\xa7\xd9\x85\x20\xd8\xa7\xd9\x86\xd8\xaa\xd8\xae\xd8\xa7\xd8\xa8\x20\xd9\x86\xda\xa9\xd8\xb1\xd8\xaf\xd9\x87\x20\xd8\xa7\xdb\x8c\xd8\xaf\x2e\x20\xd8\xa8\xd8\xa7\x20\xd8\xa7\xd8\xb3\xd8\xaa\xd9\x81\xd8\xa7\xd8\xaf\xd9\x87\x20\xd8\xaf\xd8\xb3\xd8\xaa\xd9\x88\xd8\xb1\x0a\x2f\x6e\x65\x77\x0a\xd8\xaf\xd8\xb1\xd8\xae\xd9\x88\xd8\xa7\xd8\xb3\xd8\xaa\x20\x20\xd8\xa7\xd8\xb1\xd8\xb3\xd8\xa7\xd9\x84\x20\xd9\xbe\xdb\x8c\xd8\xa7\xd9\x85\x20\xd8\xa8\xd9\x87\x20\xd8\xb5\xd9\x88\xd8\xb1\xd8\xaa\x20\xd9\x86\xd8\xa7\xd8\xb4\xd9\x86\xd8\xa7\xd8\xb3\x20\xd8\xa7\xd8\xb1\xd8\xb3\xd8\xa7\xd9\x84\x20\xda\xa9\xd9\x86\xdb\x8c\xd8\xaf\x2e")

if __name__ == '__main__':
    main()
