# BaiduCrawler
爬取百度搜索结果中c-abstract里的数据，并使用不断更换代理ip的方式绕过百度反爬虫策略，从而实现对数以10w计的词条的百度搜索结果进行连续爬取。

![](https://github.com/fancoo/BaiduCrawler/blob/master/images/git.png)

### 获取代理ip策略

* 1. 抓取页面上全部[ip:port]对，并检测可用性（有的代理ip是连不通的）。
* 2. 使用"多轮检测"策略，即每个ip要经历N轮，间隔为duration连接测试，每轮都会丢弃连接时间超过timeout的ip。N轮下来，存活的ip都是每次都在timeout范围以内连通的，从而避免了"辉煌的15分钟"效应。

### 爬取策略

有3个策略：
   * 1. 每当出现download_error，更换一个IP
   * 2. 每爬取200条文本，更换一个IP
   * 3. 每爬取20,000次，更新一次IP资源池
  
上述参数均可手动调整。
目前ip池的使用都是一次性的，<b>如果需要更多的优质ip</b>，可参考我的另一个项目[Proxy](https://github.com/fancoo/Proxy),它是一个代理ip抓取测试评估存储一体化工具，也许可以帮到你。


### TODO

* 1. 对因网络原因未爬取的词进行二次爬取，直到达到用户指定的爬取率
* 2. 对爬取速度快的优质ip增加权重，从而形成一个具有优先级的ip池
* 3. ip评估改写成多线程

### 使用
#### 准备工作
```bash
pip install requests
pip install lxml
pip install beautifulsoup4

git clone https://github.com/fancoo/BaiduCrawler
cd BaiduCrawler
```
#### Python 2.7
```bash
python baidu_crawler.py
```
#### Python 3
本程序仅在win版本的Python3.6测试通过。
```bash
cd Py3
python baidu_crawler.py
```


### 2017/5/4更新
 * 原有的判断ip是否有效的网站失效，已替换。
 * 增加更多代理ip网站。
 * 提高可配置性。


### 2017/6/13更新
 * 新增抓取的代理IP数据存到MySql中 下次先从库中读取 再从网站抓取

### 2017/6/18更新
 * 修改了部分[BoBoGithub](https://github.com/BoBoGithub)提交的PR，并重构了[ip_pool.py](https://github.com/fancoo/Crawler/blob/master/ip_pool.py)的代码。
 * 目前这个版本其实只将有效ip保存到数据库，没能实现ip质量评优以及爬取的多线程，因时间精力有限，考虑未来再加入。

### 2017/7/25更新
* 增加对Python3.6的支持。

