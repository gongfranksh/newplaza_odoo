# -*- coding: utf-8 -*-

from odoo import models, fields, api

class bn_floor(models.Model):
    _name = 'bn.floor'
    code = fields.Char(string=u'编号', required=True)
    name = fields.Char(string=u'名称', required=True)
    lngitemvalue = fields.Integer(string=u'内部值', required=True)

    @api.multi
    def query(self,res):
        rst=self.env['bn.floor'].search([('code', '=', res['code'])])
        if len(rst)==0 :
            return None
        else:
            return  rst

    @api.multi
    def query_by_id(self,res):
        rst=self.env['bn.floor'].search([('name', '=', res)])
        if len(rst)==0 :
            return None
        else:
            return  rst


    @api.multi
    def query_by_value(self,res):
        rst=self.env['bn.floor'].search([('lngitemvalue', '=', res)])
        if len(rst)==0 :
            return None
        else:
            return  rst

class bn_resourcetype(models.Model):
    _name = 'bn.resourcetype'
    code = fields.Char(string=u'编号', required=True)
    name = fields.Char(string=u'名称', required=True)
    itemcode = fields.Char(string=u'内部编号', required=True)

    @api.multi
    def query(self,res):
        rst=self.env['bn.resourcetype'].search([('code', '=', res['code'])])
        if len(rst)==0 :
            return None
        else:
            return  rst

    @api.multi
    def query_by_id(self,res):
        rst=self.env['bn.resourcetype'].search([('itemcode', '=', res)])
        if len(rst)==0 :
            return None
        else:
            return  rst

class bn_plantype(models.Model):
    _name = 'bn.plantype'
    code = fields.Char(string=u'编号', required=True)
    name = fields.Char(string=u'名称', required=True)
    itemvalue = fields.Char(string=u'内部编号', required=True)

    @api.multi
    def query(self,res):
        rst=self.env['bn.plantype'].search([('code', '=',res)])
        if len(rst)==0 :
            return None
        else:
            return  rst

    @api.multi
    def query_by_id(self,res):
        rst=self.env['bn.plantype'].search([('itemvalue', '=', res)])
        if len(rst)==0 :
            return None
        else:
            return  rst


class bn_salearea(models.Model):
    _name = 'bn.salearea'
    code = fields.Char(string=u'编号', required=True)
    name = fields.Char(string=u'名称', required=True)
    @api.multi
    def query(self,res):
        rst=self.env['bn.salearea'].search([('code', '=', res['code'])])
        if len(rst)==0 :
            return None
        else:
            return  rst

    @api.multi
    def query_by_id(self,res):
        rst=self.env['bn.salearea'].search([('code', '=', res)])
        if len(rst)==0 :
            return None
        else:
            return  rst

class bn_pmplan(models.Model):
    _name = 'bn.pmplan'
    code = fields.Char(string=u'编号', required=True)
    name = fields.Char(string=u'名称', required=True)
    resourcetype = fields.Char(string=u'类型')
    salearea  = fields.Char(string=u'区域')
    decQuantity  = fields.Float(string=u'面积')
    decSimpleShopPrice = fields.Float(string=u'底价')
    lngPlanTypeId=fields.Integer(string=u'席位类型')
    blnIsCancel  = fields.Selection([(1, '作废'), (0, '有效')], string='作废标志', default='0')
    strDescription  = fields.Char(string=u'描述')
    lngfloor  = fields.Integer(string=u'楼层')
    dtActiveDate  = fields.Datetime(string=u'激活日期')
    dtCancleDate  = fields.Datetime(string=u'取消日期')
    shopid = fields.Many2one( 'res.company', u'门店', required=True)
    floorid = fields.Many2one( 'bn.floor', u'楼层', required=True)


    @api.multi
    def query_by_id(self, res):
        rst = self.env['bn.pmplan'].search([('code', '=', res)])
        if len(rst) == 0:
            return None
        else:
            return rst


class res_company(models.Model):
    _name = 'res.company'
    _inherit = 'res.company'
    lngshopid=fields.Integer(string='lngshopid' )
    bn_strShopName=fields.Char(string=u'店名称' )
    bn_strShortName=fields.Char(string=u'店简称' )
    bn_sign_contractor_desc=fields.Char(string=u'换约信息' )
    bn_sign_contractor_date=fields.Datetime(string=u'换约日期' )

    @api.multi
    def query(self,res):
        rst=self.env['res.company'].search([('lngshopid', '=', res)])
        if len(rst)==0 :
            return None
        else:
            return  rst



class bn_shopplanhymonth(models.Model):
    _name = 'bn.shopplanhymonth'
    hy_month  = fields.Char(string=u'换约月份')
    hy_year  = fields.Char(string=u'换约年份')
    shopid = fields.Many2one( 'res.company', u'门店', required=True)
    plantypeid = fields.Many2one( 'bn.plantype', u'楼层', required=True)

    @api.multi
    def query(self, res):
        rst = self.env['bn.shopplanhymonth'].search([
                                                     ['shopid',  '=', res['shopid']],
                                                     ['plantypeid', '=', res['plantypeid']]
                                                     ]
                                                    )
        if len(rst) == 0:
            return None
        else:
            return rst