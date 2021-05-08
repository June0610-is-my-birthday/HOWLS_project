# -*- coding: utf-8 -*-
"""
Created on Fri May  7 19:41:24 2021

@author: 장준호
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import csv
import os


# 인풋

options = Options()
options.add_argument("'User-Agent': 'Mozilla/5.0'")

comment_list, like_list, dislike_list, writer_list = [], [], [], []
article_idx = 0
comment_total = 0
total_article = 0
url_list = []

with open('url.txt', 'r') as f:
    url_list = f.readlines()



for url in url_list:
    total_article_page = 0
    driver = webdriver.Chrome("C:\\Users\\장준호\\Desktop\\chromedriver.exe")
    driver.implicitly_wait(5)

    driver.get(url)

    sleep(5)
    cur_comment = driver.find_element_by_xpath('// *[ @ id = "cbox_module"] / div[2] / div[2] / ul / li[1] / span')
    if int(cur_comment.text) < 10:
        print('댓글이 부족하여 창을 닫습니다.')
        total_article_page += 1
        print(f'수집 기사 : {total_article}')
        driver.quit()
        continue

        # 더보기
    more_see = driver.find_element_by_xpath('//*[@id="cbox_module"]/div[2]/div[9]/a/span[1]')
    more_see.click()
    print('더보기 클릭 중')
    # 댓글, 좋아요/싫어요, 아이디 가져오기
    comment = driver.find_elements_by_class_name('u_cbox_contents')
    comment_list.extend([c.text for c in comment])
    print('댓글 수집')
    like = driver.find_elements_by_class_name('u_cbox_cnt_recomm')
    like_list.extend([int(l.text) for l in like])
    print('좋아요 수집')
    dislike = driver.find_elements_by_class_name('u_cbox_cnt_unrecomm')
    dislike_list.extend([int(d.text) for d in dislike])
    print('싫어요 수집')
    writer = driver.find_elements_by_class_name('u_cbox_nick')
    writer_list.extend([w.text for w in writer])
    print('작성자 수집')

    comment_total += len(comment)
    print(comment_total)

    print('창 닫음')
    total_article += 1
    total_article_page += 1
    print(f'수집 기사 : {total_article}')
    driver.quit()



result = list(zip(comment_list, like_list, dislike_list, writer_list))
print(result)

file_name = '중국댓글_0508_2043'


f = open(f'{file_name}.csv', 'w', encoding = 'utf-8-sig', newline = '') 
csvWriter = csv.writer(f)
for i in result:
    csvWriter.writerow(i)

f.close()    
print('문서 생성 완료')    


print('크롤링 종료')