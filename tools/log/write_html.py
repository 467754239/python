#coding:utf-8


# 这两段代码写的还是比较巧妙的
dt = {}
f = open('access.log', 'r')
for line in f:
    l = line.split()
    k = l[0], l[5], l[7]
    #ip, url, status_code = l[0], l[5], l[7]
    dt[k] = dt.get(k, 0) + 1
#print dt
f.close()

dst = {}
for k, v in dt.items():
    dst.setdefault(v, [])
    dst[v].append(k)
print dst

rt='''
        <tr>
             <td>%s</td>
             <td>%s</td>
             <td>%s</td>
             <td>%s</td>
             <td>%s</td>
        </tr>
'''

fd = open('table.html', 'a+')
fd.write('<table border="1">')
fd.write(rt % ('No', 'ip', 'url', 'status', 'count'))

cnt = 1
cnt_end = 10
return_code = False

for k, v in dst.items():
    if return_code:
        break
    for l in v:
        ip, url, status_code = l
        fd.write(rt % (cnt, ip, url, status_code, k))
        if cnt == cnt_end:
            return_code = True
            break
        cnt += 1
fd.write('</table>')
fd.close()
