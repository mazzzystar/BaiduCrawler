# coding:utf-8

# 从代理ip网站上总共要爬取的ip页数。一般每页20条，小项目(20-30个代理ip即可完成的)可以设置为1-2页。
page_num = 1

# 对已经检测成功的ip测试轮次。普通爬虫服务设置1轮足矣，若希望减少抓取数据缺失，可适当提高轮次，然而可能ip也将更少。
examine_round = 1

# 超时时间。代理ip在测试过程中的超时时间。
timeout = 1.5

#如果超过这个时间就在数据库里删除
delet_timeout = 3

# 数据库链接地址
host = '127.0.0.1'

# 数据库链接端口
port = 3306

# 数据库链接用户名
user = 'root'

# 数据库密码
passwd = '******'

# 数据库名
DB_NAME = 'proxies'

# 表名
TABLE_NAME = 'valid_ip'

# 数据库字符
charset = 'utf8'
