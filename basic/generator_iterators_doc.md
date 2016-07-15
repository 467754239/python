## Generator 生成器
- 生成器的定义？

```
生成器是一次生成一个值的特殊类型函数。可以将其视为可恢复函数。调用该函数将返回一个可用于生成连续 x 值的生成器.

简单的说就是在函数的执行过程中，yield语句会把你需要的值返回给调用生成器的地方，
然后退出函数，下一次调用生成器函数的时候又从上次中断的地方开始执行，
而生成器内的所有变量参数都会被保存下来供下一次使用。
```
- 创建生成器   
    - 示例1  

```python
#coding:utf-8

class yrange(object):
    def __init__(self, num):
        self.num = num
        self.initial_val= 0

    def __iter__(self):
        return self

    def next(self):
        while self.initial_val < self.num:
            self.initial_val += 1
            return self.initial_val
        raise StopIteration

yx = yrange(10)
print yx

```
- 示例2   

```python
#coding:utf-8

def create_generator(N):
    i = 0
    while i < N:
        yield i
        i += 1

cg = create_generator(10) 
print cg

```
    - 示例3  

```python
#coding:utf-8

class yrange(object):
    def __init__(self, num):
        self.num = num
        self.initial_val= 0 
        
    def __iter__(self):
        return self.next()

    def next(self):
        while self.initial_val < self.num:
            self.initial_val += 1
            yield self.initial_val

gen = yrange(10)
for n in gen:
    print n
```
    - 示例4  

```python
def read_file(fpath):
    block_size = 1024
    with open(fpath, 'rb') as f:
        while True:
            block = f.read(block_size)
            if not block:
		return
            yield block
```

- 生成器解决了什么问题？

```
避免一次性或者无限制的占用较大的内存.
```
- iterators 迭代器  

    - 迭代器的定义？  
```
xxxxx
```
