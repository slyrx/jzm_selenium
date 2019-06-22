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
driver = webdriver.Chrome('./chromedriver')
driver.get('https://www.juzimi.com/dynasty/%E5%85%88%E7%A7%A6')
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
            people_in_one_tag.append(one.find('a')['href'])
    except IndexError:
        print("IndexError: list index out of range")
    else:

        jzm.loger.info("get first page info!")


        def get_all_sentences_by_one_author(soup, author, k):
            one_author_sentencs = []
            try:
                for one in soup.select('div.view.view-xqfamoustermspage')[0].find_all('div', class_="views-row"):
                    content = one.find('div', class_="views-field-phpcode-1").text
                    from_book = one.find('div', class_="xqjulistwafo").text if one.find('div',
                                                                                        class_="xqjulistwafo") else None
                    like = one.find('div', class_="views-field-ops").text
                    comment = one.find('div', class_="views-field-comment-count").text
                    enterer = one.find('div', class_="views-field-name").text

                    sentence_json = {
                        "content": content,
                        "from_book": from_book,
                        "like": like,
                        "comment": comment,
                        "enterer": enterer,
                    }
                    one_author_sentencs.append(sentence_json)
            except IndexError:
                jzm.loger.info("IndexError: list index out of range")

            one_author["page_" + str(k)] = one_author_sentencs
            with codecs.open(author + "_page: " + str(j) + '.json', "a+", 'utf-8') as f:
                json.dump(one_author_sentencs, f, ensure_ascii=False)

        def get_url(url):
            driver.get(url)
            html = driver.page_source
            sub_soup = BeautifulSoup(html, "html.parser")

            return sub_soup
        # one author info page
        for i in range(2,len(people_in_one_tag)):
            url = base_url + people_in_one_tag[i]
            sub_soup = get_url(url)

            author = unquote(people_in_one_tag[i].split("/")[2])
            jzm.loger.info("{},{}".format(i,author))
            interval_1 = random.choice(range(15))
            jzm.loger.info("1 随机数为:{}".format(interval_1))
            time.sleep(interval_1)
            one_author = {}


            while True:
                if "无法访问此网站" not in sub_soup.text:
                    break
                else:
                    sub_soup = get_url(url)
            get_all_sentences_by_one_author(sub_soup, author, 0)

            #next page
            for j in range(1, int(sub_soup.find("li", class_="pager-last").text)):
                next_page_url = url + "?page=" + str(j)
                driver.get(next_page_url)
                interval_2 = random.choice(range(20))
                jzm.loger.info("2 随机数为:{},{}".format(interval_2,"page: " + str(j)))
                time.sleep(interval_2)
                sub_soup = BeautifulSoup(driver.page_source, "html.parser")
                get_all_sentences_by_one_author(sub_soup, unquote(people_in_one_tag[i].split("/")[2]), j)

            with codecs.open(author + '.json', "a+", 'utf-8') as f:
                json.dump(one_author, f, ensure_ascii=False)
driver.quit()
