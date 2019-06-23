from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"

driver = webdriver.Chrome(desired_capabilities=capa)
wait = WebDriverWait(driver, 20)

driver.get('https://stackoverflow.com/')

wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#h-top-questions')))

driver.execute_script("window.stop();")

print("end")