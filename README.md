# odoo_medical
Odoo module for medical entities.

## Environment Setup
Before executing any Python commands or running Odoo, ensure you activate the virtual environment:

```bash
source /opt/odoo18/venv/bin/activate
```

When running Odoo, use the configuration file and test database:

```bash
# Activate virtual environment first
source /opt/odoo18/venv/bin/activate

# Run Odoo with specific configuration and database
odoo -c /etc/odoo18.conf -d test --http-port=8070
```

## Version Compatibility
This module is designed for **Odoo v18** and follows the coding standards and best practices for this version.

## Development Guidelines
When working with this module, please ensure:

- **All code must comply with Odoo v18 standards**
- **All field labels, strings, and UI elements must be written in English**
- **All translatable strings must be added to translation files in the `i18n/` folder**
- **Use modern Odoo syntax** (avoid deprecated attributes like `attrs`, use `invisible` domains instead)
- **Follow Odoo's naming conventions** and coding best practices

## Agent Permissions
AI agents are authorized to modify or delete any files required, but **only within the `l10n_ec_edi_import_ee` module directory**. This restriction ensures:

- Safe modifications within the designated module scope
- Protection of core system files and other modules
- Controlled development environment for EDI import functionality

## Translation Support
The module includes translation support with Spanish translations available in the `i18n/` folder. When adding new features:

1. Write all strings in English in the code
2. Add corresponding translations to the appropriate `.po` files
3. Test translations are working correctly
