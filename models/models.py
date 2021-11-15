# -*- coding: utf-8 -*-

from itertools import product
from odoo import models, fields, api
import xml.etree.ElementTree as xml 
import base64
from pdf417 import encode, encoding, render_image, render_svg
import logging
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning


_logger = logging.getLogger(__name__)

try:
    from io import BytesIO
except ImportError:
    _logger.warning("no se ha cargado io")
try:
    import pdf417gen
except ImportError:
    _logger.warning("Cannot import pdf417gen library")
try:
    import base64
except ImportError:
    _logger.warning("Cannot import base64 library")
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    _logger.warning("no se ha cargado PIL")
class StockPicking(models.Model):
    _inherit = 'stock.picking'

    string_picking = fields.Char(string='XML del Picking')    
    barcode_img = fields.Binary(string="Barcode Image", help="Barcode Image in PDF417 format",)
    str_origin_codigobarra = fields.Char(string='String código de barras')  
    str_codigobarra = fields.Char(string='String código de barras',compute="_compute_str_codigobarra", store=True)  

    @api.depends('str_origin_codigobarra')
    def _compute_str_codigobarra(self):
        self.str_codigobarra = self.str_origin_codigobarra.replace('Ñ',':').replace('ñ',';').replace('?','_')
    
    @api.multi
    def leer_productos(self):
        strcodigo=self.str_codigobarra
        codigo_split=strcodigo.split(';')
        for c in codigo_split:
            if c!='':
                separacion=c.split(':')
                productostr=separacion[0]            
                cantidad=separacion[1]          
                producto=self.env['product.product'].search([('default_code','=',productostr)],limit=1)
                if producto:
                    product_id=producto.id
                    uom_id=producto.product_tmpl_id.uom_id.id

                    values = {
                                "name":self.name,
                                "product_id":product_id,
                                "product_uom_qty":cantidad,
                                "product_uom":uom_id,
                                "location_id":self.location_id.id,
                                "location_dest_id":self.location_dest_id.id
                            }
                    stock_move=self.env['stock.move'].create(values)
                    
                    self.sudo().write({
                            'move_ids_without_package': [(4,stock_move.id,False)],
                    })  
                else:
                    raise Warning(("El siguiente producto no existe: %s" % productostr))


    @api.multi
    def button_validate(self):
        root = xml.Element("Picking")
        linea=""
        for i in self.move_ids_without_package:      
            linea+=i.product_id.default_code +":"+str(i.product_uom_qty)+";"
        self.string_picking=linea
        barcodes = encode(linea)
        barcodes_img= render_image(barcodes) 
        barcodefile = BytesIO()
        image = self.pdf417bc(self.string_picking, 13, 3)
        image.save(barcodefile, "PNG")
        data = barcodefile.getvalue()
        self.barcode_img= base64.b64encode(data)
        super(StockPicking,self).button_validate()

    def pdf417bc(self, ted, columns=13, ratio=3):
        #bc = pdf417gen.encode(ted, security_level=5, columns=columns, encoding="ISO-8859-1",)
        bc = pdf417gen.encode(ted, security_level=5, columns=columns, encoding="UTF-8",)
        image = pdf417gen.render_image(bc, padding=15, scale=1, ratio=ratio,)
        return image            