
## threading 多线程示例1 
> 执行代码

```python
# coding:utf-8

import time
import threading

class Th(threading.Thread):
    def __init__(self, threadName):
        threading.Thread.__init__(self)
        self.threadName = threadName

    def run(self):
        print 'This threadName is %s' % self.threadName
        time.sleep(1)
        print 'child thread %s is over' % self.threadName

if __name__ == '__main__':
    thread1 = Th('thread1')
    thread1.start()
    thread1.join()  # 自动执行Th类下的run方法
    print 'main thread is over'
```
> 执行结果

```
This threadName is thread1
child thread thread1 is over
main thread is over
```

## threading 多线程示例2
> 执行代码   

```python
# coding:utf-8

import threading

def func(num):
    print 'func is start.'
    print range(num)
    print 'func is over.'

if __name__ == '__main__':
    thread1 = threading.Thread(target=func, name='thread1', args=(10,))
    thread1.start()
    thread1.join()
    print 'main thread is over'
```
> 执行结果  

```
func is start.
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
func is over.
main thread is over
```


## threading 多线程示例3
> 执行代码

```python
# coding:utf-8

import threading

class Th(object):
    def __init__(self):
	pass

    def process(self, N):
        print 'Th is start.'
        print range(N)
        print 'Th is end.'

if __name__ == '__main__':
    th = Th()
    thread1 = threading.Thread(target=th.process, name='th_process', args=(10,))
    thread1.start()
    thread1.join()
    print 'main thread is over'
```
> 执行结果

```
Th is start.
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
Th is end.
main thread is over
```
- - -
## threading模块介绍

> threading.Thread

```
threading.Thread(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None)

A class that represents a thread of control.
This class can be safely subclassed in a limited fashion.
译:
一个类代表一个线程控制
这个类可以安全地以有限的方式从它派生出子类

类构造函数有以下参数:
group       # None
target      # 一个可调用的对象来调用对象的run()方法, 默认是None.
name        # 线程名字.默认情况下，构造一个唯一名称"Thread-N"(N是一个小的十进制数).
args        # target调用的元组参数,默认是().
kwargs      # target调用的字典参数,默认是{}.
```

## join和setDaemon
```
# setDaemon
setDeamon(True)
设置此线程是否被主线程守护回收。
默认False不回收，需要在start方法前调用；
设为True相当于向主线程中注册守护，主线程结束时会将其一并回收.
 
# join
设置主线程是否同步阻塞自己来等待子线程执行完毕。如果不设置的话则主进程会继续执行自己的，
在结束时根据 setDaemon 有无注册为守护模式的子进程，有的话将其回收，没有的话就结束自己，某些子线程可以仍在执行
```
