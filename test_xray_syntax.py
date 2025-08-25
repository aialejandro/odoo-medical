#!/usr/bin/env python3
"""
Test script to validate X-ray models syntax
"""

import ast
import os

def check_python_file(file_path):
    """Check if a Python file has valid syntax"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        ast.parse(content)
        return True, "OK"
    except SyntaxError as e:
        return False, f"Syntax Error: {e}"
    except Exception as e:
        return False, f"Error: {e}"

def check_xml_basic(file_path):
    """Basic XML validation"""
    try:
        import xml.etree.ElementTree as ET
        ET.parse(file_path)
        return True, "OK"
    except ET.ParseError as e:
        return False, f"XML Parse Error: {e}"
    except Exception as e:
        return False, f"Error: {e}"

# Test all new files
test_files = [
    ('models/medical_xray_area.py', 'python'),
    ('models/medical_xray_order_line.py', 'python'),
    ('models/medical_xray_order.py', 'python'),
    ('data/medical_xray_sequence.xml', 'xml'),
    ('views/medical_xray_area_views.xml', 'xml'),
    ('views/medical_xray_order_views.xml', 'xml'),
    ('views/medical_xray_menus.xml', 'xml'),
    ('demo/xray_demo.xml', 'xml'),
]

print("Testing X-ray module files...")
print("=" * 50)

all_good = True
for file_path, file_type in test_files:
    full_path = os.path.join('/opt/odoo18/odoo-custom-addons/odoo_medical', file_path)
    if os.path.exists(full_path):
        if file_type == 'python':
            success, msg = check_python_file(full_path)
        else:
            success, msg = check_xml_basic(full_path)
        
        status = "✓" if success else "✗"
        print(f"{status} {file_path}: {msg}")
        if not success:
            all_good = False
    else:
        print(f"✗ {file_path}: File not found")
        all_good = False

print("=" * 50)
if all_good:
    print("✓ All files passed basic validation!")
else:
    print("✗ Some files have issues")
