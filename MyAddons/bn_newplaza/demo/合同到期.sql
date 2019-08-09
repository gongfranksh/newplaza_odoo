select c.strShortName,a.strcontractcode,a.strBsideName,a.dtsigndate,d.strResourceCode,
		round(b.decSimpleShopPrice,2)  as  decSimpleShopPrice,b.decScale2,b.decFactPrice,b.dtBeginDate,b.dtEndDate,
		x.strItemName ,d.strResourceName,o.strItemName as strstatus,a.lngstatus
    FROM Pm_Contract a (NOLOCK)
            inner join (select * from Pm_Contractresource(NOLOCK) where 1=1  ) b  on a.Strcontractid=b.strcontractid
            inner join pm_plan d on d.strplanid = b.strplanid
            left join Pm_Shop c on a.lngShopID=c.lngShopID
            left join pm_enum x(NOLOCK) on x.lngItemValue = d.lngResourceType and x.lngEnumTypeID = 3
            left join pm_enum o(NOLOCK) on b.lngstatus = o.lngItemValue and o.lngEnumTypeID = 102
        where (a.lngstatus = 0 Or a.lngstatus = 3) and b.lngStatus=1 and DATEDIFF(day,getdate(),b.dtEndDate)<=31
        order by b.dtEndDate, a.strBsideName