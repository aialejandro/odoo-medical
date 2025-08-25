#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar la validación de métodos como lo haría Odoo
"""

import re

def check_model_methods():
    """Verifica que los métodos estén correctamente definidos en el modelo"""
    
    model_file = '/opt/odoo18/odoo-custom-addons/odoo_medical/models/medical_consultation.py'
    
    with open(model_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar la clase MedicalConsultation
    class_pattern = r'class\s+MedicalConsultation\s*\([^)]+\):'
    class_match = re.search(class_pattern, content)
    
    if not class_match:
        print("❌ No se encontró la clase MedicalConsultation")
        return False
    
    class_start = class_match.end()
    
    # Buscar la siguiente clase para determinar el final de MedicalConsultation
    next_class_pattern = r'\nclass\s+\w+'
    next_class_match = re.search(next_class_pattern, content[class_start:])
    
    if next_class_match:
        class_end = class_start + next_class_match.start()
    else:
        class_end = len(content)
    
    class_content = content[class_start:class_end]
    
    # Buscar métodos específicos
    methods = [
        'action_print_private_certificate',
        'action_print_iess_certificate'
    ]
    
    found_methods = []
    for method in methods:
        method_pattern = rf'def\s+{method}\s*\([^)]*\):'
        if re.search(method_pattern, class_content):
            found_methods.append(method)
            print(f"✅ Método encontrado: {method}")
        else:
            print(f"❌ Método NO encontrado: {method}")
    
    # Verificar indentación (todos los métodos deberían tener la misma indentación base)
    method_lines = []
    for line_num, line in enumerate(class_content.split('\n'), 1):
        if line.strip().startswith('def '):
            indent = len(line) - len(line.lstrip())
            method_lines.append((line_num, line.strip(), indent))
    
    if method_lines:
        base_indent = method_lines[0][2]
        print(f"\n📐 Verificando indentación (base: {base_indent} espacios):")
        for line_num, method_def, indent in method_lines:
            if 'action_print_' in method_def:
                if indent == base_indent:
                    print(f"   ✅ {method_def[:30]}... - Indentación correcta")
                else:
                    print(f"   ❌ {method_def[:30]}... - Indentación incorrecta ({indent} vs {base_indent})")
    
    print(f"\n📊 Resumen:")
    print(f"   • Métodos requeridos: {len(methods)}")
    print(f"   • Métodos encontrados: {len(found_methods)}")
    print(f"   • Estado: {'✅ OK' if len(found_methods) == len(methods) else '❌ INCOMPLETO'}")
    
    return len(found_methods) == len(methods)

if __name__ == '__main__':
    success = check_model_methods()
    if success:
        print("\n🎉 ¡Todos los métodos están correctamente definidos!")
    else:
        print("\n⚠️  Hay problemas con la definición de métodos.")
