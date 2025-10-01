# -*- coding: utf-8 -*-

from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    doctor_license = fields.Char(
        string='Doctor License Number',
        related='partner_id.doctor_license',
        store=True,
        readonly=False,
        help="License number associated with the related partner"
    )
