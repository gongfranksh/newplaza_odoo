# -*- coding: utf-8 -*-
from .BNMsSql import bnmssql



# class Floor(BnEntity):
class Floor(bnmssql):

    def __init__(self):
        bnmssql.__init__(self)

    def get_floor_all(self):
        sql ="""select lngItemValue,strItemName from Pm_Enum where lngEnumTypeID=7"""
        rst = self.get_remote_result_by_sql(sql)
        return rst

