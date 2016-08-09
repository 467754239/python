## Nginx access.log

> 处理日志文件，按ip字段进行排序。

```
$ head -n 10 access-8000.log
54.222.132.12 - - [2016-08-09T00:15:19+00:00] "POST /user/app/customer/AuthenCross.json HTTP/1.1" 200 213 "-" "Apache-HttpClient/4.5.2 (Java/1.6.0_45)" "-"
54.222.132.12 - - [2016-08-09T00:19:54+00:00] "POST /user/app/customer/getUserInfo.json HTTP/1.1" 200 343 "-" "Apache-HttpClient/4.5.2 (Java/1.6.0_45)" "-"
222.168.25.10 - - [2016-08-09T00:19:55+00:00] "GET /amazon-storage/download?bucketName=sengledimagebucket&filename=origin.png HTTP/1.1" 404 5 "-" "okhttp/2.6.0" "-"
220.248.15.74 - - [2016-08-09T00:24:56+00:00] "GET /amazon-storage/download?bucketName=sengledimagebucket&filename=F59B7A3F03317289EFDC9648C4D507B0_motion_1470646715652_small.jpg HTTP/1.1" 200 12996 "-" "snap/1.1.53 CFNetwork/758.5.3 Darwin/15.6.0" "-"
220.248.15.74 - - [2016-08-09T00:24:56+00:00] "GET /amazon-storage/download?bucketName=sengledimagebucket&filename=F59B7A3F03317289EFDC9648C4D507B0_motion_1470645596591_small.jpg HTTP/1.1" 200 11746 "-" "snap/1.1.53 CFNetwork/758.5.3 Darwin/15.6.0" "-"
220.248.15.74 - - [2016-08-09T00:24:56+00:00] "GET /amazon-storage/download?bucketName=sengledimagebucket&filename=F59B7A3F03317289EFDC9648C4D507B0_motion_1470646030985_small.jpg HTTP/1.1" 200 12758 "-" "snap/1.1.53 CFNetwork/758.5.3 Darwin/15.6.0" "-"
220.248.15.74 - - [2016-08-09T00:24:57+00:00] "GET /amazon-storage/download?bucketName=sengledimagebucket&filename=F59B7A3F03317289EFDC9648C4D507B0_motion_1470646494666_small.jpg HTTP/1.1" 200 12942 "-" "snap/1.1.53 CFNetwork/758.5.3 Darwin/15.6.0" "-"
220.248.15.74 - - [2016-08-09T00:25:03+00:00] "GET /amazon-storage/download?bucketName=sengledimagebucket&filename=F59B7A3F03317289EFDC9648C4D507B0_motion_1470644654148_small.jpg HTTP/1.1" 200 12263 "-" "snap/1.1.53 CFNetwork/758.5.3 Darwin/15.6.0" "-"
220.248.15.74 - - [2016-08-09T00:25:07+00:00] "GET /amazon-storage/download?bucketName=sengledimagebucket&filename=F59B7A3F03317289EFDC9648C4D507B0_motion_1470644291204_small.jpg HTTP/1.1" 200 12690 "-" "snap/1.1.53 CFNetwork/758.5.3 Darwin/15.6.0" "-"
220.248.15.74 - - [2016-08-09T00:25:08+00:00] "GET /amazon-storage/download?bucketName=sengledimagebucket&filename=F59B7A3F03317289EFDC9648C4D507B0_motion_1470643977078_small.jpg HTTP/1.1" 200 12680 "-" "snap/1.1.53 CFNetwork/758.5.3 Darwin/15.6.0" "-"
```

```
$ awk '{ print $1 }' access-8000.log | uniq -c | sort -n -r | head -n 10
    261 219.232.105.98
    117 219.232.105.98
     69 219.232.105.98
     56 220.248.15.74
     56 219.232.105.104
     49 219.232.105.98
     41 219.232.105.98
     39 219.232.105.98
     36 219.232.105.98
     36 219.232.105.104
```

```python
import sys

def main(logfile):
    ips = {}
    with open(logfile, 'r') as f:
        count = 1
        for line in f:
            ip = line.split()[0]
            if ip not in ips:
                ips[ip] = count
            else:
                ips[ip] = ips[ip] + 1

    return sorted(ips.items(), key=lambda x:x[1], reverse=True)

if __name__ == '__main__':
    print main(sys.argv[1])
```
