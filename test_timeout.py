# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime

print (datetime.datetime.now())
driver = webdriver.Chrome('./chromedriver')
#driver.implicitly_wait(10)  # 隐性等待和显性等待可以同时用，但要注意：等待的最长时间取两者之中的大者
driver.get('https://www.juzimi.com/')
locator = (By.CLASS_NAME, 'view-content')

try:
    res = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    print (res)
    print(datetime.datetime.now())
except:
    print(datetime.datetime.now())
finally:
    driver.close()