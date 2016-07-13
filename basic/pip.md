## 安装pip软件包
```
下载pip脚本(两者任选其一)
# wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
# wget https://bootstrap.pypa.io/get-pip.py

安装pip工具
# python get-pip.py

确定pip的安装路径
# find / -name pip
/usr/local/python27/bin/pip	# 默认被安装了python27的路径下.
/usr/local/python27/lib/python2.7/site-packages/pip
/root/.cache/pip

添加pip环境变量
# echo "PATH=/usr/local/python27/bin/:\$PATH" > /etc/profile.d/pip.sh
# source /etc/profile

查看pip当前版本
# pip -V
pip 8.1.2 from /usr/local/python27/lib/python2.7/site-packages (python 2.7)
```
