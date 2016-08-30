#!/usr/bin/env python2.7
#
#

import sys
from os import path
import os
import MySQLdb
DIRNAME = path.dirname(__file__)
OPSTOOLS_DIR = path.abspath(path.join(DIRNAME, '..'))
sys.path.append(OPSTOOLS_DIR)

from library.mysql import MySQLDConfig, getMyVariables
from optparse import OptionParser
from subprocess import Popen, PIPE

import time
import re

MYSQL_DATA_DIR = "/var/mysqlmanager/data"
MYSQL_CONF_DIR = "/var/mysqlmanager/cnfs"
MYSQL_BACK_DIR = "/var/mysqlmanager/backup"

REPLICATION_PASS = "123qwe"
REPLICATION_USER = "repl"

def opts():
    parser = OptionParser(usage="usage: %prog options")
    parser.add_option("-c", "--cmd", 
                      dest="cmd", 
                      action="store",
                      default="check",)
    parser.add_option("-n", "--name", 
                      dest="name", 
                      action="store",
                      default="mysqlinstance",)
    parser.add_option("-p", "--port", 
                      dest="port", 
                      action="store",
                      default="3306",)
    return parser.parse_args()


def readConfs():
    import glob
    confs = glob.glob(path.join(MYSQL_CONF_DIR,'*.cnf'))
    return [MySQLDConfig(c) for c in confs]

def checkPort(d, p):
    for m in d:
        if p == m.mysqld_vars['port']:
            return True
    return False

def _genDict(name, port):
    return {
        "pid-file": path.join(MYSQL_DATA_DIR, name,"%s.pid" % name ),
        "socket": "/tmp/%s.sock" % name,
        "port": port,
        "datadir": path.join(MYSQL_DATA_DIR, name),
        "log-error": path.join(MYSQL_DATA_DIR,name,"%s.log" % name),
    }

def mysql_install_db(cnf):
    p = Popen("mysql_install_db --defaults-file=%s"%cnf, stdout=PIPE, shell=True)
    stdout, stderr = p.communicate()
    return p.returncode

def run_mysql(cnf):
    cmd = "mysqld_safe --defaults-file=%s &" % cnf
    p = Popen(cmd, stdout=PIPE, shell=True)
    #stdout, stderr = p.communicate()
    time.sleep(5)
    return p.returncode

def setOwner(p, user):
    os.system("chown -R mysql:mysql %s" % p) 

def getCNF(name):
    return path.join(MYSQL_CONF_DIR, "%s.cnf" % name)

def setReplMaster(cur):
    sql = "GRANT REPLICATION SLAVE ON *.*  TO %s@'localhost'  IDENTIFIED BY '%s'" % (REPLICATION_USER, REPLICATION_PASS)
    cur.execute(sql)


def createInstance(name, port, dbtype="master", **kw):
    cnf = path.join(MYSQL_CONF_DIR, "%s.cnf" % name)
    datadir = path.join(MYSQL_DATA_DIR, name)
    exists_cnfs = readConfs()
    if checkPort(exists_cnfs, port):
        print >> sys.stderr, "Port exist"
        sys.exit(-1)
    if not path.exists(cnf):
        c = _genDict(name, port)
        c.update(kw)
        mc = MySQLDConfig(cnf, **c)
        mc.save()
    else:
        mc = MySQLDConfig(cnf)
    if not path.exists(datadir):
        mysql_install_db(cnf)
        setOwner(datadir, mc.mysqld_vars['user'])
        run_mysql(cnf)
        cur = connMySQLd(mc)
        setReplMaster(cur)

def connMySQLd(mc):
     host = '127.0.0.1'
     user = 'root'
     port = int(mc.mysqld_vars['port'])
     conn = MySQLdb.connect(host, port=port, user=user)
     cur = conn.cursor()
     return cur


def diffVariables(instance_name):
    cnf = getCNF(instance_name)
    if path.exists(cnf):
         mc = MySQLDConfig(cnf)
         cur = connMySQLd(mc)
         vars = getMyVariables(cur)
         for k,v in mc.mysqld_vars.items():
             k = k.replace('-','_')
             if k in vars and vars[k] != v:
                  print k, v, vars[k]

def setVariable(instance_name, variable, value):
    cnf = getCNF(instance_name)
    if path.exists(cnf):
         mc = MySQLDConfig(cnf)
         cur = connMySQLd(mc)
         cur.execute("set global %s = %s" % (variable, value))
         mc.set_var(variable, value)
         mc.save()

