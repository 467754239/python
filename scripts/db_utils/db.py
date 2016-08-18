#coding:utf-8

import MySQLdb
import logging

class DB(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.db = None
        self.cur = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        
    def connect(self):
        self.db = MySQLdb.connect(**self.kwargs)
        self.cur = self.db.cursor()

    def close(self):
        self.cur.close()
        self.db.close()

    def execute_insert_sql(self, table_name, data):
        sql = self._insert_sql(table_name, data)
        logging.debug('sql:%s' % sql)
        if sql:
            return self._execute(sql)
        return

    def execute_delete_sql(self):
        pass

    def execute_update_sql(self):
        pass

    def get_one_result(self, table_name, fields=[], where=None, order=None, asc_order=True, limit=None):
        sql = self._select_sql(table_name, fields, where, order, asc_order, limit)
        logging.debug('sql:%s' % sql)
        if sql:
            self._execute(sql)
            # return tuple
            result = self._fetchone()
            
            # format: return dict
            return { k:v for k, v in zip(fields, result) }
        return
        
    def get_all_results(self, table_name, fields=[], where=None, order=None, asc_order=True, limit=None):
        sql = self._select_sql(table_name, fields, where, order, asc_order, limit)
        logging.debug('sql:%s' % sql)
        if sql:
            self._execute(sql)
            # return tuple
            result = self._fetchall()

            # format: return dict
            return self._format_all_result(fields, result)
        return
        
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
            logging.error('params error, data must dict.')
            return False
        
    def _select_sql(self, table_name, fields=[], where=None, order=None, asc_order=True, limit=None):
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
                    logging.error('where args value error.')

            sql = 'SELECT %s FROM %s WHERE %s;' % (','.join(fields), table_name, ' AND '.join(conditions))
        elif not where:
            sql = 'SELECT %s FROM %s;' % (','.join(fields), table_name)
        else:
            sql = ''
        return sql
    
    def _execute(self, sql):
        self.connect()
        try:
            return self.cur.execute(sql)
        except Exception as e:
            logging.error('execute insert error, %s', e)
            return
    
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
