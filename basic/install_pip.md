### 安装pip软件包
```
# wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
or
# wget https://bootstrap.pypa.io/get-pip.py
# python get-pip.py 

# echo "PATH=/usr/local/python27/bin:\$PATH" > /etc/profile.d/python.sh
# source /etc/profile

有时候会遇到这样的问题？
系统中pip明明已经安装了，但是在使用pip的时候仍然提示pip不能被使用；
# find / -name pip
/usr/local/python27/bin/pip     # 手动使用这个pip命令 将其加入到环境变量中.
/usr/local/python27/lib/python2.7/site-packages/pip
/usr/bin/pip
/usr/lib/python2.6/site-packages/pip
/root/.cache/pip

```
