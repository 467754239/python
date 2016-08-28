#coding:utf-8

L = ['ab', 'abc', 'cc', 'ac', 'cc', 'ba', 'abc']

'''
前提：不使用python的内置去重方法.
1. 求出列表中哪些元素出现2次及2次以上.
'''

ret = []
for item in L:
    if L.count(item) >= 2:
        ret.append(item)
print ret
