# -*- coding:utf-8 -*-
import sys
import requests
import time
import config as cfg
from lxml import etree
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')


# get proxies on http://www.66ip.cn/
def get_66ip(page):
    """
    Parameter
    --------
    current_page: int, the current page's number.
    Return
    ------
    ip_list: list, a list with all 20*page ip with their corresponding ports.
    """
    url = 'http://www.66ip.cn/areaindex_1/'+str(page)+'.html'  # The ip resources url
    url_xpath = '/html/body/div[last()]//table//tr[position()>1]/td[1]/text()'
    port_xpath = '/html/body/div[last()]//table//tr[position()>1]/td[2]/text()'
    results = requests.get(url)
    tree = etree.HTML(results.text)
    url_results = tree.xpath(url_xpath)    # Get ip
    port_results = tree.xpath(port_xpath)  # Get port
    urls = [line.strip() for line in url_results]
    ports = [line.strip() for line in port_results]

    ip_list = []
    if len(urls) != len(ports):
        print "No! It's crazy!"
    else:
        for i in range(len(urls)):
            # Match each ip with it's port
            full_ip = urls[i]+":"+ports[i]
            print full_ip
            ip_list.append(full_ip)
    return ip_list


# get proxies on http://www.xicidaili.com
def get_xici(page):
    ip_list = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
        url = 'http://www.xicidaili.com/nn/'+str(page)  # The ip resources url
        # url_xpath = '/html/body//table[@class="sortable"]//tr[position()>2]/td[1]/text()'
        # port_xpath = '/html/body//table[@class="sortable"]//tr[position()>2]/td[2]/text()'
        results = requests.get(url, headers=headers, timeout=4)
        soup = BeautifulSoup(results.text)
        ip = []
        port = []
        for s in soup.find("table").find_all("tr")[1:]:
            try:
                d = s.find_all("td")
                ip.append(str(d[1].string))
                port.append(str(d[2].string))
            except Exception as e:
                    print ('XiCiDaiLi parse error: %s', e)
        ip_list = []
        if len(ip) != len(port):
            print "No! It's crazy!"
        else:
            for i in range(len(ip)):
                # Match each ip with it's port
                full_ip = ip[i]+":"+port[i]
                print full_ip
        return ip_list
    except Exception, e:
            print 'get proxies error: ', e
            return ip_list


#  Get all ip in 0~page pages website
def get_all_ip(page):
    ip_list = []
    # get proxies on 66ip
    for i in range(page):
        cur_ip_list = get_66ip(i+1)
        for item in cur_ip_list:
            ip_list.append(item)
    # get proxies on xici
    for i in range(page):
        cur_ip_list = get_xici(i+1)
        for item in cur_ip_list:
            ip_list.append(item)

    for item in ip_list:
        print item
    print len(ip_list)
    return ip_list


# Use http://lwons.com/wx to test if the server is available.
def get_valid_proxies(proxies, timeout):
    # You may change the url by yourself if it didn't work.
    url = 'http://httpbin.org/get?show_env=1'
    results = []
    for p in proxies:
        proxy = {'http': 'http://'+p}
        succeed = False
        try:
            start = time.time()
            r = requests.get(url, proxies=proxy, timeout=timeout)
            end = time.time()
            if r.text is not None:
                succeed = True
        except Exception as e:
            print 'timeout:', p
            succeed = False
        if succeed:
            print 'succeed: '+p+'\t' + " in " + format(end-start, '0.2f') + 's'
            results.append(p)
        time.sleep(1)  # Avoid frequent crawling
    results = list(set(results))
    return results


def get_the_best(round, proxies, timeout, sleep_time):
    """
    ========================================================
    With a strategy of N round test to find secure and stable 
    ip, during each round it will sleep a period of time to 
    avoid the 'famous 15 minutes".
    ========================================================
    Parameters
    ----------
    round: int, a number to decide how many round the test will hold.
    proxies: list, the ip list to be detected.
    timeout:  float, for each ip, decide the longest time we assume it's disconnected.
    sleeptime: float, how many seconds it sleep between two round test.
    """
    for i in range(round):
        print '\n'
        print ">>>>>>>Round\t"+str(i+1)+"<<<<<<<<<<"
        proxies = get_valid_proxies(proxies, timeout)
        if i != round-1:
            time.sleep(sleep_time)
    return proxies


def main():
    ip_list = get_all_ip(cfg.page_num)
    proxies = get_the_best(cfg.examine_round, ip_list, cfg.timeout, cfg.sleep_time)  # The suggested parameters
    print "\n\n\n"
    print ">>>>>>>>>>>>>>>>>>>The Final Ip<<<<<<<<<<<<<<<<<<<<<<"
    for item in proxies:
        print item


if __name__ == '__main__':
    main()



