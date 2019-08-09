# -*- coding: utf-8 -*-
from ..models.Entity.Floor  import Floor
from ..models.Entity.Plan import Plan
from ..models.Entity.ResourceType import ResourceType
from ..models.Entity.RptFloorPlan import RptFloorPlan
from ..models.Entity.SaleArea import SaleArea
from ..models.Entity.Shops import Shops
from ..models.bn_decorator import bnfunlog
from ..models.Entity.DiscountReport import DiscountReport


@bnfunlog('')
def proc_sync_floor(self):
    np = Floor()
    floors = np.get_floor_all()
    for fl in floors:
        res = {'code': fl['strenumid'],
               'name': fl['stritemname'],
               'lngitemvalue':fl['lngItemValue']
                    }
        rst= self.env['bn.floor'].query(res)
        if rst is None:
            self.env['bn.floor'].create(res)
    return True


@bnfunlog('')
def proc_sync_resourcetype(self):
    np = ResourceType()
    resources = np.get_all()
    for rs in resources:
        res = {'code': rs['strenumid'],
               'name': rs['stritemname'],
               'itemcode':rs['lngItemValue']
                    }
        rst= self.env['bn.resourcetype'].query(res)
        if rst is None:
            self.env['bn.resourcetype'].create(res)
    return True

@bnfunlog('')
def proc_sync_salearea(self):
    np = SaleArea()
    salesareas = np.get_all()
    for sl in salesareas:
        res = {'code': sl['strSaleAreaID'],
               'name': sl['strsaleareaname'],
                    }
        rst= self.env['bn.salearea'].query(res)
        if rst is None:
            self.env['bn.salearea'].create(res)
    return True

@bnfunlog('')
def proc_sync_shop(self):
    np = Shops()
    shops = np.get_all()
    for shop in shops:
        res = {
            'lngshopid': shop['lngshopid'],
            'name':shop['strshopname'],
            'bn_strShopName': shop['strshopname'],
            'bn_strShortName': shop['strShortName']
        }
        rst= self.env['res.company'].query(shop['lngshopid'])
        if rst is None:
            self.env['res.company'].create(res)
    return True


@bnfunlog('')
def proc_sync_pmplan(self):
    rst1=self.env['bn.rptfloorplan'].get_need_sync_pm_plan()
    rst2=self.env['bn.discount.report'].get_need_sync_pm_plan()
    rst=list(set(rst1+rst2))
    if rst is not None:
        task_plan=Plan()
        plans=task_plan.get_all(rst)
        i = 0
        for plan in plans:
            print('pmplan==>current:' + str(i) + '-/-total:' + str(len(plans)))
            shopid = self.env['res.company'].query(plan['lngshopid']).id
            floorid = self.env['bn.floor'].query_by_value(plan['lngfloor']).id
            res={
               'code' :plan['strplanid'],
               'name' :plan['strresourcename'],
               'decQuantity' :plan['decquantity'],
               'decSimpleShopPrice' :plan['decsimpleshopprice'],
               'lngPlanTypeId' :plan['lngresourcetype'],
               'blnIsCancel' :plan['blniscancel'],
               'strDescription' :plan['strresourcename'],
               'lngfloor' :plan['lngfloor'],
               'dtActiveDate' :plan['dtactivedate'],
               'dtCancleDate' :plan['dtCancelDate'],
               'shopid' :shopid,
               'floorid' :floorid,
            }
            rst=self.env['bn.pmplan'].query_by_id(plan['strplanid'])
            if rst is None:
                nplan=self.env['bn.pmplan'].create(res).id
                query="""update {0}  set plan_id={1} where plan_strid='{2}'"""
                query1=query.format('bn_rptfloorplan',nplan,plan['strplanid'])
                query2 = query.format('bn_discount_report',nplan, plan['strplanid'])
                self.env.cr.execute(query1)
                self.env.cr.execute(query2)
            i+=1


@bnfunlog('')
def proc_sync_floorplan_data(self):
    rpt1=RptFloorPlan()
    reports= rpt1.get_all(self.dtDate)
    i=0
    for line in reports:
        print('floorplan_data==>current:'+str(i)+'-/-total:'+str(len(reports)))
        shopid=self.env['res.company'].query(line['lngshopid']).id
        floorid=self.env['bn.floor'].query_by_id(line['strFloor']).id
        resource_type_id=self.env['bn.resourcetype'].query_by_id(line['lngResourceType']).id

        plan_tmp=self.env['bn.pmplan'].query_by_id(line['strPlanID'])
        if plan_tmp is None :
            plan_id=None
        else:
            plan_id=plan_tmp.id

        res={
            'dtDate':self.dtDate,
            'lngshopid': line['lngshopid'],
            'strfloor': line['strFloor'],
            'strresourcetype':  line['lngResourceType'],
            'decQuantity':  line['decAreaQuantity'],
            'plan_shopprice':  line['plan_shopprice'],
            'rent_shopprice':  line['rent_shopprice'],
            'real_factprice':  line['decRealFactPrice'],
            'ar_balance':  line['decArBalance'],
            'plan_strid':  line['strPlanID'],
            'resource_code':  line['strResourceCode'],
            'contract_id':  line['strContractID'],
            'business_id':  line['strBusinessID'],
            'shop_id':  shopid,
            'floor_id': floorid,
            'resource_type_id':  resource_type_id,
            'plan_id':  plan_id,
        }
        self.env['bn.rptfloorplan'].create(res)
        i+=1
    return True


