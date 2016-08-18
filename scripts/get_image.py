# -*- coding:utf-8 -*-


import requests

url_1 = "http://www.tngou.net/tnfs/api/list"
url_2 = "http://www.tngou.net/tnfs/api/classify"
src_header = "http://tnfs.tngou.net/image"

r = requests.get(url_1)
r = r.json()
print r


def saveImage(imgUrl, imgName= 'default.jpg'):
    response = requests.get(imgUrl, stream = True)
    image = response.content
    dst = r'C:\Users\zizi\Desktop\share\images\\'
    path = dst+imgName
    print 'save the file:'+path+'\n'
    f = open(path, 'wb')
    f.write(image)
    f.close()


def run():
    for line in r['tngou']:
        title = line['title']
        img = line['img']
        src_path = src_header+img
        saveImage(src_path,title+'.jpg')

run()