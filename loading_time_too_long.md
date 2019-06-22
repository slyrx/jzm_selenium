### 遇到反爬虫的处理方式
---
1. 加载时间过长
+ 解决方法：WebDriverWait + expected_conditions<br>
使用headless浏览器


##### 什么是WebDriverWait？如何使用？
---
+ WebDriverWait是显性等待类
+ 使用方式
```
from selenium.webdriver.support.ui import WebDriverWait

WebDriverWait(driver, 超时时长(单位为秒), 调用频率(单位为秒), 忽略异常).until(可执行方法, 超时时返回的信息)
```
+ Tips发现：设置10s时，并不是整10s停止，有时候会是十几秒，但不会出现小于10s的情况。
+ 疑问
+ + 对象一定有 __call__() 方法 是什么意思？

##### 什么是expected_conditions？如何使用？
---
+ expected_conditions是selenium的一个模块，其中包含一系列可用于判断的条件。
+ 默认情况下会每500毫秒调用一次ExpectedCondition直到结果成功返回。
+ ExpectedCondition成功的返回结果是一个布尔类型的true或是不为null的返回值。
```
from selenium.webdriver.support import expected_conditions as EC

locator = (By.CLASS_NAME, 'view-content')
res = WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located(locator))
```

##### 什么是By？如何使用？
---
+ 查找元素类
+ 使用方式
```
locator = (By.CLASS_NAME, 'view-content')
```

##### 什么是headless浏览器？如何使用？
---
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
