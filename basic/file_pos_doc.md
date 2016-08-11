## fd 

> fd.tell

```
current file position, an integer (may be a long integer).

#译
当前文件指针的位置，一个整型（也有可能是一个长整型）.
```

> fd.seek

```
seek(offset[, whence]) -> None.  Move to new file position.

Argument offset is a byte count.  Optional argument whence defaults to
0 (offset from start of file, offset should be >= 0); other values are 1
(move relative to current position, positive or negative), and 2 (move
relative to end of file, usually negative, although many platforms allow
seeking beyond the end of a file).  If the file is opened in text mode,
only offsets returned by tell() are legal.  Use of other offsets causes
undefined behavior.
Note that not all file objects are seekable.

#译
移动文件指针的位置.

参数offset是一个字节数.  
可选参数whence默认是0（从文件开始的位置，offset应该大于等于0）；
其它值是1（相对当前指针的位置移动），
2（移动文件指针到文件的末尾）.

如果在文件模式下打开文件，仅偏移返回tell()是合法的. 使用其它的偏移将引起一个未定义的行为.
注意并非所有的文件对象是可查找.

#参数
offset: 文件的读/写指针位置.
whence: 这是可选的，默认为0，这意味着绝对的文件定位，其他值是1，这意味着当前的位置和2手段寻求相对寻求相对文件的结束.
```
