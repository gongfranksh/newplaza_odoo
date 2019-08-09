# -*- coding: utf-8 -*-

from .BNMsSql import bnmssql
class Plan(bnmssql):

    def __init__(self):
        bnmssql.__init__(self)

    def get_all(self,planlist):

        sql = "select lngshopid, strplanid,strresourcename,lngresourcetype,strsaleareaid,decquantity, \
                     decsimpleshopprice,lngplantypeid,blniscancel,lngfloor,dtactivedate,dtCancelDate \
                      from Pm_Plan  \
                     where strplanid  in (%s)" % ','.join(["'%s'" % item for item in planlist])


        # print(sql)
        rst = self.get_remote_result_by_sql(sql)
        return rst

    def get_plantype(self):
        sql = """
        select
        strenumid, stritemname, lngitemvalue
        from Pm_Enum where
        lngEnumTypeID = 8
        """
        # print(sql)
        rst = self.get_remote_result_by_sql(sql)
        return rst

    def get_ShopPlanHyMonth(self):
        sql = """
            select lngshopid,lngplantype,strHyYear,strHyMonths 
            from Pm_ShopPlanHyMonth
        """
        # print(sql)
        rst = self.get_remote_result_by_sql(sql)
        return rst
