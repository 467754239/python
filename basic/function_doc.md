## function
> 函数参数  
 
1. 位置参数
2. 关键字参数
3. 默认参数
4. 可变长参数(定义时)
    1. args元组方式位置参数
    2. kwargs字典方式关键字参数
5. 调用时
    1. **dict -> 关键字参数传递，key作为关键字，value作为值.
    2. *tuple -> 位置参数.

> 示例  

```python
def func(a, b, c=0, *args, **kwargs):
    print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kwargs)
```
