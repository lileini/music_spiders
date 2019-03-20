import time

import scrapy
from scrapy.spiders import CrawlSpider
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from music.items import MusicItem
from selenium.webdriver.support import expected_conditions as ec

class MusicListSpider(CrawlSpider):
    name = 'music'
    allowed_domains = ['music.163.com', '163.com']
    start_urls = ['https://music.163.com/#/my/m/music/playlist?id=12682425']

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': '_ntes_nuid=9356ef8c97fe194f90eb806304c6d250; __utma=94650624.1675450719.1498797426.1498797426.1498797426.1; _iuqxldmzr_=32; vjuids=4d4755941.162664e2ee9.0.3c72a7f342f3b; vjlast=1522134823.1522134823.30; mail_psc_fingerprint=897cfbd4518fd274369c2820aad790e0; _ntes_nnid=9356ef8c97fe194f90eb806304c6d250,1532331066266; WM_TID=%2B1ueF2pst3pFEVFUAAc4PZzvynysjbAm; ne_analysis_trace_id=1543563949039; s_n_f_l_n3=3f5ce9bf167249241543563949059; vinfo_n_f_l_n3=3f5ce9bf16724924.1.0.1543563949059.0.1543564049854; __f_=1545284685262; playliststatus=visible; WM_NI=w3WYeV7qUhZwTW1FGnwzvyn7Y%2FXHeyZ02ufdm76Kx16XO1Ad7kKH5gV1XyitCj7WuURJ6v74rs1%2BWYL%2B7IThXdj3sIyYktPn%2F2%2Bu371jnpEr%2B0gjwk3vmS6tKoW7zhOOc3o%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee91ec45bb86a38bf548bcac8bb6c14f839e9fbbbb7d98b7be88d553fb8e9cd9c92af0fea7c3b92ab5ed99bae85ef5af9b89d97d9889ffa7c666b5a6ba9aed3d9bf198a9e8739af0fe96e570afe9faacfb3bf68881d2c470f5b585a9b86d96ef989aec8081b6f9b8f85f9296fa97b640b2adffccd65390f5f9aad7649cbca6d4f243bb87a595d366edeee596b23df3b6a291c87ae9f0a98bf661f1aaa3b4b58089b199d8f9648d91add4ee37e2a3; __remember_me=true; MUSIC_U=cc8246660f76b482ef8c4757a6d3d3cb15c1e39591827c851e019ab8266d17a6956b04f31746bcdae202b40834fd329941506e0f8e8d8f1cbf122d59fa1ed6a2; __csrf=1195915b4d27e775d38811584208e6f5; JSESSIONID-WYYY=N0GoIunhMQoDWtXpc95WZAxXfgxHB8FPQ083qYyfA0FXrtE%2B7O%5CRnNsZfDo5CNjFp29IzhS9k163zlscg6rYm0PQPVqShOgW8mvjnwwDMmHOjf3YvUpDMhnDB6b%5ChKiEUXE4eI9Z50MbqgjMIJXcEiblIT17oTyAnaxiK%2BzK3YxHqCRJ%3A1548063813994',
        'Referer': 'https://music.163.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }

    def start_requests(self):
        # for url in self.start_urls:
        # url = self.start_urls[0]
        #
        # yield scrapy.Request(
        #     url=url, priority=1, headers=self.headers,
        #     dont_filter=True,
        #     callback=self.parse)
        self.starts()

    def parse(self, response):
        list = response.css('.m-table tbody<tr')
        for tr in list:
            css = tr.css('td b::attr(title)')
            name = css[0].css('td b::attr(title)').extract_first()
            singer = css[3].css('span::attr(title)').extract_first()
            item = MusicItem()
            item.name = name
            item.singer = singer
            yield item
    def starts(self):
        option = webdriver.ChromeOptions()
        # option.add_argument("--start-maximized")
        # option.add_argument('--no-sandbox')  # ubuntu 需要这个参数
        # option.add_argument("--incognito")
        # option.add_argument("--headless")  # 不弹出浏览器
        self.timeout  =60000
        # option.add_argument(
        #     '--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"')
        # option.add_argument('--')
        self.browser = webdriver.Chrome(chrome_options=option)
        # self.browser.set_window_size(1000, 800)
        # self.browser.set_page_load_timeout(self.timeout)
        # self.browser.delete_all_cookies()
        # self.wait = WebDriverWait(self.browser, self.timeout)

        self.browser.get('https://music.163.com/')
        self.wait = WebDriverWait(self.browser,30)
        # self.wait.until(ec.presence_of_element_located((By.XPATH,'.m-tophead')))
        login = self.browser.find_element_by_class_name('m-tophead')
        login.click()
        time.sleep(1)
        self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.u-alt li:last-child a')))
        netease = self.browser.find_element_by_css_selector('.u-alt li:last-child a')
        netease.click()
        time.sleep(2)
        self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.n-log2 .f-pr #e')))
        user_input = self.browser.find_element_by_css_selector('.n-log2 .f-pr #e')
        pwd_input = self.browser.find_element_by_css_selector('.n-log2 .f-mgt10 #epw')
        user_input.send_keys('skyvtars@126.com')
        pwd_input.send_keys('76958825aini@')
        btn = self.browser.find_element_by_css_selector('.f-mgt20 a')
        btn.click()
