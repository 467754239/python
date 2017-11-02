# large log


## Python处理一个2.3G的日志文件的方式

```python
# 方式1：
with open('/tmp/test.log', 'rb') as f:
    for line in f:
        print line.readline()


# 方式2：        
import fileinput
for line in fileinput.input(['/tmp/test.log']):
    print


# 方式3：
def read_in_chunks(filePath, chunk_size=1024*1024):
    """
    Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1M
    You can set your own chunk size 
    """
    file_object = open(filePath)
    while True:
        chunk_data = file_object.read(chunk_size)
        if not chunk_data:
            break
        yield chunk_data


# 方式4：
def read_file(file):
    BLOCK_SIZE = 1024
    with open(file, 'rb') as f:
        while True:
            block = f.read(BLOCK_SIZE)
            if block:
                yield block
            else:
                return 
```

