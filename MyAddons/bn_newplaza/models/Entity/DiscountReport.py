from .BNMsSql import bnmssql

class DiscountReport(bnmssql):

    def __init__(self):
        bnmssql.__init__(self)

    def get_all(self,procdate):
        sql="""select * from Bn_ContractDisCountYearMonth where
            strCreateYearMonth='{0}'""".format(procdate)
        rst = self.get_remote_result_by_sql(sql)
        return rst