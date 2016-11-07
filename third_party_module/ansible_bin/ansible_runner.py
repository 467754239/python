# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys
import argparse
import threading

from ansible.runner import Runner

import update_inventory
from sendMail import send_mail

# export ANSIBLE_HOST_KEY_CHECKING=False
# os.environ['ANSIBLE_HOST_KEY_CHECKING'] = "False"

alarm_disk_message = ''
alarm_processNum_message = ''

def processDiskSpace(result, pattern, ip):
    global alarm_disk_message
    for line in result.split('\n'):
        if '/var/log' in line:
            UsePrecent = int(line.split()[4].rstrip('%'))
            if UsePrecent > 80:
                alarm_disk_message += 'asgname:%s, ip:%s, partition:%s, partition_space:%s.\n' % (pattern, ip, '/var/log', UsePrecent)

        elif '/tmp' in line:
            UsePrecent = int(line.split()[4].rstrip('%'))
            if UsePrecent > 80:
                alarm_disk_message += 'asgname:%s, ip:%s, partition:%s, partition_space:%s.\n' % (pattern, ip, '/var/log', UsePrecent)

def processProcessNum(result, pattern, ip):
    global alarm_processNum_message
    if int(result) >= 4:
        alarm_processNum_message += 'asgname:%s, ip:%s, process number more than 4.' % (pattern, ip)


def output_format(results, module_args, pattern, debug):
    if debug.lower() == 'true':
        print results
        print '\n'

    # execute sucessful
    for ip, val in results['contacted'].items():
        print pattern, ip
        try:
            if val['rc'] == 0:
                stdout = val['stdout']
                if 'df -h' in module_args:
                    try:
                processDiskSpace(stdout, pattern, ip)
                    except Exception as e:
                        print 'processDiskSpace -> ', e

                elif 'ps -ef' in module_args:
                    try:
                        processProcessNum(stdout, pattern, ip)
                    except Exception as e:
                        print 'processProcessNum ->', e

                print '%s >>> stdout' % module_args
                print stdout
            else:
                print 'stderr'
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
                    sudo_user='root',
                    private_key_file = '/home/ec2-user/.ssh/awscn_sengled_release.pem'.replace('cn', region), 
                    host_list = os.path.join( os.path.dirname( os.path.abspath(__file__) ), 'hosts'), 
                    forks = forks,
                    ).run()

    return output_format(results, module_args, pattern, debug)

def get_asgname(region_name):
    asg_name = []
    with open(os.path.join( os.path.dirname( os.path.abspath(__file__) ), 'hosts'), 'r') as f:
        for line in f:
            if line.strip().startswith(r'['):
                asg_name.append( line.strip().strip('[]') )

    return [ x for x in asg_name if x.startswith(region_name)]
    
def args_parse():
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
    return args

def main():
    args = args_parse()

    if args.pattern == 'all':
        filter_asg_name = get_asgname(args.region)

        threads = []
        for asg_name in filter_asg_name:
            t = threading.Thread(target=exec_cmd, args=(args.module_name, args.module_args, asg_name, args.forks, args.debug, args.remote_port, args.region))
            t.daemon = True
            threads.append(t)
            t.start()

        for t in threads:
            t.join(100)

    if alarm_disk_message:
        print 'alarm disk message >>> ', alarm_disk_message
            if send_mail("aws disk alarm", alarm_disk_message):
                print 'sendmail sucessful'
            else:
                print 'sendmail failed'
        elif alarm_processNum_message:
            print 'alarm process number message >>> ', alarm_processNum_message
            if send_mail("aws process number alarm", alarm_processNum_message):
                print 'sendmail sucessful'
            else:
                print 'sendmail failed'
        else:
            print 'alarm_message ok'
    else:
        exec_cmd( args.module_name, args.module_args, args.pattern, args.forks, args.debug, args.remote_port, args.region )

if __name__ == '__main__':
    main()