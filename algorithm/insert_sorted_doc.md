## 实现插入排序

> 示例代码

```python
#coding:utf-8

import sys
import logging

class SimpleInsertSort(object):
    def __init__(self):
        self.menu = {"add" : self.add, "show" : self.show, "exit" : self.exit}
        self.ret = []

    def add(self):
        try:
            num = input('please input a number: ')
            logging.debug("input number : %s" % num)
        except NameError as e:
            logging.error("you must a number, %s" % e)
            return

        # 1 insert 
        if len(self.ret) == 0:  
            self.ret.append(num)

        # 2 insert
        elif len(self.ret) == 1:    
            if num > self.ret[0]:    
                self.ret.append(num)    
            else:    
                self.ret.insert(0, num)

        # 3+ insert
        elif len(self.ret) >= 2:    
            if num < self.ret[0]:    
                self.ret.insert(0, num)   
            elif num > self.ret[-1]:    
                self.ret.append(num)
            for index in range(len(self.ret)):        
                if num > self.ret[index] and num < self.ret[index+1]:   
                    self.ret.insert(index+1, num)

    def flush_db(self):
        # 可实现持久化存储
        pass

    def load_db(self):
        # 加载到内存中
        pass

    def show(self):
        logging.debug(self.ret)

    def exit(self):
        self.flush_db()
        sys.exit(0)

    def process(self):
        self.load_db()
        action = raw_input('please input add or show or exit: ')
        if action in self.menu:
            self.menu[action]() # 实现switch的功能
        else:
            logging.error('input error, KeyError')

    def run(self):
        while True:
            self.process()

if __name__ == "__main__":
    FORMAT = '%(asctime)-15s %(levelname)s %(message)s '
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    sis = SimpleInsertSort()
    sis.run()
```

> 执行代码输出结果

```python
$ python th02.py 
please input add or show or exit: show
2016-08-13 15:21:52,937 DEBUG [] 
please input add or show or exit: add
please input a number: 7
2016-08-13 15:22:04,521 DEBUG input number : 7 
please input add or show or exit: show
2016-08-13 15:22:07,816 DEBUG [7] 
please input add or show or exit: 10
2016-08-13 15:22:10,355 ERROR input error, KeyError 
please input add or show or exit: add
please input a number: 10
2016-08-13 15:22:16,658 DEBUG input number : 10 
please input add or show or exit: show
2016-08-13 15:22:17,929 DEBUG [7, 10] 
please input add or show or exit: add
please input a number: 8
2016-08-13 15:22:24,634 DEBUG input number : 8 
please input add or show or exit: show
2016-08-13 15:22:25,534 DEBUG [7, 8, 10] 
please input add or show or exit: add
please input a number: -1
2016-08-13 15:22:36,181 DEBUG input number : -1 
please input add or show or exit: show
2016-08-13 15:22:40,166 DEBUG [-1, 7, 8, 10] 
please input add or show or exit: exit
```
