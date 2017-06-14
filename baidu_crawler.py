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

#抓取数据
def download_html(keywords, proxy):
    #抓取参数 https://www.baidu.com/s?wd=testRequest
    key = {'wd': keywords}
    
    #请求Header
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0 cb) like Gecko'}
    
    #请求代理
    proxy = {'http': 'http://'+proxy}

    #抓取数据内容
    web_content = requests.get("https://www.baidu.com/s?", params=key, headers=headers, proxies=proxy, timeout=4)

    return web_content.text

#解析html
def html_parser(html):
    #设置提取数据正则
    path_cn = "//div[@id='content_left']//div[@class='c-abstract']/text()"
    path_en = "//div[@id='content_left']//div[@class='c-abstract c-abstract-en']/text()"

    #提取数据
    tree	= etree.HTML(html)
    results_cn	= tree.xpath(path_cn)
    results_en	= tree.xpath(path_en)
    text_cn	= [line.strip() for line in results_cn]
    text_en	= [line.strip() for line in results_en]

    #设置返回结果
    text_str	= []

    #提取数据
    if len(text_cn) != 0 or len(text_en) != 0:
	#提取中文
        if len(text_cn):
            for i in text_cn:
	    	text_str.append(i.strip())

        #提取英文
        if len(text_en) != 0:
            for i in text_en:
	    	text_str.append(i.strip())
 
    #返回结果
    return text_str

#获取代理数据
def get_proxies():
    #获取代理数据
    return ip_pool.get_proxies()
    return ['202.108.2.42:80','153.36.35.183:808']

    #设置抓取页数
    dataPageNum = cfg.page_num

    #抓取可用的IP数据
    ip_list = ip_pool.get_all_ip(dataPageNum)

    #验证代理IP是否可用
    useful_proxies = ip_pool.get_the_best(cfg.examine_round, ip_list, cfg.timeout, cfg.sleep_time)

    #返回可用的代理数据
    return useful_proxies

#抓取数据
def extract_all_text(keyword_dict, keyword_text):
    #读取要抓取的关键词
    cn = open(keyword_dict, 'r')

    #逐行行读取关键字抓取数据
    with open(keyword_text, 'w') as ct:
        #获取代理IP数据
        useful_proxies = get_proxies()
	#useful_proxies = ['202.108.2.42:80','153.36.35.183:808']

        #输出代理数据情况
        print "总共：", len(useful_proxies),'IP可用'

	#逐行读取关键词
	for line in cn:
		#设置随机代理
		rd	= random.randint(0, len(useful_proxies)-1)
		proxy	= useful_proxies[rd]
        	print "change proxies: " + proxy
 
		#抓取数据
		content	= download_html(line, proxy)
		raw_text= html_parser(content)
		raw_text= (' |-| '.join(raw_text)).replace('\n', ' ')
		print raw_text

		#写入数据到文件
		ct.write(line.strip()+':\t'+raw_text+'\n')

    #关闭文件句柄
    ct.close()
    cn.close()

#入口方法
def main():
    #抓取搜索关键词
    keyword_dict	= 'data/samples.txt'

    #抓取存取结果
    keyword_text	= 'data/results.txt'

    #抓取数据
    extract_all_text(keyword_dict, keyword_text)

if __name__ == '__main__':
    main()
