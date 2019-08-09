from .BNMsSql import bnmssql


class DiscountReport(bnmssql):

    def __init__(self):
        bnmssql.__init__(self)

    def get_all(self,procdate):
        year=procdate.year
        month=procdate.month
        sql="""select * from Bn_ContractDisCountYearMonth where 
            YEAR(strCreateDate) ={0} and MONTH(strCreateDate)={1} """.format(year,month)
        rst = self.get_remote_result_by_sql(sql)
        return rst