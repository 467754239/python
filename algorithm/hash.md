## FNV hash ##

[ FNV hash Docment](http://www.isthe.com/chongo/tech/comp/fnv/)

一个简单的示例
```
def fnvhash(string):
    ret = 97
    for i in string:
        ret = ret ^ ord(i) * 13
    return ret

fnvhash('zhengys4') % 4
```
