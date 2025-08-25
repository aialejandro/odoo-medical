# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MedicalAffectedApparatus(models.Model):
    _name = 'medical.affected.apparatus'
    _description = 'Medical Affected Apparatus'
    _order = 'name'

    name = fields.Char(
        string='Apparatus Name',
        required=True,
        translate=True,
        help='Name of the affected apparatus'
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        help='Set to false to hide this apparatus without removing it'
    )
    
    description = fields.Text(
        string='Description',
        translate=True,
        help='Additional description for the apparatus'
    )
    
    therapy_count = fields.Integer(
        string='Therapy Count',
        compute='_compute_therapy_count',
        help='Number of therapies using this apparatus'
    )
    
    @api.depends('therapy_ids')
    def _compute_therapy_count(self):
        for record in self:
            record.therapy_count = len(record.therapy_ids)
    
    therapy_ids = fields.One2many(
        comodel_name='medical.therapy',
        inverse_name='affected_apparatus_id',
        string='Related Therapies',
        help='Therapies using this apparatus'
    )
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The apparatus name must be unique!'),
    ]
    
    def action_view_therapies(self):
        """Open therapies using this apparatus"""
        self.ensure_one()
        action = self.env.ref('odoo_medical.action_medical_therapy').read()[0]
        if self.therapy_count > 1:
            action['domain'] = [('affected_apparatus_id', '=', self.id)]
        elif self.therapy_count == 1:
            action['views'] = [(self.env.ref('odoo_medical.view_medical_therapy_form').id, 'form')]
            action['res_id'] = self.therapy_ids.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
