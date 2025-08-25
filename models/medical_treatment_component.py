# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MedicalTreatmentComponent(models.Model):
    _name = 'medical.treatment.component'
    _description = 'Medical Treatment Component'
    _order = 'sequence, name'

    name = fields.Char(
        string='Component Name',
        required=True,
        translate=True,
        help='Name of the treatment component'
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Used to order components'
    )
    
    session_ids = fields.Many2many(
        comodel_name='medical.treatment.session',
        relation='medical_session_component_rel',
        column1='component_id',
        column2='session_id',
        string='Treatment Sessions',
        help='Sessions this component is used in'
    )
    
    description = fields.Text(
        string='Description',
        translate=True,
        help='Detailed description of the component'
    )
    
    duration_minutes = fields.Integer(
        string='Duration (Minutes)',
        help='Expected duration in minutes for this component'
    )
    
    instructions = fields.Html(
        string='Instructions',
        translate=True,
        help='Specific instructions for this component'
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        help='Set to false to hide this component without removing it'
    )
    
    session_count = fields.Integer(
        string='Sessions Count',
        compute='_compute_session_count',
        help='Number of sessions using this component'
    )
    
    @api.depends('session_ids')
    def _compute_session_count(self):
        for record in self:
            record.session_count = len(record.session_ids)
    
    def action_view_sessions(self):
        """Open sessions that use this component"""
        self.ensure_one()
        action = self.env.ref('odoo_medical.action_medical_treatment_session').read()[0]
        if self.session_count > 1:
            action['domain'] = [('treatment_component_ids', 'in', [self.id])]
        elif self.session_count == 1:
            action['views'] = [(self.env.ref('odoo_medical.view_medical_treatment_session_form').id, 'form')]
            action['res_id'] = self.session_ids.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
