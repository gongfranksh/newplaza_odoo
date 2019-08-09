# -*- coding: utf-8 -*-

import json
import pymssql


# reload(sys)
# sys.setdefaultencoding("utf-8")
#
from DBUtils.PooledDB import PooledDB

# from ..bn_decorator import singleton
from ..Entity import db_host, db_user, db_pwd, db_dbname

#Sqlserver数据库连接池
# @singleton
class bnmssql(object):
    __pool=None

    def __init__(self):
        self.conn = bnmssql.getconn()
        self.cur = self.conn.cursor(as_dict=True)
        print('bnmssql.conn===> ' + str(self.conn))

    @classmethod
    def getconn(cls):

        if bnmssql.__pool is None:
            __pool=PooledDB(creator=pymssql, mincached=1, maxcached=5,
                                    host=db_host, user=db_user, password=db_pwd, database=db_dbname,charset='utf8')

            return __pool.connection()

    def op_insert(self, sql):
        insert_num = self.cur.execute(sql)
        self.conn.commit()
        return insert_num

    # 查询
    def op_select(self, sql):
        self.cur.execute(sql)  # 执行sql
        select_res = self.cur.fetchall()  # 返回结果为字典
        return select_res

    # 释放资源
    def dispose(self):
        self.conn.close()
        self.cur.close()

    def get_remote_result_by_sql(self,sql):
        res = self.op_select(sql)
        # json_res= json.dumps(res,cls=MsSqlResultDataEncoder)
        return res

