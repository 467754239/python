### CentOS install python 2.7
yum -y install python-devel readline-devel xz wget openssl-devel zlib-devel gcc gcc-c++ make
cd /usr/local/src
wget https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tar.xz
xz -d Python-2.7.11.tar.xz
tar xf Python-2.7.11.tar
cd Python-2.7.11
./configure --prefix=/usr/local/python27
make && make install
cd ..
mv /usr/bin/python /usr/bin/python_old
ln -s /usr/local/python27/bin/python /usr/bin/
sed -i '/#!/ s/python$/python2.6/g' /usr/bin/yum

wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
or
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py   

echo "PATH=/usr/local/python27/bin:\$PATH" > /etc/profile.d/python.sh
source /etc/profile

有时候会遇到即使pip安装成功了 但是pip在安装其它第三方包的时候 依然被安装到python2.6中 导致模块不能被使用 这个时候我们应该如下解决方案
# find / -name pip
/usr/local/python27/bin/pip     # 手动使用这个pip命令 将其加入到环境变量中.
/usr/local/python27/lib/python2.7/site-packages/pip
/usr/bin/pip
/usr/lib/python2.6/site-packages/pip
/root/.cache/pip

# mv /usr/bin/pip /usr/bin/pip_python2.6
# ln -sv /usr/local/python27/bin/pip /usr/bin/pip
# /usr/local/python27/bin/pip install ipython
# ipython   # 这个时候执行ipython命令的时候仍然提示找不到 这个时候find查找
-bash: /usr/bin/ipython: No such file or directory
# find / -name ipython
/usr/local/python27/bin/ipython
# ln -sv /usr/local/python27/bin/ipython /usr/bin/ipython
[root@localhost ~]# ipython
WARNING: IPython History requires SQLite, your history will not be saved
Python 2.7.11 (default, Apr 21 2016, 15:38:56) 
Type "copyright", "credits" or "license" for more information.

IPython 4.2.0 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.

In [1]: 
