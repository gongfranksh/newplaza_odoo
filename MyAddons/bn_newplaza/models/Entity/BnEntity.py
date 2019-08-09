# -*- coding: utf-8 -*-

import json
import pymssql


# reload(sys)
# sys.setdefaultencoding("utf-8")
#
from ..Entity import db_host, db_user, db_pwd, db_dbname



class BnEntity(object):

    def __CONNECT_INFO(self):
        self.js_host = db_host
        self.js_user = db_user
        self.js_pwd = db_pwd
        self.js_db =db_dbname

    def __init__(self):
        self.__CONNECT_INFO()

    def __IsNoneRow(self,row):
            if row[0] is None:
                return 0
            else:
                return row[0]

    def IsNone(self,row):
            if row is None:
                return 0
            else:
                return row

    def __GetConnect_mssql(self):
        if not self.js_db:
            raise (NameError, "没有设置数据库信息")
        self.conn_js = pymssql.connect(host=self.js_host, user=self.js_user, password=self.js_pwd, database=self.js_db, charset="utf8")

        #add para as_dict=true return dict recordset

        cur = self.conn_js.cursor(as_dict=True)
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur

    def __MsSql_ExecQuery(self, sql):
        cur = self.__GetConnect_mssql()
        cur.execute(sql)
        resList = cur.fetchall()
        return resList


    def get_remote_result_by_sql(self,sql):
        res = self.__MsSql_ExecQuery(sql)
        # json_res= json.dumps(res,cls=MsSqlResultDataEncoder)
        return res

    def get_remote_list_by_sql(self,sql):
        res = self.__MsSql_ExecQuery(sql)
        return res

    def execSql(self,sql):
        try:
            if not self.js_db:
                raise (NameError, "没有设置数据库信息")
            conn = pymssql.connect(host=self.js_host, user=self.js_user, password=self.js_pwd,
                                           database=self.js_db, charset="utf8")
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
        except Exception as e:
            print(e.message)

