## elasticsearch api

工作中遇到es写入性能的瓶颈，在这里记录下优化调整的思路.
```
1. 提高写入性能，减少写入磁盘的次数.

1分钟平均的日志量在1.6w左右.
在没有任何优化的情况下单台es的写入性能2700左右(待测试)
```


## elasticsearch优化参考文章
* [亿级规模的Elasticsearch优化实战](http://chuansong.me/n/1610745)
* [ElasticSearch优化配置](http://www.cnblogs.com/Jerryshome/p/5036171.html)
* [elasticsearch集成各路好用插件，优化配置，开箱即用，快速上手](https://github.com/full-stack-engineer/elasticsearch-integrated)
* [如何提高ElasticSearch 索引速度](http://www.jianshu.com/p/5eeeeb4375d4)