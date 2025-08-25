# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    medical_default_consultation_product_id = fields.Many2one(
        'product.product',
        string='Default Consultation Item',
        config_parameter='odoo_medical.default_consultation_product_id',
    )
    medical_default_consultation_tax_id = fields.Many2one(
        'account.tax',
        string='Default Consultation Tax',
        config_parameter='odoo_medical.default_consultation_tax_id',
    )
    medical_default_consultation_journal_id = fields.Many2one(
        'account.journal',
        string='Default Consultation Journal',
        config_parameter='odoo_medical.default_consultation_journal_id',
    )
    
    medical_default_therapy_product_id = fields.Many2one(
        'product.product',
        string='Default Therapy Product',
        config_parameter='odoo_medical.default_therapy_product_id',
        help='Default product for therapy invoicing'
    )
    medical_default_therapy_tax_id = fields.Many2one(
        'account.tax',
        string='Default Therapy Tax',
        config_parameter='odoo_medical.default_therapy_tax_id',
        help='Default tax for therapy invoicing'
    )
    medical_default_therapy_journal_id = fields.Many2one(
        'account.journal',
        string='Default Therapy Journal',
        config_parameter='odoo_medical.default_therapy_journal_id',
        help='Default journal for therapy invoicing'
    )
    
    # X-ray configuration fields
    medical_default_xray_product_id = fields.Many2one(
        'product.product',
        string='Default X-ray Product',
        config_parameter='odoo_medical.default_xray_product_id',
        help='Default product for X-ray invoicing'
    )
    medical_default_xray_tax_id = fields.Many2one(
        'account.tax',
        string='Default X-ray Tax',
        config_parameter='odoo_medical.default_xray_tax_id',
        help='Default tax for X-ray invoicing'
    )
    medical_default_xray_journal_id = fields.Many2one(
        'account.journal',
        string='Default X-ray Journal',
        config_parameter='odoo_medical.default_xray_journal_id',
        help='Default journal for X-ray invoicing'
    )
