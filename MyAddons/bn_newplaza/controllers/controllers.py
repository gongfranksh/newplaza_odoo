# -*- coding: utf-8 -*-
from odoo import http

# class BnNewplaza(http.Controller):
#     @http.route('/bn_newplaza/bn_newplaza/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bn_newplaza/bn_newplaza/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bn_newplaza.listing', {
#             'root': '/bn_newplaza/bn_newplaza',
#             'objects': http.request.env['bn_newplaza.bn_newplaza'].search([]),
#         })

#     @http.route('/bn_newplaza/bn_newplaza/objects/<model("bn_newplaza.bn_newplaza"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bn_newplaza.object', {
#             'object': obj
#         })