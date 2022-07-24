import urllib
from urllib.request import urlopen
import os
import requests
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time

os.makedirs("./car_image", exist_ok=True)

url_path = "https://www.bobaedream.co.kr"

driver = webdriver.Chrome("./chromedriver.exe")
driver.implicitly_wait(3)
time.sleep(5)

# 페이지 이동
# 총 909 페이지 존재
# https://www.bobaedream.co.kr/cyber/CyberCar.php?sel_m_gubun=ALL&page={num}&order=S11&view_size=70

# 보배드림 접속
def next_page(num):
    driver.get(f'https://www.bobaedream.co.kr/cyber/CyberCar.php?sel_m_gubun=ALL&page={num}&order=S11&view_size=70')
    # time.sleep(1)

# 현재 페이지 주소리스트

for num in range(1, 909):

    next_page(num)
    html = driver.page_source
    soup = bs(html, 'html.parser')
    href_list = soup.findAll('p', 'tit ellipsis')

    for h in href_list:
        # 파일이름
        last_url = h.find('a')['href']
        driver.get(url_path+last_url)
        html = driver.page_source
        soup = bs(html, 'html.parser')
        image_list = soup.findAll('a', {"data-fancybox": "gallery"})

        for e, i in enumerate(image_list, start=1):
            # 세번째사진까지만
            if e == 4:
                break
            img_url = i['href']
            file_name = str(img_url).split('/')[-1]
            urllib.request.urlretrieve('https:'+img_url, f"./car_image/{file_n}")
            # time.sleep(1)
        # time.sleep(1)