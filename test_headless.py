from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
print(datetime.now())
driver.get("http://www.baidu.com")
print(datetime.now())
driver.close()
