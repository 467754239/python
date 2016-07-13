## 安装ipython 

```
方式1> pip
# pip install ipython
# pip install ipython=='4.2.0'

方式2> 源码方式
# wget https://pypi.python.org/packages/09/2e/870d1058768f5240062beb0bd2ff789ac689923501b0dd6b480fb83314fc/ipython-5.0.0.tar.gz#md5=9c00df2f7e2e2636aba02671f45eea6b
# tar zxvf ipython-5.0.0.tar.gz
# cd ipython-5.0.0
# python setup.py install
```

## 卸载ipython
```
方式1> pip
# pip uninstall ipython

方式2> 源码方式
使用python setup.py install来安装的python包，但是如何卸载呢？
只能手动删除安装的文件
# python setup.py install --record files.txt 	# 记录安装后文件的路径
# cat files.txt | xargs rm -rf  		# 删除这些文件
```