def findLogPos(s):
    """
    >>> findLogPos("CHANGE MASTER TO MASTER_LOG_FILE='mysql-bin.000006', MASTER_LOG_POS=106;")
    ('mysql-bin.000006', 106)
    """
    rlog = re.compile(r"MASTER_LOG_FILE='(\S+)',",re.IGNORECASE)
    rpos = re.compile(r"MASTER_LOG_POS=(\d+),?",re.IGNORECASE)
    log = rlog.search(s)
    pos = rpos.search(s)
    if log and pos:
        return log.group(1), int(pos.group(1))
    else:
        return (None, None)

def getBinlogPOS(f):
    with open(f) as fd:
        for l in fd:
            f,p = findLogPos(l)
            if f and p:
                return f,p

def runMySQLdump(cmd):
    p = Popen(cmd, stdout=PIPE, shell=True)
    stdout, stderr = p.communicate()
    return p.returncode

def backupMySQL(instance_name):
    cnf = getCNF(instance_name)
    if path.exists(cnf):
        mc = MySQLDConfig(cnf)
        import datetime
        now = datetime.datetime.now()
        timestamp = now.strftime('%Y-%m-%d-%H%M%S')
        backup_file = path.join(MYSQL_BACK_DIR, instance_name, timestamp+'.sql')
        _dir = path.dirname(backup_file)

        if not path.exists(_dir):
            os.makedirs(_dir)
        cmd = "mysqldump -A -x -F --master-data=1 --host=127.0.0.1 --user=root --port=%s > %s" % (mc.mysqld_vars['port'], backup_file)
        runMySQLdump(cmd)


def changeMaster(
        cur,
        host,
        port,
        user,
        mpass,
        mf,
        p):
    sql = """ CHANGE MASTER TO
                MASTER_HOST='%s',
                MASTER_PORT=%s,
                MASTER_USER='%s',
                MASTER_PASSWORD='%s',
                MASTER_LOG_FILE='%s',
                MASTER_LOG_POS=%s;""" % ( host,
                port,
                user,
                mpass,
                mf,
                p)
    cur.execute(sql)
    
def restoreMySQL(instance_name, instance_port, sqlfile, **kw):
    createInstance(instance_name, instance_port, **kw)
    cnf = getCNF(instance_name)
    if path.exists(cnf):
        mc = MySQLDConfig(cnf)
        cur = connMySQLd(mc)
        cmd = "mysql -h 127.0.0.1 -P %s -u root < %s" % (
            mc.mysqld_vars['port'],
            sqlfile
        )
        f, p = getBinlogPOS(sqlfile)
        runMySQLdump(cmd)
        changeMaster(cur,
            host=kw['master-host'],
            port=kw['master-port'],
            user=REPLICATION_USER,
            mpass=REPLICATION_PASS,
            mf=f,
            p = p
            )

def _init():
    if not path.exists(MYSQL_DATA_DIR):
        os.makedirs(MYSQL_DATA_DIR)
    if not path.exists(MYSQL_CONF_DIR):
        os.makedirs(MYSQL_CONF_DIR)
    if not path.exists(MYSQL_BACK_DIR):
        os.makedirs(MYSQL_BACK_DIR)

def main():
    _init()
    opt, args = opts()
    instance_name = opt.name
    instance_port = opt.port
    command = opt.cmd
    if command == "create":
        if not args:
            createInstance(instance_name, instance_port)
        else:
            dbtype = args[0]
            serverid = args[1]
            mysqld_options = {'server-id':serverid}
            if dbtype == 'master':
                mysqld_options['log-bin']='mysql-bin'
            elif dbtype == 'slave':
                master_host = args[2]
                master_port = args[3]
                mysqld_options['master-host'] =master_host
                mysqld_options['master-port'] = master_port
                mysqld_options['master-user'] = REPLICATION_USER
                mysqld_options['master-password'] = REPLICATION_PASS
                mysqld_options['skip-slave-start'] = None
                mysqld_options['replicate-ignore-db'] = 'mysql'
                mysqld_options['read-only'] = None
            createInstance(
                instance_name, 
                instance_port,
                dbtype=dbtype,
                **mysqld_options
                )
    elif command == "check":
        diffVariables(instance_name)
    elif command == "adjust":
        variable = args[0]
        value = args[1]
        setVariable(instance_name, variable, value)
    elif command == "backup":
        backupMySQL(instance_name)
    elif command == "restore":
        serverid = args[0]
        mhost = args[1]
        mport = args[2]
        sqlfile = args[3]
        mysqld_options = {
            "master-host":mhost,
            "master-port":mport,
            "server-id":serverid,
            "skip-slave-start":None,
        }
        restoreMySQL(instance_name, instance_port, sqlfile,**mysqld_options)

if __name__ == '__main__':
    main()
