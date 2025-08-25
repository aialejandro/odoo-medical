# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class MedicalXrayOrder(models.Model):
    _name = 'medical.xray.order'
    _description = 'X-ray Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'date desc, id desc'

    name = fields.Char(
        string='Order Number',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
        tracking=True
    )
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='State',
       default='draft',
       required=True,
       tracking=True)
    
    patient_id = fields.Many2one(
        'res.partner',
        string='Patient',
        required=True,
        domain=[('is_company', '=', False)],
        tracking=True,
        help='Patient for whom the X-ray is ordered'
    )
    
    date = fields.Datetime(
        string='Order Date',
        required=True,
        default=fields.Datetime.now,
        tracking=True,
        help='Date when the X-ray order was created'
    )
    
    line_ids = fields.One2many(
        'medical.xray.order.line',
        'xray_order_id',
        string='X-ray Lines',
        copy=True,
        help='List of X-rays to be taken'
    )
    
    total_price = fields.Float(
        string='Total Price',
        compute='_compute_total_price',
        store=True,
        digits='Product Price',
        tracking=True
    )
    
    # Invoice related fields
    journal_id = fields.Many2one(
        'account.journal',
        string='Journal',
        compute='_compute_default_invoice_fields',
        store=True,
        help='Journal for invoice creation'
    )
    
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        compute='_compute_default_invoice_fields',
        store=True,
        help='Product for invoice creation'
    )
    
    tax_id = fields.Many2one(
        'account.tax',
        string='Tax',
        compute='_compute_default_invoice_fields',
        store=True,
        help='Tax for invoice creation'
    )
    
    invoice_id = fields.Many2one(
        'account.move',
        string='Invoice',
        readonly=True,
        copy=False,
        help='Generated invoice'
    )
    
    invoice_state = fields.Selection(
        related='invoice_id.state',
        string='Invoice Status',
        readonly=True
    )
    
    notes = fields.Text(
        string='Notes',
        help='Additional notes for the X-ray order'
    )
    
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('medical.xray.order') or _('New')
        return super().create(vals_list)

    @api.depends('line_ids.price')
    def _compute_total_price(self):
        for order in self:
            order.total_price = sum(order.line_ids.mapped('price'))

    @api.depends('company_id')
    def _compute_default_invoice_fields(self):
        for order in self:
            # Get default values from system parameters
            order.journal_id = self.env['ir.config_parameter'].sudo().get_param(
                'odoo_medical.default_xray_journal_id', False)
            order.product_id = self.env['ir.config_parameter'].sudo().get_param(
                'odoo_medical.default_xray_product_id', False)
            order.tax_id = self.env['ir.config_parameter'].sudo().get_param(
                'odoo_medical.default_xray_tax_id', False)

    def action_confirm(self):
        """Confirm the X-ray order"""
        for order in self:
            if not order.line_ids:
                raise ValidationError(_("Cannot confirm an order without X-ray lines."))
            order.state = 'confirmed'
        return True

    def action_start(self):
        """Start the X-ray process"""
        for order in self:
            if order.state != 'confirmed':
                raise ValidationError(_("Only confirmed orders can be started."))
            order.state = 'in_progress'
        return True

    def action_done(self):
        """Mark the X-ray order as done"""
        for order in self:
            if order.state != 'in_progress':
                raise ValidationError(_("Only orders in progress can be marked as done."))
            order.state = 'done'
        return True

    def action_cancel(self):
        """Cancel the X-ray order"""
        for order in self:
            if order.invoice_id and order.invoice_id.state == 'posted':
                raise ValidationError(_("Cannot cancel an order with a posted invoice."))
            order.state = 'cancelled'
        return True

    def action_create_invoice(self):
        """Create invoice for the X-ray order"""
        for order in self:
            if order.invoice_id:
                raise UserError(_("Invoice already exists for this order."))
            
            if order.state not in ['done']:
                raise ValidationError(_("You can only create invoices for completed orders."))
            
            if not order.journal_id:
                raise ValidationError(_("Please configure the default X-ray journal in settings."))
            
            if not order.product_id:
                raise ValidationError(_("Please configure the default X-ray product in settings."))
            
            # Prepare invoice values
            invoice_vals = {
                'partner_id': order.patient_id.id,
                'move_type': 'out_invoice',
                'journal_id': int(order.journal_id),
                'invoice_date': fields.Date.today(),
                'ref': order.name,
                'invoice_line_ids': [(0, 0, {
                    'name': f"X-ray Order: {order.name}",
                    'product_id': int(order.product_id),
                    'quantity': 1,
                    'price_unit': order.total_price,
                    'tax_ids': [(6, 0, [int(order.tax_id)])] if order.tax_id else [],
                })],
            }
            
            # Create invoice
            invoice = self.env['account.move'].create(invoice_vals)
            order.invoice_id = invoice.id
            
            return {
                'name': _('Invoice'),
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'res_id': invoice.id,
                'view_mode': 'form',
                'target': 'current',
            }

    def action_view_invoice(self):
        """View the generated invoice"""
        self.ensure_one()
        if not self.invoice_id:
            return False
        
        return {
            'name': _('Invoice'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': self.invoice_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
