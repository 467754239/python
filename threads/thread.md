
## thread模块已经被弃用
> 执行代码

```
#coding:utf-8

import thread

def func(threadName):
    print 'This threadName is %s' % threadName

if __name__ == '__main__':
    thread.start_new(func, ('thread1', ))
    while True:
        pass
```
