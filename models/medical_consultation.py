# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class MedicalConsultation(models.Model):
    _name = 'medical.consultation'
    _description = 'Medical Consultation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'consultation_date desc'

    # Basic Information
    name = fields.Char(string='Consultation Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    patient_id = fields.Many2one('res.partner', string='Patient', required=True, tracking=True,
                                domain="[('is_company', '=', False)]")
    patient_vat = fields.Char(string='Patient VAT', related='patient_id.vat', store=True, readonly=True)
    birth_date = fields.Date(string='Birth Date', related='patient_id.birthdate_date', store=True, readonly=False)
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    consultation_date = fields.Datetime(string='Consultation Date', required=True, default=fields.Datetime.now, tracking=True)
    doctor_id = fields.Many2one('res.users', string='Doctor', required=True, default=lambda self: self.env.user, tracking=True)
    doctor_license = fields.Char(string='Doctor License Number', tracking=True)
    state = fields.Selection([
        ('waiting', 'Waiting'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished')
    ], string='Consultation Status', default='waiting', required=True, tracking=True)
    start_datetime = fields.Datetime(string='Start Time', readonly=True)
    end_datetime = fields.Datetime(string='End Time', readonly=True)
    duration_minutes = fields.Float(string='Consultation Duration (min)', compute='_compute_duration', store=True, readonly=True)
    def action_start_consultation(self):
        for rec in self:
            if rec.state == 'waiting':
                rec.state = 'in_progress'
                rec.start_datetime = fields.Datetime.now()

    def action_finish_consultation(self):
        for rec in self:
            if rec.state == 'in_progress':
                rec.state = 'finished'
                rec.end_datetime = fields.Datetime.now()

    @api.depends('start_datetime', 'end_datetime')
    def _compute_duration(self):
        for rec in self:
            if rec.start_datetime and rec.end_datetime:
                delta = fields.Datetime.from_string(rec.end_datetime) - fields.Datetime.from_string(rec.start_datetime)
                rec.duration_minutes = delta.total_seconds() / 60.0
            else:
                rec.duration_minutes = 0.0
    
    # Vital Signs
    systolic_pressure = fields.Integer(string='Systolic Pressure (mmHg)', tracking=True)
    diastolic_pressure = fields.Integer(string='Diastolic Pressure (mmHg)', tracking=True)
    weight_kg = fields.Float(string='Weight (Kg)', digits=(5, 2), tracking=True)
    weight_lb = fields.Float(string='Weight (Lb)', digits=(5, 2), compute='_compute_weight_lb', 
                            inverse='_set_weight_lb', store=True, tracking=True)
    
    # Medical Background
    medical_history_ids = fields.One2many(related='patient_id.medical_history_ids', readonly=False)
    
    # Consultation Type and Reason
    consultation_type = fields.Selection([
        ('first_time', 'First Time'),
        ('follow_up', 'Follow-up'),
        ('post_operative', 'Post-operative Control'),
        ('wound_care', 'Wound Care')
    ], string='Consultation Type', required=True, tracking=True)
    consultation_reason = fields.Text(string='Consultation Reason', required=True, tracking=True)
    cie10_code = fields.Many2one('medical.icd10', string='ICD-10 Code', tracking=True,
                                help='International Classification of Diseases 10th Revision code for the diagnosis')
    
    # Medical Information
    diagnosis = fields.Text(string='Diagnosis', tracking=True)
    treatment_description = fields.Text(string='Treatment Description', tracking=True)
    prescription_line_ids = fields.One2many('medical.prescription.line', 'consultation_id', string='Medical Prescription')
    evolution = fields.Text(string='Evolution', tracking=True)
    observations = fields.Text(string='Observations', tracking=True)
    next_appointment_date = fields.Date(string='Next Appointment Date', tracking=True)
    
    # Campos adicionales solicitados
    has_symptoms = fields.Boolean(string='Has Symptoms', tracking=True, help="Indicates if the patient presents symptoms")
    
    work_restriction_type = fields.Selection([
        ('isolation', 'Isolation'),
        ('absolute_rest', 'Absolute Rest'),
        ('telework', 'Telework'),
        ('none', 'None')
    ], string='Work Restriction Type', tracking=True, help="Type of work restriction recommended")
    
    medical_cause = fields.Selection([
        ('general_illness', 'General Illness'),
        ('work_accident', 'Work Accident'),
        ('traffic_accident', 'Traffic Accident'),
        ('maternity', 'Maternity'),
        ('catastrophic_illness', 'Catastrophic Illness')
    ], string='Medical Cause', tracking=True, help="Cause of the medical condition")
    
    rest_days = fields.Integer(string='Rest Days', tracking=True, help="Number of rest days prescribed")
    rest_start_date = fields.Date(string='Rest Start Date', tracking=True, help="Start date of medical rest")
    rest_end_date = fields.Date(string='Rest End Date', tracking=True, help="End date of medical rest")
    
    
    # Payment Information
    consultation_fee = fields.Float(string='Consultation Fee', digits=(12, 2), tracking=True)
    discount_percentage = fields.Float(string='Discount (%)', digits=(5, 2), tracking=True)
    total_to_pay = fields.Float(string='Total to Pay', compute='_compute_total_to_pay', store=True, tracking=True)

    # Defaulted fields from settings
    consultation_product_id = fields.Many2one(
        'product.product',
        string='Default Consultation Item',
        default=lambda self: self.env['ir.config_parameter'].sudo().get_param('odoo_medical.default_consultation_product_id') and int(self.env['ir.config_parameter'].sudo().get_param('odoo_medical.default_consultation_product_id')) or False,
        required=True,
        tracking=True,
    )
    consultation_tax_id = fields.Many2one(
        'account.tax',
        string='Default Consultation Tax',
        default=lambda self: self.env['ir.config_parameter'].sudo().get_param('odoo_medical.default_consultation_tax_id') and int(self.env['ir.config_parameter'].sudo().get_param('odoo_medical.default_consultation_tax_id')) or False,
        tracking=True,
    )
    consultation_journal_id = fields.Many2one(
        'account.journal',
        string='Default Consultation Journal',
        default=lambda self: self.env['ir.config_parameter'].sudo().get_param('odoo_medical.default_consultation_journal_id') and int(self.env['ir.config_parameter'].sudo().get_param('odoo_medical.default_consultation_journal_id')) or False,
        tracking=True,
    )

    def action_create_invoice(self):
        self.ensure_one()
        if not self.consultation_product_id or not self.consultation_journal_id:
            raise ValidationError(_('You must configure the consultation item and journal.'))
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.patient_id.id,
            'journal_id': self.consultation_journal_id.id,
            'invoice_date': fields.Date.context_today(self),
            'invoice_line_ids': [
                (0, 0, {
                    'product_id': self.consultation_product_id.id,
                    'name': self.consultation_product_id.name,
                    'quantity': 1,
                    'price_unit': self.consultation_fee,
                    'discount': self.discount_percentage or 0.0,
                    'tax_ids': [(6, 0, [self.consultation_tax_id.id]) if self.consultation_tax_id else (5,)],
                })
            ],
            'ref': self.name,
        }
        invoice = self.env['account.move'].create(invoice_vals)
        return {
            'type': 'ir.actions.act_window',
            'name': _('Consultation Invoice'),
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
        }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('medical.consultation') or _('New')
        return super(MedicalConsultation, self).create(vals_list)

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        """Enable search by patient VAT number"""
        args = args or []
        if name:
            # Search by consultation name, patient name, or patient VAT
            domain = ['|', '|', 
                     ('name', operator, name),
                     ('patient_id.name', operator, name),
                     ('patient_vat', operator, name)]
            records = self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)
            return records
        return super()._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = date.today()
                record.age = today.year - record.birth_date.year - ((today.month, today.day) < (record.birth_date.month, record.birth_date.day))
            else:
                record.age = 0

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

    @api.depends('consultation_fee', 'discount_percentage')
    def _compute_total_to_pay(self):
        for record in self:
            if record.consultation_fee and record.discount_percentage:
                discount_amount = record.consultation_fee * (record.discount_percentage / 100)
                record.total_to_pay = record.consultation_fee - discount_amount
            else:
                record.total_to_pay = record.consultation_fee

    @api.constrains('systolic_pressure', 'diastolic_pressure')
    def _check_blood_pressure(self):
        for record in self:
            if record.systolic_pressure and record.diastolic_pressure:
                if record.systolic_pressure <= record.diastolic_pressure:
                    raise ValidationError(_('Systolic pressure must be higher than diastolic pressure.'))

    @api.constrains('discount_percentage')
    def _check_discount_percentage(self):
        for record in self:
            if record.discount_percentage and (record.discount_percentage < 0 or record.discount_percentage > 100):
                raise ValidationError(_('Discount percentage must be between 0 and 100.'))

    @api.constrains('rest_start_date', 'rest_end_date')
    def _check_rest_dates(self):
        for record in self:
            if record.rest_start_date and record.rest_end_date:
                if record.rest_start_date > record.rest_end_date:
                    raise ValidationError(_('Rest start date must be before rest end date.'))

    @api.constrains('rest_days')
    def _check_rest_days(self):
        for record in self:
            if record.rest_days and record.rest_days < 0:
                raise ValidationError(_('Rest days must be a positive number.'))

    @api.onchange('rest_start_date', 'rest_days')
    def _onchange_rest_dates(self):
        """Automatically calculate rest end date based on start date and rest days"""
        if self.rest_start_date and self.rest_days:
            from datetime import timedelta
            self.rest_end_date = self.rest_start_date + timedelta(days=self.rest_days - 1)

    @api.onchange('rest_start_date', 'rest_end_date')
    def _onchange_calculate_rest_days(self):
        """Automatically calculate rest days based on start and end dates"""
        if self.rest_start_date and self.rest_end_date:
            delta = self.rest_end_date - self.rest_start_date
            self.rest_days = delta.days + 1

    def action_print_private_certificate(self):
        """Generate private medical certificate"""
        self.ensure_one()
        if self.state != 'finished':
            raise ValidationError(_('Medical certificate can only be generated for finished consultations.'))
        
        # Buscar el reporte por su nombre
        report = self.env['ir.actions.report'].search([
            ('report_name', '=', 'odoo_medical.report_private_medical_certificate')
        ], limit=1)
        
        if report:
            return report.report_action(self)
        else:
            # Fallback si el reporte no está disponible
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': _('Private medical certificate report is not available yet. Please update the module.'),
                    'type': 'warning',
                }
            }

    def action_print_iess_certificate(self):
        """Generate IESS medical certificate"""
        self.ensure_one()
        if self.state != 'finished':
            raise ValidationError(_('Medical certificate can only be generated for finished consultations.'))
        
        # Buscar el reporte por su nombre
        report = self.env['ir.actions.report'].search([
            ('report_name', '=', 'odoo_medical.report_iess_medical_certificate')
        ], limit=1)
        
        if report:
            return report.report_action(self)
        else:
            # Fallback si el reporte no está disponible
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': _('IESS medical certificate report is not available yet. Please update the module.'),
                    'type': 'warning',
                }
            }


