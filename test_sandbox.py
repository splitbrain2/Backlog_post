#!/usr/bin/python
# -*- coding:utf-8 -*-

import xmlrpclib

USER="xxxx"
PASSWORD="xxxx"

# すべてのメソッドで使用するURLは次の通り
# https://[スペースID].backlog.jp/XML-RPC
#
# 認証を含めると次のようになる。
# https://[ユーザー名]:[パスワード]@[スペースID].backlog.jp/XML-RPC


def manipulate_backlog():
    #backlog = xmlrpclib.ServerProxy("https://gluegent.backlog.jp/XML-RPC")# % (USER, PASSWORD))
    backlog = xmlrpclib.ServerProxy("https://%s:%s@gluegent.backlog.jp/XML-RPC" % (USER, PASSWORD))
    projects = backlog.backlog.getProjects()
    for project in projects:
        print project['id']
        print project['key']
        print project['name']

manipulate_backlog()

