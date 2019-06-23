#coding=utf-8
from selenium import webdriver
from settings import Settings
from bs4 import BeautifulSoup
import logging
import time
import redis
import json
from urllib.parse import quote, unquote, urlencode
import codecs
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime
import redis
import test_proxy
import os


chop = webdriver.ChromeOptions()
chop.add_extension('Adblock-Plus-free-ad-blocker_v3.5.2.crx')
#chop.add_argument('--headless')
chop.add_argument("--start-maximized")
chop.add_extension(test_proxy.proxy_auth_plugin_path)

class juzimipy:
    def __init__(self):
        self.username = "guest"
        self.loger = self.get_jzm_logger()
        pass

    def get_jzm_logger(self, show_logs=True):
        existing_logger = Settings.loggers.get(self.username)
        if existing_logger is not None:
            return existing_logger
        else:
            logger = logging.getLogger(self.username)
            logger.setLevel(logging.DEBUG)

            extra = {"username": self.username}
            logger_formatter = logging.Formatter(
                '%(levelname)s [%(asctime)s] [%(username)s]  %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')

            if show_logs is True:
                console_handler = logging.StreamHandler()
                console_handler.setLevel(logging.DEBUG)
                console_handler.setFormatter(logger_formatter)
                logger.addHandler(console_handler)

            logger = logging.LoggerAdapter(logger, extra)
            Settings.loggers[self.username] = logger
            Settings.loggers = logger

            return logger
jzm = juzimipy()
client = redis.StrictRedis()
driver = webdriver.Chrome('./chromedriver', chrome_options=chop)
driver.implicitly_wait(7)
try:
    driver.get('https://www.juzimi.com/dynasty/%E5%85%88%E7%A7%A6')
    jzm.loger.info("first datetime: {}".format(datetime.now()))
    locator = (By.CLASS_NAME, 'contentin')
    WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located(locator))
except:
    jzm.loger.info("TimeOutException")
    driver.quit()

base_url = 'https://www.juzimi.com/'
Tag = unquote("%E5%85%88%E7%A7%A6")

try:
    soup = BeautifulSoup(driver.page_source, "html.parser")
except IndexError:
    jzm.loger.info("IndexError: list index out of range")
else:
    page_count_list = []
    people_in_one_tag = []

    try:
        for one in soup.find_all("li", class_="pager-item"):
            page_count_list.append(one.find("a")["href"])

        for one in soup.find_all("div", class_="view-content")[0].find_all('div', class_="views-row"):
            one_author_stat = {
                "href": one.find('a')['href'],
                "s_count": int(one.find("a", class_="xqagepawirdesclink").text.split("个")[0])
            }
            people_in_one_tag.append(one_author_stat)
    except IndexError:
        print("IndexError: list index out of range")
    else:

        jzm.loger.info("get first page info!")


        def get_all_sentences_by_one_author(soup, author, k):
            one_author_sentencs = {}
            try:
                q = 0
                for one in soup.select('div.view.view-xqfamoustermspage')[0].find_all('div', class_="views-row"):
                    content = one.find('div', class_="views-field-phpcode-1").text
                    from_book = one.find('div', class_="xqjulistwafo").text if one.find('div',
                                                                                        class_="xqjulistwafo") else None
                    like = one.find('div', class_="views-field-ops").text
                    comment = one.find('div', class_="views-field-comment-count").text
                    enterer = one.find('div', class_="views-field-name").text

                    sentence_json = {
                        "content": content if content else "None",
                        "from_book": from_book if from_book else "None",
                        "like": like if like else "None",
                        "comment": comment if comment else "None",
                        "enterer": enterer if enterer else "None",
                    }
                    jzm.loger.info("crawl {}".format(author + "_page_" + str(k) +"_"+ str(q)))
                    one_author_sentencs[author + "_page_" + str(k) +"_"+ str(q)] = str(sentence_json)
                    q += 1

                jzm.loger.info("wg {}".format(author + "_page_" + str(k)))
                client.hmset(author + "_page_" + str(k), one_author_sentencs)
            except IndexError:
                jzm.loger.info("IndexError: list index out of range")

        def get_url(url):
            sub_soup = None
            try:
                jzm.loger.info("get datetime: {}".format(datetime.now()))
                driver.get(url)
                locator = (By.CLASS_NAME, 'view-content')
                WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located(locator))
                jzm.loger.info("get datetime: {}".format(datetime.now()))
                sub_soup = BeautifulSoup(driver.page_source, "html.parser")
            except:
                jzm.loger.info("TimeExecption")
                driver.quit()
                os.system("python3.6 jzmbot.py")


            return sub_soup

        # one author info page
        for i in range(len(people_in_one_tag)):
            author = unquote(people_in_one_tag[i]["href"].split("/")[2])
            jzm.loger.info("{},{}".format(i,author))
            url = base_url + people_in_one_tag[i]["href"]

            #next page
            for j in range(0, people_in_one_tag[i]["s_count"] // 10 + 1):
                if client.exists(author + "_page_" + str(j)):
                    continue
                next_page_url = url + "?page=" + str(j)
                sub_soup = get_url(next_page_url)
                while True:
                    if "无法访问此网站" not in sub_soup.text:
                        break
                    else:
                        sub_soup = get_url(next_page_url)

                get_all_sentences_by_one_author(sub_soup, author, j)

driver.quit()
