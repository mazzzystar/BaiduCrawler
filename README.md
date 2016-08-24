# BaiduCrawler
A crawler crawling baidu searching results by means of constantly changing proxies.

爬取百度搜索结果中c-abstract里的数据，并使用不断更换代理ip的方式绕过百度反爬虫策略，从而实现对数以10w计的词条的百度搜索结果进行连续爬取。

![](https://github.com/fancoo/BaiduCrawler/blob/master/images/git.png)

###获取代理ip策略

* 1. 抓取页面上全部[ip:port]对，并检测可用性（有的代理ip是连不通的）。
* 2. 使用“多轮检测”策略，即每个ip要经历N轮，每间隔duration再次尝试连通一次。因此N轮下来，存活的ip须满足：每次都在timeout范围以内连通。

###爬取策略

有3个策略：
   * 1. 每当出现download_error，更换一个IP
   * 2. 每爬取200条文本，更换一个IP
   * 3. 每爬取20,000次，更新一次IP资源池

###TODO

* 1. 对因网络原因未爬取的词进行二次爬取，直到达到用户指定的爬取率
* 2. 对爬取速度快的优质ip增加权重，从而形成一个具有优先级的ip池
