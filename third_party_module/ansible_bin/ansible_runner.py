# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys
import argparse
import logging

from ansible.runner import Runner

import update_inventory
import threading
import config
from sendMail import send_mail

'''
export ANSIBLE_HOST_KEY_CHECKING=False
os.environ['ANSIBLE_HOST_KEY_CHECKING'] = "False"
'''

def Action(results, pattern, ip):
    conf = reload(config)
    threshold = conf.threshold
    mailto_list = ['zys@sengled.com'] 

    for line in results.split('\n'):
        if '/tmp' in line:
            use_precent = int( line.split()[4].rstrip('%') )
            if use_precent > threshold:
                alarm_content = 'asgname: {0} \t\t ip: {1} \t\t /tmp alarm {2}%'.format(pattern, ip, use_precent)
                if send_mail(mailto_list, "alarm", alarm_content):  
                    logging.info( "发送成功"  )
                else:  
                    logging.info( "发送失败" )


def output_format(results, module_args, pattern, debug):
    if debug.lower() == 'true':
        print results
        print '\n'

    # execute sucessful
    for ip, val in results['contacted'].items():
        print pattern, ip
        try:
            print 'interval: ', val['delta']
            if val['rc'] == 0:
                result_ok = val['stdout']
                if 'df' in module_args:
                    Action(result_ok, pattern, ip)
                print result_ok
            else:
                print val['stderr']
        except Exception as e:
            print val
        print ''

    # execute failed
    for ip, val in results['dark'].items():
        print pattern, ip
        print val['msg']
        print ''


def exec_cmd( module_name, module_args, pattern, forks, debug, remote_port, region ):

    results = Runner(
                    module_name = module_name,
                    module_args = module_args,
                    pattern = pattern,
                    remote_user = 'ec2-user',
                    remote_port = remote_port,
                    sudo = True,
                    private_key_file = '/home/ec2-user/.ssh/awscn_sengled_release.pem'.replace('cn', region), 
                    host_list = os.path.join( os.path.dirname( os.path.abspath(__file__) ), 'hosts'), 
                    forks = forks,
                    ).run()

    return output_format(results, module_args, pattern, debug)

def get_inventory():
    asg_name = []
    with open(os.path.join( os.path.dirname( os.path.abspath(__file__) ), 'hosts'), 'r') as f:
        for line in f:
            if line.strip().startswith(r'['):
                asg_name.append( line.strip().strip('[]') )
    return asg_name
    
def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--module_name', type=str, help='module name', required=True)
    parser.add_argument('--module_args', type=str, help='module args', required=True)
    parser.add_argument('--pattern', type=str, help='host or group', required=True)
    parser.add_argument('--region', type=str, help='region', choices=['cn', 'us', 'eu', 'ap'], required=True)
    parser.add_argument('--remote_port', type=int, help='connect remote host port', default=22022)
    parser.add_argument('--remote_user', type=str, help='connect remote host user', default='ec2-user')
    parser.add_argument('--forks', type=int, help='parallelism level', default=1)
    parser.add_argument('--debug', type=str, help='debug message', default='false')
    args = parser.parse_args()

    if args.pattern == 'all':
        all_asg_name = get_inventory()
        filter_asg_name = [ x for x in all_asg_name if x.startswith(args.region)]

        threads = []
        for asg_name in filter_asg_name:
            t = threading.Thread(target=exec_cmd, args=(args.module_name, args.module_args, asg_name, args.forks, args.debug, args.remote_port, args.region))
            t.daemon = True
            threads.append(t)
            t.start()

        for t in threads:
            t.join(80)
    else:
        exec_cmd( args.module_name, args.module_args, args.pattern, args.forks, args.debug, args.remote_port, args.region )

if __name__ == '__main__':
    FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    main(sys.argv)
