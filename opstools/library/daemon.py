
import time
import os
import sys
import atexit
import os 
import signal

def writeData(signum, fram):
    with open('/tmp/data','a+') as fd:
        fd.write('asdfasa\n')


def term(signum, fram):
    #sys.exitfunc()
    raise SystemExit(
            u"Terminating on signal %(signum)r"
                % vars())

def writepid(name,pid):
    pidpath = os.path.join('/tmp','%s.pid'%name)
    with open(pidpath,'w') as fd:
        fd.write(str(pid))

def delpid(name):
    pidpath = os.path.join('/tmp',name+'.pid')
    os.remove(pidpath)

def run():
    while True:
        print '1time'
        time.sleep(1)

def daemon(name):
    try:
        pid = os.fork()
        if pid > 0:
           sys.exit(0)
    except OSError, e:
        print 'fork #1 fail', e
        sys.exit(1)
    os.chdir('/')
    os.setsid()
    os.setgid(99)
    os.setuid(99)
    os.umask(0)
    try:
        pid = os.fork()
        if pid > 0:
           writepid(name,pid)
           print 'daemon pid %d' % pid
           sys.exit(0)
    except OSError, e:
        print 'fork #2 fail', e
        sys.exit(1)
    nulldev = '/dev/null'
    stdin = file(nulldev, 'r')
    stdout = file(nulldev, 'a+', 0)
    stderr = file(nulldev, 'a+', 0)
    os.dup2(stdin.fileno(), sys.stdin.fileno())
    os.dup2(stdout.fileno(), sys.stdout.fileno())
    #os.dup2(stderr.fileno(), sys.stderr.fileno())
    atexit.register(delpid,name=name)
    signal.signal(signal.SIGHUP, writeData)
    signal.signal(signal.SIGTERM, term)
    return pid

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '-d':
        daemon('example-daemon')
    run()
