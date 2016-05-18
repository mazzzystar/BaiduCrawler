# BaiduCrawler
A crawler crawling baidu searching results by means of constantly changing proxies.

爬取百度搜索结果中c-abstract里的数据，并使用不断更换代理ip的方式绕过百度反爬虫策略，从而实现对数以10w计的词条的百度搜索结果进行连续爬取。

![](https://github.com/fancoo/BaiduCrawler/blob/master/images/git.png)

###爬取策略

有3个策略：
   * 1. 每当出现download_error，更换一个IP
   * 2. 每爬取200条文本，更换一个IP
   * 3. 每爬取20,000次，更新一次IP资源池

###TODO

* 1. 对因网络原因未爬取的词进行二次爬取，直到达到用户指定的爬取率
* 2. 对爬取速度快的优质ip增加权重，从而形成一个具有优先级的ip池
