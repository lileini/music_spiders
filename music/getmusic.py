# -*- coding: utf-8 -*-
import time
import urllib
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as ec

from music.items import MusicItem

musics = list()
with open('./music_html', 'r+', encoding='utf-8') as f:
    html = f.readline()
    root = etree.HTML(html)
    names = root.xpath("//div[@class='f-cb']//b/@title")
    artists = root.xpath("//div[@class='text']/@title")
    print(names)
    print(artists)
    # with open('./music.csv', 'a', encoding='utf-8') as f:
    for i in range(len(names)):
        item = MusicItem()
        item['name'] = names[i]
        item['singer'] = artists[i]
        musics.append(item)
            # f.write(names[i]+"|"+artists[i])
            # f.write('\n')
option = webdriver.ChromeOptions()
# option.add_argument("--start-maximized")
# option.add_argument('--no-sandbox')  # ubuntu 需要这个参数
# option.add_argument("--incognito")
# option.add_argument("--headless")  # 不弹出浏览器
timeout  =600
# option.add_argument(
#     '--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"')
# option.add_argument('--')
browser = webdriver.Chrome(chrome_options=option)
# self.browser.set_window_size(1000, 800)
# self.browser.set_page_load_timeout(self.timeout)
# self.browser.delete_all_cookies()
# self.wait = WebDriverWait(self.browser, self.timeout
browser.get('https://www.91flac.com/')
wait = WebDriverWait(browser,30)
time.sleep(1)
wait.until(ec.presence_of_element_located((By.CSS_SELECTOR,'.btn-primary')))
login = browser.find_element_by_css_selector('.btn-primary')
login.click()
time.sleep(1)
# wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.col-md-8 .btn-primary')))
# netease = browser.find_element_by_css_selector('.col-md-8 .btn-primary')
# netease.click()
# time.sleep(2)
wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.col-md-8 .btn-primary')))
user_input = browser.find_element_by_css_selector('#email')
pwd_input = browser.find_element_by_css_selector('#password')
user_input.send_keys('1822021960@qq.com')
pwd_input.send_keys('76958825')
btn = browser.find_element_by_css_selector('.col-md-8 .btn-primary')
btn.click()


for i in range(183,len(musics),1):
    item= musics[i]
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.form-control')))
    search_input = browser.find_element_by_css_selector('.form-control')
    key = item['name'] + "-" + item['singer']
    search_input.clear()
    search_input.send_keys(key)
    search_btn = browser.find_element_by_css_selector('.btn-success')
    search_btn.click()
    try:
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.table-borderless a')))
        music_first = browser.find_element_by_css_selector('.table-borderless a')
        music_first.click()
        time.sleep(3)

        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR,'#player-sources option')))
        link = browser.find_elements_by_css_selector('#player-sources option')[1].get_attribute('value')
        # link = a.get_attribute('value')
        cookies = browser.get_cookies()
        cookie = dict()
        for i in cookies:
            cookie[i['name']] = i['value']
        get = requests.get(link, cookies=cookie)
        key = key.replace('\xa0',' ').replace('/','|')
        path = './files/{key}.aac'.format(key=key)
        with open(path, 'wb') as file:
            file.write(get.content)
        print('下载了:'+key)
    except Exception as e:
        print(e)

# for item in musics:
    # key = urllib.parse.quote(item['name'] + " " + item['singer'])
    # search_url = 'https://www.91flac.com/search?keyword={key}'.format(key=key)
    # headers = {
    #     'authority': 'www.91flac.com',
    #     'upgrade-insecure-requests': '1',
    #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #     'referer': 'https://www.91flac.com/search?keyword=The+Upside+of+Down',
    #     'accept-encoding': 'gzip, deflate, br',
    #     'accept-language': 'zh-CN,zh;q=0.9',
    #     'cookie': 'Hm_lvt_af518ab1fe8f21a70e3f6d2cdceb85c4=1548120939; Hm_lpvt_af518ab1fe8f21a70e3f6d2cdceb85c4=1548120939; _ga=GA1.2.1868293804.1548120951; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6IlY0VWhWTllBUzVEV0FXdjBNa05ZaUE9PSIsInZhbHVlIjoiTFwvanRvRkFFeno3QTF0N2VGMWlkUEUwcFJkeUVwb2NDZjQ1OUhmNThvcjc4RENaK05PdWt3RVBHQXRKVnNpR1NsYXFTM0djOVFJRXRFcWIwWXNmM0NVN0wwMXBZT2pMRTdobms5ZHRKXC9CcklERms3WFwvTFB2d2JRdjNWVThcL1wvdTZsbHZlbjljNU92eG1nVnpKOUFzUnJXZDFnTHVQYXYrWlA3dHlta1JvSGdjZmNxSG5QS053STBhYlNxeDUwWGYiLCJtYWMiOiIzMmZmZDA5YjM5MWMzYmE4N2FjZDcwYjZiZGZmOTk2NTBmMDc1ZThhYjBhYmRjYWFhNjAyYWE2MDlhZDc3NmVlIn0%3D; io=P6z16-ocBAXELhiyAAky; XSRF-TOKEN=eyJpdiI6Ik4rK0lOR3lcLysyVkFURXBieUlRbnl3PT0iLCJ2YWx1ZSI6ImdTK09aQ0hPbGYxc2x3VitIZ2RVRGpUUGJKRDVtcGdscVNcL0VDeWlKVlM5WEJaMktjaks1WlVmRzZmODBzN2ExIiwibWFjIjoiODI1Y2Y3YTQ1YTMxMzAwNjQ2MjYxMDRiMGRkMzU5ZTg3MmQxZGQ0ZjRiYjE0ZWIxZjAzZmUyYmY2N2M4NmE2NyJ9; 91flac_session=eyJpdiI6IktFQ1F6RDFIanlNTk85b2sySDFjMFE9PSIsInZhbHVlIjoiNFUrUXZwUStvTndkZXk5Tmxsd0tINjVaS3U4XC9yN1QxZWdSQ3g2SFdBamFRWlRnclEwTk1vUUsxSDJGODJHaUoiLCJtYWMiOiJhYmFhNjQ1NmJlMTVlMWRmMzA5MTg1MzQ4ODkzNWNlZDI4YjZmZGZjZmM3MGZiYWM1ZmVhOWIwMGI5MzAxNDNjIn0%3D',
    # }
    #
    # response = requests.get(url=search_url,headers=headers)
    # etree_html = etree.HTML(response.text)
    # links = etree_html.xpath('//table//tr//a/@href')
    # if len(links)>0:
    #     song_number = links[0].spilt('/song/')[1]
    #     add_url = 'https://www.91flac.com/users/packs/select/add'
