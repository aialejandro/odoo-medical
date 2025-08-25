# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MedicalTreatment(models.Model):
    _name = 'medical.treatment'
    _description = 'Medical Treatment'
    _order = 'name'

    name = fields.Char(
        string='Treatment Name',
        required=True,
        translate=True,
        help='Name of the medical treatment'
    )
    
    code = fields.Char(
        string='Treatment Code',
        help='Internal code for the treatment'
    )
    
    session_ids = fields.One2many(
        comodel_name='medical.treatment.session',
        inverse_name='treatment_id',
        string='Treatment Sessions',
        help='Sessions that compose this treatment'
    )
    
    description = fields.Text(
        string='Description',
        translate=True,
        help='Detailed description of the treatment'
    )
    
    objectives = fields.Html(
        string='Treatment Objectives',
        translate=True,
        help='Main objectives of this treatment'
    )
    
    contraindications = fields.Html(
        string='Contraindications',
        translate=True,
        help='Medical contraindications for this treatment'
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        help='Set to false to hide this treatment without removing it'
    )
    
    price = fields.Float(
        string='Price',
        digits='Product Price',
        help='Price for this medical treatment'
    )
    
    session_count = fields.Integer(
        string='Sessions Count',
        compute='_compute_session_count',
        help='Number of sessions in this treatment'
    )
    
    total_estimated_duration = fields.Integer(
        string='Total Estimated Duration (Minutes)',
        compute='_compute_total_estimated_duration',
        store=True,
        help='Total estimated duration for all sessions'
    )
    
    therapy_count = fields.Integer(
        string='Therapy Count',
        compute='_compute_therapy_count',
        help='Number of therapies using this treatment'
    )
    
    @api.depends('session_ids')
    def _compute_session_count(self):
        for record in self:
            record.session_count = len(record.session_ids)
    
    @api.depends('session_ids.estimated_duration')
    def _compute_total_estimated_duration(self):
        for record in self:
            total_duration = sum(
                session.estimated_duration or 0 
                for session in record.session_ids
            )
            record.total_estimated_duration = total_duration
    
    @api.depends('therapy_ids')
    def _compute_therapy_count(self):
        for record in self:
            record.therapy_count = len(record.therapy_ids)
    
    therapy_ids = fields.One2many(
        comodel_name='medical.therapy',
        inverse_name='treatment_id',
        string='Related Therapies',
        help='Therapies using this treatment'
    )
    
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'The treatment code must be unique!'),
    ]
    
    def action_view_sessions(self):
        """Open sessions of this treatment"""
        self.ensure_one()
        action = self.env.ref('odoo_medical.action_medical_treatment_session').read()[0]
        if self.session_count > 1:
            action['domain'] = [('treatment_id', '=', self.id)]
        elif self.session_count == 1:
            action['views'] = [(self.env.ref('odoo_medical.view_medical_treatment_session_form').id, 'form')]
            action['res_id'] = self.session_ids.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
    
    def action_view_therapies(self):
        """Open therapies using this treatment"""
        self.ensure_one()
        action = self.env.ref('odoo_medical.action_medical_therapy').read()[0]
        if self.therapy_count > 1:
            action['domain'] = [('treatment_id', '=', self.id)]
        elif self.therapy_count == 1:
            action['views'] = [(self.env.ref('odoo_medical.view_medical_therapy_form').id, 'form')]
            action['res_id'] = self.therapy_ids.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
