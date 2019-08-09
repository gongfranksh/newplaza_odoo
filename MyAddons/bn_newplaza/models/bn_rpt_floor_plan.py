# -*- coding: utf-8 -*-
from odoo import models, fields, api


class bn_RptFloorPlan(models.Model):
    _name = 'bn.rptfloorplan'

    dtDate = fields.Date(string=u'统计日期')
    lngshopid = fields.Integer(string=u'店号')
    strfloor = fields.Char(string=u'楼层')
    strresourcetype = fields.Char(string=u'资源类型')
    decQuantity = fields.Float(string=u'面积')
    plan_shopprice = fields.Float(string=u'规划单店底价')
    rent_shopprice = fields.Float(string=u'已租合同单店底价')
    real_factprice = fields.Float(string=u'合同实际单价')

    plan_shopprice_untax = fields.Float(string=u'规划单店底价_未税',compute='_computer_plan_shopprice_untax',store=True)
    rent_shopprice_untax = fields.Float(string=u'已租合同单店底价_未税',compute='_computer_rent_shopprice_untax',store=True)
    real_factprice_untax = fields.Float(string=u'合同实际单价_未税',compute='_computer_real_factprice_untax',store=True)


    plan_unitprice = fields.Float(string=u'规划均价', compute='_compute_plan_unitprice',store=True)
    rent_unitprice = fields.Float(string=u'已租均价', compute='_compute_rent_unitprice',store=True)
    unrent_flag = fields.Char(string=u'租赁标识', compute='_compute_unrent_flag',store=True)
    discount_rate_title = fields.Char(string=u'折扣率', compute='_discount_rate_title',store=True)

    ar_balance = fields.Float(string=u'AR')
    plan_strid = fields.Char(string=u'席位id')
    resource_code = fields.Char(string=u'席位编号')
    contract_id = fields.Char(string=u'合同id')
    business_id = fields.Char(string=u'商家id')

    shop_id = fields.Many2one('res.company', u'门店')
    floor_id = fields.Many2one('bn.floor', u'楼层')
    resource_type_id = fields.Many2one('bn.resourcetype', u'资源类型')
    plan_id = fields.Many2one('bn.pmplan', u'席位')

    @api.depends('plan_shopprice')
    def _computer_plan_shopprice_untax(self):
        for rec in self:
            rec.plan_shopprice_untax = rec.plan_shopprice / 1.05

    @api.depends('rent_shopprice')
    def _computer_rent_shopprice_untax(self):
        for rec in self:
            rec.rent_shopprice_untax = rec.rent_shopprice / 1.05


    @api.depends('real_factprice')
    def _computer_real_factprice_untax(self):
        for rec in self:
            rec.real_factprice_untax = rec.real_factprice / 1.05



    @api.depends('decQuantity')
    def _compute_rent_unitprice(self):
        for rec in self:
            if rec.decQuantity ==0:
                rec.rent_unitprice=0
            else:
                rec.rent_unitprice=rec.real_factprice / rec.decQuantity

    @api.depends('decQuantity')
    def _compute_plan_unitprice(self):
        for rec in self:
            if rec.decQuantity == 0:
                rec.plan_unitprice = 0
            else:
                rec.plan_unitprice = rec.plan_shopprice / rec.decQuantity

    @api.depends('contract_id')
    def _compute_unrent_flag(self):
        for rec in self:
            if not rec.contract_id :
                rec.unrent_flag='空租'
            else:
                rec.unrent_flag='已租'


    @api.depends('rent_unitprice')
    def _discount_rate_title(self):
        for rec in self:
            if rec.rent_unitprice == 0:
                rec.discount_rate_title =None
            else:

                if rec.plan_unitprice==0:
                    rec.discount_rate_title = None
                else:
                    rec.discount_rate_title = "%.2f%%" % (rec.rent_unitprice/ rec.plan_unitprice * 100)


    @api.multi
    def get_need_sync_pm_plan(self):
        rstlist = self.env['bn.rptfloorplan'].search([('plan_id', '=',None)])
        if len(rstlist) == 0:
            return None
        else:
            rst_tmp=[]
            for rec in rstlist:
                rst_tmp.append(rec.plan_strid)
            rst=list(set(rst_tmp))
            return rst

