# -*- coding: utf-8 -*-
from odoo import http

# class MethodLocalizacionHenua(http.Controller):
#     @http.route('/method_localizacion__henua/method_localizacion__henua/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/method_localizacion__henua/method_localizacion__henua/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('method_localizacion__henua.listing', {
#             'root': '/method_localizacion__henua/method_localizacion__henua',
#             'objects': http.request.env['method_localizacion__henua.method_localizacion__henua'].search([]),
#         })

#     @http.route('/method_localizacion__henua/method_localizacion__henua/objects/<model("method_localizacion__henua.method_localizacion__henua"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('method_localizacion__henua.object', {
#             'object': obj
#         })