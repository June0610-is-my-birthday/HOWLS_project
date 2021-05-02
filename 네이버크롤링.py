# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
import re
import csv

#중국 / 네이버 뉴스 외교파트 (하위 파트 중 국방 외교 부문)
# 한 페이지 당 10개 존재함
# 크롤링 개수를 우선 한 페이지 대상으로, 인기 댓글 5개씩 추출

options = Options()
driver = webdriver.Chrome("C:\\Users\\장준호\\Desktop\\chromedriver.exe")
#driver = webdriver.Chrome(options = options) WebDriverException: 'chromedriver' executable needs to be in PATH. Please see https://sites.google.com/a/chromium.org/chromedriver/home 오류가 발생함

driver.implicitly_wait(5)

search_word = input('검색어 입력: ')

driver.get(f'https://search.naver.com/search.naver?where=news&query={search_word}')

class Crawler:
    def __init__(self, num):
        self._count =1
        self._num = num
        self._comment, self._like = [], []
        self.ar_per_page = 0
        
    def com_crawl(self):
        for count in range(1,11):
            try:
                site = driver.find_element_by_xpath(f'// *[ @ id = "sp_nws{count}"] / div[1] / div / div[1] / div / a[2]')
                site.click()

                driver.switch_to.window(driver.window_handles[-1])  # 열린 탭으로 이동
                sleep(1)

                comment = driver.find_elements_by_class_name('u_cbox_contents')
                like = driver.find_elements_by_class_name('u_cbox_cnt_recomm')

                comment = [c.text for c in comment]
                like = [n.text for n in like]

                self._comment.extend(comment)
                self._like.extend(like)

                driver.close()
                driver.switch_to.window(driver.window_handles[-1])  # 닫힌 탭으로 이동

                self.ar_per_page += 1

            except:
                continue
        print("크롤링 완료")
        driver.quit()
        
        return self._comment, self._like

c = Crawler(10)
result = c.com_crawl()
print(list(zip(*result)), len(list(zip(*result))))

f = open(f'{search_word}.csv', 'w', encoding = 'utf-8', newline = '') 
csvWriter = csv.writer(f)
for i in list(zip(*result)):
    csvWriter.writerow(i)

f.close()    
print('문서 생성 완료')     
            
            
            
            
            
            
            
            
            
            
            
            
            
            