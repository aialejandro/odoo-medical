# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class MedicalXrayOrderLine(models.Model):
    _name = 'medical.xray.order.line'
    _description = 'X-ray Order Line'
    _order = 'sequence, id'

    name = fields.Char(
        string='Description',
        compute='_compute_name',
        store=True
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Sequence for ordering the lines'
    )
    
    xray_order_id = fields.Many2one(
        'medical.xray.order',
        string='X-ray Order',
        ondelete='cascade',
        required=True
    )
    
    area_id = fields.Many2one(
        'medical.xray.area',
        string='X-ray Area',
        required=True,
        help='Body area to be X-rayed'
    )
    
    projection_type = fields.Selection([
        ('ap', 'Anteroposterior (AP)'),
        ('pa', 'Posteroanterior (PA)'),
        ('lateral', 'Lateral'),
        ('oblique', 'Oblique'),
    ], string='Projection Type',
       required=True,
       help='Type of X-ray projection')
    
    price = fields.Float(
        string='Price',
        digits='Product Price',
        required=True,
        default=0.0,
        help='Price for this X-ray'
    )
    
    images = fields.Many2many(
        'ir.attachment',
        'xray_line_attachment_rel',
        'line_id',
        'attachment_id',
        string='X-ray Images',
        help='Upload X-ray images for this line'
    )
    
    image_count = fields.Integer(
        string='Number of Images',
        compute='_compute_image_count',
        store=True
    )
    
    @api.depends('area_id', 'projection_type')
    def _compute_name(self):
        for line in self:
            if line.area_id and line.projection_type:
                projection_name = dict(line._fields['projection_type'].selection).get(line.projection_type, '')
                line.name = f"{line.area_id.name} - {projection_name}"
            else:
                line.name = _("X-ray Line")
    
    @api.depends('images')
    def _compute_image_count(self):
        for line in self:
            line.image_count = len(line.images)
    
    @api.constrains('price')
    def _check_price(self):
        for line in self:
            if line.price < 0:
                raise ValidationError(_("Price cannot be negative"))
