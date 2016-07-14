## os._exit
```
>>> os._exit?
_exit(status)
Exit to the system with specified status, without normal exit processing.
译:
退出系统指定的状态，没有正常退出处理.

os._exit()类似于sys.exit()
但它不执行任何的清除工作(例如刷新缓冲区)，所以os._exit()尤其适用于退出子进程.
如果程序使用sys.exit()，操作系统会回收父进程或其它子进程可能仍然需要的资源。
传给os._exit()函数的参数必须是进程的退出状态。退出状态为0，表示正常终止。
```

