# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MedicalTreatmentSession(models.Model):
    _name = 'medical.treatment.session'
    _description = 'Medical Treatment Session'
    _order = 'sequence, name'

    name = fields.Char(
        string='Session Name',
        required=True,
        translate=True,
        help='Name of the treatment session'
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Used to order sessions in treatment'
    )
    
    treatment_id = fields.Many2one(
        comodel_name='medical.treatment',
        string='Treatment',
        ondelete='cascade',
        help='Treatment this session belongs to'
    )
    
    treatment_component_ids = fields.Many2many(
        comodel_name='medical.treatment.component',
        relation='medical_session_component_rel',
        column1='session_id',
        column2='component_id',
        string='Treatment Components',
        help='Components that make up this session'
    )
    
    description = fields.Text(
        string='Description',
        translate=True,
        help='Description of the session objectives and procedures'
    )
    
    estimated_duration = fields.Integer(
        string='Estimated Duration (Minutes)',
        compute='_compute_estimated_duration',
        store=True,
        help='Total estimated duration based on components'
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        help='Set to false to hide this session without removing it'
    )
    
    component_count = fields.Integer(
        string='Components Count',
        compute='_compute_component_count',
        help='Number of components in this session'
    )
    
    @api.depends('treatment_component_ids')
    def _compute_component_count(self):
        for record in self:
            record.component_count = len(record.treatment_component_ids)
    
    @api.depends('treatment_component_ids.duration_minutes')
    def _compute_estimated_duration(self):
        for record in self:
            total_duration = sum(
                component.duration_minutes or 0 
                for component in record.treatment_component_ids
            )
            record.estimated_duration = total_duration
    
    def action_view_components(self):
        """Open components of this session"""
        self.ensure_one()
        action = self.env.ref('odoo_medical.action_medical_treatment_component').read()[0]
        if self.component_count > 1:
            action['domain'] = [('session_ids', 'in', [self.id])]
        elif self.component_count == 1:
            action['views'] = [(self.env.ref('odoo_medical.view_medical_treatment_component_form').id, 'form')]
            action['res_id'] = self.treatment_component_ids.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
