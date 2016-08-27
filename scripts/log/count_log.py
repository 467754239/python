#coding:utf-8
import time
import codecs
import datetime

# 统计每分钟每个ip的访问次数.

logfile = "C:/Users/Administrator/Desktop/git/github/python/scripts/log/access.log"

def format_atime(atime_str):
    token = atime_str.split('T')
    normal_atime_str = '%s %s' % (token[0], token[1].split('+')[0])
    return datetime.datetime.strptime(normal_atime_str, "%Y-%m-%d %H:%M:%S")

def next_atime(cur_atime, interval):
    first_atime = cur_atime
    atime_after_one_minutes = first_atime + datetime.timedelta(minutes=interval)
    return first_atime, atime_after_one_minutes

def count_ips(res):
    m = {}
    for line in res:
        atime, ip_list = line.items()[0]
        count_ips = {}
        for item in ip_list:
            count_ips[item] = count_ips.get(item, 0) + 1
        m[atime] = count_ips
    return m

def execute(interval):
    ret = []
    ips = []
    cmap = {}
    cnt = 1
    with codecs.open(logfile, 'rb', 'utf-8') as f:
        for line in f:
            ip = line.split()[0]
            atime = line.split()[3][1:-1]

            cur_atime = format_atime(atime)
            if cnt == 1:
                first_atime, atime_after_one_minutes = next_atime(cur_atime, interval)

            if cur_atime <= atime_after_one_minutes:
                k = '%s ~ %s' % (first_atime, atime_after_one_minutes)
                ips.append(ip)
            else:
                cmap[k] = ips
                ret.append(cmap)
                first_atime, atime_after_one_minutes = next_atime(cur_atime, interval)

                ips = []
                cmap = {}
                ips.append(ip)
            cnt += 1

        k = '%s ~ %s' % (first_atime, atime_after_one_minutes)
        cmap[k] = ips
        ret.append(cmap)
    return ret

def main():
    interval = 1
    result = execute(interval)
    count_res = count_ips(result)
    return count_res

if __name__ == '__main__':
    print main()