#coding:utf-8
import logging
from db import DB
from utils import get_config

if __name__ == '__main__':
    FORMAT = '%(asctime)-15s %(filename)s line:%(lineno)d %(levelname)s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)

    kwargs = get_config('mysql')
    ret = {}
    for k, v in kwargs.items():
        if k == 'port':
            v = int(v)
        ret[k] = v

    table_name = 'tbs'

    # 插入数据
    '''
    data = {'id':1, 'username':'zhengys'}
    with DB(**ret) as conn:
        conn.execute_insert_sql('tbs', data)
    '''

    # 查询指定条目的数据
    '''
    fields = ['id', 'username']
    where = {'username':'zhengys'}
    with DB(**ret) as conn:
        print conn.get_one_result(table_name, fields, where)
    '''

    # 查询所有数据
    fields = ['id', 'username']
    where = {'username':'zhengys'}
    with DB(**ret) as conn:
        print conn.get_all_results(table_name, fields, where)
