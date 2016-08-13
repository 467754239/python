## 实现插入排序

```
#coding:utf-8

'''
实现一个简单的插入排序.
'''

import sys
import logging

class SimpleInsertSort(object):
    def __init__(self):
        self.menu = {"add" : self.add, "show" : self.show, "exit" : self.exit}
        self.ret = []
        
    def add(self):
        try:
            num = input('please input a number:')
            logging.debug("input number : %s" % num)
        except NameError as e:
            logging.error("you must a number, %s" % e)
            return
        
        if len(self.ret) == 0:  
            self.ret.append(num)
            
        elif len(self.ret) == 1:    
            if num > self.ret[0]:    
                self.ret.append(num)    
            else:    
                self.ret.insert(0, num)
                
        elif len(self.ret) >= 2:    
            if num < self.ret[0]:    
                self.ret.insert(0, num)   
            elif num > self.ret[-1]:    
                self.ret.append(num)
            for index in range(len(self.ret)):        
                if num > self.ret[index] and num < self.ret[index+1]:   
                    self.ret.insert(index+1, num)
                    
    def flush_db(self):
        pass
        
    def load_db(self):
        pass
                    
    def show(self):
        logging.debug(self.ret)
        
    def exit(self):
        self.flush_db()
        sys.exit(0)
        
    def process(self):
        self.load_db()
        action = raw_input('please input add or show or exit:')
        if action in self.menu:
            self.menu[action]()
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
