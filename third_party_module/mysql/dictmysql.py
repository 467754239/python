# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from __future__ import print_function
import pymysql
import pymysql.cursors
import re

'''
https://github.com/467754239/DictMySQL/blob/master/dictmysql.py
'''


class DictMySQL:
    def __init__(self, host, user, passwd, db=None, port=3306, charset='utf8', init_command='SET NAMES UTF8',
                 dictcursor=False, use_unicode=True):
        self.host = host
        self.port = int(port)
        self.user = user
        self.passwd = passwd
        self.db = db
        self.dictcursor = dictcursor
        self.cursorclass = pymysql.cursors.DictCursor if dictcursor else pymysql.cursors.Cursor
        self.charset = charset
        self.init_command = init_command
        self.use_unicode = use_unicode
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db,
                                    charset=charset, init_command=init_command, cursorclass=self.cursorclass,
                                    use_unicode=self.use_unicode)
        self.cur = self.conn.cursor()
        self.debug = False
        self.last_query = None

    def reconnect(self):
        # TODO: add auto reconnect
        try:
            self.cursorclass = pymysql.cursors.DictCursor if self.dictcursor else pymysql.cursors.Cursor
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                        db=self.db, cursorclass=self.cursorclass, charset=self.charset,
                                        init_command=self.init_command,
                                        use_unicode=self.use_unicode)
            self.cur = self.conn.cursor()
            return True
        except pymysql.Error as e:
            print("Mysql Error: %s" % (e,))
            return False

    def query(self, sql, args=None):
        """
        :param sql: string. SQL query.
        :param args: tuple. Arguments of this query.
        """
        try:
            result = self.cur.execute(sql, args)
        except pymysql.Error as e:
            result = None
            print("Mysql Error: %s\nOriginal SQL:%s" % (e, sql))
        return result

    @staticmethod
    def _backtick_columns(cols):
        # backtick the former part when it meets the first dot, and then all the rest
        def bt(s):
            b = '' if s == '*' or not s else '`'
            return [_ for _ in [b + (s or '') + b] if _]
        return ', '.join(
                [c[1:] if c[0] == '#' else '.'.join(bt(c.split('.')[0]) + bt('.'.join(c.split('.')[1:]))) for c in cols]
        )

    def _backtick(self, value):
        return self._backtick_columns((value,))

    @staticmethod
    def _whitespace_decorator(s, p=True, n=False):
        return ''.join((' ' if p else '', s, ' ' if n else ''))

    def _tablename_parser(self, table):
        result = re.match('^(\[(|>|<|<>|><)\])??(\w+)(\((|\w+)\))??$', table.replace(' ', ''))
        join_type = ''
        alias = ''
        formatted_tablename = self._backtick(table)
        if result:
            alias = result.group(5) if result.group(5) else ''

            tablename = result.group(3)

            formatted_tablename = ' '.join([self._backtick(tablename),
                                            'AS', self._backtick(alias)]) if alias else self._backtick(tablename)

            join_type = {'>': 'LEFT', '<': 'RIGHT', '<>': 'FULL', '><': 'INNER'}.get(result.group(2), '')
        else:
            tablename = table

        return {'join_type': join_type,
                'tablename': tablename,
                'alias': alias,
                'formatted_tablename': formatted_tablename}

    def _value_parser(self, value, columnname=False, placeholder='%s'):
        """
        Input: {'c1': 'v', 'c2': None, '#c3': 'uuid()'}
        Output:
        ('%s, %s, uuid()', [None, 'v'])                             # insert; columnname=False
        ('`c2` = %s, `c1` = %s, `c3` = uuid()', [None, 'v'])        # update; columnname=True
        No need to transform NULL value since it's supported in execute()
        """
        if not isinstance(value, dict):
            raise TypeError('Input value should be a dictionary')
        q = []
        a = []
        for k, v in value.items():
            if k[0] == '#':  # if is sql function
                q.append(' = '.join([self._backtick(k[1:]), str(v)]) if columnname else v)
            else:
                q.append(' = '.join([self._backtick(k), placeholder]) if columnname else placeholder)
                a.append(v)
        return ', '.join(q), tuple(a)

    def _join_parser(self, join):
        if not join:
            return ''

        join_q = ''
        for j_table, j_on in join.items():
            join_table = self._tablename_parser(j_table)
            join_q += ''.join([(' ' + join_table['join_type']) if join_table['join_type'] else '', ' JOIN ',
                               join_table['formatted_tablename'],
                               ' ON ',
                               ' AND '.join(['='.join([self._backtick(o_k),
                                                       self._backtick(o_v)]) for o_k, o_v in j_on.items()])])
        return join_q

    def _where_parser(self, where, placeholder='%s'):
        if not where:
            return '', ()

        result = {'q': [], 'v': ()}

        _operators = {
            '$=': '=',
            '$EQ': '=',
            '$<': '<',
            '$LT': '<',
            '$>': '>',
            '$GT': '>',
            '$<=': '<=',
            '$LTE': '<=',
            '$>=': '>=',
            '$GTE': '>=',
            '$<>': '<>',
            '$NE': '<>',
            '$LIKE': 'LIKE',
            '$BETWEEN': 'BETWEEN',
            '$IN': 'IN'
        }

        _connectors = {
            '$AND': 'AND',
            '$OR': 'OR'
        }

        negative_symbol = {
            '=': '<>',
            '<': '>=',
            '>': '<=',
            '<=': '>',
            '>=': '<',
            '<>': '=',
            'LIKE': 'NOT LIKE',
            'BETWEEN': 'NOT BETWEEN',
            'IN': 'NOT IN',
            'AND': 'OR',
            'OR': 'AND'
        }
        # TODO: confirm datetime support for more operators
        # TODO: LIKE Wildcard support

        def _get_connector(c, is_not, whitespace=False):
            c = c or '='
            c = negative_symbol.get(c) if is_not else c
            return ' ' + c + ' ' if whitespace else c

        placeholder = '%s'

        def _combining(_cond, _operator=None, upper_key=None, connector=None, _not=False):
            if isinstance(_cond, dict):
                i = 1
                for k, v in _cond.items():
                    # {'$AND':{'value':10}}
                    if k.upper() in _connectors:
                        result['q'].append('(')
                        _combining(v, upper_key=upper_key, _operator=_operator, connector=_connectors[k.upper()], _not=_not)
                        result['q'].append(')')
                    # {'>':{'value':10}}
                    elif k.upper() in _operators:
                        _combining(v, _operator=_operators[k.upper()], upper_key=upper_key, connector=connector, _not=_not)
                    # {'$NOT':{'value':10}}
                    elif k.upper() == '$NOT':
                        _combining(v, upper_key=upper_key, _operator=_operator, connector=connector, _not=not _not)
                    # {'value':10}
                    else:
                        _combining(v, upper_key=k, _operator=_operator, connector=connector, _not=_not)
                    # append 'AND' by default except for the last one
                    if i < len(_cond):
                        result['q'].append(_get_connector('AND', is_not=_not, whitespace=True))
                    i += 1

            elif isinstance(_cond, list):
                # [{'age': {'$>': 22}}, {'amount': {'$<': 100}}]
                if all(isinstance(c, dict) for c in _cond):
                    l_index = 1
                    for l in _cond:
                        _combining(l, _operator=_operator, upper_key=upper_key, connector=connector, _not=_not)
                        if l_index < len(_cond):
                            result['q'].append(_get_connector(connector, is_not=_not, whitespace=True))
                        l_index += 1
                elif _operator in ['=', 'IN'] or not _operator:
                    s_q = self._backtick(upper_key) + (' NOT' if _not else '') + ' IN (' + ', '.join(['%s']*len(_cond)) + ')'
                    result['q'].append('(' + s_q + ')')
                    result['v'] += tuple(_cond)
                elif _operator == 'BETWEEN':
                    s_q = self._backtick(upper_key) + (' NOT' if _not else '') + ' BETWEEN ' + ' AND '.join(['%s']*len(_cond))
                    result['q'].append('(' + s_q + ')')
                    result['v'] += tuple(_cond)
                elif _operator == 'LIKE':
                    s_q = ' OR '.join(['(' + self._backtick(upper_key) + (' NOT' if _not else '') + ' LIKE %s)'] * len(_cond))
                    result['q'].append('(' + s_q + ')')
                    result['v'] += tuple(_cond)
                # if keyword not in prefilled list but value is not dict also, should return error

            elif not _cond:
                s_q = self._backtick(upper_key) + ' IS' + (' NOT' if _not else '') + ' NULL'
                result['q'].append('(' + s_q + ')')
            else:
                if upper_key[0] == '#':
                    item_value = _cond
                    upper_key = upper_key[1:]  # for functions, remove the # symbol and no need to quote the value
                else:
                    item_value = placeholder
                    result['v'] += (_cond,)
                s_q = ' '.join([self._backtick(upper_key), _get_connector(_operator, is_not=_not), item_value])
                result['q'].append('(' + s_q + ')')

        _combining(where)
        return ' WHERE ' + ''.join(result['q']), result['v']

    @staticmethod
    def _limit_parser(limit=None):
        if isinstance(limit, list) and len(limit) == 2:
            return ' '.join((' LIMIT', ', '.join(str(l) for l in limit)))
        elif str(limit).isdigit():
            return ' '.join((' LIMIT', str(limit)))
        else:
            return ''

    def select(self, table, columns=None, join=None, where=None, order=None, limit=None):
        """
        :type table: string
        :type columns: list
        :type join: dict
        :param join: {'[>]table1(t1)': {'user.id': 't1.user_id'}} -> "LEFT JOIN table AS t1 ON user.id = t1.user_id"
        :type where: dict
        :type order: string
        :type limit: int|list
        :param limit: The max row number you want to get from the query.
        """
        if not columns:
            columns = ['*']
        where_q, _args = self._where_parser(where)

        _sql = ''.join(['SELECT ', self._backtick_columns(columns),
                        ' FROM ', self._tablename_parser(table)['formatted_tablename'],
                        self._join_parser(join),
                        where_q,
                        (' ORDER BY ' + order) if order else '',
                        self._limit_parser(limit), ';'])

        self.last_query = _sql % _args

        if self.debug:
            print(self.last_query)
            return

        self.cur.execute(_sql, _args)
        return self.cur.fetchall()

    def get(self, table, column, join=None, where=None, insert=False, ifnone=None):
        """
        A simplified method of select, for getting the first result in one column only. A common case of using this
        method is getting id.
        :type table: string
        :type column: str
        :type join: dict
        :type where: dict
        :type insert: bool
        :param insert: If insert==True, insert the input condition if there's no result and return the id of new row.
        :type ifnone: string
        :param ifnone: When ifnone is a non-empty string, raise an error if query returns empty result. insert parameter
                       would not work in this mode.
        """
        select_result = self.select(table=table, columns=[column], join=join, where=where, limit=1)

        if self.debug:
            return

        result = select_result[0] if select_result else None

        if result:
            return result[0 if self.cursorclass is pymysql.cursors.Cursor else column]

        if ifnone:
            raise ValueError(ifnone)

        if insert:
            if any([isinstance(d, dict) for d in where.values()]):
                raise ValueError("The where parameter in get() doesn't support nested condition with insert==True.")
            # TODO: debug insert
            return self.insert(table=table, value=where)

        return None

    def insert(self, table, value, ignore=False, commit=True):
        """
        Insert a dict into db.
        :type table: string
        :type value: dict
        :type ignore: bool
        :type commit: bool
        :return: int. The row id of the insert.
        """
        value_q, _args = self._value_parser(value, columnname=False)
        _sql = ''.join(['INSERT', ' IGNORE' if ignore else '', ' INTO ', self._backtick(table),
                        ' (', self._backtick_columns(value), ') VALUES (', value_q, ');'])

        self.last_query = _sql % _args

        if self.debug:
            print(self.last_query)
            return

        self.cur.execute(_sql, _args)
        if commit:
            self.conn.commit()
        return self.cur.lastrowid

    def upsert(self, table, value, update_columns=None, commit=True):
        """
        :type table: string
        :type value: dict
        :type update_columns: list
        :param update_columns: specify the columns which will be updated if record exists
        :type commit: bool
        """
        if not isinstance(value, dict):
            raise TypeError('Input value should be a dictionary')

        if not update_columns:
            update_columns = value.keys()

        value_q, _args = self._value_parser(value, columnname=False)

        _sql = ''.join(['INSERT INTO ', self._backtick(table), ' (', self._backtick_columns(value), ') VALUES ',
                        '(', value_q, ') ',
                        'ON DUPLICATE KEY UPDATE ', ', '.join(['='.join([k, k]) for k in update_columns]), ';'])
        # TODO: bt this column names

        self.last_query = _sql % _args

        if self.debug:
            print(self.last_query)
            return

        self.cur.execute(_sql, _args)
        if commit:
            self.conn.commit()
        return self.cur.lastrowid

    def insertmany(self, table, columns, value, ignore=False, commit=True):
        """
        Insert multiple records within one query.
        :type table: string
        :type columns: list
        :type value: list|tuple
        :param value: Doesn't support MySQL functions
        :param value: Example: [(value1_column1, value1_column2,), ]
        :type ignore: bool
        :type commit: bool
        :return: int. The row id of the LAST insert only.
        """
        if not isinstance(value, (list, tuple)):
            raise TypeError('Input value should be a list or tuple')

        _sql = ''.join(['INSERT', ' IGNORE' if ignore else '', ' INTO ', self._backtick(table),
                        ' (', self._backtick_columns(columns), ') VALUES (', ', '.join(['%s'] * len(columns)), ');'])
        _args = tuple(value)

        self.last_query = _sql

        if self.debug:
            print(self.last_query)
            return

        self.cur.executemany(_sql, _args)
        if commit:
            self.conn.commit()
        return self.cur.lastrowid

    def update(self, table, value, where, commit=True):
        """
        :type table: string
        :type value: dict
        :type where: dict
        :type commit: bool
        """
        # TODO: join support

        value_q, _value_args = self._value_parser(value, columnname=True)

        where_q, _where_args = self._where_parser(where)

        _sql = ''.join(['UPDATE ', self._backtick(table), ' SET ', value_q, where_q, ';'])
        _args = _value_args + _where_args

        self.last_query = _sql % _args

        if self.debug:
            print(self.last_query)
            return

        result = self.cur.execute(_sql, _args)
        if commit:
            self.commit()
        return result

    def delete(self, table, where, commit=True):
        """
        :type table: string
        :type where: dict
        :type commit: bool
        """
        where_q, _args = self._where_parser(where)

        _sql = ''.join(['DELETE FROM ', self._backtick(table), where_q, ';'])

        self.last_query = _sql % _args

        if self.debug:
            print(self.last_query)
            return

        result = self.cur.execute(_sql, _args)
        if commit:
            self.commit()
        return result

    def column_name(self, table):
        _sql = "SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`=%s AND `TABLE_NAME`=%s;"
        _args = (self.db, table)

        self.cur.execute(_sql, _args)
        return self.cur.fetchall()

    def now(self):
        query = "SELECT NOW() AS now;"
        if self.debug:
            print(query)
            return
        self.cur.execute(query)
        return self.cur.fetchone()[0 if self.cursorclass is pymysql.cursors.Cursor else 'now'].strftime(
                "%Y-%m-%d %H:%M:%S")

    def last_insert_id(self):
        query = "SELECT LAST_INSERT_ID() AS lid;"
        if self.debug:
            print(query)
            return
        self.query(query)
        return self.cur.fetchone()[0 if self.cursorclass is pymysql.cursors.Cursor else 'lid']

    def fetchone(self):
        return self.cur.fetchone()

    def fetchall(self):
        return self.cur.fetchall()

    def lastrowid(self):
        return self.cur.lastrowid

    def rowcount(self):
        return self.cur.rowcount

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def __del__(self):
        try:
            self.cur.close()
            self.conn.close()
        except:
            pass

    def close(self):
        self.cur.close()
        self.conn.close()