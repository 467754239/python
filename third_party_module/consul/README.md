## consul api

```
import consul
c = consul.Consul()

# 递归删除一个父级key下的所有key.
c.kv.delete('sengled/devops/', recurse=True)
```


---

## 参考资料
[python-consul latest](http://python-consul.readthedocs.io/en/latest/#)  