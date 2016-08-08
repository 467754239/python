## Decorate 装饰器

`装饰器的使用场景`  
1. flask框架中路由的设定就是通过装饰器完成的。  
2. flask框架写后台程序时，判断是否需要登录，也可以用装饰器来完成。  

> 示例1  
> 函数以参数的形式传递给装饰器并返回一个改变后的函数.

```python
def decorate(func):
    def wrapper():
        print 'wrapper function'
        func()
    return wrapper

@decorate
def func():
    print 'hello world.'
```

> 示例2  
> 装饰器修改了原始的function\_name和function\_doc

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

func()
print func.__doc__
print func.__name__
```

> 示例3  
> 对示例2的改进 保留原始函数的属性

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

> 个人的几个小结论  

```
如果你想对一个"原始函数"或"原始类"在不改变原有代码的情况下对其进行增加功能，可以考虑装饰器.

装饰器允许你接收一个函数并返回一个函数
函数可以以参数的形式传递给装饰器

装饰器用@符号来表示
```

参考资料
- [pc大神 两个实用的Python的装饰器](https://zhuanlan.zhihu.com/p/20175869)
