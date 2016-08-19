# -*- coding: utf-8 -*-
from __future__ import unicode_literals

list = [90, 8, 100, 203, 8, 3, 35, 67, 1000, 0, 789, 8, 90, 100, 789, 100, 204, 730]

# 冒泡排序1
def bubble_sort(list):
    length = len(list)
    print 'length:%s' % length

    # 第一级遍历
    for index in xrange(length):
        
        # 第二级遍历
        for j in xrange(1, length-index):
            if list[j-1] > list[j]:

                 # 交换两者数据，这里没用temp是因为python 特性元组。
                list[j-1], list[j] = list[j], list[j-1]
    return list

# 冒泡排序2
# 这种排序其实还可以稍微优化一下，添加一个标记，在排序已完成时，停止排序。
def bubble_sort_flag(list):
    length = len(list)
    print 'length:%s' % length

    # 标志位
    flag = True

    # 第一级遍历
    for index in xrange(length):
        
        # 第二级遍历
        for j in xrange(1, length-index):
            if list[j-1] > list[j]:

                 # 交换两者数据，这里没用temp是因为python 特性元组。
                list[j-1], list[j] = list[j], list[j-1]

                flag = False

    if flag:
        # 没有发生交换，直接返回list
        return list   

new_list = bubble_sort(list)
print new_list