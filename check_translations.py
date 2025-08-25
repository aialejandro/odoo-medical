#!/usr/bin/env python3
"""
Translation Analysis Script for Odoo Medical Module
Analyzes the i18n/es.po file to identify untranslated strings by category
"""

import re
import sys

def analyze_translations(po_file_path):
    """Analyze the .po file and categorize untranslated strings"""
    
    with open(po_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all translation entries
    pattern = r'#\. module: odoo_medical\n((?:#[^\n]*\n)*)(#: [^\n]+\n)msgid "([^"]*(?:"[^"]*")*)"\nmsgstr "([^"]*(?:"[^"]*")*)"'
    matches = re.findall(pattern, content, re.MULTILINE)
    
    categories = {
        'field_descriptions': [],
        'model_terms_views': [],
        'model_names': [],
        'icd10_descriptions': [],
        'selection_values': [],
        'help_texts': [],
        'python_code': [],
        'other': []
    }
    
    total_strings = 0
    untranslated_strings = 0
    
    for match in matches:
        comments, source_line, msgid, msgstr = match
        total_strings += 1
        
        if msgstr.strip() == "":
            untranslated_strings += 1
            
            # Categorize based on source line
            if 'field_description' in source_line:
                categories['field_descriptions'].append((msgid, source_line.strip()))
            elif 'model_terms:ir.ui.view' in source_line:
                categories['model_terms_views'].append((msgid, source_line.strip()))
            elif 'model:ir.model,' in source_line:
                categories['model_names'].append((msgid, source_line.strip()))
            elif 'medical.icd10,description' in source_line:
                categories['icd10_descriptions'].append((msgid, source_line.strip()))
            elif 'selection,name' in source_line:
                categories['selection_values'].append((msgid, source_line.strip()))
            elif 'help:' in source_line:
                categories['help_texts'].append((msgid, source_line.strip()))
            elif 'code:addons' in source_line:
                categories['python_code'].append((msgid, source_line.strip()))
            else:
                categories['other'].append((msgid, source_line.strip()))
    
    return total_strings, untranslated_strings, categories

def main():
    po_file = '/opt/odoo18/odoo-custom-addons/odoo_medical/i18n/es.po'
    
    total, untranslated, categories = analyze_translations(po_file)
    
    print("=" * 80)
    print("ODOO MEDICAL MODULE - TRANSLATION ANALYSIS")
    print("=" * 80)
    print(f"Total strings: {total}")
    print(f"Untranslated strings: {untranslated}")
    print(f"Translation progress: {((total - untranslated) / total * 100):.1f}%")
    print("=" * 80)
    
    print("\nUNTRANSLATED STRINGS BY CATEGORY:")
    print("-" * 50)
    
    for category, items in categories.items():
        if items:
            print(f"\n{category.upper().replace('_', ' ')} ({len(items)} items):")
            print("-" * 30)
            for i, (msgid, source) in enumerate(items[:5], 1):  # Show first 5 of each category
                print(f"{i}. \"{msgid}\"")
                if len(msgid) > 60:
                    print(f"   (truncated)")
            if len(items) > 5:
                print(f"   ... and {len(items) - 5} more")
    
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS:")
    print("=" * 80)
    
    if categories['field_descriptions']:
        print(f"• {len(categories['field_descriptions'])} field descriptions need translation")
    if categories['model_terms_views']:
        print(f"• {len(categories['model_terms_views'])} UI view terms need translation")
    if categories['icd10_descriptions']:
        print(f"• {len(categories['icd10_descriptions'])} ICD10 descriptions need translation")
    if categories['selection_values']:
        print(f"• {len(categories['selection_values'])} selection field values need translation")
    if categories['python_code']:
        print(f"• {len(categories['python_code'])} Python code strings need translation")
    if categories['help_texts']:
        print(f"• {len(categories['help_texts'])} help texts need translation")
    
    print("\nTo complete translations, focus on:")
    print("1. Field descriptions for user interface")
    print("2. View terms and labels")
    print("3. Selection field values")
    print("4. Error messages from Python code")

if __name__ == "__main__":
    main()
