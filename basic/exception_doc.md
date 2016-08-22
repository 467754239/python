## except异常 ##

```
try:
    f = open('/etc/passwd')
    file_content = f.read()
    print file_content
except IOError as e:
    print e
    print e.args
    print e.errno
    print e.filename
    print e.message
except Exception as e:
    # 捕获全部异常
    print e
else:
    # 没有发生异常时执行此处代码.
    pass
finally:
    # 无论异常是否发生都会执行此处代码.
    if 'f' in locals:
        f.close()
    print 'end'
    
print 'ok'
```
