## xrange实现

> version 1
```
#coding: utf-8

class yrange(object):

    def __init__(self, N):
        self.i = 0
        self.N = N

    def __iter__(self):
        return self

    def next(self):
        if self.i >= self.N:
            # 抛异常
            raise StopIteration
        # 保存状态
        ii = self.i
        self.i += 1
        return ii

y = yrange(10)
print list(y)

for x in yrange(10):
    print x
```

> version 2
```
#coding: utf-8

# version 1
def gen(N):
    i = 0
    while i < N:
        yield i
        i += 1

# version 2
class yxrange(object):

    def __init__(self, N):
       self.N = N
       self.i = 0

    def __iter__(self):
        '''
        必须实现__iter__方法，才是识别你是一个可迭代的对象。
        调用generator才能返回一个生成器。
        '''
        return self.generator()

    def generator(self):
        while self.i < self.N:
            yield self.i
            self.i += 1

# version 1
print 'gen(10): ', gen(10)
for x in gen(10):
    print x
g = gen(3)
print g.next()
print g.next()
print g.next()

# version 2
y = yxrange(10)
print y
print list(y)
for x in yxrange(10):
    print x
```
