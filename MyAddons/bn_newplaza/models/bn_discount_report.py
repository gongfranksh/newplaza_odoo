# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime
class bn_discount_report(models.Model):
    _name = 'bn.discount.report'

    contract_strid=fields.Char(string=u'商管id')
    contract_code=fields.Char(string=u'合同编码')
    contract_begin_date=fields.Date(string=u'合同开始日期')
    contract_end_date=fields.Date(string=u'合同结束日期')
    contract_change_date=fields.Date(string=u'合同异动日期')
    contract_execute_state=fields.Char(string=u'合同执行情况')
    contract_all_money=fields.Float(string=u'合同总金额')
    contract_day_money = fields.Float(string=u'合同单日金额')
    contract_day=fields.Integer(string=u'合同天数')
    contract_price=fields.Float(string=u'合同单价')
    contract_shop_price = fields.Float(string=u'合同单店底价')
    contract_month=fields.Float(string=u'合同月数（倍数）')

    plan_strid = fields.Char(string=u'席位id')
    plan_id = fields.Many2one('bn.pmplan', string=u'席位编码')

    second_party=fields.Char(string=u'乙方')
    abdication_type = fields.Char(string=u'退位类型')
    receivables_type=fields.Char(string=u'收款方式')
    area=fields.Float(string=u'面积')
    shop_price_discount=fields.Float(string=u'单店底价折扣')
    all_price=fields.Float(string=u'底价总额')
    discount_price=fields.Float(string=u'折扣总额')
    resources_subsidy=fields.Float(string=u'资源补贴金额')
    day_discount=fields.Float(string=u'天折扣')

    january=fields.Float(string=u'一月')
    february=fields.Float(string=u'二月')
    march=fields.Float(string=u'三月')
    april=fields.Float(string=u'四月')
    may=fields.Float(string=u'五月')
    june=fields.Float(string=u'六月')
    july=fields.Float(string=u'七月')
    august=fields.Float(string=u'八月')
    september=fields.Float(string=u'九月')
    october=fields.Float(string=u'十月')
    november=fields.Float(string=u'十一月')
    december=fields.Float(string=u'十二月')
    all_month=fields.Float(string=u'合计',compute='_compute_month',store=True)
    text=fields.Char(string=u'文本',compute='_compute_text',store=True)

    shop_id = fields.Many2one('res.company', u'门店')
    lngshopid = fields.Integer(string='商管门店id')
    strCreateYearMonth = fields.Char(string=u'月份')


    @api.depends('january','february','march','april','may','june','july','august','september','october','november','december')
    def _compute_month(self):
        self.all_month=self.january+self.february+self.march+self.april+self.may+ \
                       self.june+self.july+self.august+self.september+self.october+ \
                       self.november+self.december

    @api.depends('contract_day_money')
    def _compute_text(self):
        if self.contract_day_money>=100:
            self.text='>=100小计'
        else:
            self.text='<100小计'
    @api.multi
    def get_need_sync_pm_plan(self):
        rstlist = self.env['bn.discount.report'].search([('plan_id', '=',None)])
        rst_tmp=[]
        for rec in rstlist:
            rst_tmp.append(rec.plan_strid)
        rst=list(set(rst_tmp))
        return rst
    @api.multi
    def query_same(self,strCreateYearMonth,contract_strid,plan_strid):
        rst=self.env['bn.discount.report'].search([('strCreateYearMonth', '=', strCreateYearMonth),
                                                   ('contract_strid','=',contract_strid),
                                                   ('plan_strid','=',plan_strid)
                                                   ])
        if len(rst)==0:
            return None
        else:
            return rst
    @api.multi
    def delete_history(self,procdate):
        sql="""delete  from bn_discount_report where "strCreateYearMonth"='{0}'""".format(procdate)
        self.env.cr.execute(sql)
        #self.env.cr.commit()
    @api.multi
    def update_relateshop(self,procdate):
        sql="""update bn_discount_report  A 
               set "shop_id"=B."id"
               FROM res_company B
               where  A."strCreateYearMonth"='{0}' 
               and A."lngshopid"=B."lngshopid" """.format(procdate)
        self.env.cr.execute(sql)
    @api.multi
    def update_relateplan(self,procdate):
        sql="""update bn_discount_report  A 
               set "plan_id"=C."id"
               FROM bn_pmplan C
               where  A."strCreateYearMonth"='{0}' 
               and A."plan_strid"=C."code" """.format(procdate)
        self.env.cr.execute(sql)