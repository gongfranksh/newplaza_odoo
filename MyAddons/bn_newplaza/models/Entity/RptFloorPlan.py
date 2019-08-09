# -*- coding: utf-8 -*-
from .BNMsSql import bnmssql


class RptFloorPlan(bnmssql):

    def __init__(self):
        bnmssql.__init__(self)

    def get_all(self,procdate):
        sql ="""
declare @dtARDate datetime

declare @shop table
(
  lngShopID int
)


insert into @shop
(lngShopID)
  select lngShopID
  from
    (
      select 1248 lngShopID
      union
      select 1029
      union
      select 1332
      union
      select 1109
    ) shop

select @dtARDate = '{0}'


select a.*,b.decArBalance from (
select
  lngshopid,
  strFloor,
  a.lngResourceType,
  a.strPlanID,
  strResourceCode,
  a.decAreaQuantity,
  a.decSimpleShopPrice as plan_shopprice,
  b.decSimpleShopPrice as rent_shopprice,
  a.decRealFactPrice,
  a.strContractID,
  a.strBusinessID
FROM Eproject.dbo.E_SeatPlanAndHireInfo_History a left join
  (
    select
      ROW_NUMBER()
      OVER ( PARTITION BY strContractID
        ORDER BY dtBeginDate asc ) num,
      *
    from Pm_ContractResource with ( nolock )
  ) b
    on a.strContractID = b.strContractID and b.num = 1
where DATEDIFF(day, dtDate, @dtARDate) = 0 and lngPlanTypeID = 1--and lngResourceType in(101,106,107,108)
      and isnull(a.lngstatus, 0) <> 3
	  ) a

	  left join (
	  select
  lngshopId,
  lngfloor,
  strplanid,
  sum(decArBalance) decArBalance,
  strResourceType
from (
       SELECT
         a.lngShopID,
         a.lngFloor,
         isnull(a.decMoney, 0) - isnull(b.decHxMoney, 0) AS decArBalance,
         a.strResourceType,
         strplanid,
         strcontractid
       FROM
         (
           select
             d.strBusinessCode,
             d.strName,
             c.strExpenseItemName,
             b.decMoney,
             a.strARMasterID,
             b.strARDetailID,
             a.lngShopID,
             e.lngFloor,
             b.strplanid,
             b.strcontractid,
             b.strContractCode,
             e.strResourceCode,
             case when e.lngResourceType in (101, 106, 107, 108)
               then 'IT席位'
             when e.lngResourceType in (102)
               then '餐饮席位'
             when e.lngResourceType in (105)
               then '异业席位'
             when e.lngResourceType in (2100)
               then '餐饮异业'
             end AS strResourceType
           from Pm_ARMaster a WITH ( NOLOCK )
             inner join Pm_ARDetail b WITH ( NOLOCK ) on a.strARMasterID = b.strARMasterID
             inner join Pm_ExpenseItem c on b.strExpenseItemID = c.strExpenseItemID
             inner join Pm_Business d on d.strBusinessID = b.strBusinessID
             INNER JOIN pm_plan e ON b.strPlanID = e.strPlanID
           where 1 = 1
                 and e.lngPlanTypeID = 1
                 and lngPeriod <> -1

                 and a.dtTrans <= @dtARDate
                 and (
                   not exists(
                       select lngShopID
                       from @shop s
                       where s.lngShopID = a.lngShopID
                   )
                   or not exists(
                       select strExpenseItemID
                       from Pm_ExpenseItem t
                       where t.strexpenseitemName like '%水电%' and t.strExpenseItemID = b.strExpenseItemID
                   )

                 )
           union all
           --初始的应缴余额中,应收单不为负数的那部分数据
           select
             d.strBusinessCode,
             d.strName,
             c.strExpenseItemName,
             b.decMoney,
             a.strARMasterID,
             b.strARDetailID,
             a.lngShopID,
             e.lngFloor,
             b.strplanid,
             b.strcontractid,
             b.strContractCode,
             e.strResourceCode,
             case when e.lngResourceType in (101, 106, 107, 108)
               then 'IT席位'
             when e.lngResourceType in (102)
               then '餐饮席位'
             when e.lngResourceType in (105)
               then '异业席位'
             when e.lngResourceType in (2100)
               then '餐饮异业'
             end AS strResourceType
           from Pm_ARMaster a WITH ( NOLOCK )
             inner join Pm_ARDetail b WITH ( NOLOCK ) on a.strARMasterID = b.strARMasterID
             inner join Pm_ExpenseItem c WITH ( NOLOCK ) on b.strExpenseItemID = c.strExpenseItemID
             inner join Pm_Business d WITH ( NOLOCK ) on d.strBusinessID = b.strBusinessID
             INNER JOIN pm_plan e WITH ( NOLOCK ) ON b.strPlanID = e.strPlanID
           where 1 = 1
                 and e.lngPlanTypeID = 1
                 and lngPeriod = -1
                 and b.decMoney > 0
                 and (a.strPeriod = '期初')
                 and (a.lngShopID not in (1248, 1029, 1332, 1109) or b.strExpenseItemID not in (select strExpenseItemID
                                                                                                from Pm_ExpenseItem
                                                                                                where strexpenseitemName
                                                                                                      like '%水电%'))
         ) a
         LEFT JOIN
         (
           select
             f.lngShopID,
             h.lngFloor,
             g.strARDetailID,
             g.strARMasterID,
             sum(isnull(e.decMoney, 0)) decHxMoney
           from Pm_HXAR e WITH ( NOLOCK )
             inner join Pm_HXMaster f WITH ( NOLOCK ) on e.strHXMasterID = f.strHXMasterID and f.strBillType = 2
             INNER JOIN Pm_ARDetail g WITH ( NOLOCK ) ON e.strDetailID = g.strARDetailID
             INNER JOIN pm_plan h WITH ( NOLOCK ) ON h.strPlanID = g.strPlanID
           where dtTrans <= @dtARDate
                 and h.lngPlanTypeID = 1
                 and (
                   not exists(
                       select lngShopID
                       from @shop s
                       where s.lngShopID = f.lngShopID
                   )
                   or not exists(
                       select strExpenseItemID
                       from Pm_ExpenseItem t
                       where t.strexpenseitemName like '%水电%' and t.strExpenseItemID = g.strExpenseItemID
                   )

                 )
           group by f.lngShopID, h.lngFloor, g.strARDetailID, g.strARMasterID
         ) b ON a.strARMasterID = b.strARMasterID AND a.strARDetailID = b.strARDetailID
         left join pm_shop c on a.lngShopID = c.lngShopID
       where (isnull(a.decMoney, 0) - isnull(b.decHxMoney, 0)) <> 0
     ) t
group by lngshopId, lngfloor, strplanid,  strResourceType

	  ) b on a.lngShopID=b.lngShopID and a.strPlanID=b.strPlanID        
        
        """
        sql=sql.format(procdate)
        # print(sql)
        rst = self.get_remote_result_by_sql(sql)
        return rst

