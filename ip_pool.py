# -*- coding:utf-8 -*-
import sys
import requests
import time
import datetime
import config as cfg
import pymysql as mdb
from lxml import etree
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')


# get proxies on http://www.66ip.cn/
def get_66ip(page):
    #抓取代理IP地址
    #url		= 'http://www.66ip.cn/areaindex_1/'+str(page)+'.html' 
    url		= 'http://www.66ip.cn/'+str(page)+'.html' 

    #提取元素
    url_xpath	= '/html/body/div[last()]//table//tr[position()>1]/td[1]/text()'
    port_xpath	= '/html/body/div[last()]//table//tr[position()>1]/td[2]/text()'

    #设置请求头信息
    headers	= {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}

    #获取页面数据
    results	= requests.get(url, headers=headers)
    tree	= etree.HTML(results.text)

    #提取ip:port
    url_results	= tree.xpath(url_xpath)
    port_results= tree.xpath(port_xpath)
    urls	= [line.strip() for line in url_results]
    ports	= [line.strip() for line in port_results]
   
    #设置返回值
    ip_list = []

    #赋值返回值
    if len(urls) == len(ports):
        for i in range(len(urls)):
            # Match each ip with it's port
            full_ip = urls[i]+":"+ports[i]
            
            #代理数据入栈
            ip_list.append(full_ip)

    #返回代理IP数组
    return ip_list


# get proxies on http://www.xicidaili.com
def get_xici(page):
    #设置返回值
    ip_list = []

    try:
        #设置请求头
        headers	= {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}

        #设置请求地址
        url	= 'http://www.xicidaili.com/nn/'+str(page)

        #抓取数据
        results	= requests.get(url, headers=headers, timeout=4)
        soup	= BeautifulSoup(results.text)

	#提取ip:port
        ip	= []
        port	= []
        for s in soup.find("table").find_all("tr")[1:]:
            try:
                d = s.find_all("td")
                ip.append(str(d[1].string))
                port.append(str(d[2].string))
            except Exception as e:
                    print ('XiCiDaiLi parse error: %s', e)

        #赋值返回值
        if len(ip) == len(port):
            for i in range(len(ip)):
                # Match each ip with it's port
                full_ip = ip[i]+":"+port[i]

		#代理ip:port数据入栈
		ip_list.append(full_ip)

    except Exception, e:
    	    #异常处理
            print 'get proxies error: ', e
	    
    #设置返回值
    return ip_list

# Get all #mimiip.com# ip in a specified page
def get_mimi(page):
    #设置返回值
    ip_list = []
    
    try:
    	#设置请求头
        headers		= {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}

        #设置抓取地址
        url		= 'http://www.mimiip.com/gngao/'+str(page)

	#设置抓取正则
        url_xpath	= '//table[@class="list"]//tr[position()>1]/td[1]/text()'
        port_xpath	= '//table[@class="list"]//tr[position()>1]/td[2]/text()'

	#抓取数据
        results		= requests.get(url, headers=headers, timeout=4)
        tree		= etree.HTML(results.text)
        url_results	= tree.xpath(url_xpath)
        port_results	= tree.xpath(port_xpath)

	#提取数据
        urls	= [line.strip() for line in url_results]
        ports	= [line.strip() for line in port_results]

        if len(urls) == len(ports):
            for i in range(len(urls)):
                # Match each ip with it's port
                full_ip = urls[i]+":"+ports[i]

		#追加到返回值列表中
                ip_list.append(full_ip)

    except Exception, e:
            print 'get proxies error: ', e
    
    #返回代理数据
    return ip_list

# Get all #kuaidaili# ip in a specified page
def get_kuaidaili(page):
    #设置返回值
    ip_list = []

    try:
    	#设置请求头信息
        headers	= {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}

	#设置抓取地址
        url	= 'http://www.kuaidaili.com/free/inha/'+str(page)+'/'

	#设置提取正则
        url_xpath	= '//td[@data-title="IP"]/text()'
        port_xpath	= '//td[@data-title="PORT"]/text()'
	
	#抓取数据
        results		= requests.get(url, headers=headers, timeout=4)
        tree		= etree.HTML(results.text)
        url_results	= tree.xpath(url_xpath)
        port_results	= tree.xpath(port_xpath)
        urls		= [line.strip() for line in url_results]
        ports		= [line.strip() for line in port_results]

        if len(urls) == len(ports):
            for i in range(len(urls)):
                # Match each ip with it's port
                full_ip = urls[i]+":"+ports[i]

		#追加数据到返回结果栈中
                ip_list.append(full_ip)

    except Exception, e:
            print 'get proxies error: ', e
    
    #返回结果
    return ip_list


