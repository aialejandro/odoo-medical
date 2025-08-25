# -*- coding: utf-8 -*-
# pyright: reportMissingImports=false
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MedicalIcd10Group(models.Model):
    _name = 'medical.icd10.group'
    _description = 'ICD-10 Group'
    _rec_name = 'display_name'
    _parent_name = 'parent_id'
    _parent_store = True
    _order = 'sequence, code, name'

    name = fields.Char(string='Group Name', required=True, translate=True)
    code = fields.Char(string='Group Code', help='Optional code for the group (e.g., A00-B99)')
    description = fields.Text(string='Description', translate=True)
    parent_id = fields.Many2one('medical.icd10.group', string='Parent Group', ondelete='cascade', index=True)
    child_ids = fields.One2many('medical.icd10.group', 'parent_id', string='Child Groups')
    parent_path = fields.Char(index=True)
    sequence = fields.Integer(default=10, help='Sequence for ordering groups')
    display_name = fields.Char(compute='_compute_display_name', store=True)
    
    # Related ICD-10 codes
    icd10_ids = fields.One2many('medical.icd10', 'group_id', string='ICD-10 Codes')
    
    # Statistics
    icd10_count = fields.Integer(string='Direct ICD-10 Codes', compute='_compute_icd10_count')
    total_icd10_count = fields.Integer(string='Total ICD-10 Codes', compute='_compute_total_icd10_count')

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Group code must be unique.'),
    ]

    @api.depends('code', 'name')
    def _compute_display_name(self):
        for rec in self:
            if rec.code and rec.name:
                rec.display_name = f"{rec.code} - {rec.name}"
            else:
                rec.display_name = rec.name or rec.code

    def _compute_icd10_count(self):
        for group in self:
            group.icd10_count = self.env['medical.icd10'].search_count([('group_id', '=', group.id)])

    def _compute_total_icd10_count(self):
        for group in self:
            # Count ICD-10 codes in this group and all child groups
            child_groups = self.search([('parent_path', '=like', group.parent_path + '%')])
            group.total_icd10_count = self.env['medical.icd10'].search_count([('group_id', 'in', child_groups.ids)])

    @api.constrains('parent_id')
    def _check_parent_recursion(self):
        if self._has_cycle():
            raise UserError(_('You cannot create recursive group hierarchies.'))


class MedicalIcd10(models.Model):
    _name = 'medical.icd10'
    _description = 'ICD-10 Code'
    _rec_name = 'display_name'
    _order = 'code'

    code = fields.Char(required=True, index=True)
    description = fields.Char(required=True, translate=True)
    group_id = fields.Many2one('medical.icd10.group', string='ICD-10 Group', index=True, 
                               help='Assign this code to a specific ICD-10 group')
    chapter = fields.Char(translate=True, help='Optional ICD-10 chapter (deprecated - use group_id instead)')
    display_name = fields.Char(compute='_compute_display_name', store=True)

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'ICD-10 code must be unique.'),
    ]

    @api.depends('code', 'description')
    def _compute_display_name(self):
        for rec in self:
            if rec.code and rec.description:
                rec.display_name = f"{rec.code} - {rec.description}"
            else:
                rec.display_name = rec.code or rec.description


class MedicalHistory(models.Model):
    _name = 'medical.history'
    _description = 'Patient History Entry'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_record desc, id desc'

    partner_id = fields.Many2one('res.partner', string='Patient', required=True, index=True, ondelete='restrict')

    category = fields.Selection(
        selection=[
            ('medical', 'Medical'),
            ('surgical', 'Surgical'),
            ('social', 'Social'),
            ('obstetric', 'Gyneco-Obstetric'),
            ('allergy', 'Allergy'),
        ],
        string='Category', required=True, tracking=True, index=True,
    )

    icd10_id = fields.Many2one('medical.icd10', string='ICD-10', tracking=True, help='Search and assign ICD-10 code and description')

    name = fields.Char(string='History Title', required=True, tracking=True, translate=True)
    description = fields.Text(string='Notes', translate=True)

    date_record = fields.Date(string='Record Date', default=fields.Date.context_today, required=True, tracking=True)
    event_date = fields.Date(string='Event Date', help='If different from the record date (e.g., date of surgery/event)')

    state = fields.Selection(
        selection=[
            ('active', 'Active'),
            ('resolved', 'Resolved'),
            ('chronic', 'Chronic'),
            ('inactive', 'Inactive'),
        ],
        string='Status', default='active', required=True, tracking=True, index=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        recs = super().create(vals_list)
        for rec in recs:
            # Usar self.env._() para asegurar la traducción correcta
            # El contexto de idioma se hereda automáticamente del usuario actual
            rec.message_post(body=self.env._('History created'))
        return recs

    def unlink(self):
        raise UserError(_('History entries cannot be deleted. Set status to "Inactive" or "Resolved" instead.'))


class ResPartner(models.Model):
    _inherit = 'res.partner'

    medical_history_ids = fields.One2many('medical.history', 'partner_id', string='Past History')
    
    # Weight fields
    weight_kg = fields.Float(string='Weight (Kg)', digits=(5, 2))
    weight_lb = fields.Float(string='Weight (Lb)', digits=(5, 2), 
                            compute='_compute_weight_lb', inverse='_set_weight_lb', store=True)
    
    # Age calculation
    age = fields.Integer(string='Age', compute='_compute_age', store=True)

    @api.depends('weight_kg')
    def _compute_weight_lb(self):
        for record in self:
            if record.weight_kg:
                record.weight_lb = record.weight_kg * 2.20462
            else:
                record.weight_lb = 0.0

    def _set_weight_lb(self):
        for record in self:
            if record.weight_lb:
                record.weight_kg = record.weight_lb / 2.20462

    @api.depends('birthdate_date')
    def _compute_age(self):
        from datetime import date
        for record in self:
            if record.birthdate_date:
                today = date.today()
                record.age = today.year - record.birthdate_date.year - ((today.month, today.day) < (record.birthdate_date.month, record.birthdate_date.day))
            else:
                record.age = 0
