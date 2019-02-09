from selenium import webdriver
from bs4 import BeautifulSoup
import time
import dbhelper
from bot import *
from video import *

driver = webdriver.Chrome()
# 数据库连接
conn, c = dbhelper.connect_db()

tmp_bots = dbhelper.get_all_bots(c)

for bot in tmp_bots:
    if bot.total == bot.cursor:
        pass

    print("BOT ID:", bot.id)
    driver.get("URL:Hidden" +
               str(bot.id) + "/comment_list")

    game_nav_list = driver.find_elements_by_class_name('game-nav')
    game_nav_list[1].click()
    time.sleep(1)
    post_info_list = driver.find_elements_by_class_name('post-info')

    if bot.total == -1:
        bot.total = len(post_info_list)
        # print(bot.total)
        dbhelper.update_bot(
            c, conn, bot)

    for i in range(bot.total - bot.cursor):
        print(post_info_list[bot.cursor].text)
        time.sleep(0.5)
        post_info_list[bot.cursor].click()
        time.sleep(0.5)

        windows = driver.window_handles
        driver.switch_to.window(windows[-1])
        title = driver.find_element_by_class_name('post-title').text
        author = driver.find_element_by_class_name('username').text
        id = str(driver.current_url).split('/')[-1]

        if dbhelper.get_video_by_id(c, id) == []:
            tmp_video = Video(id=id, title=title, author=author)
            names = ['id', 'title', 'author']
            values = [tmp_video.id, tmp_video.title, tmp_video.author]
            dbhelper.insert_data(c, conn, 'video', names, values)

        time.sleep(1)
        bots_name = driver.find_elements_by_class_name('username')[1:-1]
        for name in bots_name:
            print(name.text)
            name.click()
            time.sleep(0.2)

            bot_id = driver.find_element_by_class_name(
                'user-id').text.split('：')[-1]
            print("====================")
            print("botID:", bot_id)
            if dbhelper.get_bot_by_id(c, bot_id) == []:
                bot_name = name.text
                names = ['id', 'name', 'cursor', 'total']
                values = [bot_id, bot_name]
                dbhelper.insert_data(c, conn, 'bot', names, values)
            timer.sleep(0.2)
            driver.back()

        bot.cursor += 1
        dbhelper.update_bot(c, conn, bot)
        driver.close()
        driver.switch_to.window(windows[0])

driver.quit()


# 14760283
# print(post_info_list)
# for info in post_info_list:
#     print(info.text)
