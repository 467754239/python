# -*- coding: utf-8 -*-
from __future__ import unicode_literals

Python多线程中如果某个线程遇到异常没有捕捉处理，那么这个线程就将被阻塞无法继续后续的动作.
Python信号处理在子线程有问题。

Python多线程中 有一个线程调用subprocess模块执行一个命令，比如启动一个服务，
当主线程被kill -9后再启动 发现启动的那个服务进程也不在线了。
