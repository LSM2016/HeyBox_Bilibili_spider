from selenium import webdriver
import sys
import time
import dbhelper
from video import *
from selenium.common.exceptions import NoSuchElementException


driver = webdriver.Chrome("chromedriver.exe")
# 数据库连接
conn, c = dbhelper.connect_db()

if len(sys.argv) < 3:
    start_id = 12872143
    end_id = 12972143
else:
    start_id = int(sys.argv[1])
    end_id = int(sys.argv[2])
    print("Start_ID:",sys.argv[1])
    print("End_ID:",sys.argv[2])

base_url = "https://xiaoheihe.cn/community/21982/list/"

i = 0
while (start_id+i)>end_id:
    if start_id + i < 0:
        break
    driver.get(base_url + str(start_id + i))
    
    try:
        video = driver.find_element_by_id("post_video")
    except NoSuchElementException as msg:
        print("ID:",str(start_id + i)," | 非视频页面!")
        pass
    else:
        if video != []:
            try:
                title = driver.find_element_by_class_name('post-title').text
            except NoSuchElementException as msg:
                title = "空"
            try:
                author = driver.find_element_by_class_name('username').text
            except NoSuchElementException as msg:
                author = "空"
            id = start_id + i
            if dbhelper.get_video_by_id(c, id) == []:
                tmp_video = Video(id=id, title=title, author=author)
                names = ['id', 'title', 'author']
                values = [tmp_video.id, tmp_video.title, tmp_video.author]
                dbhelper.insert_data(c, conn, 'video', names, values)
                print("ID:", id, "检测到视频:", title, "原作者:", author)

    i -= 1
driver.quit()
