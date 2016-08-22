## subprocess

[subprocess doc](https://docs.python.org/2/library/subprocess.html?highlight=subprocess#module-subprocess)

```
#coding:utf-8

import os
import time
import signal
import logging
import subprocess


# 执行命令 
def execute_command(cmd, specific_user=None, timeout=300):
    """
    Run command and return the output
    cmd - the command to run    
    specific_user - execute user
    timeout - max seconds to wait for    
    """    
    execute_log = "/var/log/execute_command"
    
    if specific_user:    
        cmd = "su - %s -c '%s'" % (specific_user, cmd)    
    logging.debug("execute_command %s, timeout is %s." % (cmd, timeout))    
    log_fo = open(execute_log, "a")    
    ISOTIMEFORMAT='%Y-%m-%d %X'    
    log_fo.write("%s : execute_command %s, timeout is %s.\n" % (time.strftime(ISOTIMEFORMAT, time.localtime()), cmd, timeout))    
    log_fo.flush()    
    p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=log_fo.fileno(), shell=True, preexec_fn=os.setsid)    
    t_beginning = time.time()    
    seconds_passed = 0    
    while True:    
        if p.poll() is not None:    
            break    
        seconds_passed = time.time() - t_beginning    
        if timeout and seconds_passed > timeout:    
            os.killpg(p.pid, signal.SIGTERM)    
            logging.debug("execute_command %s timeout." % cmd)    
            log_fo.write("execute_command timeout.\n")    
            log_fo.close()    
            raise TimeoutError(cmd, timeout)    
        time.sleep(0.1)    
    logging.debug("execute_command %s finish, return code is %s." % (cmd, p.returncode))    
    log_fo.write("execute_command %s finish, return code is %s.\n" % (cmd, p.returncode))    
    log_fo.close()    
    return p.returncode
```
