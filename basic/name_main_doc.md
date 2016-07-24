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
## 使用场景 ##

```
$ th3.py
def func1():
    pass

def func2():
    pass

def func3():
    pass

if __name__ == '__main__':
    func1()
    func2()
    func3()

$ th4.py
from th3 import func1, func2, func3

脚本th3.py中有定义了3个函数(func1，func2，func3)，当你想直接执行这3个函数的时候可以执行这个脚本就可以.
如果你想在另外一个脚本中导入这三个函数，仅是导入并不想在导入这三个函数的时候执行者3个函数，这个时候__name__和__main__就起到了作用.

脚本th4.py仅是导入了模块下的函数，并没有执行执行函数，如果在th4.py中执行这些函数，那么你就在导入模块后调用该方法就可以了.
```


