# tail -f

```python
#!/usr/bin/env python
#coding=utf-8
#vim: tabstop=4 shiftwidth=4 softtabstop=4

'''
有两种情况下直接break
1. 文件的总字符数小于1000个字符 
    比如 有5行 一行120个字符 那么文件总共有600个字符
    这时break
    
2. 文件的总字符数大于1000个字符 
    分两种情况
        2.1 
            比如 有70行 一行20个字符 那么文件总共有1400个字符
            70行明显大于tail -f 10 中的10 
            这时break
        2.2
            比如 文件行数介于0和9之间
                如果文件行数为0 那么说明文件为空 或者 文件只有一行 直接打印这一行就可以了
                如果文件行数为9 那么也要直接打印这九行
'''

import sys
import time

class Tail(object):
    def __init__(self, file_name, callback=sys.stdout.write):
		self.file_name = file_name
		self.callback = callback

    def follow(self, n=10):
        try:
            # 打开文件
            with open(self.file_name) as f:
                self._file = f
                self._file.seek(0,2)
                
                # 存储文件字符的总总长度
                self.file_length = self._file.tell()
                # 另外一个函数 处理打印最后十行数据
                self.showLastLine(n)
                # 持续读文件每行 打印增量
                while True:
                    line = self._file.readline()
                    if line:
						self.callback(line)
                    time.sleep(1)
        except Exception,e:
            print '打开文件失败，囧，看看文件是不是不存在，或者权限有问题'
            print e
            
    def showLastLine(self, n):
		len_line = 100              # 初始值 假设一行有100个字符 这个数改成1或者1000都行
		read_len = len_line * n     # n默认是10 也可以通过follow的参数传递进来

        # 用last_lines存储最后要处理的内容
		while True:
            # 如果要读取的1000个字符，大于之前存储的文件长度
            # 读完文件，直接break
		    if read_len > self.file_length:
                self._file.seek(0)
                last_lines = self._file.read().split('\n')[-n:]
                break
            else:
                # 先读1000个 然后判断1000个字符里换行符的数量
                self._file.seek(-read_len, 2)   # 移动-1000个字符 从文件末尾.
                last_words = self._file.read(read_len)

                # count是换行符的数量
                count = last_words.count('\n')
                if count >= n:
                    # 换行符数量大于10 很好处理，直接读取
                    last_lines = last_words.split('\n')[-n:]
                    break
                # 换行符不够10个
                else:
                    if count == 0:
                        # 如果一个换行符也没有，那么我们就认为一行大概是100个字符
                        len_perline = len_line
                    else:
                        # 如果有4个换行符，我们认为每行大概有250个字符
                        len_perline = read_len / 4
                    # 要读取的长度变为2500，继续重新判断
                    read_len = len_perline * n

        for num, line in enumerate(last_lines):
            if line:
               self.callback('%s %s\n' %(int(num)+1, line))

if __name__ == '__main__':
    py_tail = Tail('/var/log/agent.log')
    py_tail.follow()

```
