# jzm_selenium
1. 遇到的反爬虫问题
+ + 使用 scrapy 爬取第2页就会出现404。 解决办法：换策略
+ + 使用 selenium 在爬取一段时间后会被网站禁止一段时间。解决办法：加随机数，使等待时间变随机; 外加换IP
+ + 在class类里面增加了混淆，后面会更改随机数，变化标签的类名。
+ + + 解决办法：正则表达式
```
soup.find_all(href=re.compile("elsie"), id='link1')
```
+ + + find_all可以取一个类的名称，两个不行
+ + + If you want to search for tags that match two or more CSS classes, you should use a CSS selector:
```
soup.select('div.tvgenre.clear')
```
+ + 某一页长时间加载不上，TimeOut显示。解决办法:增加重试机制
```
while True:
    retry
```
2. 如何做增量处理
+ + 通过制定命名规则的方式，在程序开启时检查上一次爬取的位置，从而调整爬取队列中链接的开始顺序。

3. 控件加载时间过长，selenium.common.exceptions.TimeoutException: Message: timeout
+ + 单个网页的内容在浏览器中以及可以看到，但是在selenium里却一直显示在加载。
+ + 解决方法：如果超过10s还没有加载完，就不加载了
+ + by
+ + WebDriverWait
+ 加载时间的长短还和代理链路的好用情况有关。
