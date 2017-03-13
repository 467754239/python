## 安装pip软件包

1 下载pip安装脚本
```
# wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
# wget https://bootstrap.pypa.io/get-pip.py
```

2 运行脚本
```
# python get-pip.py
```

3 确定pip的安装路径
```
# find / -name pip
/usr/local/python27/bin/pip         # 默认被安装了python27的路径下.
/usr/local/python27/lib/python2.7/site-packages/pip
/root/.cache/pip
```

4 添加pip环境变量
```
# echo "PATH=/usr/local/python27/bin/:\$PATH" > /etc/profile.d/pip.sh
# source /etc/profile
```

5 查看pip当前版本
```
# pip -V
pip 8.1.2 from /usr/local/python27/lib/python2.7/site-packages (python 2.7)
```

6 pip批量安装指定包
```
# pip install [options] -r <requirements file> [package-index-options]
# cat > requirements.txt << EOF
Flask 
Flask-Bootstrap 
Flask-Moment
Flask-Script 
Flask-Migrate
Flask-SQLAlchemy 
Flask-WTF 
MySQL-python 
requests
EOF
# pip install -r requirements.txt 
```

7. pip自定义配置文件
```
$ vim /etc/pip.conf
[global]
trusted-host = pypi.douban.com 
index-url = http://pypi.douban.com/simple 

[list]
format=columns
```
