## 列表推倒式
> 语法  
> variable = [ out_exp for out_exp in input_list if out_exp == 2 ]

```
示例1：
>>> multiples = [i for i in range(30) if i % 3 is 0]

示例2:
>>> squared = [x**2 for x in range(10)]
```

## 字典推倒式
> 语法  
> variable = { k:v for k, v in dict.items() }

```
示例1:
>>> names = {'name' : 'zhengys', 'age' : 25, 'address' : 'bj', 'tel' : '13260071987'}

示例2:
>>> names = {'name' : 'zhengys', 'age' : 25, 'address' : 'bj', 'tel' : '13260071987'}

示例3:
>>> mcase = {'a': 10, 'b': 34, 'A': 7, 'Z': 3}
>>> mcase_frequency = {
	k.lower(): mcase.get(k.lower(), 0) + mcase.get(k.upper(), 0)
	for k in mcase.keys()
>>> mcase_frequency == {'a': 17, 'z': 3, 'b': 34} 
```


## 集合推倒式
> 语法  
> variable = { out_exp for out_exp in input_list if out_exp == 2 }

```
示例1:
>>> squared = {x**2 for x in [1, 1, 2]}
>>> print squared
{1, 4}
```
