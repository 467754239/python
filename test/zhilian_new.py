#!coding:utf-8

import requests
import logging


# 登录页的url
url = 'https://passport.zhaopin.com/'

# 有些网站反爬虫，这里用headers把程序伪装成浏览器
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'}

# 登录需要提交的表单
form_data = {
    'bkurl': '',
    'LoginName': '477754239@qq.com',   # 填入网站的上网帐号
    'Password': 'yi15093547036',               # 填入网站密码
    'RememberMe': 'false'
}

req = requests.session()
login_response = req.post(url, data=form_data, headers=header)
print login_response.text
