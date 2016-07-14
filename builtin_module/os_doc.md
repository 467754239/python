## builtin_module
> os.wait() | os.waitpid(pid, options)

```
>>> os.wait?
wait() -> (pid, status)
Wait for completion of a child process.
译:
return (pid, status)
等待一个子进程完成.

>>> os.waitpid?
waitpid(pid, options) -> (pid, status)

Wait for completion of a given child process.
译:
return (pid, status)
等待一个给定的子进程完成.
```

> os.fork()

```
>>> os.fork?
fork() -> pid
Fork a child process.
Return 0 to child process and PID of child to parent process.
译:
return pid
Fork一个子进程.
如果pid是0表示是父进程对应的子进程.
```