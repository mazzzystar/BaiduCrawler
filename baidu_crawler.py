# -*- coding:utf-8 -*-
import sys
import requests
from lxml import etree
import random
import ip_pool
import config as cfg

reload(sys)
sys.setdefaultencoding('utf-8')

"""
================================================
 Extract text from the result of BaiDu search
================================================
"""


def download_html(keywords, proxy):
    """
    download html

    Parameters
    ---------
    keywords: keywords need to be search.
    proxy: an ip with port.

    Returns
    ------
    utf8_content: the web content encode in utf-8.

    """
    key = {'wd': keywords}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    web_content = requests.get("http://www.baidu.com/s?", params=key, headers=headers, proxies=proxy, timeout=4)
    content = web_content.text
    return content


def html_parser(html):
    """
    web parser

    Parameters
    ----------
    html: the web html.

    Returns
    -------
    text: the whole text of the search results.
    times: the times that key word hits.

    """
    path = "//div[@id='content_left']//div[@class='c-abstract']/text()"  # Xpath of abstract in BaiDu search results
    tree = etree.HTML(html)
    results = tree.xpath(path)
    text = [line.strip() for line in results]
    text_str = ''
    if len(text) == 0:
        print "error, no data!"
    else:
        for i in text:
            i = i.strip()
            text_str += i
    return text_str


def extract_all_text(keyword_dict, keyword_text):
    """
    ========================================================
    Extract all text of elements in company dict
    There are 3 strategies:
        1. Every time appears "download timeout", I will choose another proxy.
        2. Every 200 times after I crawl, change a proxy.
        3. Every 2000,0 times after I crawl, Re-construct an ip_pool.

    ========================================================
    Parameters
    ---------
    keyword_dict: the keyword name dict.
    keyword_text: file that save all text.

    Return
    ------
    """

    cn = open(keyword_dict, 'r')
    print ">>>>>start to get proxies<<<"
    with open(keyword_text, 'w') as ct:
        flag = 0  # Change ip
        switch = 0  # Change the proxies list
        useful_proxies = []
        new_ip = ''
        for line in cn:
            if switch % 20000 == 0:
                switch = 1
                ip_list = ip_pool.get_all_ip(cfg.page_num)
                useful_proxies = ip_pool.get_the_best(cfg.examine_round, ip_list, cfg.timeout, cfg.sleep_time)
            switch += 1
            try:
                if flag % cfg.n == 0 and len(useful_proxies) != 0:
                    flag = 1
                    rd = random.randint(0, len(useful_proxies)-1)
                    new_ip = useful_proxies[rd]
                    print "change proxies: " + new_ip
                flag += 1
                proxy = new_ip
                content = download_html(line, proxy)
                raw_text = html_parser(content)
                raw_text = raw_text.replace('\n', ' ')
                print raw_text
                ct.write(line.strip()+'\t'+raw_text+'\n')
            except Exception, e:
                rd = random.randint(0, len(useful_proxies)-1)
                new_ip = useful_proxies[rd]
                print 'download error: ', e
    ct.close()
    cn.close()


def main():
    keyword_dict = 'data/samples.txt'
    keyword_text = 'data/results.txt'
    extract_all_text(keyword_dict, keyword_text)

if __name__ == '__main__':
    main()

