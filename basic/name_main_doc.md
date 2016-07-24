## \__name__ and \__main__

> 示例1

```
这里以th1.py和th2.py为例
$ cat th1.py
print __name__

$ cat th2.py 
import th1

# 说明
th1.py打印__name__
th2.py导如模块th1

# 执行结果
$ python th1.py 
__main__

$ python th2.py 
th1

# 结论
当我们执行th1.py脚本的时候，__name__等价于'__main__'；
当我们导如th1模块的时候,__name__等价于模块的名称.
```

> 示例1

```
这里以然以th1.py和th2.py为例
$ cat th1.py
if __name__ == '__main__':
    print __name__

$ cat th2.py 
import th1

# 说明
th1.py依然是打印__name，不过在打印前加了一个判断，如果__name__等于字符串"__main__"，我在打印，否则跳过.
th2.py依然是导入模块th1

# 执行结果
$ python th1.py
__main__

$ python th2.py #没有任何输出

# 结论
当我们想直接执行一个脚本的时候，__name__ == '__main__'没有任何用处.
但当我们想导入这个脚本或者这个模块的时候，并调用脚本中的变量、函数、类的但
仅是调用并不想执行自动执行的时候，__name__就起到了作用，因为在导入模块th1的时候,
在th1.py脚本中的__name__就是等于字符串'__main__'，所以放置在if语句下面的代码都不会执行.
```