#  Get all ip in 0~page pages website
def get_all_ip(page):
    #设置返回值
    ip_list = []

    # get proxies on 66ip  2017/06/13 共:912页
    for i in range(page):
	#获取代理数据
        cur_ip_list = get_66ip(i+1)

        #停0.5s再抓取
	time.sleep(0.5)

        #抓取的ip追加到返回值中
        for item in cur_ip_list:
            ip_list.append(item)

    # get proxies on xici  2017/06/13 共:2062页
    for i in range(page):
	#获取代理数据
        cur_ip_list = get_xici(i+1)
        
	#停0.5s再抓取
	time.sleep(0.5)
        
	#抓取的ip追加到返回值中
        for item in cur_ip_list:
            ip_list.append(item)
    
    # get proxies on mimiip.com 2017/06/13 共:682页
    for i in range(page):
	#获取代理数据
        cur_ip_list = get_mimi(i+1)
        
	#停0.5s再抓取
	time.sleep(0.5)
        
	#抓取的ip追加到返回值中
        for item in cur_ip_list:
            ip_list.append(item)

    # get proxies on kuaidaili.com  2017/06/13 共:10页
    for i in range(page):
	#获取代理数据
        cur_ip_list = get_kuaidaili(i+1)
        
	#停0.5s再抓取
	time.sleep(0.5)
        
	#抓取的ip追加到返回值中
        for item in cur_ip_list:
            ip_list.append(item)

    #设置返回值
    return ip_list


# Use http://lwons.com/wx to test if the server is available.
# 检查代理是否可用
def get_valid_proxies(proxies, timeout):
    # You may change the url by yourself if it didn't work.
    #url = 'http://httpbin.org/get?show_env=1'

    #设置请求地址
    url		= 'https://www.baidu.com'

    #设置可用的代理数据
    results	= []

    #挨个检查代理是否可用
    for p in proxies:
	#设置代理
        proxy = {'http': 'http://'+p}

        try:
	    #设置请求开始时间
            start	= time.time()
	 
	    #使用代理请求数据
            r		= requests.get(url, proxies=proxy, timeout=timeout)

	    #设置请求结束时间
            end		= time.time()

	    #判断是否可用
            if r.text is not None:
	    	print 'succeed: '+p+'\t' + " in " + format(end-start, '0.2f') + 's'

		#追加代理ip到返回的数组中
            	results.append(p)

        except Exception as e:
	    #异常处理
            print 'timeout:', p
	    
	#停1s
	#time.sleep(1)

    #去掉重复数据
    results = list(set(results))

    #返回可用代理数据
    return results

#检查代理是否可用
def get_the_best(round, proxies, timeout, sleep_time):
    #循环检查次数
    for i in range(round):
        print "\n>>>>>>>\tRound\t"+str(i+1)+"\t<<<<<<<<<<"

        #检查代理是否可用
        proxies = get_valid_proxies(proxies, timeout)

        #停一下
        time.sleep(sleep_time)

    #返回可用数据
    return proxies

#获取代理数据
def get_proxies():
	#设置返回变量
	ip_list	= []
	
        #链接数据库
    	conn	= mdb.connect(cfg.host, cfg.user, cfg.passwd, cfg.db)
	cursor	= conn.cursor()

	#设置数据表名称
	TABLE_NAME = 'valid_ip'
	
	#检查数据表中是否有数据
	ipExist = cursor.execute('SELECT * FROM %s ' %(TABLE_NAME))
	
	#提取数据
	result	= cursor.fetchall()

	#若表里有数据　直接返回，没有则抓取再返回
	if len(result) != 0:
		for item in result:
			ip_list.append(item[0])
	else:
	    	#获取代理数据
		ip_list = main()

	#返回代理数据
	return ip_list	


#入口方法
def main():

    print "\n>>>>>>>>>>>>>>>>>>> 代理IP数据抓取中...   <<<<<<<<<<<<<<<<<<<<<<<<<<\n"

    #获取代理数据
    ip_list = get_all_ip(cfg.page_num)

    #检查代理是否可用
    proxies = get_the_best(cfg.examine_round, ip_list, cfg.timeout, cfg.sleep_time)

    print "\n>>>>>>>>>>>>>>>>>>>> 代理数据入库处理 Start  <<<<<<<<<<<<<<<<<<<<<<\n"
    if len(proxies) != 0:
    	#链接数据库
    	conn	= mdb.connect(cfg.host, cfg.user, cfg.passwd, cfg.db)
	cursor	= conn.cursor()

	#设置数据表名称
	TABLE_NAME = 'valid_ip'

	#处理可用的代理入库
    	for item in proxies:
		#检查表中是否存在数据
		ipExist = cursor.execute('SELECT * FROM %s WHERE content="%s"' %(TABLE_NAME, item))
	
		#新增代理数据入库
		if ipExist == 0:
			#插入数据
			n = cursor.execute('INSERT INTO %s VALUES("%s", 1, 0, 0, 1.0, 2.5)' %(TABLE_NAME, item))
			conn.commit()

			#输出入库状态
			if n:
				print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" "+item+" insert success.\n"
			else:
				print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" "+item+" insert failure.\n"
			
		else:
			print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" "+item+" has already exist.\n"

    else:
   	print "\n没有抓到可用数据\n "

    print "\n>>>>>>>>>>>>>>>>>>>> 代理数据入库处理 End  <<<<<<<<<<<<<<<<<<<<<<\n"

    #返回代理数据
    return proxies

if __name__ == '__main__':
    main()
