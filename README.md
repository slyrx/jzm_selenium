# jzm_selenium
+ 遇到的反爬虫问题
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
