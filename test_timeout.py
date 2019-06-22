# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime

print (datetime.datetime.now())
driver = webdriver.Chrome('./chromedriver')
#driver.implicitly_wait(10)  # 隐性等待和显性等待可以同时用，但要注意：等待的最长时间取两者之中的大者
driver.get('https://www.juzimi.com/writer/%E8%80%81%E5%AD%90?page=13')
locator = (By.CLASS_NAME, 'view-content')

try:
    WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located(locator))
    print (driver.find_element_by_class_name("view-content").text)
    print(datetime.datetime.now())
finally:
    driver.close()