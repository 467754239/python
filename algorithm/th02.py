# -*- coding: utf-8 -*-
from __future__ import unicode_literals


list = [90, 8, 100, 203, 8, 3, 35, 67, 1000, 0, 789, 8, 90, 100, 789, 100, 204, 730]


def quick(list):
    if len(list) <= 1:
        return list
    left, middle, right =[], [], []
    i = list[0]

    for x in list:
        if x < i:
            left.append(x)
        elif x > i:
            right.append(x)
        else:
            middle.append(x)

    left = quick(left)
    right = quick(right)

    return left + middle + right

print quick(list)