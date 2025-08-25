# -*- coding: utf-8 -*-

from odoo.tests import TransactionCase
from odoo.exceptions import UserError


class TestMedicalTreatmentTherapyPricing(TransactionCase):

    def setUp(self):
        super(TestMedicalTreatmentTherapyPricing, self).setUp()
        
        # Create test patient
        self.patient = self.env['res.partner'].create({
            'name': 'Test Patient',
        })
        
        # Create test affected apparatus
        self.apparatus = self.env['medical.affected.apparatus'].create({
            'name': 'Test Apparatus',
            'code': 'TEST',
        })
        
        # Create test treatment with price
        self.treatment = self.env['medical.treatment'].create({
            'name': 'Test Treatment',
            'code': 'TT001',
            'price': 150.0,
        })
        
        # Create test product for therapy
        self.therapy_product = self.env['product.product'].create({
            'name': 'Therapy Service',
            'type': 'service',
        })
        
        # Create test tax
        self.therapy_tax = self.env['account.tax'].create({
            'name': 'Test Tax',
            'amount': 10.0,
            'type_tax_use': 'sale',
        })
        
        # Create test journal
        self.therapy_journal = self.env['account.journal'].create({
            'name': 'Test Sales Journal',
            'code': 'TSJ',
            'type': 'sale',
        })

    def test_treatment_price_field(self):
        """Test that treatment has a price field"""
        self.assertEqual(self.treatment.price, 150.0)

    def test_therapy_price_onchange(self):
        """Test that therapy price is updated when treatment is selected"""
        therapy = self.env['medical.therapy'].create({
            'patient_id': self.patient.id,
            'affected_apparatus_id': self.apparatus.id,
            'treatment_id': self.treatment.id,
        })
        
        # Manually trigger the onchange (in real usage this would be automatic)
        therapy._onchange_treatment_id()
        
        # Check that price was copied from treatment
        self.assertEqual(therapy.price, self.treatment.price)

    def test_therapy_default_values(self):
        """Test that therapy loads default configuration values"""
        # Set configuration parameters
        self.env['ir.config_parameter'].sudo().set_param(
            'odoo_medical.default_therapy_product_id', self.therapy_product.id
        )
        self.env['ir.config_parameter'].sudo().set_param(
            'odoo_medical.default_therapy_tax_id', self.therapy_tax.id
        )
        self.env['ir.config_parameter'].sudo().set_param(
            'odoo_medical.default_therapy_journal_id', self.therapy_journal.id
        )
        
        # Create therapy and check default values are loaded
        therapy = self.env['medical.therapy'].create({
            'patient_id': self.patient.id,
            'affected_apparatus_id': self.apparatus.id,
            'treatment_id': self.treatment.id,
        })
        
        self.assertEqual(therapy.therapy_product_id, self.therapy_product)
        self.assertEqual(therapy.therapy_tax_id, self.therapy_tax)
        self.assertEqual(therapy.therapy_journal_id, self.therapy_journal)

    def test_therapy_invoice_creation(self):
        """Test invoice creation from therapy"""
        therapy = self.env['medical.therapy'].create({
            'patient_id': self.patient.id,
            'affected_apparatus_id': self.apparatus.id,
            'treatment_id': self.treatment.id,
            'price': 200.0,
            'therapy_product_id': self.therapy_product.id,
            'therapy_tax_id': self.therapy_tax.id,
            'therapy_journal_id': self.therapy_journal.id,
        })
        
        # Create invoice
        action = therapy.action_create_invoice()
        
        # Check that invoice was created
        self.assertTrue(therapy.invoice_id)
        self.assertEqual(therapy.invoice_id.partner_id, self.patient)
        self.assertEqual(therapy.invoice_id.move_type, 'out_invoice')
        
        # Check invoice line
        self.assertEqual(len(therapy.invoice_id.invoice_line_ids), 1)
        line = therapy.invoice_id.invoice_line_ids[0]
        self.assertEqual(line.product_id, self.therapy_product)
        self.assertEqual(line.price_unit, 200.0)
        self.assertEqual(line.quantity, 1)

    def test_therapy_invoice_validation(self):
        """Test invoice creation validation"""
        therapy = self.env['medical.therapy'].create({
            'patient_id': self.patient.id,
            'affected_apparatus_id': self.apparatus.id,
            'treatment_id': self.treatment.id,
            # Missing required fields for invoice
        })
        
        # Should raise error for missing patient
        therapy.patient_id = False
        with self.assertRaises(UserError):
            therapy.action_create_invoice()
        
        # Should raise error for missing price
        therapy.patient_id = self.patient.id
        therapy.price = 0
        with self.assertRaises(UserError):
            therapy.action_create_invoice()
        
        # Should raise error for missing product
        therapy.price = 100.0
        therapy.therapy_product_id = False
        with self.assertRaises(UserError):
            therapy.action_create_invoice()
