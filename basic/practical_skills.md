Python 实用技巧
======
- enumerate
- 切片



## enumerate ##
翻译
```
enumerate(iterable[, start]) -> iterator for index, value of iterable

Return an enumerate object.  iterable must be another object that supports
iteration.  The enumerate object yields pairs containing a count (from
start, which defaults to zero) and a value yielded by the iterable argument.
enumerate is useful for obtaining an indexed list:
    (0, seq[0]), (1, seq[1]), (2, seq[2]), ...

# 译:
内置函数
enumerate(可迭代的对象[, 起始值]) -> 返回可迭代对象的索引，可迭代对象的值.

把可迭代的对象转换成枚举对象。
iterable是可迭代的参数，比如列表、数组、字典等对象；
start是枚举的起始值，默认是从0开始。
这个内置函数实现原理是这样的，从迭代对象的方法__next__()取得一项值，
然后对参数start开始计数，每一项增加1，生成一个元组返回。
```

enumerate函数实现的原理
```
def new_enumerate(sequence, start=0):
    index = start
    for x in l:
        yield index, x
        index += 1
```

示例
> 如果对一个列表，既要遍历索引又要遍历元素时：

```
a = ['a', 'b', 'c', 'd', 'e']

# 方式1：
for x in xrange(len(a)):
    print x, a[x]

# 方式2：
for index, item in enumerate(a):
    print index, item

# 执行结果：
0 a
1 b
2 c
3 d
4 e
```

> enumerate还可以接收第二个参数，用于指定索引起始值，如：

```
a = ['a', 'b', 'c', 'd', 'e']
start = 100
for index, item in enumerate(a, start):
    print index, item

# 执行结果:
100 a
101 b
102 c
103 d
104 e
```


## 切片 ##







## 参考
[hidden features of python](http://stackoverflow.com/questions/101268/hidden-features-of-python?rq=1)