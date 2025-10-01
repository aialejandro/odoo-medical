# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'


    doctor_license = fields.Char(
        string='Doctor License Number',
        tracking=True,
        help="License number associated with the doctor"
    )

    # Historia Clínica Secuencial
    medical_record_number = fields.Char(
        string='Medical Record Number',
        copy=False,
        readonly=True,
        help="Sequential medical record number"
    )

    # Campo computed para contar las consultas médicas
    consultation_count = fields.Integer(
        string='Consultation Count',
        compute='_compute_consultation_count'
    )

    @api.depends('consultation_ids')
    def _compute_consultation_count(self):
        for partner in self:
            partner.consultation_count = len(partner.consultation_ids)

    # Relación one2many con las consultas médicas
    consultation_ids = fields.One2many(
        'medical.consultation',
        'patient_id',
        string='Medical Consultations'
    )

    # Relación one2many con las terapias médicas
    therapy_ids = fields.One2many(
        'medical.therapy',
        'patient_id',
        string='Medical Therapies'
    )

    # Campo computed para contar las terapias médicas
    therapy_count = fields.Integer(
        string='Therapy Count',
        compute='_compute_therapy_count'
    )

    @api.depends('therapy_ids')
    def _compute_therapy_count(self):
        for partner in self:
            partner.therapy_count = len(partner.therapy_ids)

    @api.model_create_multi
    def create(self, vals_list):
        """Generar número de historia clínica secuencial al crear un partner"""
        for vals in vals_list:
            if not vals.get('medical_record_number'):
                vals['medical_record_number'] = self.env['ir.sequence'].next_by_code('medical.record') or 'New'
        return super(ResPartner, self).create(vals_list)
