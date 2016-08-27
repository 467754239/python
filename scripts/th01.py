#coding:utf-8

# 对ip列表进行排序

ip_list = '''
192.168.1.100
192.168.1.2
192.168.1.30
'''

new_ip_lists = ip_list.split()

m = {}
for item in new_ip_lists:
    k = int(item.split('.')[-1])
    m[k] = item

new_map = sorted(m.items(), key=lambda x:x[0])
print [ line[1] for line in new_map if line ]
