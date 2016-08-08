## Decorate 装饰器
> 示例1

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
