#!/usr/bin/python
# -*- coding:utf-8 -*-

import xmlrpclib
import ConfigParser
import os
import argparse # Python 2.7〜

# すべてのメソッドで使用するURLは次の通り
# https://[スペースID].backlog.jp/XML-RPC
#
# 認証を含めると次のようになる。
# https://[ユーザー名]:[パスワード]@[スペースID].backlog.jp/XML-RPC

class Backlog():
    def __init__(self, username, password, space):
        self.username = username
        self.password = password
        self.space = space
        self.backlog_url = "https://%s:%s@%s.backlog.jp/XML-RPC" % (self.username, self.password, self.space)
        self.backlog_handle = xmlrpclib.ServerProxy(self.backlog_url)

    def display_projects(self):
        projects = self.backlog_handle.backlog.getProjects()
        for project in projects:
            print project['id']
            print project['key']
            print project['name']

    def get_users(self):
        """Test function"""
        print self.backlog_handle.backlog.getUsers(28691)
        
    def get_user_id(self):
        userinfo = self.backlog_handle.backlog.getUser(self.username)
        return userinfo['id']

    def close_issue_range(self, user_id, project, from_num, to_num, comment="This is a test post"):
        if to_num == None:
             self.backlog_handle.backlog.switchStatus({'key':'%s-%d' % (project, from_num),
                                                      'statusId':4,
                                                      'assignerId':user_id,
                                                      'comment':comment
                                                     })
        else:
            for x in range(from_num, to_num + 1):
                self.backlog_handle.backlog.switchStatus({'key':'%s-%d' % (project, x),
                                                          'statusId':4,
                                                          'assignerId':user_id,
                                                          'comment':comment
                                                          })
    def close_issue_enumrate(self, user_id, project, case_nums, comment="This is a test post"):
        for case_num in case_nums:
            self.backlog_handle.backlog.switchStatus({'key':'%s-%d' % (project, case_num),
                                                      'statusId':4,
                                                      'assignerId':user_id,
                                                      'comment':comment
                                                      })


def read_ini(ini_filename = "backlog.ini"):
    """このスクリプトの配置パスになるbacklog.iniファイルを解析し、ユーザー名とパスワード、スペース名を取得する
    backlog.ini
    ------------
    [Account]
    user = anonymous
    password = 1234abcd
    space = your_space
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
    space = ini.get('Account', 'space')
    return (username, password, space)

# manipulate_backlog()
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', dest='project', help="Project name such as MLA or DAZ", required='True')
    parser.add_argument('-f', '--from', dest='from_num', type=int, help="Issue number to delete")
    parser.add_argument('-t', '--to', dest='to_num', help='Issue number to delete from FROM_NUM to TO_NUM', type=int)
    parser.add_argument('-c', '--comment', dest='comment', help='Comment to post', required='True')
    parser.add_argument('cases', nargs='*', type=int)
    args = parser.parse_args()

    (username, password, space) = read_ini()
    Backlog_handle = Backlog(username, password, space)
    user_id = Backlog_handle.get_user_id()
    if args.cases != []:
        Backlog_handle.close_issue_enumrate(user_id, args.project, args.cases, comment=args.comment)
    if args.from_num != None:
        Backlog_handle.close_issue_range(user_id, args.project, args.from_num, args.to_num,
                                         comment=args.comment)


