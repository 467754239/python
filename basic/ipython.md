## 安装ipython 

```
方式1> pip
# pip install ipython
# pip install ipython=='4.2.0'

方式2> 源码方式
# wget https://pypi.python.org/packages/09/2e/870d1058768f5240062beb0bd2ff789ac689923501b0dd6b480fb83314fc/ipython-5.0.0.tar.gz
# tar zxvf ipython-5.0.0.tar.gz
# cd ipython-5.0.0
# python setup.py install
```

## 卸载ipython
```
方式1> pip
# pip uninstall ipython

方式2> 源码方式
使用python setup.py install来安装的python包，只能手动删除安装的文件

记录安装后文件的路径
# python setup.py install --record files.txt

删除这些文件
# cat files.txt | xargs rm -rf
```

## ipython功能
```
1. 命令补全功能(tab键命令补全)
2. 快捷查看模块帮助信息(?问号查看模块帮助信息)
```
