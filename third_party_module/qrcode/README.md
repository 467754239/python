# 二维码 
> https://github.com/lincolnloop/python-qrcode

```python
# pip install Image
# pip install qrcode

import qrcode

# 设置二维码图片绑定的网址
img = qrcode.make('https://github.com/467754239')

# 生成二维码图片
with open('reboot-actual.png', 'wb') as f:
    img.save(f)
```
