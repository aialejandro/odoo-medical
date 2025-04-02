# -*- coding: utf-8 -*-
# from odoo import http


# class Odoo-medical(http.Controller):
#     @http.route('/odoo-medical/odoo-medical', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo-medical/odoo-medical/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo-medical.listing', {
#             'root': '/odoo-medical/odoo-medical',
#             'objects': http.request.env['odoo-medical.odoo-medical'].search([]),
#         })

#     @http.route('/odoo-medical/odoo-medical/objects/<model("odoo-medical.odoo-medical"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo-medical.object', {
#             'object': obj
#         })

