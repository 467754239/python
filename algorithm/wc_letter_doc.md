## 统计字符数量之后，打印出现次数前10的字符

- 打印前十
- 考虑并列排名

```
read_me = '''first of all, i want make it clear that i can not claim undellllllrstddddddddddddanding this holy book in just a few weeks, and i would not dare comment on this sacred book, in addition, i don't think i can give you a full picture of the holy bible in just few words.i can not preach anything here. what i want to do here is to express ffffffffffffffffffffmy understanding by sharing two events described in this book. the fist story i want to share is abandoned tower of babel.according to the bibel,people use the same language to communicate with each other in ancient times.with the soaring vanity,they decided to build a heaven-reaching tower to show off their achievement, god knows, he change the human language into different kinds and make it difficult for people to communicate with each other,hence the failure of building tower of babel.this story tells people,never do things in selfishness, but make a life out of enternal glory.the other story,before jesus christ was crucified,he said, father,forgive them, for they know not what they do. with great love, he shouldered all the sins of people. what can we learn from this story?we live in this world thanks to the love of god, for this reanson, we should make our lives glorious to honor our god.finally,i want to sum up by saying that only if we put our lives in the eternal love of god,can we live a perfect life, and what you appealed is what god expected!'''
```

> 示例代码

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

> 执行结果

```python
[{'No 1': {' ': 247}}, {'No 2': {'e': 131}}, {'No 3': {'t': 103}}, {'No 4': {'o': 96}}, {'No 5': {'i': 86}}, {'No 6': {'a': 77, 'n': 77}}, {'No 7': {'h': 66}}, {'No 8': {'s': 58}}, {'No 9': {'r': 55, 'l': 55, 'd': 55, 'f': 55}}, {'No 10': {'c': 32, 'u': 32, 'w': 32}}]
```

> 格式化输出

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
