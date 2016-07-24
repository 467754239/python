## 函数式编程(lambda | filter | map | reduce | zip)

> lambda

```
俗称"匿名函数"
lambda与def定义的函数相比有以下几点不同
    1. 匿名函数不需要指定函数名字.
    2. 匿名函数都是一行代码完成 所以不能写复杂的函数.

示例1
func1 = lambda x:x * 2 
等价于
def func1(x):
    return x * 2
    
示例2
func2 = lambda x, y: x + y
等价于
def func2(x, y):
    return x + y
    
示例3
func3 = lambda x, y: (x+y, x*y)
等价于
def func3(x, y):
    return (x+y, x*y)
    
示例4
new_list = [('zhengys', 26), ('wshuai', 28), ('songxy', 25), ("wshuiping", 30)]
对new_list这个数组用第二个元素排序
new_ret = sorted(new_list, key=lambda x:x[1])
```	
