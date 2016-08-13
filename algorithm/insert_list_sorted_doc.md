## 实现一个简单的插入排序

```
#coding:utf-8

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
        
	# 第一次插入
        if len(self.ret) == 0:  
            self.ret.append(num)
            
	# 第二次插入
        elif len(self.ret) == 1:    
            if num > self.ret[0]:    
                self.ret.append(num)    
            else:    
                self.ret.insert(0, num)
                
	# 第三次及第三次以后的任何插入
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
        action = raw_input('please input add or show or exit:')
        if action in self.menu:
            self.menu[action]()	# 实现switch的功能
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
