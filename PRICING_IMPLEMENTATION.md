# Medical Module Pricing and Invoicing Implementation

## Overview
This document describes the implementation of pricing and invoicing features for the `odoo_medical` module, following Odoo v18 development guidelines.

## Features Implemented

### 1. Treatment Pricing
- **Field Added**: `price` field to `medical.treatment` model
- **Type**: Float field with 'Product Price' precision
- **Location**: Added to treatment form and tree views
- **Purpose**: Store the base price for each medical treatment

### 2. Therapy Pricing with Auto-Update
- **Field Added**: `price` field to `medical.therapy` model
- **Auto-Update**: Price automatically updates when treatment is selected via `onchange` method
- **Manual Override**: Users can still manually modify the price after selection

### 3. Configuration Settings
Added new configuration parameters in Settings > Medical:

#### Default Therapy Parameters
- **therapy_product_id**: Default product for therapy invoicing
- **therapy_tax_id**: Default tax for therapy invoicing  
- **therapy_journal_id**: Default journal for therapy invoicing

These settings are automatically loaded when creating new therapies.

### 4. Therapy Invoicing Fields
Added to `medical.therapy` model:
- **therapy_product_id**: Product to use for invoicing
- **therapy_tax_id**: Tax to apply to invoice
- **therapy_journal_id**: Journal for invoice creation
- **invoice_id**: Link to generated invoice (readonly)
- **invoice_state**: Display invoice state (readonly)

### 5. Invoice Generation
- **Button**: "Create Invoice" button in therapy form
- **Smart Button**: Changes to "View Invoice" after invoice creation
- **Validation**: Ensures required fields (patient, price, product) are present
- **Auto-Creation**: Creates customer invoice with therapy details

## Code Implementation Details

### Model Changes

#### medical_treatment.py
```python
price = fields.Float(
    string='Price',
    digits='Product Price',
    help='Price for this medical treatment'
)
```

#### medical_therapy.py
```python
# Pricing fields
price = fields.Float(
    string='Therapy Price',
    digits='Product Price',
    help='Price for this therapy'
)

# Invoicing fields
therapy_product_id = fields.Many2one('product.product', string='Therapy Product')
therapy_tax_id = fields.Many2one('account.tax', string='Therapy Tax')  
therapy_journal_id = fields.Many2one('account.journal', string='Therapy Journal')
invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True)

@api.onchange('treatment_id')
def _onchange_treatment_id(self):
    if self.treatment_id:
        self.price = self.treatment_id.price
        # ... existing session creation logic

def action_create_invoice(self):
    # Validation and invoice creation logic
```

#### res_config_settings.py
```python
medical_default_therapy_product_id = fields.Many2one(
    'product.product',
    string='Default Therapy Product',
    config_parameter='odoo_medical.default_therapy_product_id'
)
medical_default_therapy_tax_id = fields.Many2one(
    'account.tax', 
    string='Default Therapy Tax',
    config_parameter='odoo_medical.default_therapy_tax_id'
)
medical_default_therapy_journal_id = fields.Many2one(
    'account.journal',
    string='Default Therapy Journal', 
    config_parameter='odoo_medical.default_therapy_journal_id'
)
```

### View Updates

#### Treatment Views
- Added `price` field to tree and form views
- Positioned in the basic information group

#### Therapy Views  
- Added invoice creation/view buttons in button box
- Added invoicing configuration group with therapy-specific fields
- Added `price` field to form and tree views
- Enhanced search view to include price field

#### Configuration Views
- Added "Medical Therapies" configuration block
- Included all three default therapy parameters

## User Workflow

### Setting Up Defaults
1. Go to Settings > Medical
2. Configure default therapy product, tax, and journal
3. Save settings

### Creating Treatment with Price
1. Go to Medical > Treatments
2. Create new treatment
3. Set name, code, and **price**
4. Configure sessions and other details

### Creating Therapy with Auto-Pricing
1. Go to Medical > Therapies  
2. Create new therapy
3. Select patient and apparatus
4. **Select treatment** → Price automatically copies
5. Default invoicing parameters load automatically
6. Modify price if needed

### Generating Invoice
1. Open existing therapy
2. Click **"Create Invoice"** button
3. System validates required fields
4. Invoice created with therapy details
5. Button changes to **"View Invoice"**

## Validation Rules

The system validates the following before invoice creation:
- Patient must be assigned
- Price must be greater than 0  
- Therapy product must be selected

Error messages follow Odoo v18 patterns using `UserError` with translatable strings.

## Technical Standards Compliance

### Odoo v18 Guidelines Followed
- ✅ All strings in English in code
- ✅ Translatable strings marked with `translate=True`
- ✅ Modern syntax (no deprecated `attrs`)
- ✅ Proper field ordering and grouping
- ✅ Standard Odoo naming conventions
- ✅ Proper use of `digits='Product Price'`
- ✅ UserError for validation with `_()` translation

### Dependencies
- Module already depends on `account` module (required for invoicing)
- No additional dependencies needed

## Testing

A comprehensive test script was created (`test_medical_pricing.py`) that validates:
- ✅ Treatment price field functionality
- ✅ Therapy price auto-update on treatment selection  
- ✅ Default configuration loading
- ✅ Invoice creation with correct data
- ✅ Validation error handling

All tests pass successfully, confirming the implementation works as expected.

## Files Modified

1. `models/medical_treatment.py` - Added price field
2. `models/medical_therapy.py` - Added pricing, invoicing fields and methods
3. `models/res_config_settings.py` - Added default configuration fields
4. `views/medical_treatment_views.xml` - Updated treatment views
5. `views/medical_therapy_views.xml` - Updated therapy views with invoice features
6. `views/res_config_settings_views.xml` - Added therapy configuration section
7. `tests/test_therapy_pricing.py` - Comprehensive test coverage
8. `tests/__init__.py` - Imported new test module

## Future Enhancements

Potential improvements could include:
- Therapy invoice line descriptions customization
- Bulk invoice generation for multiple therapies  
- Integration with therapy session billing
- Advanced pricing rules based on patient or apparatus type
- Invoice payment tracking integration
