

where = {'name':'zhengys', 'age':24}

'''
name='zhengys' AND age=24
'''


format_where = [ '%s = "%s"' % (k, v) for k, v in where.items() ]
where = ' AND '.join(format_where)
print where