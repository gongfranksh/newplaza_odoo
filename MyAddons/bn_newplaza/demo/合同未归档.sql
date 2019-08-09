declare @rep_date datetime
select @rep_date='2019-7-31'

select a.lngshopid,strShortName,lngPlanTypeID,plantype,contractvol,filed,unfiled, unfiled_rate,tdays,t2sdays,stondays,nabove,strHyMonths as changmonth  from
(
	select lngshopid,strShortName,plantype,lngPlanTypeID,count(*) as 'contractvol',sum(filed) as 'filed',sum(unfiled) as 'unfiled',sum(unfiled) *0.01*100/count(*) as unfiled_rate,
		sum(tdays) as 'tdays' ,sum(t2sdays) as 't2sdays',sum(stondays) as 'stondays',sum(nabove) as 'nabove'
	from
	(
			 select distinct case when isnull(isFile,0)=1 then 1 else 0 end as 'filed'
					,case when isnull(isFile,0)=0 then 1 else 0 end as 'unfiled'
					,case b.lngstatus when 1 then '正常' when 0 then '退位' when 4 then '到期' end as 'status'
					,f.strItemName as 'plantype'
					,d.lngPlanTypeID
					,a.strContractCode
					,a.strContractID
					,case when isnull(isFile,0)=0 and DATEDIFF(day,b.dtBeginDate,@rep_date)<=30 then 1 else 0 end as 'tdays'
					,case when isnull(isFile,0)=0 and DATEDIFF(day,b.dtBeginDate,@rep_date)>30 and DATEDIFF(day,b.dtBeginDate,@rep_date)<=60 then 1 else 0 end as 't2sdays'
					,case when isnull(isFile,0)=0 and DATEDIFF(day,b.dtBeginDate,@rep_date)>60 and DATEDIFF(day,b.dtBeginDate,@rep_date)<=90 then 1 else 0 end as 'stondays'
					,case when isnull(isFile,0)=0 and DATEDIFF(day,b.dtBeginDate,@rep_date)>90 then 1 else 0 end as 'nabove'
					,e.strShortName
					,e.lngShopID
			 from Pm_Contract a
					   left join (select ROW_NUMBER() OVER(PARTITION BY strContractID ORDER BY dtBeginDate asc) num ,* from Pm_ContractResource where lngStatus=1) b
						on a.strContractID=b.strContractID and (b.num=1 or b.num is null)
					   left join Pm_Plan d on b.strPlanID=d.strPlanID
					   left join Pm_Shop e on a.lngShopID=e.lngShopID
					   left join Pm_Enum f on f.lngEnumTypeID=8 and f.lngItemValue=d.lngPlanTypeID
			 where (a.lngstatus = 0 Or a.lngstatus = 3)  and isnull(a.lngFinancerID,0)>0
	) t
	group by lngshopid,strShortName,plantype,lngPlanTypeID
) a
left join Pm_ShopPlanHyMonth m on a.lngShopID =m.lngshopid  and a.plantype =m.strPlanType
where plantype not in('写字间规划')
order by a.lngShopID ,a.plantype desc