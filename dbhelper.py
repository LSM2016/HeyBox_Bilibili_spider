# -*- coding:utf-8 -*-
import sqlite3
from bot import *
from video import *

# 连接到数据库


def connect_db():
    conn = sqlite3.connect('heybox.db')
    c = conn.cursor()
    return conn, c


# 数据库相关配置
bot_tablename = "bot"
video_tablename = "video"


# 获取相应表内所有数据
def get_all_bots(c):
    sql = "SELECT * FROM " + bot_tablename
    c.execute(sql)
    bot_list = []
    for item in c.fetchall():
        bot_list.append(Bot(item[0], item[1], item[2], item[3]))
    return bot_list


def update_bot(c, conn, bot):
    sql = "UPDATE " + "bot" + " SET name = \'" + str(bot.name) + "\',cursor = \'" + str(
        bot.cursor) + "\',total = \'" + str(bot.total) + "\' WHERE id = \'" + str(bot.id) + "\'"
    c.execute(sql)
    conn.commit()


def get_bot_by_id(c, id):
    sql = "SELECT * FROM " + bot_tablename + \
        " WHERE id = " + "\'" + str(id) + "\'"
    c.execute(sql)
    data = c.fetchall()

    bots = []
    if len(data) == 0:
        return bots
    else:
        for x in data:
            bots.append(Bot(id=x[0], name=x[1], cursor=x[2], total=x[3]))
        return bots[0]


def get_video_by_id(c, id):
    sql = "SELECT * FROM " + video_tablename + \
        " WHERE id = " + "\'" + str(id) + "\'"
    c.execute(sql)
    data = c.fetchall()

    vids = []
    if len(data) == 0:
        return vids
    else:
        for x in data:
            vids.append(Video(id=x[0], title=x[1], author=x[2]))
        return vids[0]


def insert_data(c, conn, tablename, names, values):
    sql = "INSERT INTO " + tablename + '('
    for i in range(len(names) - 1):
        sql += names[i] + ', '
    sql += names[-1] + ')' + " VALUES ("
    for i in range(len(names) - 1):
        sql += '?,'
    sql += '?)'
    c.execute(sql, values)
    conn.commit()


def insert_video(c, conn, video):
    sql = "INSERT INTO " + video_tablename + "(id, title, author) VALUES (" + str(
        video.id) + ", " + str(video.title) + "," + str(video.author) + ")"
    c.execute(sql)
    conn.commit()