class MedicalPrescriptionLine(models.Model):
    _name = 'medical.prescription.line'
    _description = 'Medical Prescription Line'

    consultation_id = fields.Many2one('medical.consultation', string='Consultation', required=True, ondelete='cascade')
    medication_name = fields.Char(string='Medication Name', required=True)
    pharmaceutical_form = fields.Selection([
        ('syrup', 'Syrup'),
        ('tablet', 'Tablet'),
        ('capsule', 'Capsule'),
        ('injection', 'Injection'),
        ('cream', 'Cream'),
        ('ointment', 'Ointment'),
        ('drops', 'Drops'),
        ('solution', 'Solution'),
        ('powder', 'Powder'),
        ('spray', 'Spray')
    ], string='Pharmaceutical Form', required=True)
    concentration = fields.Float(string='Concentration', required=True)
    concentration_unit = fields.Selection([
        ('mg', 'mg'),
        ('g', 'g'),
        ('ml', 'ml'),
        ('mcg', 'mcg'),
        ('iu', 'IU'),
        ('percent', '%')
    ], string='Concentration Unit', required=True)
    quantity_to_dispense = fields.Float(string='Quantity to Dispense', required=True)
    posology = fields.Text(string='Posology', required=True)

    @api.constrains('concentration', 'quantity_to_dispense')
    def _check_positive_values(self):
        for record in self:
            if record.concentration <= 0:
                raise ValidationError(_('Concentration must be greater than zero.'))
            if record.quantity_to_dispense <= 0:
                raise ValidationError(_('Quantity to dispense must be greater than zero.'))
