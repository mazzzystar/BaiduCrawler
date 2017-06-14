//创建数据库
create database proxy;

//创建表
use proxy;
CREATE TABLE `valid_ip` (
  `content` varchar(30) NOT NULL,
  `test_times` int(5) NOT NULL DEFAULT '0',
  `failure_times` int(5) NOT NULL DEFAULT '0',
  `success_rate` float(5,2) NOT NULL DEFAULT '0.00',
  `avg_response_time` float NOT NULL DEFAULT '0',
  `score` float(5,2) NOT NULL DEFAULT '0.00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
