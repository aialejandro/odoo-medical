# X-ray Orders Module Implementation

## Overview
This implementation adds a complete X-ray orders management system to the odoo_medical module. The system allows healthcare providers to create, manage, and invoice X-ray orders for patients.

## Models Created

### 1. Medical X-ray Area (`medical.xray.area`)
- **Purpose**: Defines the body areas that can be X-rayed
- **Fields**:
  - `name`: Name of the X-ray area (e.g., Chest, Spine, Abdomen)
  - `description`: Additional information about the area
  - `active`: Boolean to archive/unarchive areas

### 2. Medical X-ray Order Line (`medical.xray.order.line`)
- **Purpose**: Individual line items within an X-ray order
- **Fields**:
  - `area_id`: Reference to the X-ray area
  - `projection_type`: Selection field with options:
    - Anteroposterior (AP)
    - Posteroanterior (PA)
    - Lateral
    - Oblique
  - `price`: Cost for this specific X-ray
  - `images`: Many2many field to upload X-ray images
  - `sequence`: For ordering the lines
  - `image_count`: Computed field showing number of uploaded images

### 3. Medical X-ray Order (`medical.xray.order`)
- **Purpose**: Main X-ray order containing patient info and line items
- **Fields**:
  - `name`: Auto-generated order number (XR00001, XR00002, etc.)
  - `patient_id`: Reference to patient (res.partner)
  - `date`: Date of the order
  - `line_ids`: One2many relation to order lines
  - `total_price`: Computed sum of all line prices
  - `state`: Workflow states (draft, confirmed, in_progress, done, cancelled)
  - `journal_id`, `product_id`, `tax_id`: Invoice configuration fields
  - `invoice_id`: Reference to generated invoice
  - `notes`: Additional notes

## Configuration Settings

Added to `res.config.settings`:
- `medical_default_xray_product_id`: Default product for X-ray invoicing
- `medical_default_xray_tax_id`: Default tax for X-ray invoicing  
- `medical_default_xray_journal_id`: Default journal for X-ray invoicing

## User Interface

### Menus
- **X-ray Management** menu added after "Therapy Management"
  - **X-ray Orders** submenu for managing orders
- **Configuration** menu includes:
  - **X-ray Areas** for configuring available body areas

### Views
- **X-ray Order Form**: Complete workflow management with buttons for each state
- **X-ray Order Tree**: List view with filtering and grouping
- **X-ray Area Management**: Simple form and tree views for area configuration

## Workflow

1. **Draft**: Order is created in draft state
2. **Confirmed**: Order is confirmed and ready for processing
3. **In Progress**: X-ray procedure has started
4. **Done**: X-ray procedure completed, ready for invoicing
5. **Cancelled**: Order cancelled (not allowed if invoice is posted)

## Invoicing Features

- **Create Invoice** button appears when order is in "Done" state
- Uses default journal, product, and tax from configuration
- Invoice line includes total price from all X-ray lines
- **View Invoice** button to access generated invoice

## File Structure

```
models/
├── medical_xray_area.py
├── medical_xray_order_line.py
├── medical_xray_order.py
└── res_config_settings.py (updated)

views/
├── medical_xray_area_views.xml
├── medical_xray_order_views.xml
├── medical_xray_menus.xml
└── res_config_settings_views.xml (updated)

data/
└── medical_xray_sequence.xml

demo/
└── xray_demo.xml

security/
└── ir.model.access.csv (updated)
```

## Demo Data

Pre-configured X-ray areas:
- Chest
- Spine
- Abdomen
- Pelvis
- Skull
- Extremities

## Security

- All models accessible to base.group_user
- Standard CRUD permissions configured

## Installation

The module automatically creates:
- Sequence for X-ray order numbering
- Demo X-ray areas for testing
- Menu items in the Medical module

## Usage

1. Configure default settings in Settings > Medical > X-ray Services
2. Create/manage X-ray areas in Configuration menu
3. Create X-ray orders from the X-ray Management menu
4. Add lines specifying area, projection type, and price
5. Upload images as needed
6. Follow workflow: Draft → Confirmed → In Progress → Done
7. Create invoices for completed orders
