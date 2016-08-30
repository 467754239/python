#!/usr/bin/env python

import MySQLdb
import dns.tsigkeyring
import dns.query
import dns.update
import dns.rdatatype
import dns.rdata
import dns.rdataclass

key = "mQx7YHOWLzEDXy2HXwhAvM70wC1ks330ZQontYAXV5qv3TZxTH2QZBzOxJ/WtWpPgH7mkpRtABb7UNLg5+HpWw=="

keyring = dns.tsigkeyring.from_text({
    'example.net':key
})
keys = [
"Slave_IO_State",
"Master_Host",
"Master_User",
"Master_Port",
"Connect_Retry",
"Master_Log_File",
"Read_Master_Log_Pos",
"Relay_Log_File",
"Relay_Log_Pos",
"Relay_Master_Log_File",
"Slave_IO_Running",
"Slave_SQL_Running",
"Replicate_Do_DB",
"Replicate_Ignore_DB",
"Replicate_Do_Table",
"Replicate_Ignore_Table",
"Replicate_Wild_Do_Table",
"Replicate_Wild_Ignore_Table",
"Last_Errno",
"Last_Error",
"Skip_Counter",
"Exec_Master_Log_Pos",
"Relay_Log_Space",
"Until_Condition",
"Until_Log_File",
"Until_Log_Pos",
"Master_SSL_Allowed",
"Master_SSL_CA_File",
"Master_SSL_CA_Path",
"Master_SSL_Cert",
"Master_SSL_Cipher",
"Master_SSL_Key",
"Seconds_Behind_Master",
"Master_SSL_Verify_Server_Cert",
"Last_IO_Errno",
"Last_IO_Error",
"Last_SQL_Errno",
"Last_SQL_Error",
]


conf = {
   'master':'127.0.0.1:3306',
   'slaves':[
       '127.0.0.1:3307',
       '127.0.0.1:3308',
       '127.0.0.1:3309',
       '127.0.0.1:3310',
    ]
}


def checkSlaveStatus(host,port):
    try:
        conn = MySQLdb.connect(host=host,port=port, user='root',connect_timeout=1)
    except Exception, e:
        print e
        return False 
    cur = conn.cursor()
    cur.execute('show slave status;')
    data = cur.fetchone()
    status_dict = dict(zip(keys,data))
    if status_dict['Slave_IO_Running'].lower() == 'no' or status_dict['Slave_SQL_Running'].lower() == 'no':
        return False
    if status_dict['Seconds_Behind_Master'] > 2:
        return False
    return True

def parserConf(s):
    host, port = s.split(':')
    return (host, int(port))


def updatens(zone, name, dlist):
    up = dns.update.Update(zone,keyring=keyring)
    ttl = 60
    rdata_list = [dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.A,i) for i in dlist]
    rdata_set = dns.rdataset.from_rdata_list(ttl,rdata_list)
    up.replace(name, rdata_set)
    q = dns.query.tcp(up, '127.0.0.1')
    print q

def main():
    slaves = conf['slaves']
    alive = []
    for s in slaves:
        h, p = parserConf(s)
        if checkSlaveStatus(h,p):
            alive.append(h)
    if float(len(alive))/float(len(slaves)) > 0.6:
       updatens('example.net','s.db',alive)

if __name__ == '__main__':
    main()

