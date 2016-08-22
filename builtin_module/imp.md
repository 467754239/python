## imp

```
参考文章
https://docs.python.org/2/library/imp.html?highlight=imp#module-imp
http://blog.csdn.net/csujiangyu/article/details/45285897

imp.find_module(name, [path])
1. 如果path为空, 则按照sys.path路径搜索模块名, 返回三元组(file, pathname, description).
   file为刚打开的模块文件; pathname为模块的路径; description为imp.get_suffixes()返回的元组.
2. 如果模块为包,file返回None, pathname为包路径, description返回的type为PKG_DIRECTORY.
3. find_module不会处理层次结构的模块名(带’.’号的模块名module.name1.name2).
4. path必须是一个列表.
    
imp.load_module(name, file, pathname, description)
1. 加载一个被find_module找到的模块. 如果模块已经被加载, 等同于reload().    
2. 当模块是包或者不从文件加载时, file和pathname可以是None和”.    
3. 成功加载后返回一个模块对象,否则抛出 ImportError异常.    
4. 需要自己关闭file,最好用try…finally…    
```

> 示例1

```
import imp
fp, pathname, desc = imp.find_module('idc', ['/zhengys/jsonrpc/modules'])
module = imp.load_module('idc', fp, pathname, desc)
```

> 示例2

```
import os, imp
fp, pathname, desc = imp.find_module('os')
module = imp.load_module('os', fp, pathname, desc)
module.system('df -h')
```
