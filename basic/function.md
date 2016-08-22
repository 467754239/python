## 参数的分类  
1. 位置参数
2. 关键字参数
3. 默认参数
4. 可变长参数(定义时)
    1. args元组方式位置参数
    2. kwargs字典方式关键字参数
5. 调用时
    1. \*\*dict -> 关键字参数传递，key作为关键字，value作为值.
    2. \*tuple -> 位置参数.

## 示例1 
```python
# 代码
def func(a, b, c=0, *args, **kwargs):
    print 'a', a
    print 'b', b
    print 'c', c
    print 'args', args
    print 'kwargs', kwargs

# 执行
args = ('cn', 'henan', '13xxxxxx')
dic = {'name' : 'zhengys', 'age' : 26, 'sex' : 'male'}
func('sengled', 'bj', '10', *args, **dic)

# 输出
a sengled
b bj
c 10
args ('cn', 'henan', '13xxxxxx')
kwargs {'age': 26, 'name': 'zhengys', 'sex': 'male'}
```

## 示例2
```python
# 代码
def A(*args, **kwargs):
    return B(*args, **kwargs)

def B(*args, **kwargs):
    print 'args=', args
    print 'kwargs=', kwargs

'''
# 函数A等价于
def A(*args, **kwargs):
    args = args
    kwargs = kwargs
    return B(*args, **kwargs)
'''

# 执行
args = ('zhengys', 'china')
kwargs = {'tel' :'132', 'age' : '26'}
A(*args, **kwargs)

# 输出
args= ('zhengys', 'china')
kwargs= {'age': '26', 'tel': '132'}
```

> 示例1代码  
> 是为了区分位置参数、关键字参数、任意数量的位置参数、任意数量的关键字参数.  
> 示例2代码  
> 是为了说明在函数A中调用函数B，函数B的参数就是接收的函数A的参数 这个时候函数B也要用\*args和\*\*kwargs

## 注意

```
位置或关键字参数应该在最前面，其中，没有默认值的应该在有默认值的参数前面
任意数量位置参数应该放在所有位置或关键字参数的后面
任意数量关键字参数应该放在任意数量位置参数的后面
任意数量位置参数和任意数量关键字参数只能在函数中定义一次
```
