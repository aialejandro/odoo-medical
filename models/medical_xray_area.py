# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class MedicalXrayArea(models.Model):
    _name = 'medical.xray.area'
    _description = 'X-ray Area'
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char(
        string='Area Name',
        required=True,
        translate=True,
        help='Name of the X-ray area (e.g., Chest, Spine, Abdomen)'
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        help='If unchecked, it will allow you to hide the area without removing it'
    )
    
    description = fields.Text(
        string='Description',
        translate=True,
        help='Additional information about the X-ray area'
    )
