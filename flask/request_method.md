## request.method
    - request.args  
    - request.form  
    - request.values  
    - request.data  
    - request.json  
    - request.get_json()  

```
# request.args
If you want the parameters in the URL. 
如果你想要在URL中传递参数；使用request.args.

# request.form 
If you want the information in the body (as sent by a html POST form)
如果你想要body的这些信息(以POST表单的发送方式通过一个html)
Form input 表单输入
注意:这种方式似乎不接受json数据.

# request.data、request.json和request.get_json()这三种类型很相似.
request.data接收到的数据是字符串类型，接收到的数据必须json.loads.
request.json和request.get_json()返回的都是json类型，可以直接使用.
```

示例
> restful.py

```
#coding:utf-8

import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def index():
    if request.method == 'GET':
        print type(request.args), request.args
        name = request.args.get('name')
        age = request.args.get('age')
        return 'action:%s, username:%s, age:%s.' % (request.method, name, age)

    elif request.method == 'POST':
        formdata = request.form
        print type(formdata), formdata

        data_string = request.data
        print type(data_string), data_string

        jsondata = request.json
        print type(jsondata), jsondata

        jsondata = request.get_json()
        print type(jsondata), jsondata

        return 'sucessful.', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

Client请求

> 方式1； GET params

```
$ curl 'http://localhost:5000/'
action:GET, username:None, age:None.

$ curl 'http://localhost:5000/?name=zhengys&age=27'
action:GET, username:zhengys, age:27.

# flask log
<class 'werkzeug.datastructures.ImmutableMultiDict'> ImmutableMultiDict([])
127.0.0.1 - - [05/Sep/2016 02:21:11] "GET / HTTP/1.1" 200 -
<class 'werkzeug.datastructures.ImmutableMultiDict'> ImmutableMultiDict([('age', u'27'), ('name', u'zhengys')])
127.0.0.1 - - [05/Sep/2016 02:21:16] "GET /?name=zhengys&age=27 HTTP/1.1" 200 -
```

> 方式2； POST params

```
$ curl -X POST 'http://localhost:5000/' -d 'name=zhengys&age=27'
sucessful.

<class 'werkzeug.datastructures.ImmutableMultiDict'> ImmutableMultiDict([('age', u'27'), ('name', u'zhengys')])
<type 'str'> 
<type 'NoneType'> None
<type 'NoneType'> None
```

```
import json
import requests

url = 'http://localhost:5000/'
data = {'name':'zhengyh', 'age':'35'}
req = requests.post(url=url, json=data, timeout=5)
#req = requests.post(url=url, data=json.dumps(data), timeout=5)

print req.status_code
print req.content
```

```
# flask log
<class 'werkzeug.datastructures.ImmutableMultiDict'> ImmutableMultiDict([])
<type 'str'> {"age": "35", "name": "zhengyh"}
<type 'dict'> {u'age': u'35', u'name': u'zhengyh'}
<type 'dict'> {u'age': u'35', u'name': u'zhengyh'}
```





参考文章

[Python flask.request.method Examples](http://www.programcreek.com/python/example/51533/flask.request.method)  
[How can I get the whole request POST body in Python with Flask?](http://stackoverflow.com/questions/10434599/how-can-i-get-the-whole-request-post-body-in-python-with-flask)