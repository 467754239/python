#!/usr/bin/env python

import urllib, urllib2
import json
import os 
CURR_DIR=os.path.abspath(os.path.dirname(__file__))
HOST_CONF_DIR=os.path.join(CURR_DIR,'hosts')
CACHE_FILE='/var/tmp/api-cache.json'

HOST_TMP="""define host {
        use                     linux-server
        host_name              	%(hostname)s
        alias                   %(hostname)s
        address                 %(ipaddr)s
    	contact_groups		admins
}
"""
HOSTGROUP_TMP="""define hostgroup{
	hostgroup_name		%(hostgroup)s
	alias			%(hostgroup)s
	members			%(members)s
}
"""

def getHosts():
    url = "http://localhost:80/api/gethosts.json"
    try:
        data = urllib2.urlopen(url).read()
        writeFile(CACHE_FILE, data)
    except:
        data = open(CACHE_FILE,'r').read()
    return json.loads(data)

def initDir():
    if not os.path.exists(HOST_CONF_DIR):
        os.mkdir(HOST_CONF_DIR)

def writeFile(f,s):
    with open(f,'w') as fd:
        fd.write(s)

def genNagiosHost(hostdata):
    initDir()
    fp_hostconf = os.path.join(HOST_CONF_DIR,'hosts.cfg')
    fp_hostgroupconf = os.path.join(HOST_CONF_DIR,'hostgroups.cfg')
    hostconf = ""
    hostgroupconf = ""
    for hg in hostdata:
        members = []
        for h in hg['members']:
            hostconf += HOST_TMP % h
            members.append(h['hostname'])
        print members
        hostgroupconf += HOSTGROUP_TMP % {'hostgroup':hg['hostgroup'],'members':','.join(members)}
    writeFile(fp_hostconf,hostconf)
    writeFile(fp_hostgroupconf,hostgroupconf)

def main():
    result = getHosts()
    print result
    if result['status'] == 0:
        print genNagiosHost(result['data'])
    else:
        print 'Err: %s' % result['message']

if __name__=="__main__":
    main()
