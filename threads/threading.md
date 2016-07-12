
## threading 多线程示例1 
> 执行代码

```
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

```
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

```
# coding:utf-8

import threading

class Th(object):
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

参数解释:

```

