## RESTFUL API客户端封装

```python

import requests


class httpRequest(object):

    def __init__(self):
        pass

    @classmethod
    def get(cls, url, payload=None):
        '''
        Sends a GET request.
        '''
        req = requests.get(url=url, params=payload)
        return httpRequest()._do(req)

    @classmethod
    def post(cls, url, payload):
        '''
        Sends a POST request.
        '''
        if isinstance(payload, dict):
            req = requests.post(url, data=payload)
        elif isinstance(payload, list):
            req = requests.post(url, json=payload)
        else:
            return 'method: post, params is error, please check your params.', False
        return httpRequest()._do(req)

    @classmethod
    def put(cls, url, payload):
        '''
        Sends a PUT request.
        '''
        if isinstance(payload, dict):
            req = requests.put(url, data=payload)
            return httpRequest()._do(req)
        else:
            return 'method: put, params is error, please check your params.', False

    @classmethod
    def delete(cls, url):
        '''
        Sends a DELETE request.
        '''
        req = requests.delete(url)
        return httpRequest()._do(req)

    @classmethod
    def options(cls, url):
        '''
        Sends an OPTIONS request.
        '''
        req = requests.options(url)
        return httpRequest()._do(req)

    @classmethod
    def head(cls, url):
        '''
        Sends an HEAD request.
        '''
        req = requests.options(url)
        return httpRequest()._do(req)

    @classmethod
    def _do(cls, obj):
        if obj.status_code == 200:
            return httpRequest()._parseException(obj), True
        else:
            return httpRequest()._parseException(obj), False 
    
    @classmethod
    def _parseException(cls, obj):
        try:
            return obj.json() 
        except ValueError as e:
            return obj.text
        except Exception as e:
            return e.args


if __name__ == '__main__':
    data = {}
    url = ''
    httpResponse, ok = httpRequest.post(url, data)
    print httpResponse, ok
```
