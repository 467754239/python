# 多进程、多线程、协程
- thraed  
- thraeding  
- os.fork  
- multiprocessing  
- gevent

## 原理 ##
```
# 核心
线程是"调度"的基本单位
进程是"资源管理"的基本单位

# 资源
内存、信号处理、文件描述符、进程锁、socket等

进程与资源通信、线程与cpu通信.
操作系统分配资源都进程，进程中的线程共享进程中的资源.
操作系统调度线程而非进程.
一个进程下的所有线程共享同一个地址空间资源.

# 地址空间资源
内存资源
文件描述符fd
共享代码
进程用户ID（UID）与进程组ID（PGID）


# 并发与并行的区别
单核也可以并发，但是单核不能并行，只有多核才能并行.


# 线程轻量
1. 内存占用开销
2. 上下文切换

用户态线程 协程 不参与内核的上下文切换
```

## thread ##
> thread模块已经被弃用  

```python
#coding:utf-8

import thread

def func(threadName):
    print 'This threadName is %s' % threadName

if __name__ == '__main__':
    thread.start_new(func, ('thread1', ))
    while True:
        pass
```


## threading ##

threading模块参数
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

join和setDaemon
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

示例1  

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

示例2  

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

示例3

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

## 协程 ##
概念性
```
协程不同于线程，线程是抢占式的调度，而协程是协同式的调度，协程需要自己做调度。

协程没有线程的安全问题，一个进程可以同时存在多个协程，但是只有一个协程是激活的，而且协程的激活和休眠又程序员通过编程来控制，
而不是操作系统控制的，

协程是用户空间线程，操作系统其存在一无所知，所以需要用户自己去调度，用来执行协程多任务非常合适。
```

简介
```
gevent is a coroutine-based Python networking library that uses greenlet to provide a high-level synchronous API on top of the libevent event loop.

#译:
gevent一个基于协程的Python网络库，依赖于libevent的event loop使用greenlet提供高级同步API。

gevent给了你线程,但是没有使用线程
```


## 参考资料
[Python 中的进程、线程、协程、同步、异步、回调](https://segmentfault.com/a/1190000001813992)  
[gevent官方文档](http://www.gevent.org/contents.html)  
[廖雪峰gevent](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001407503089986d175822da68d4d6685fbe849a0e0ca35000)