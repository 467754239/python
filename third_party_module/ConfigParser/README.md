# ConfigParser

```python
import os
import ConfigParser

'''
模块介绍
https://docs.python.org/2/library/configparser.html

字典生成公式
info = [('name','zhengys'),('age', 26)]
dict(info) >>> {'age': 26, 'name': 'zhengys'}
'''

def parseConf(filename, section=''):
    # 1. 如果section为空 那么仅组合common下的kv数据 并以字典格式返回
    # 2. 如果section不为空 那么组合common以及对应section下的kv数据 并以字典格式返回
    config = ConfigParser.ConfigParser()
    config.read(filename)
    conf_items = dict(config.items("common")) if config.has_section("common") else {}
    
    if section and config.has_section(section):
        conf_items.update(config.items(section))
    return conf_items
    
if __name__ == "__main__":
    filename = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname('__file__'))), "conf/sengled.conf")
    conf1 = parseConf(filename)
    # 以字典的方式读取
    
    conf2 = parseConf(filename, "api")
```
