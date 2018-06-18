##版本升级 2.6到2.7
```
当前python版本
# python -V
Python 2.6.6

安装依赖包
# yum install gcc gcc-c++ make xz wget readline-devel
# yum install python-devel openssl-devel zlib-devel

下载
# wget https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tar.xz

编译安装
# xz -d Python-2.7.11.tar.xz
# tar xf Python-2.7.11.tar
# cd Python-2.7.11
# ./configure --prefix=/usr/local/python27
# make
# make install

替换掉python2.6.6的二进制文件成python2.7.11
# mv /usr/bin/python /usr/bin/python_old
# ln -s /usr/local/python27/bin/python /usr/bin/
# sed -i '/#!/ s/python$/python2.6/g' /usr/bin/yum

配置python2.7.11环境变量
# echo "PATH=/usr/local/python27/bin:\$PATH" > /etc/profile.d/python2.7.sh
# source /etc/profile

查看编译后当前python版本
# python -V
Python 2.7.11

测试python2.7.11是否安装成功
# python
Python 2.7.11 (default, Jul 11 2016, 19:15:36) 
[GCC 4.4.7 20120313 (Red Hat 4.4.7-17)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> print "hello world."
hello world.
```
