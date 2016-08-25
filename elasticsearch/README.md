## elasticsearch api

对Elasticsearch进行压力测试
```
AWS的ec2主机

(1)硬件配置：2核cpu、8G内存、普通硬盘
flush_size: 2w
单进程模式：每秒钟消费3000条记录
系统负载情况：
python程序：cpu在12%和94%之间切换
es进程：cpu在0和105%之间切换.

(2)硬件配置：4核cpu、8G内存、普通硬盘
同时启动两个python进程
flush_size: 2w
系统负载情况：
python程序：cpu最高在89%
es进程：cpu最高在198%

>>> 1085294 / 182
5963
每秒钟消费5963条记录

(2)硬件配置：4核cpu、8G内存、普通硬盘
同时启动三个python进程
flush_size: 2w
系统负载情况：
python程序：cpu最高在89%
es进程：cpu最高在205%

>>> 1003399 / 137
7324
每秒钟消费7324条记录
```



## elasticsearch优化参考文章
* [亿级规模的Elasticsearch优化实战](http://chuansong.me/n/1610745)
* [ElasticSearch优化配置](http://www.cnblogs.com/Jerryshome/p/5036171.html)
* [elasticsearch集成各路好用插件，优化配置，开箱即用，快速上手](https://github.com/full-stack-engineer/elasticsearch-integrated)
* [如何提高ElasticSearch 索引速度](http://www.jianshu.com/p/5eeeeb4375d4)
* [api](http://elasticsearch-py.readthedocs.io/en/latest/index.html)