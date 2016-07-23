## 符号#!是什么鬼

```
符号(#!)叫做'Shebang'或者'Sha-bang'
在Unix/linux系统脚本中比较常见，它指明了执行脚本文件的解释器.

1. 如果脚本文件中没有#!这一行，那么它执行时会默认用当前Shell去解释这个脚本(即：$SHELL环境变量）
2. 如果#!之后的解释程序是一个可执行文件，那么执行这个脚本时，它就会把文件名及其参数一起作为参数传给那个解释程序去执行
3. 如果#!指定的解释程序没有可执行权限，则会报错“bad interpreter: Permission denied“
   如果#!指定的解释程序不是一个可执行文件，那么指定的解释程序会被忽略，转而交给当前的SHELL去执行这个脚本
4. 如果#!指定的解释程序不存在，那么会报错“bad interpreter: No such file or directory”
   注意：#!之后的解释程序，需要写其绝对路径（如：#!/bin/bash），它是不会自动到$PATH中寻找解释器的
5. 当然，如果你使用”bash test.sh”这样的命令来执行脚本，那么#!这一行将会被忽略掉，解释器当然是用命令行中显式指定的bash.
```
#### hexdump是Linux下的一个二进制文件查看工具，可以将二进制文件转换为ASCII、10进制、16进制或8进制进行查看。
> 二进制文件  
> 457f表示二进制文件 

```
# hexdump /bin/cat | head -n 1 | awk '{ print $1, $2 }'
0000000 457f
# hexdump /bin/ping | head -n 1 | awk '{ print $1, $2 }'
0000000 457f
# hexdump /bin/sed | head -n 1 | awk '{ print $1, $2 }'
0000000 457f
```
> 2123表示脚本
```
$ cat th1.sh 
echo 'hello world.'

$ cat th2.sh 
#!/bin/bash
echo 'hello world.'

$ cat th3.py
print 'hello world.'

$ cat th4.py
#!/usr/bin/env python
print 'hello world.'

# hexdump th1.sh  | head -n 1 | awk '{ print $1, $2 }'
0000000 6365

# hexdump th2.sh  | head -n 1 | awk '{ print $1, $2 }'
0000000 2123

# hexdump th3.py  | head -n 1 | awk '{ print $1, $2 }'
0000000 7270

# hexdump th4.py  | head -n 1 | awk '{ print $1, $2 }'
0000000 2123
```
二进制文件的前两位决定了是什么文件、视频格式等.
