## 统计字符数量之后，打印出现次数前10的字符

- 打印前十
- 考虑并列排名

```
read_me = '''first of all, i want make it clear that i can not claim undellllllrstddddddddddddanding this holy book in just a few weeks, and i would not dare comment on this sacred book, in addition, i don't think i can give you a full picture of the holy bible in just few words.i can not preach anything here. what i want to do here is to express ffffffffffffffffffffmy understanding by sharing two events described in this book. the fist story i want to share is abandoned tower of babel.according to the bibel,people use the same language to communicate with each other in ancient times.with the soaring vanity,they decided to build a heaven-reaching tower to show off their achievement, god knows, he change the human language into different kinds and make it difficult for people to communicate with each other,hence the failure of building tower of babel.this story tells people,never do things in selfishness, but make a life out of enternal glory.the other story,before jesus christ was crucified,he said, father,forgive them, for they know not what they do. with great love, he shouldered all the sins of people. what can we learn from this story?we live in this world thanks to the love of god, for this reanson, we should make our lives glorious to honor our god.finally,i want to sum up by saying that only if we put our lives in the eternal love of god,can we live a perfect life, and what you appealed is what god expected!'''
```

> 示例代码

```
#coding:utf-8

import sys
import json

read_me = '''first of all, i want make it clear that i can not claim undellllllrstddddddddddddanding this holy book in just a few weeks, and i would not dare comment on this sacred book, in addition, i don't think i can give you a full picture of the holy bible in just few words.i can not preach anything here. what i want to do here is to express ffffffffffffffffffffmy understanding by sharing two events described in this book. the fist story i want to share is abandoned tower of babel.according to the bibel,people use the same language to communicate with each other in ancient times.with the soaring vanity,they decided to build a heaven-reaching tower to show off their achievement, god knows, he change the human language into different kinds and make it difficult for people to communicate with each other,hence the failure of building tower of babel.this story tells people,never do things in selfishness, but make a life out of enternal glory.the other story,before jesus christ was crucified,he said, father,forgive them, for they know not what they do. with great love, he shouldered all the sins of people. what can we learn from this story?we live in this world thanks to the love of god, for this reanson, we should make our lives glorious to honor our god.finally,i want to sum up by saying that only if we put our lives in the eternal love of god,can we live a perfect life, and what you appealed is what god expected!'''

def simple_merge():
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
    
def main():
    old_ret = simple_merge()
    sorted_dict = sorted_dic(old_ret)
    res = merge_ranking(sorted_dict)
    print res
    
if __name__ == "__main__":
    main()
```

> 执行结果

```
[('No 1', [(' ', 247)]), ('No 2', [('e', 131)]), ('No 3', [('t', 103)]), ('No 4', [('o', 96)]), ('No 5', [('i', 86)]), ('No 6', [('a', 77), ('n', 77)]), ('No 7', [('h', 66)]), ('No 8', [('s', 58)]), ('No 9', [('d', 55), ('f', 55), ('l', 55), ('r', 55)]), ('No 10', [('c', 32), ('u', 32), ('w', 32)]), ('No 11', [('g', 25)]), ('No 12', [(',', 22)]), ('No 13', [('y', 20)]), ('No 14', [('b', 19), ('m', 19)]), ('No 15', [('p', 17)]), ('No 16', [('v', 14)]), ('No 17', [('k', 13)]), ('No 18', [('.', 10)]), ('No 19', [('j', 3)]), ('No 20', [('x', 2)]), ('No 21', [('!', 1), ("'", 1), ('-', 1), ('?', 1)])]
```

> 格式化输出

```
[
('No 1', [(' ', 247)]), 
('No 2', [('e', 131)]),
('No 3', [('t', 103)]),
('No 4', [('o', 96)]), 
('No 5', [('i', 86)]),
('No 6', [('a', 77), ('n', 77)]), 
('No 7', [('h', 66)]), 
('No 8', [('s', 58)]),
('No 9', [('d', 55), ('f', 55), ('l', 55), ('r', 55)]),
('No 10', [('c', 32), ('u', 32), ('w', 32)]), 
('No 11', [('g', 25)]), 
('No 12', [(',', 22)]),
('No 13', [('y', 20)]), 
('No 14', [('b', 19), ('m', 19)]), 
('No 15', [('p', 17)]), 
('No 16', [('v', 14)]), 
('No 17', [('k', 13)]), 
('No 18', [('.', 10)]), 
('No 19', [('j', 3)]), 
('No 20', [('x', 2)]), 
('No 21', [('!', 1), ("'", 1), ('-', 1), ('?', 1)])
]
```
