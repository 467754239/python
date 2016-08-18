# algorithm #

## 求一个list最大的两个值  ##
```
list = [1,2,3,2,12,3,1,3,21,2,2,3,4111,22,3333,444,111,4,5,777,65555,45,33,45]

max_val = list[0]

for x in list[1:]:
    if x > max_val:
        sec_val = max_val
        max_val = x
    else:
        pass
        
print max_val
print sec_val
```

## 实现插入排序 ##

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

## 统计字符数量之后，打印出现次数前10的字符  ##

> 打印前十  
> 考虑并列排名  

```python
#coding:utf-8

import sys
import json

read_me = '''first of all, i want make it clear that i can not claim undellllllrstddddddddddddanding this holy book in just a few weeks, and i would not dare comment on this sacred book, in addition, i don't think i can give you a full picture of the holy bible in just few words.i can not preach anything here. what i want to do here is to express ffffffffffffffffffffmy understanding by sharing two events described in this book. the fist story i want to share is abandoned tower of babel.according to the bibel,people use the same language to communicate with each other in ancient times.with the soaring vanity,they decided to build a heaven-reaching tower to show off their achievement, god knows, he change the human language into different kinds and make it difficult for people to communicate with each other,hence the failure of building tower of babel.this story tells people,never do things in selfishness, but make a life out of enternal glory.the other story,before jesus christ was crucified,he said, father,forgive them, for they know not what they do. with great love, he shouldered all the sins of people. what can we learn from this story?we live in this world thanks to the love of god, for this reanson, we should make our lives glorious to honor our god.finally,i want to sum up by saying that only if we put our lives in the eternal love of god,can we live a perfect life, and what you appealed is what god expected!'''

def merge_dic():
    res = {}
    for x in read_me:
        if not x:
            continue
        if x not in res:
            res[x] = 1
        else:
            res[x] = res[x] + 1
    return res

def sorted_dic(d={}):
    return sorted(d.items(), key=lambda x:x[1], reverse=True)

def merge_ranking(sorted_dict):
    c = 1
    ret = []
    tmp = []
    for index in range(len(sorted_dict)):
        if not tmp:
            ret.append(("No %d" % c, [sorted_dict[index]]))
            tmp.append(sorted_dict[index])
        else:
            if tmp[-1][1] != sorted_dict[index][1]:
                format_c = "No %d" % (int(ret[-1][0].split()[-1]) + 1)
                ret.append((format_c, [sorted_dict[index]]))
                tmp = []
                tmp.append(sorted_dict[index])
            else:
                ret[-1][1].append(sorted_dict[index])
        c += 1
    return ret

def format_result(data):
    # [{'No 1' : {' ':'247'}}]
    result = []
    for line in data:
        tmp = {}
        k = line[0]
        v = line[1]
        for l in v:
            tmp[l[0]] = l[1]
        result.append({k:tmp})
    return result
        
def main():
    old_ret = merge_dic()
    sorted_dict = sorted_dic(old_ret)
    res = merge_ranking(sorted_dict)
    result = format_result(res)
    return result[:10]

if __name__ == "__main__":
    print main()
```

```python
名次: No 1, 单词和次数: {' ': 247}
名次: No 2, 单词和次数: {'e': 131}
名次: No 3, 单词和次数: {'t': 103}
名次: No 4, 单词和次数: {'o': 96}
名次: No 5, 单词和次数: {'i': 86}
名次: No 6, 单词和次数: {'a': 77, 'n': 77}
名次: No 7, 单词和次数: {'h': 66}
名次: No 8, 单词和次数: {'s': 58}
名次: No 9, 单词和次数: {'r': 55, 'l': 55, 'f': 55, 'd': 55}
名次: No 10, 单词和次数: {'c': 32, 'u': 32, 'w': 32}
```