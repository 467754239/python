# jira

```
#coding: utf-8

import re
import json
import datetime
from jira import JIRA

'''
https://pypi.python.org/pypi/jira/1.0.10
https://github.com/pycontribs/jira/blob/develop/tests/tests.py
'''
def printJson(data, format='json'):
    if format == 'json':
        print json.dumps(data, indent=4)
    elif format == 'table':
        print 'table'


class JiraAdmin(object):

    def __init__(self, url, auth_user, auth_pass):
        self.url = url
        self.auth_user = auth_user
        self.auth_pass = auth_pass
        self.timeout = 10
        self.max_retries = 3
        self.conn = None

    def connect(self):
        if self.conn:
            return
        options = {'server' : self.url, 'basic_auth' : (auth_user, auth_pass), 'timeout' : self.timeout, 'max_retries' : self.max_retries}
        self.conn = JIRA(**options)

    def get_projects(self):
        self.connect()

        ret = []
        for obj in self.conn.projects():
            # 'avatarUrls', 'delete', 'expand', 'find', 'id', 'key', 'name', 'projectCategory', 'projectTypeKey', 'raw', 'self', 'update'
            # print obj.id, obj.name, obj.key
            token = obj.raw.get('projectCategory')
            if not token:
                continue
            print 'id:%s, en_name:%s, zn_name:%s, desc:%s' % ( obj.id, obj.name, token['name'], token['description'] )
            #ret.append({'id':obj.id, 'en_name':obj.name, 'zn_name':token['name'], 'desc':token['description']})        
        return ret

    def get_issues(self, project_name):
        self.connect()

        ret = []
        issues = self.conn.search_issues('project=%s' % project_name, fields='summary,comment,subtasks')
        # 'add_field_value', 'delete', 'expand', 'fields', 'find', 'id', 'key', 'permalink', 'raw', 'self', 'update'
        for obj in issues:
            #print x.id, x.key, x.fields.summary
            temp = {'iid' : obj.id, 'key': obj.key, 'summary':obj.fields.summary}
            subtasks_obj = obj.fields.subtasks
            if not subtasks_obj:
                continue
            temp['subtasks'] = self._fmt_subtasks( subtasks_obj )
            ret.append(temp)
        return ret

    def _fmt_subtasks(self, subtasks):
        ret = []
        for subtask in subtasks:
            #printJson( subtask.raw )
            temp = {}
            token = subtask.raw
            temp['subtask_id'] = token['id']
            temp['key'] = token['key']
            temp['summary'] = token['fields']['summary']
            ret.append( temp )
        return ret



    def get_worklogs(self, issue_name):
        self.connect()

        ret = []
        worklogs = self.conn.worklogs(issue_name)
        for obj in worklogs:
            # 'author', 'comment', 'created', 'delete', 'find', 'id', 'issueId', 'raw', 'self', 'started', 'timeSpent', 'timeSpentSeconds', 'update', 'updateAuthor', 'updated'
            #temp = {'startTime' : obj.created, 'timeSpend':obj.timeSpent}
            #temp = {'startTime' : obj.started, 'endTime':fmt_endTime( str(obj.started), str(obj.timeSpent) ), 'en_author' : obj.author.name, 'zn_author' : obj.author.displayName, 'email' : obj.author.emailAddress}
            temp = {'startTime' : obj.started, 'endTime':fmt_endTime( str(obj.started), str(obj.timeSpent) ), 'en_author' : obj.author.name, 'email' : obj.author.emailAddress}
            ret.append(temp)
        return ret


def fmt_endTime(startTime, timeSpent):
    fmt_startTime = startTime.replace('T', ' ').split('.')[0]
    startTime = datetime.datetime.strptime(fmt_startTime, "%Y-%m-%d %H:%M:%S")

    hours = fmt_hours(timeSpent)
    endTime = startTime + datetime.timedelta(hours=hours)
    return endTime.strftime("%Y-%m-%d %H:%M:%S")


def fmt_hours(timeSpent):
    if not timeSpent:
        return 0
    hours = 0
    for x in timeSpent.split():
        if x.endswith('h'):
            hour = int( x.strip('h') )
        elif x.endswith('d'):
            hour = int( x.strip('d') ) * 24
        hours += hour
    return hours



if __name__ == '__main__':
    url = ''
    auth_user = ''
    auth_pass = ''
    jira_admin = JiraAdmin(url, auth_user, auth_pass)

    '''
    Get all project
    '''
    #data = jira_admin.get_projects()
    #printJson(data)    

    '''
    Get all issue from project
    '''
    project_name = 'CLT-PMM_Projects'
    issues = jira_admin.get_issues( project_name )
    #import sys
    #sys.exit(1)

    '''
    Get worklogs from issue
    '''
    ret = []
    for x in issues:
        temp = {}
        issue_parent_name = x['key']
        issue_parent_summary = x['summary']
        for obj in x['subtasks']:
            subtask_child_id = obj['subtask_id']
            subtask_child_key = obj['key']
            subtask_child_summary = obj['summary']
            worklogs = jira_admin.get_worklogs(subtask_child_key)
            print '%s - %s' % (issue_parent_summary, subtask_child_summary)
            print worklogs
            print '\n\n'

        print '\n\n'
    #printJson(ret)
```
