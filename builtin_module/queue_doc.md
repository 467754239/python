## Queue
> 

```python
#coidng:utf-8

import time
import Queue
import logging
import threading

FORMAT = '%(asctime)-15s %(threadName)5s %(levelname)s %(message)s '
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

class thread(threading.Thread):
    def __init__(self, name, q):
        threading.Thread.__init__(self)
        self.name = name
        self.q = q

    def run(self):
        if self.name == 'collect':
            self.collectLoop() 
        elif self.name == 'sendjson':
            self.sendloop()

    def collectLoop(self):
        for x in range(100):
            self.q.put(x)
            logging.debug('put %s', x)
            time.sleep(0.5)

    def sendloop(self):
        while True:
            if not self.q.empty():
                data = self.q.get()
                logging.debug('get %s', data)
            time.sleep(2)

def main():
    q = Queue.Queue(10)

    q1 = thread('collect', q)
    q1.start()

    time.sleep(1)

    q2 = thread('sendjson', q)
    q2.start()

    q1.join()
    q2.join()

if __name__ == '__main__':
    main()
```

> Queue类方法  
```
```
