## open
```
>>> open?
open(name[, mode[, buffering]]) -> file object

Open a file using the file() type, returns a file object.  This is the
preferred way to open a file.  See file.__doc__ for further information.

译:
返回值是一个文件对象；
打开一个文件使用file()，返回一个文件对象，这是首选方式打开一个文件.

```



## file 
```
>>> file?
file(name[, mode[, buffering]]) -> file object

Open a file.  The mode can be 'r', 'w' or 'a' for reading (default),
writing or appending.  The file will be created if it doesn't exist
when opened for writing or appending; it will be truncated when
opened for writing.  Add a 'b' to the mode for binary files.
Add a '+' to the mode to allow simultaneous reading and writing.
If the buffering argument is given, 0 means unbuffered, 1 means line
buffered, and larger numbers specify the buffer size.  The preferred way
to open a file is with the builtin open() function.
Add a 'U' to mode to open the file for input with universal newline
support.  Any line ending in the input file will be seen as a '\n'
in Python.  Also, a file so opened gains the attribute 'newlines';
the value for this attribute is one of None (no newline read yet),
'\r', '\n', '\r\n' or a tuple containing all the newline types seen.

'U' cannot be combined with 'w' or '+' mode.

译:
返回值是一个文件对象；
打开一个文件，
mode可以是三种类型'r', 'w' or 'a'，默认是'r'；这三种类型分别对应着reading，writing or appending.
当mode使用writing or appending时，如果这个文件不存在，那么会创建这个文件；
当mode使用writing时，文件将被删除或覆盖；
当mode使用'b'时，是打开二进制文件；
当mode使用'+'时，允许同时读和写；
如果buffering参数给了，0表示无缓冲，1表示缓冲，也可以指定缓冲的大小
'U'不能和'w' or '+'联合使用.

```

# 参数解释
```
f.read([size])              # 返回值是string； 读取文件全部内容或读取指定大小的文件内容.    
f.readline([size])          # 返回值是string； 每次读取文件的一行.    
readlines([size])           # 返回值是list；   读取文件的全部，每一行是list中的一个元素.    
    
f.flush()                   # 将write到buffer的数据刷新到对应的磁盘文件中.    
    
f.tell()                    # 指针当前文件的position(文件所在的字节位置).    
f.seek(offset[, whence])    # 移动文件指针.
    
f.close()                   # 保存文件并退出，释放资源；
                            # 如果不关闭文件 文件内容还在buffer缓存 并不会刷新到磁盘文件上.
```

> 示例1  

```python
f = open(filename, 'r')
data = f.read()
for line in data.split('\n'):
    print line
```

> 示例2  

```python
f = open(filename, 'r')
lines = f.readline()
for line in lines:
    print line
```

> 示例3  

```python
f = open(filename, 'r')
for line in f:
    print line
```	
