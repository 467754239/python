## 装饰器(decorate)

### 示例1  
> func函数以参数的形式传递给装饰器并返回一个改变后的func函数.

```python
def decorate(func):
    def wrapper():
        print 'wrapper function'
        func()
    return wrapper

@decorate
def func():
    print 'hello world.'

等价于
func = decorate(func)
func()
```

使用:
```
func()	# 调用

### 输出
wrapper function
hello world.
```

### 示例2  
> 装饰器修改了原始的function\_name和function\_doc属性

```python
def decorator(f):
    def wrapper():
        '''
        decorator of wrapper func
        '''
        f()
    return wrapper

@decorator
def func():
    '''
    do someting
    '''
    print 'hello world.'

```

使用:
```
# 调用
func()
print func.__doc__
print func.__name__

### 输出
hello world.

        decorator of wrapper func
        
wrapper
```

### 示例3  
> 对示例2的改进 保留原始函数func的属性

```python
#coding:utf-8

import functools

def decorator(func):
    def wrapper():
        '''
        decorator of wrapper func
        '''
        func()
    # 用wrapper来替代func但同时保留它的doc和func等...
    return functools.wraps(func)(wrapper)
    

@decorator
def func():
    '''
    do someting
    '''
    print 'hello world.'

func()
print func.__doc__
print func.__name__
```

使用:
```python
# 调用
func()
print func.__doc__
print func.__name__

### 输出
hello world.

    do someting
    
func
```

### 示例4
> 接收任意数量的可变长参数

```python
def decorate(func):
    def wrapper(*args, **kwargs):
        print 'wrapper function'
        func(*args, **kwargs)
    return wrapper 

@decorate
def func(*args, **kwargs):
    print 'hello world.'
    print 'args = ', args
    print 'kwargs = ', kwargs

kw = {'age' : '26'}
func('zhengys', **kw)
```

使用：
```
# 调用
kw = {'age' : '26'}
func('zhengys', **kw)

### 输出
wrapper function
hello world.
args =  ('zhengys',)
kwargs =  {'age': '26'}
```

### 示例5
> 摘录 知乎pc大神  
> 这个函数的作用在于可以给任意可能会hang住的函数添加超时功能，这个功能在编写外部API调用 、网络爬虫、数据库查询的时候特别有用  

```python
import signal, functools #下面会用到的两个库
 
class TimeoutError(Exception):      # 定义一个Exception，后面超时抛出 
    pass 

def timeout(seconds, error_message = 'Function call timed out'):
    def decorated(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)
      
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)        # 为信号绑定一个处理函数.
            signal.alarm(seconds)                                 # 多长时间触发SIGALRM信号.
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)                                   # 取消SIGALRM信号，不在继续抛出异常.
            return result
        return functools.wraps(func)(wrapper)
    return decorated
```

使用：
```
@timeout(5) # 限定下面的slowfunc函数如果在5s内不返回就强制抛TimeoutError Exception结束.
def slowfunc(sleep_time):
  import time
  time.sleep(sleep_time) #这个函数就是休眠sleep_time秒.

slowfunc(3) #sleep 3秒，正常返回 没有异常.


slowfunc(10) #被终止 

## 输出 
---------------------------------------------------------------------------
TimeoutError                              Traceback (most recent call last)
```

### 示例6
> 摘录 知乎pc大神  
> 有时候出于演示目的或者调试目的，我们需要程序运行的时候打印出每一步的运行顺序 和调用逻辑。类似写bash的时候的bash -x调试功能,然后Python解释器并没有 内置这个时分有用的功能，那么我们就“自己动手，丰衣足食”。  

```python
import sys,os,linecache
def trace(f):
    def globaltrace(frame, why, arg):
        if why == "call": 
            return localtrace
        return None
        
    def localtrace(frame, why, arg):
        if why == "line":
            # record the file name and line number of every trace 
            filename = frame.f_code.co_filename
            lineno = frame.f_lineno
            bname = os.path.basename(filename)
            print "{}({}): {}".format(  bname,
                                        lineno,
                                        linecache.getline(filename, lineno).strip('\r\n')),
        return localtrace
        
    def _f(*args, **kwds):
        sys.settrace(globaltrace)
        result = f(*args, **kwds)
        sys.settrace(None)
        return result
    return _f
```

使用：
```pyhon
@trace
def xxx():
  print 1
  print 22
  print 333

xxx() #调用 

## 输出 
<ipython-input-4-da50741ac84e>(3):     print 1 # @trace 的输出 
1
<ipython-input-4-da50741ac84e>(4):     print 22 # @trace 的输出 
22
<ipython-input-4-da50741ac84e>(5):     print 333 # @trace 的输出 
333
```

### 结论  
```
# 什么时候使用装饰器.
如果你想对一个"原始函数"或"原始类"在不改变原有代码的情况下对其进行增加新功能，你可以考虑使用装饰器.

# 装饰器的特点
装饰器接收一个原始函数并返回一个被装饰后的函数
函数可以以参数的形式传递给装饰器
装饰器用@符号来声明

# 装饰器的应用场景
flask框架中路由的设定就是通过装饰器完成的。
flask框架中写后台程序时，判断用户是否需要登录，也可以用装饰器来完成。
```

参考资料
- [两个实用的Python的装饰器(pc大神)](https://zhuanlan.zhihu.com/p/20175869)
