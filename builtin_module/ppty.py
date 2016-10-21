# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import os
import pty
import select
import time

class selectPty(object):
    def __init__(self):
        self._setupPty()

    def _setupPty(self):
        (pid, master_fd) = pty.fork()
        self.stdout = master_fd
        self.stdin = master_fd
        self.stderr = master_fd

        if pid == 0:
            os.execv("/bin/bash",["/bin/bash","-l"])

    def exec_command(self, cmd):
        cmd = cmd.strip() + os.linesep
        self.write(cmd)

    def read(self):
        rlist = [self.stdout]
        wlist = []
        xlist = []

        timeout = 0.5
        output =""

        while 1:
            rlist, wlist, xlist = select.select(rlist, wlist, xlist, timeout)
            for r in rlist:
                tmp = os.read(self.stdout, 1024)
                output += tmp
                if tmp == "":
                    r=[]
                    break
            if not len(rlist) and len(output):
                return output.split(os.linesep)

    def write(self, cmd):
        os.write(self.stdin, cmd)

def main():
    cmdList=["ls","uptime","df -h", 'cat /etc/passwd', 'dfs']
    zt = selectPty()
    for cmd in cmdList:
        zt.exec_command(cmd)
        lines=zt.read()
        for line in lines:
            print line
   
if __name__=="__main__":
    main()