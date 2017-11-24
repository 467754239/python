# Api

```python
HTTP 标准的方法有如下:
==========  =====================  ==============================================
HTTP 方法   行为                   示例
==========  =====================  ==============================================
GET         获取资源的信息         http://example.com/api/v1/tasks
GET         获取某个特定资源的信息 http://example.com/api/v1/tasks/<int:task_id>
POST        创建新资源             http://example.com/api/v1/tasks
PUT         更新资源               http://example.com/api/v1/tasks/<int:task_id>
DELETE      删除资源               http://example.com/api/v1/tasks/<int:task_id>
==========  ====================== ==============================================

def ApiSucess(data, message, code=0):
    response = {'data' : data, 'message' : message, 'code' : code}
    return response
    
def ApiError(data, message, code=-1):
    response = {'data' : data, 'message' : message, 'code' : code}
    return response

# response
{
    'code' : 0,
    'data' : None,
    'message' : '',

}

raise ApiError('GET /tasks/ {}'.format(resp.status_code))
```
