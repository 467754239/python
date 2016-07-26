## 上下文管理器 ##
[`Context Manager Types`](https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers)

语法
```
with context_expr [as var]:
    with_suite
    
context_expr是支持上下文管理协议的对象，也就是上下文管理器对象，负责维护上下文环境
as var是一个可选部分，通过变量方式保存上下文管理器对象
with_suite就是需要放在上下文环境中执行的语句块
```

功能
```
1. 代码块执行前的准备动作, 调用对象的__enter__()方法.
2. 代码块执行后的收拾动作, 调用对象的__exit__()方法.
```

应用场景
```
保存和恢复各种全局状态,锁定和释放资源,关闭打开的文件
```

示例1
> Python 2.5+中内置的上下文管理器，用于对文件的读写操作

```
with open('filename.txt', 'r') as fd:
    fd.read()
```

示例2
```
# coding
class fileopen(object):
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.fd = None
        
    def __enter__(self):
        self.fd = open(self.filename, self.mode)
        return self.fd
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.fd.close()

# execute cdoing
with fileopen('/tmp/nihao.txt', 'w') as fd_write:
    fd_write.write('123456')
```
