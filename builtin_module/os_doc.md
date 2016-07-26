## os ##
os.fork
```
>>> os.fork?
fork() -> pid
Fork a child process.
Return 0 to child process and PID of child to parent process.
Fork一个子进程.
如果pid是0表示是父进程对应的子进程.

```

os.wait
```
>>> os.wait?
wait() -> (pid, status)
Wait for completion of a child process.

等待一个子进程完成.
```

os.waitpid

```
>>> os.waitpid?
waitpid(pid, options) -> (pid, status)
Wait for completion of a given child process.

等待一个给定的子进程完成.
```

os.\_exit

```
>>> os._exit?
_exit(status)
Exit to the system with specified status, without normal exit processing.

退出系统指定的状态，没有正常退出处理.
os._exit()类似于sys.exit()
但os._exit()不执行任何的清除工作(例如刷新缓冲区)，所以os._exit()尤其适用于退出子进程.
如果程序使用sys.exit()，操作系统会回收父进程或其它子进程可能仍然需要的资源。
传给os._exit()函数的参数必须是进程的退出状态。退出状态为0，表示正常终止。
```
