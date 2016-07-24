## \__name__ and \__main__

> 示例1

```
这里以th1.py和th2.py为例
$ cat th1.py
print __name__

$ cat th2.py 
import th1

# 脚本说明
th1.py打印__name__
th2.py导如模块th1

# 执行结果
$ python th1.py 
__main__

$ python th2.py 
th1

# 结论
执行th1.py脚本，输出的结果是__main__；
导入th1，输出的结果是th1.
```

> 示例2

```
这里依然以th1.py和th2.py为例
$ cat th1.py
if __name__ == '__main__':
    print __name__

$ cat th2.py 
import th1

# 脚本说明
th1.py依然是打印__name__，不同的是在打印前加了一个判断，如果__name__等于字符串"__main__"，那么脚本就打印__name__，否则跳过.
th2.py依然是导入模块th1

# 执行结果
$ python th1.py
__main__

$ python th2.py #没有任何输出

# 结论
执行th1.py脚本，输出结果为__main__.
执行th2.py脚本，输出结果为空，没有任何输出.
```



