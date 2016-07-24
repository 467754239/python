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

> filter

```
filter(function or None, sequence) -> list, tuple, or string
返回值是可能是列表、元组或字符串
filter接收两个参数
    参数1：函数或者None(函数的返回值只能是True或False)
    参数2：序列(列表、元组、字典等)
类似于对序列sequence遍历 遍历的每一个元素分别应用在函数上 如果函数返回True就保留 如果返回False就过来.
    
实例1
>>> filter(lambda x:x.islower(), ['zhengys', 'wshuai', '26', '13260071987'])
['zhengys', 'wshuai']
- 对列表进行遍历 过虑掉不是以小写字母组成的元素.

实例2
>>> filter(lambda x:x%2, range(0, 10, 1))
[1, 3, 5, 7, 9]
- 对列表进行遍历 过虑掉能够被2整除的(if 0为False).

实例3
>>> filter(None, range(0, 10, 1))
[1, 2, 3, 4, 5, 6, 7, 8, 9]
- function是None的情况 直接返回后面的序列
```

> map  

```
map(function, sequence[, sequence, ...]) -> list
返回值为列表
map接收两个参数
    参数1：函数
    参数2：序列1, 序列2, 序列3, ......
***注意事项 ***
    1. 函数接受参数的个数应该和sequence的个数保持一致；
    2. 返回值list中元素的个数应该和每个sequence序列元素的个数一致, 否则抛出异常.

实例1
>>> map(lambda x : x * 2, range(0, 5, 1))
[0, 2, 4, 6, 8]
- sequence为[0, 1, 2, 3, 4]5个元素 那么map执行的结果列表也必须有5个元素
- sequence只有一个 那么前面的函数只能接收一个参数.

实例2
>>> map(lambda x, y: x + y, range(0, 5, 1), range(10, 15, 1))
[10, 12, 14, 16, 18]

实例3
> map(lambda x,y,z:x+y+z, range(1, 3), range(3, 5), range(5, 7))
> 1 + 3 + 5 = 9
> 2 + 4 + 6 = 12
return [9, 12]
```

> reduce

```
reduce(function, sequence[, initial]) -> value
返回值为就是一个值 这个值就是对sequence的计算结果.

计算步骤为
1. 第1个结果=function(sequence[0], sequence[1])
2. 第2个结果=function(第1个结果, sequence[2])
3. 返回最有一个结算的值
4. 如果有initial，则先调用function(initial, sequence[0])
5. sequence只有一个元素时，返回该元素，为空时抛出异常.
如
reduce(lambda x,y:x+y, range(3), 99)
99 + 0 => 99 + 1 => 100 + 2 => 102 返回102
注:实际使用中内建函数sum来完成这个累加更合适 如这里等价于sum(range(3), 99)

示例1：
>>> reduce(lambda x, y: x+y, [1, 2, 3, 4, 5])       ---> ((((1+2)+3)+4)+5)
15
- reduce就是一个合并的过程.
```

> zip

```
zip(seq1 [, seq2 [...]]) -> [(seq1[0], seq2[0] ...), (...)]

示例1
>>> zip(['zhengys', 26, 'china'], ['wshuai', 28, 'china'])
[('zhengys', 'wshuai'), (26, 28), ('china', 'china')]
```


