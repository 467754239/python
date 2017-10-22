## 简化版range实现

```
#coding: utf-8
#filename: zhengyscn.py


'''
如果手动实现简单版的range函数
'''


def rrange(*args):
    '''
    rrange(stop) -> list of integers
    rrange(start, stop[, step]) -> list of integers
    '''
    ret = []

    if len(args) == 1:
        start, stop, step = 0, args[0], 1
        ret = counter_range(start, stop, step)

    elif len(args) == 2:
        start, stop, step = args[0], args[1], 1
        ret = counter_range(start, stop, step)

    elif len(args) == 3:
        start, stop, step = args[0], args[1], args[2]
        ret = counter_range(start, stop, step)

    else:
        ret = "rrange expected at most 3 arguments, got %d" % len(args)

    return ret

def counter_range(start, stop, step):

    counter_ret = []
    while start < stop:
        counter_ret.append(start)
        start += step
    return counter_ret


if __name__ == '__main__':
    print rrange(10)
    print rrange(10, 21)
    print rrange(10, 21, 2)
```
