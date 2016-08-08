## 实现switch功能

```
def add(*args):
    return sum(args)

def sub():
    print 'sub func'

def mul():
    print 'mul func'

def div():
    print 'div func'

switch = {
        'add' : add,
        'sub' : sub,
        'mul' : mul,
        'div' : div,
    }

def run(oper, *args, **kwargs):
    return switch[oper](*args)

if __name__ == '__main__':
    print run('add', 2, 3)
```