@bnfunlog('')
def proc_sync_plantype(self):
    task_plan = Plan()
    plantype_list= task_plan.get_plantype()
    for pt in plantype_list:
        res = {'code': pt['strenumid'],
               'name': pt['stritemname'],
               'itemvalue': pt['lngitemvalue'],
                 }
        rst= self.env['bn.plantype'].query(pt['strenumid'])
        if rst is None:
            self.env['bn.plantype'].create(res)

    hylist=task_plan.get_ShopPlanHyMonth()
    for line in hylist:
        shopid = self.env['res.company'].query(line['lngshopid']).id
        plantypeid = self.env['bn.plantype'].query_by_id(line['lngplantype']).id

        res = {'hy_month': line['strHyMonths'],
               'hy_year': line['strHyYear'],
               'shopid': shopid,
               'plantypeid': plantypeid,
               }
        rst=self.env['bn.shopplanhymonth'].query(res)
        if rst is None:
            self.env['bn.shopplanhymonth'].create(res)
    return True


@bnfunlog('')
def proc_contract_file(self):
    np = Shops()
    contlist = np.get_contract_file(self.dtDate)
    i=0
    for line in contlist:
        shopid = self.env['res.company'].query(line['lngshopid']).id
        plantypeid = self.env['bn.plantype'].query_by_id(line['lngPlanTypeID']).id
        print('contract_file_data==>current:' + str(i) + '-/-total:' + str(len(contlist)))
        res={
            'dtDate': self.dtDate,
            'shop_id': shopid,
            'plantype_id': plantypeid,
            'contract_vol': line['contractvol'],
            'filed': line['filed'],
            'unfiled': line['unfiled'],
            'change_month': line['changmonth'],
            'tdays': line['tdays'],
            't2sdays': line['t2sdays'],
            'stondays': line['stondays'],
            'nabove': line['nabove'],
        }
        self.env['bn.rptcontractfile'].create(res)
        i+=1
    return True

@bnfunlog('')
def proc_sync_discount_report(self):
    report=DiscountReport()
    resultlist=report.get_all(self.dtDate)
    i=0
    for result in resultlist:
        print('discount_report==>current:' + str(i) + '-/-total:' + str(len(resultlist)))
        sameresult=self.env['bn.discount.report'].query_same(result['strCreateDate'],
                                                             result['strContractID'],
                                                             result['strPlanID'])
        if sameresult is None:
            shopid = self.env['res.company'].query(result['lngShopID']).id
            plan_tmp=self.env['bn.pmplan'].query_by_id(result['strPlanID'])
            if plan_tmp is None :
                plan_id=None
            else:
                plan_id=plan_tmp.id
            if result['dtChangeDate'] is None or result['dtChangeDate']=="":
                dtChangeDate=None
            else:
                dtChangeDate=result['dtChangeDate']
            res={
                'contract_strid':result['strContractID'],
                'contract_code':result['strContractCode'],
                'contract_begin_date':result['dtBeginDate'],
                'contract_end_date':result['dtEndDate'],
                'contract_change_date':dtChangeDate,
                'contract_execute_state':result['strStatus'],
                'contract_all_money':result['lngTotalMoney'],
                'contract_day_money':result['decDayTotalMoney'],
                'contract_day':result['lngDays'],
                'contract_price':result['decFactPrice'],
                'contract_shop_price':result['decSimpleShopPrice'],
                'contract_month':result['decQuantity'],
                'plan_strid':result['strPlanID'],
                'plan_id':plan_id,
                'second_party':result['strBusinessName'],
                'abdication_type':result['strWithdrawType'],
                'receivables_type':result['strGatheringName'],
                'area':result['decArea'],
                'shop_price_discount':result['decScale2'],
                'all_price':result['decTotalSimpleShopPrice'],
                'discount_price':result['decTotalDisCount'],
                'resources_subsidy':result['lngChangeMoney'],
                'day_discount':result['decDayContractSimpleDiff'],
                'january':result['decMonthDisCount1'],
                'february':result['decMonthDisCount2'],
                'march': result['decMonthDisCount3'],
                'april': result['decMonthDisCount4'],
                'may': result['decMonthDisCount5'],
                'june': result['decMonthDisCount6'],
                'july': result['decMonthDisCount7'],
                'august': result['decMonthDisCount8'],
                'september': result['decMonthDisCount9'],
                'october': result['decMonthDisCount10'],
                'november': result['decMonthDisCount11'],
                'december': result['decMonthDisCount12'],
                'dtDate': result['strCreateDate'],
                'shop_id': shopid
            }
            self.env['bn.discount.report'].create(res)
        i += 1
    return True