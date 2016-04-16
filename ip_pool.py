# -*- coding:utf-8 -*-
import sys
import requests
import time
from lxml import etree
reload(sys)
sys.setdefaultencoding('utf-8')


# Get all ip in a specified page
def get_proxies_from_site(current_page):
    """
    Parameter
    --------
    current_page: int, the current page's number.
    Return
    ------
    ip_list: list, a list with all 20*page ip with their corresponding ports.
    """
    url = 'http://www.66ip.cn/areaindex_1/'+str(current_page)+'.html'  # The ip resources url
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


#  Get all ip in 0~page pages website
def get_all_ip(page):
    ip_list = []
    for i in range(page):
        cur_ip_list = get_proxies_from_site(i+1)
        for item in cur_ip_list:
            ip_list.append(item)
    for item in ip_list:
        print item
    return ip_list


# Use http://lwons.com/wx to test if the server is available.
def get_valid_proxies(proxies, timeout):
    # You may change the url by yourself if it didn't work.
    url = 'http://lwons.com/wx'
    results = []
    for p in proxies:
        proxy = {'http': 'http://'+p}
        succeed = False
        try:
            start = time.time()
            r = requests.get(url, proxies=proxy, timeout=timeout)
            end = time.time()
            if r.text == 'default':
                succeed = True
        except Exception, e:
            print 'error:', p
            succeed = False
        if succeed:
            print 'succeed: '+p+'\t'+str(end-start)
            results.append(p)
        time.sleep(1)  # Avoid frequent crawling
    results = list(set(results))
    return results


def get_the_best(round, proxies, timeout, sleeptime):
    """
    ========================================================
    With the strategy of N round test to find those secure
    and stable ip. During each round it will sleep a while to
    avoid a 'famous 15 minutes"
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
        time.sleep(sleeptime)
    return proxies


def main():
    ip_list = get_all_ip(2)
    proxies = get_the_best(3, ip_list, 1.5, 60)  # The suggested parameters
    print "\n\n\n"
    print ">>>>>>>>>>>>>>>>>>>The Final Ip<<<<<<<<<<<<<<<<<<<<<<"
    for item in proxies:
        print item


if __name__ == '__main__':
    main()



