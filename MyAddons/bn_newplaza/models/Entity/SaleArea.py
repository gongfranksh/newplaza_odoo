# -*- coding: utf-8 -*-
from .BNMsSql import bnmssql



class SaleArea(bnmssql):

    def __init__(self):
        bnmssql.__init__(self)

    def get_all(self):
        sql ="""
         select strSaleAreaID,strsaleareaname from Pm_SaleArea
        
        """
        rst = self.get_remote_result_by_sql(sql)
        return rst

