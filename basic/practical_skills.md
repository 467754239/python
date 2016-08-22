Python 实用技巧
======
- enumerate
- 条件赋值
- 变量值交换
- list切片
- dict的get方法



## enumerate ##
语法及翻译
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


## 条件赋值 ##
```python
a = 0
ret = True if a == 0 else False
print ret

# 执行输出
True
```


## 变量值交换 ##
```
a = 3
b = 5
print a, b
a, b = b, a
print a, b
```

## list切片 ##
> slice(start, stop[, step])

```
l = range(1, 11)

# 列表所有元素
> print l
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 列表切割并指定步长为2.
> print l[::2]
[1, 3, 5, 7, 9]

# 反转列表.
> print l[::-1]
[10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
```


## dict的get方法 ##
语法及翻译
```
D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.

#译
如果k在字典D中，return D[k]，否则d. d的默认值是None.
```

用法示例1
```
d = {'name':'zhengys', 'age':26, 'addr':'cn'}

print 'd:', d
print 'name:', d['name']

try:
    print d['tel']  # key not in d, raise KeyError.
except KeyError as e:
    print 'tel error'

print 'tel:', d.get('tel', '1326007198x')
print 'd:', d

# 执行结果
d: {u'age': 26, u'name': u'zhengys', u'addr': u'cn'}
name: zhengys
tel error
tel: 1326007198x
d: {u'age': 26, u'name': u'zhengys', u'addr': u'cn'}
```

用法示例2
> 统计日志文件中每个ip出现的次数

```
def func1(logfile):     # 认为这种方式更巧妙.
    d = {}
    with open(logfile, 'r') as f:
        for line in f:
            ip = line.split()[0]
            d[ip] = d.get(ip, 0) + 1
    return d

def func2(logfile):
    d = {}
    with open(logfile, 'r') as f:
        for line in f:
            ip = line.split()[0]
            if ip not in d:
                d[ip] = 1
            else:
                d[ip] = d[ip] + 1
    return d

if __name__ == '__main__':
    logfile = 'access-8000.log'
    func1(logfile)
    func2(logfile)

# 执行结果
{'93.174.93.136': 1, '54.222.132.12': 1, '198.211.17.155': 1, '54.222.138.168': 2, '219.232.105.110': 29, '163.172.173.181': 1}
{'93.174.93.136': 1, '54.222.132.12': 1, '198.211.17.155': 1, '54.222.138.168': 2, '219.232.105.110': 29, '163.172.173.181': 1}
```











## 参考
[hidden features of python](http://stackoverflow.com/questions/101268/hidden-features-of-python?rq=1)