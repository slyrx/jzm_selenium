## 断点续爬
---
+ 通过制定命名规则的方式，在程序开启时检查上一次爬取的位置，从而调整爬取队列中链接的开始顺序。
+ 建立索引，下一次取索引的最后一个位置。
+ + 使用redis数据库，将每次爬取的内容存储到redis中，再次执行爬取时，先到redis数据库中查找本次爬取的key值是否已经存在，如不存在，执行爬取，如存在执行下一个。
