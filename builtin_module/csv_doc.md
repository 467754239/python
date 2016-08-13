## csv

```python
#coding:utf-8

import csv
 
## 写入模式 
fd = open('cv_th.csv', 'a')
csv_writer = csv.writer(fd)
field_name = ['id', 'name', 'sex', 'age', 'address']

# 一次写入一行
row = [1, 'zhengys', 'boy', 27, 'henan']
csv_writer.writerow(row)

# 一次写入多行
rows = [[2, 'zhengyh', 'boy', 34, 'henan'],[3, 'qinheng', 'boy', 26, 'henan']]
csv_writer.writerows(rows)

fd.close()

## 读取模式
fd = open('cv_th.csv', 'r')
csv_reader = csv.reader(fd)
for line in csv_reader:
    print line
fd.close()
```

执行结果
```
['1', 'zhengys', 'boy', '27', 'henan']
['2', 'zhengyh', 'boy', '34', 'henan']
['3', 'qinheng', 'boy', '26', 'henan']
```
