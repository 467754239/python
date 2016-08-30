#coding:utf-8
from __future__ import unicode_literals

list = [100, 104, 103, 200, 10, 1, 900, 100002, 9090932, 200, 100, 1, 0, 90]

def quick(list):
    if len(list) <= 1:
        return list

    left, right, middle = [], [], []

    for x in list:
        if x < list[0]:
            left.append(x)
        elif x > list[0]:
            right.append(x)
        else:
            middle.append(x)

    left = quick(left)
    right = quick(right)
    return left + middle + right

print quick(list)