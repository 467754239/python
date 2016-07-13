## 安装ipython 

```
方式1> pip
# pip install ipython
# pip install ipython=='4.2.0'

方式2> 源码方式
# wget 
# tar zxvf 
# cd
# python setup.py install
```

## 卸载ipython
```
使用python setup.py install来安装的python包，但是如何卸载呢？
只能手动删除安装的文件
# python setup.py install --record files.txt 	# 记录安装后文件的路径
# cat files.txt | xargs rm -rf  		# 删除这些文件
```
