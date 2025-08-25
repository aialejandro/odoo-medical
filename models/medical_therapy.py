# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime


class MedicalTherapy(models.Model):
    _name = 'medical.therapy'
    _description = 'Medical Therapy'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'therapy_date desc, name'

    name = fields.Char(
        string='Therapy Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('medical.therapy') or 'New',
        help='Unique reference for this therapy'
    )
    
    patient_id = fields.Many2one(
        comodel_name='res.partner',
        string='Patient',
        required=True,
        tracking=True,
        help='Patient receiving the therapy'
    )
    
    therapy_date = fields.Date(
        string='Therapy Date',
        required=True,
        default=fields.Date.context_today,
        tracking=True,
        help='Date when the therapy is scheduled'
    )
    
    affected_apparatus_id = fields.Many2one(
        comodel_name='medical.affected.apparatus',
        string='Affected Apparatus',
        required=True,
        tracking=True,
        help='Apparatus that is being treated'
    )
    
    treatment_id = fields.Many2one(
        comodel_name='medical.treatment',
        string='Treatment',
        required=True,
        tracking=True,
        help='Treatment protocol to be applied'
    )
    
    session_record_ids = fields.One2many(
        comodel_name='medical.session.record',
        inverse_name='therapy_id',
        string='Session Records',
        help='Records of therapy sessions'
    )
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='State', default='draft', tracking=True, help='Current state of the therapy')
    
    notes = fields.Html(
        string='Therapy Notes',
        help='General notes about the therapy'
    )
    
    diagnosis = fields.Text(
        string='Diagnosis',
        help='Medical diagnosis related to this therapy'
    )
    
    start_date = fields.Date(
        string='Start Date',
        help='Date when therapy sessions actually started'
    )
    
    end_date = fields.Date(
        string='End Date',
        help='Date when therapy sessions ended'
    )
    
    total_sessions = fields.Integer(
        string='Total Sessions',
        compute='_compute_session_stats',
        store=True,
        help='Total number of sessions in this therapy'
    )
    
    completed_sessions = fields.Integer(
        string='Completed Sessions',
        compute='_compute_session_stats',
        store=True,
        help='Number of completed sessions'
    )
    
    progress_percentage = fields.Float(
        string='Progress (%)',
        compute='_compute_session_stats',
        store=True,
        help='Percentage of completed sessions'
    )
    
    attending_physician_id = fields.Many2one(
        comodel_name='res.users',
        string='Attending Physician',
        help='Physician responsible for this therapy'
    )
    
    # Pricing fields
    price = fields.Float(
        string='Therapy Price',
        digits='Product Price',
        help='Price for this therapy'
    )
    
    # Invoicing fields
    therapy_product_id = fields.Many2one(
        'product.product',
        string='Therapy Product',
        help='Product for therapy invoicing'
    )
    therapy_tax_id = fields.Many2one(
        'account.tax',
        string='Therapy Tax',
        help='Tax for therapy invoicing'
    )
    therapy_journal_id = fields.Many2one(
        'account.journal',
        string='Therapy Journal',
        help='Journal for therapy invoicing'
    )
    
    # Invoice tracking
    invoice_id = fields.Many2one(
        'account.move',
        string='Invoice',
        help='Generated invoice for this therapy',
        readonly=True
    )
    invoice_state = fields.Selection(
        related='invoice_id.state',
        string='Invoice State',
        readonly=True
    )
    
    @api.depends('session_record_ids', 'session_record_ids.state')
    def _compute_session_stats(self):
        for record in self:
            total = len(record.session_record_ids)
            completed = len(record.session_record_ids.filtered(lambda s: s.state == 'completed'))
            
            record.total_sessions = total
            record.completed_sessions = completed
            record.progress_percentage = (completed / total * 100) if total > 0 else 0.0
    
    @api.onchange('treatment_id')
    def _onchange_treatment_id(self):
        """When treatment changes, create session records based on treatment sessions and update price"""
        if self.treatment_id:
            # Update price from treatment
            self.price = self.treatment_id.price
            
            # Clear existing session records if any
            self.session_record_ids = [(5, 0, 0)]
            
            # Create new session records based on treatment sessions
            session_records = []
            for session in self.treatment_id.session_ids.sorted('sequence'):
                session_records.append((0, 0, {
                    'session_id': session.id,
                    'state': 'draft',
                }))
            
            self.session_record_ids = session_records
    
    @api.model
    def default_get(self, fields_list):
        """Load default values for therapy fields"""
        res = super(MedicalTherapy, self).default_get(fields_list)
        
        # Load default therapy product
        if 'therapy_product_id' in fields_list:
            default_product = self.env['ir.config_parameter'].sudo().get_param(
                'odoo_medical.default_therapy_product_id'
            )
            if default_product:
                res['therapy_product_id'] = int(default_product)
        
        # Load default therapy tax
        if 'therapy_tax_id' in fields_list:
            default_tax = self.env['ir.config_parameter'].sudo().get_param(
                'odoo_medical.default_therapy_tax_id'
            )
            if default_tax:
                res['therapy_tax_id'] = int(default_tax)
        
        # Load default therapy journal
        if 'therapy_journal_id' in fields_list:
            default_journal = self.env['ir.config_parameter'].sudo().get_param(
                'odoo_medical.default_therapy_journal_id'
            )
            if default_journal:
                res['therapy_journal_id'] = int(default_journal)
        
        return res
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('medical.therapy') or 'New'
        
        therapies = super(MedicalTherapy, self).create(vals_list)
        
        # Create session records if treatment is specified
        for therapy in therapies:
            if therapy.treatment_id:
                therapy._create_session_records()
        
        return therapies
    
    def _create_session_records(self):
        """Create session records based on treatment sessions"""
        self.ensure_one()
        
        if not self.treatment_id:
            return
        
        # Clear existing session records
        self.session_record_ids.unlink()
        
        # Create new session records
        for session in self.treatment_id.session_ids.sorted('sequence'):
            self.env['medical.session.record'].create({
                'therapy_id': self.id,
                'session_id': session.id,
                'state': 'draft',
            })
    
    def action_schedule(self):
        """Mark therapy as scheduled"""
        self.write({'state': 'scheduled'})
    
    def action_start(self):
        """Start the therapy"""
        self.write({
            'state': 'in_progress',
            'start_date': fields.Date.context_today(self)
        })
    
    def action_complete(self):
        """Complete the therapy"""
        self.write({
            'state': 'completed',
            'end_date': fields.Date.context_today(self)
        })
    
    def action_cancel(self):
        """Cancel the therapy"""
        self.write({'state': 'cancelled'})
    
    def action_reset_to_draft(self):
        """Reset therapy to draft state"""
        self.write({'state': 'draft'})
    
    def action_view_session_records(self):
        """Open session records for this therapy"""
        self.ensure_one()
        action = self.env.ref('odoo_medical.action_medical_session_record').read()[0]
        if self.total_sessions > 1:
            action['domain'] = [('therapy_id', '=', self.id)]
        elif self.total_sessions == 1:
            action['views'] = [(self.env.ref('odoo_medical.view_medical_session_record_form').id, 'form')]
            action['res_id'] = self.session_record_ids.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
    
    def action_view_progress(self):
        """Open progress view (placeholder for future implementation)"""
        self.ensure_one()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Progress View',
                'message': f'Progress: {self.progress_percentage:.1f}% ({self.completed_sessions}/{self.total_sessions} sessions)',
                'type': 'info',
            }
        }
    
    def action_create_invoice(self):
        """Create an invoice for this therapy"""
        self.ensure_one()
        
        if self.invoice_id:
            return {
                'name': 'Therapy Invoice',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'account.move',
                'res_id': self.invoice_id.id,
                'target': 'current',
            }
        
        # Validate required fields
        if not self.patient_id:
            raise UserError(_("Patient is required to create an invoice"))
        if not self.price:
            raise UserError(_("Price must be set to create an invoice"))
        if not self.therapy_product_id:
            raise UserError(_("Therapy product is required to create an invoice"))
        
        # Prepare invoice values
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.patient_id.id,
            'invoice_date': fields.Date.context_today(self),
            'invoice_origin': self.name,
            'journal_id': self.therapy_journal_id.id if self.therapy_journal_id else False,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.therapy_product_id.id,
                'name': f'Medical Therapy - {self.treatment_id.name}' if self.treatment_id else 'Medical Therapy',
                'quantity': 1,
                'price_unit': self.price,
                'tax_ids': [(6, 0, [self.therapy_tax_id.id])] if self.therapy_tax_id else [],
            })],
        }
        
        # Create the invoice
        invoice = self.env['account.move'].create(invoice_vals)
        self.invoice_id = invoice.id
        
        # Return action to open the created invoice
        return {
            'name': 'Therapy Invoice',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'target': 'current',
        }
