# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import os
import pty
import select

class selectFork(object):
    def __init__(self):
        self._setupPty()

    def _setupPty(self):
        (pid, master_fd)= pty.fork()
        self.stdout = master_fd
        self.stdin = master_fd
        self.stdout = master_fd
        if pid == 0:
            os.execv("/bin/bash",["/bin/bash","-l"])

    def read(self):
        rlist = [ self.stdout ]
        wlist = []
        xlist = []

        output = ""
        timeout = 0.5 

        while True:
            # select(rlist, wlist, xlist[, timeout]) -> (rlist, wlist, xlist)
            rlist, wlist, xlist = select.select(rlist, wlist, xlist, timeout)
            for r in rlist:
                tmp = os.read(self.stdout, 1024)
                output += tmp
                if tmp == "":
                    r = []
                    break

            if not len(rlist) and len(output):
                return output.split(os.linesep)
                break

    def write(self,cmd):
        cmd = cmd.strip() + os.linesep
        os.write(self.stdin, cmd)

def main():
    commands = '''
    ls
    uptime
    cat /etc/passwd
    df -h
    ''' 

    zt = selectFork()
    for cmd in commands.strip().split('\n'):
        zt.write(cmd)
        lines = zt.read()
        for line in lines:
            print line
   
if __name__=="__main__":
    main()