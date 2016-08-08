## 装饰器(decorate)

示例1  
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

示例2  
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

示例3  
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
```
# 调用
func()
print func.__doc__
print func.__name__

### 输出
hello world.

    do someting
    
func
```

结论  
```
## 装饰器的特点
如果你想对一个"原始函数"或"原始类"在不改变原有代码的情况下对其进行增加功能，可以考虑装饰器.
装饰器允许你接收一个函数并返回一个函数
函数可以以参数的形式传递给装饰器
装饰器用@符号来表示

## 装饰器的使用场景
flask框架中路由的设定就是通过装饰器完成的。
flask框架写后台程序时，判断是否需要登录，也可以用装饰器来完成。
```

参考资料
- [pc大神 两个实用的Python的装饰器](https://zhuanlan.zhihu.com/p/20175869)
