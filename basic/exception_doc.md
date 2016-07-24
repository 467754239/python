## except异常

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
    print e
finally:
    if 'f' in locals:
        f.close()
    print 'end'
    
print 'ok'
```
