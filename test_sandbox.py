#!/usr/bin/python
# -*- coding:utf-8 -*-

import xmlrpclib
import ConfigParser
import os

# すべてのメソッドで使用するURLは次の通り
# https://[スペースID].backlog.jp/XML-RPC
#
# 認証を含めると次のようになる。
# https://[ユーザー名]:[パスワード]@[スペースID].backlog.jp/XML-RPC

class Backlog():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.backlog_url = "https://%s:%s@gluegent.backlog.jp/XML-RPC" % (self.username, self.password)
        self.backlog_handle = xmlrpclib.ServerProxy(self.backlog_url)

    def display_projects(self):
        projects = self.backlog_handle.backlog.getProjects()
        for project in projects:
            print project['id']
            print project['key']
            print project['name']

def read_ini(ini_filename = "backlog.ini"):
    """このスクリプトの配置パスになるbacklog.iniファイルを解析し、ユーザー名とパスワードを取得する
    backlog.ini
    ------------
    [Account]
    user = anonymous
    password = 1234abcd
    ------------
    """

    INI_FILE = os.path.join(os.path.dirname(__file__), ini_filename)
    ini = ConfigParser.SafeConfigParser()
    if os.path.exists(INI_FILE):
        file = open(INI_FILE, 'r')
        ini.readfp(file)
        file.close()
    else:
        print 'Cannot find %s' % INI_FILE
        import sys
        sys.exit(1)
    username = ini.get('Account', 'user')
    password = ini.get('Account', 'password')
    return (username, password)

# manipulate_backlog()
if __name__ == '__main__':
    (username, password) = read_ini()
    Backlog_handle = Backlog(username, password)
    Backlog_handle.display_projects()

