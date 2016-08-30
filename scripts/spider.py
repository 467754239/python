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