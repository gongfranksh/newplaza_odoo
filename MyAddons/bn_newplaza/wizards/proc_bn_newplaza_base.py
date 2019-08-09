# -*- coding: utf-8 -*-
import datetime

from odoo import models, api, fields
from odoo.fields import Field
from .proc_bn_newplaza_method import proc_sync_floor, proc_sync_resourcetype, \
    proc_sync_salearea, proc_sync_shop, proc_sync_floorplan_data, proc_sync_pmplan, proc_sync_plantype, \
    proc_contract_file,proc_sync_discount_report


class bn_newplaza_proc_wizard(models.TransientModel):
    _name = "bn.newplaza.proc.wizard"
    _description = "bn.newplaza.proc.wizard"
    dtDate = fields.Date(string=u'执行日期',default=datetime.date.today() )

    @api.multi
    def sync_floor_plan(self):
        self.ensure_one()
        proc_sync_floorplan_data(self)


    @api.multi
    def sync_floor_button(self):
         proc_sync_floor(self)

    @api.multi
    def sync_resourcetype_button(self):
        proc_sync_resourcetype(self)
        pass

    @api.multi
    def sync_pm_salearea_button(self):
        proc_sync_salearea(self)
        pass

    @api.multi
    def sync_pm_plan_button(self):
        proc_sync_pmplan(self)

    @api.multi
    def sync_pm_shop_button(self):
        proc_sync_shop(self)
        pass

    @api.multi
    def sync_pm_plantype_button(self):
        proc_sync_plantype(self)
        pass

    @api.multi
    def sync_bn_discount_report(self):
        proc_sync_discount_report(self)
        pass


    @api.multi
    def sync_contract_file(self):
        proc_contract_file(self)
        pass




    @api.multi
    def sync_all_button(self):
        proc_sync_floor(self)
        proc_sync_plantype(self)
        proc_sync_resourcetype(self)
        proc_sync_salearea(self)
        proc_sync_shop(self)
        pass