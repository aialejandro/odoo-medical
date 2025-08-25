# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MedicalSessionRecord(models.Model):
    _name = 'medical.session.record'
    _description = 'Medical Session Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'therapy_id, session_sequence, entry_datetime desc'

    name = fields.Char(
        string='Record Name',
        compute='_compute_name',
        store=True,
        help='Computed name for the session record'
    )
    
    therapy_id = fields.Many2one(
        comodel_name='medical.therapy',
        string='Therapy',
        required=True,
        ondelete='cascade',
        help='Related therapy'
    )
    
    session_id = fields.Many2one(
        comodel_name='medical.treatment.session',
        string='Treatment Session',
        required=True,
        help='Reference to the treatment session template'
    )
    
    session_sequence = fields.Integer(
        related='session_id.sequence',
        string='Session Sequence',
        store=True,
        help='Sequence of the session in treatment'
    )
    
    entry_datetime = fields.Datetime(
        string='Entry Date and Time',
        help='Date and time when the session started'
    )
    
    exit_datetime = fields.Datetime(
        string='Exit Date and Time',
        help='Date and time when the session ended'
    )
    
    evolution = fields.Text(
        string='Evolution',
        help='Patient evolution during this session'
    )
    
    observations = fields.Text(
        string='Observations',
        help='Additional observations from the therapist'
    )
    
    therapist_id = fields.Many2one(
        comodel_name='res.users',
        string='Therapist',
        help='Therapist who conducted the session'
    )
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='State', default='draft', help='State of the session record')
    
    duration_minutes = fields.Integer(
        string='Actual Duration (Minutes)',
        compute='_compute_duration_minutes',
        store=True,
        help='Actual duration of the session in minutes'
    )
    
    patient_id = fields.Many2one(
        related='therapy_id.patient_id',
        string='Patient',
        store=True,
        help='Patient receiving the therapy'
    )
    
    @api.depends('therapy_id', 'session_id', 'entry_datetime')
    def _compute_name(self):
        for record in self:
            if record.therapy_id and record.session_id:
                patient_name = record.therapy_id.patient_id.name or 'Unknown Patient'
                session_name = record.session_id.name or 'Unknown Session'
                date_str = ''
                if record.entry_datetime:
                    date_str = f" - {record.entry_datetime.strftime('%Y-%m-%d %H:%M')}"
                record.name = f"{patient_name} - {session_name}{date_str}"
            else:
                record.name = 'New Session Record'
    
    @api.depends('entry_datetime', 'exit_datetime')
    def _compute_duration_minutes(self):
        for record in self:
            if record.entry_datetime and record.exit_datetime:
                delta = record.exit_datetime - record.entry_datetime
                record.duration_minutes = int(delta.total_seconds() / 60)
            else:
                record.duration_minutes = 0
    
    @api.onchange('entry_datetime')
    def _onchange_entry_datetime(self):
        if self.entry_datetime and self.state == 'draft':
            self.state = 'in_progress'
    
    @api.onchange('exit_datetime')
    def _onchange_exit_datetime(self):
        if self.exit_datetime and self.entry_datetime and self.state == 'in_progress':
            self.state = 'completed'
