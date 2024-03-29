### 遇到反爬虫的处理方式
---
1. 加载时间过长
+ 解决方法：WebDriverWait + expected_conditions<br>
使用headless浏览器


##### 什么是WebDriverWait？如何使用？
---
+ WebDriverWait是显性等待类
+ 表示找到元素前，等待10秒。如果是找到了该元素，页面还继续加载吗？
+ 没有找到重试5秒，找到了，则按照实际加载时间计，可能很长，也可能较长。
+ 使用方式
```
from selenium.webdriver.support.ui import WebDriverWait

WebDriverWait(driver, 超时时长(单位为秒), 调用频率(单位为秒), 忽略异常).until(可执行方法, 超时时返回的信息)
```
+ Tips发现：设置10s时，并不是整10s停止，有时候会是十几秒，但不会出现小于10s的情况。
+ + 因为链路阻塞，执行get函数时本身这个函数的执行时间已经是1分甚至几分种了，因此即使是第一次成功的返回就已经远远超于5秒的设定。
+ 疑问
+ + 对象一定有 __call__() 方法 是什么意思？
+ + 回答：指传入的要是一个函数指针，因为在until内部需要调用该函数指针进行执行method(self.\_driver)
+ 返回的内容根据**可执行方法**的结果返回对应的结果
+ 如果一次成功就不会在while True里循环了，如果一直找不到就会开始循环。

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

2. 停止加载的几种方法
+ 通过Python 针对浏览器控件按下ESC中断浏览器加载
+ + 需要引入多线程，chain、send_key
+ 通过设置限定页面加载限制时间
+ + window.stop()方法，是在接收到timeoutErr后，才调用执行的方法，timeoutErr是触发器。在一次get过程中不会影响到get当次的执行。
+ 通过插件解决,该方法和--headless浏览器使用有冲突
+ + 要给浏览器安装Adblock-Plus拦截广告插件
+ + 网页在主内容完整却依然加载不完整的一个原因是带有广告页面，广告内容加载不完全导致显示加载未完成，因此去掉广告即可。
