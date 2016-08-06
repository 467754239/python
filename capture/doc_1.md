## 简单示例1
> 豆瓣电影中单个url  
> 尽可能匹配url中电影的所有封面(封面的名称及图片)  

[豆瓣电影](https://movie.douban.com/)

```python
#coding:utf-8

import re
import os
import requests

def run(url):
    req = requests.get(url)
    if req.status_code != 200:
        return
    s = req.content
    imgs_iter = re.findall(r'<img src="(http.*?)"\salt="(.*?)"', s)
    imgs = { img[1]:img[0] for img in imgs_iter }
    for name, url in imgs.items():
        print '%s -> %s' % (name, url)

if __name__ == '__main__':
    url = 'https://movie.douban.com/'
    run(url)
```

> 执行结果

```
哆啦A梦：新·大雄的日本诞生 -> https://img3.doubanio.com/view/movie_poster_cover/lpst/public/p2367659423.jpg
地球物种对于探索/抵御太空所做的努力 -> https://img3.doubanio.com/view/movie_gallery_frame_hot_rec/normal/public/c06a1aa555afb8d.jpg
路边野餐 -> https://img3.doubanio.com/view/movie_poster_cover/lpst/public/p2366570716.jpg
盗墓笔记 -> https://img1.doubanio.com/view/movie_poster_cover/mpst/public/p2370646859.jpg
古曼 -> https://img1.doubanio.com/view/movie_poster_cover/mpst/public/p2369098979.jpg
巴霍巴利王：开端 -> https://img3.doubanio.com/view/movie_poster_cover/mpst/public/p2363089554.jpg
神秘世界历险记3 -> https://img3.doubanio.com/view/movie_poster_cover/mpst/public/p2370787801.jpg
陆垚知马俐 -> https://img1.doubanio.com/view/movie_poster_cover/mpst/public/p2361036748.jpg
豆列｜那些讲述异性朋友的电影 -> https://img1.doubanio.com/view/movie_gallery_frame_hot_rec/normal/public/befea2ff4c4aee7.jpg
大鱼海棠 -> https://img3.doubanio.com/view/movie_poster_cover/mpst/public/p2361744534.jpg
2016上半年豆瓣电影口碑榜Top50 -> https://img3.doubanio.com/view/movie_gallery_frame_hot_rec/normal/public/9b7ce0e31e779b5.jpg
致青春·原来你还在这里 -> https://img1.doubanio.com/view/movie_poster_cover/mpst/public/p2364795527.jpg
泰山归来：险战丛林 -> https://img3.doubanio.com/view/movie_poster_cover/mpst/public/p2367559705.jpg
爱宠大机密 -> https://img3.doubanio.com/view/movie_poster_cover/mpst/public/p2363369616.jpg
封神传奇 -> https://img3.doubanio.com/view/movie_poster_cover/mpst/public/p2366372816.jpg
夏有乔木 雅望天堂 -> https://img3.doubanio.com/view/movie_poster_cover/mpst/public/p2355434506.jpg
寒战2 -> https://img3.doubanio.com/view/movie_poster_cover/mpst/public/p2360072346.jpg
惊天大逆转 -> https://img3.doubanio.com/view/movie_poster_cover/mpst/public/p2363070684.jpg
第73届威尼斯电影节入围名单 -> https://img3.doubanio.com/view/movie_gallery_frame_hot_rec/normal/public/b9dccf1ae42f5c6.jpg
我最好朋友的婚礼 -> https://img1.doubanio.com/view/movie_poster_cover/mpst/public/p2365223709.jpg
我们诞生在中国 -> https://img3.doubanio.com/view/movie_poster_cover/mpst/public/p2370034655.jpg
绝地逃亡 -> https://img3.doubanio.com/view/movie_poster_cover/mpst/public/p2366057661.jpg
```
