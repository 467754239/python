## Python版本升级 2.6到2.7
```
# python -V
Python 2.6.6

# yum install gcc gcc-c++ make wget xz wget readline-devel
# yum install python-devel openssl-devel zlib-devel

# cd /usr/local/src
# wget https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tar.xz
# xz -d Python-2.7.11.tar.xz
# tar xf Python-2.7.11.tar
# cd Python-2.7.11
# ./configure --prefix=/usr/local/python27
# make
# make install

# mv /usr/bin/python /usr/bin/python_old
# ln -s /usr/local/python27/bin/python /usr/bin/
# sed -i '/#!/ s/python$/python2.6/g' /usr/bin/yum

# echo "PATH=/usr/local/python27/bin:\$PATH" > /etc/profile.d/python2.7.sh
# source /etc/profile

# python -V
Python 2.7.11

# python
Python 2.7.11 (default, Jul 11 2016, 19:15:36) 
[GCC 4.4.7 20120313 (Red Hat 4.4.7-17)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> print "hello world."
hello world.
```
