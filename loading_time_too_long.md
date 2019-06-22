### 遇到反爬虫的处理方式
1. 加载时间过长
+ 解决方法：WebDriverWait + expected_conditions<br>
使用headless浏览器


##### 什么是WebDriverWait？如何使用？
+ WebDriverWait是显性等待类
+ 使用方式
```
WebDriverWait(driver, 超时时长(单位为秒), 调用频率, 忽略异常).until(可执行方法, 超时时返回的信息)
```
+ 疑问
+ + 对象一定有 __call__() 方法 是什么意思？

##### 什么是expected_conditions？如何使用？

##### 什么是By？如何使用？

##### 什么是headless浏览器？如何使用？
+ 在做爬虫时，通常是不需要打开浏览器的，只使用浏览器的内核，因此可以使用Chrome的无头模式。参数设置为"--headless"。
+ 使用方式
```
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get("http://www.baidu.com")
driver.close()
```
