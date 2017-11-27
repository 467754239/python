## RESTFUL API客户端封装

```python

import requests


class httpRequest(object):

    def __init__(self):
        self.timeout = 3


    @staticmethod
    def get(url, payload=None):
        '''
        Sends a GET request.
        '''
        req = requests.get(url=url, params=payload)
        return _do(req)


    @staticmethod
    def post(url, payload):
        '''
        Sends a POST request.
        '''
        if isinstance(payload, dict):
            req = requests.post(url, data=payload)
        elif isinstance(payload, list):
            req = requests.post(url, json=payload)
        else:
            return 'method: post, params is error, please check your params.', False
        return _do(req)


    @staticmethod
    def put(url, payload):
        '''
        Sends a PUT request.
        '''
        if isinstance(payload, dict):
            req = requests.put(url, data=payload)
            return _do(req)
        else:
            return 'method: put, params is error, please check your params.', False


    @staticmethod
    def delete(url):
        '''
        Sends a DELETE request.
        '''
        req = requests.delete(url)
        return _do(req)


    @staticmethod
    def options(url):
        '''
        Sends an OPTIONS request.
        '''
        req = requests.options(url)
        return _do(req)


    @staticmethod
    def head(url):
        '''
        Sends an HEAD request.
        '''
        req = requests.options(url)
        return _do(req)


def _do(handler):
    if handler.status_code == 200:
        return _parseException(handler), True
    else:
        return _parseException(handler), False


def _parseException(handler):
    try:
        return handler.json() 
    except ValueError as e:
        return handler.text
    except Exception as e:
        return e.args




if __name__ == '__main__':
    response = httpRequest.get(url="http://www.baidu.com/")
    print response
```
