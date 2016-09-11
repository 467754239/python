#coding:utf-8
from __future__ import unicode_literals

import json
from app import app
import MySQLdb

class dbmysql(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.kwargs['port'] = int(self.kwargs['port'])
        self.db = None
        self.cur = None

    def _connect_db(self):
        self.db = MySQLdb.connect(**self.kwargs)
        self.cur = self.db.cursor()

    def _close_db(self):
        self.cur.close()
        self.db.close()

    def execute_insert_sql(self, table_name, data):
        sql = self._insert_sql(table_name, data)
        app.logger.debug('sql:%s' % sql)
        if sql:
            return self._execute(sql)
        return

    def execute_delete_sql(self, table_name, where):
        sql = self._delete_sql(table_name, where)
        if sql:
            return self._execute(sql)
        return ''

    def _delete_sql(self, table_name, where):
        '''
        delete from table_name where name='zhengys';
        '''
        if not where and not isinstance(where, dict):
            app.logger.warnning('where not None or where type must dict.')
            return None

        format_where = [ '%s = "%s"' % (k, v) for k, v in where.items() ]
        where = ' AND '.join(format_where)
        sql = 'DELETE FROM %s where %s' % (table_name, where)
        app.logger.debug('_delte_sql:%s.' % sql)
        return sql

    def execute_update_sql(self, table_name, data, where, fields=None):
        sql = self._update_sql(table_name, data, where, fields)
        if sql:
            return self._execute(sql)
        else:
            return ''

    def get_one_result(self, table_name, fields=[], where=None):
        sql = self._select_sql(table_name, fields, where)
        app.logger.debug('sql:%s' % sql)
        if sql:
            self._execute(sql)
            # return tuple
            result = self._fetchone()
            app.logger.debug('get_one_result, result:%s.' % json.dumps(result))
            # format: return dict
            if result:
                return { k:v for k, v in zip(fields, result) }
            return 
        return
        
    def get_all_results(self, table_name, fields=[], where=None):
        sql = self._select_sql(table_name, fields, where)
        app.logger.debug('sql:%s' % sql)
        if sql:
            self._execute(sql)
            # return tuple
            result = self._fetchall()
            app.logger.debug('get_all_results:%s.' % json.dumps(result))
            # format: return dict
            return self._format_all_result(fields, result)
        return

    def _update_sql(self, table_name, data, where, fields=None):
        if not where and not isinstance(where, dict):
            return ''

        where_cond = [ "%s='%s'" % (k, v) for k,v in where.items() ]
        if fields:
            conditions = [ "%s='%s'" % (k, data[k]) for k in fields ]
        else:
            conditions = [ "%s='%s'" % (k, data[k]) for k in data ]

        sql = "UPDATE %s SET %s WHERE %s" % (table_name, ','.join(conditions), ' AND '.join(where_cond))
        app.logger.debug('update sql:%s.' % sql)
        return sql

        
    def _insert_sql(self, table_name, data):
        if isinstance(data, dict):
            fields, values = [], []
            for k, v in data.items():
                fields.append(k)
                values.append('"%s"' % v)
            format_fields = ','.join(fields)
            format_values = ','.join(values)
            sql = 'INSERT INTO %s (%s) VALUES(%s);' % (table_name, format_fields, format_values)
            return sql
        else:
            app.logger.error('params error, data must dict.')
            return False
        
    def _select_sql(self, table_name, fields=[], where=None):
        if dict and isinstance(where, dict):
            conditions = []
            for k, v in where.items():
                if isinstance(v, list):
                    tmp = ('%s IN (%s)' % (k, ','.join(v)))
                    conditions.append(tmp)
                elif isinstance(v, str) or isinstance(v, unicode):
                    tmp = "%s='%s'" % (k, v)
                    conditions.append(tmp)
                elif isinstance(v, int):
                    tmp = "%s='%s'" % (k, v)
                    conditions.append(tmp)
                else:
                    app.logger.error('where args value error.')

            sql = 'SELECT %s FROM %s WHERE %s;' % (','.join(fields), table_name, ' AND '.join(conditions))
        elif not where:
            sql = 'SELECT %s FROM %s;' % (','.join(fields), table_name)
        else:
            sql = ''
        return sql
    
    def _execute(self, sql):
        self._connect_db()
        try:
            return self.cur.execute(sql)
        except Exception as e:
            self._close_db()
            self._connect_db()
            return self.cur.execute(sql)
    
    def _fetchone(self):
        return self.cur.fetchone()

    def _fetchall(self):
        return self.cur.fetchall()

    def _format_all_result(self, fields, result):
        ret = []
        for record in result:
            format_record = { k:v for k, v in zip(fields, record) }
            ret.append(format_record)
        return ret