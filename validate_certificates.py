#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validación para la implementación de Certificados Médicos
Verifica que todos los archivos estén correctamente creados y estructurados.
"""

import os
import xml.etree.ElementTree as ET

def validate_implementation():
    """Valida que la implementación de certificados médicos esté completa"""
    
    base_path = '/opt/odoo18/odoo-custom-addons/odoo_medical'
    errors = []
    success = []
    
    # Verificar archivos requeridos
    required_files = [
        'models/medical_consultation.py',
        'views/medical_consultation_views.xml', 
        'reports/medical_certificate_reports.xml',
        'reports/private_medical_certificate_template.xml',
        'reports/iess_medical_certificate_template.xml',
        '__manifest__.py'
    ]
    
    print("🔍 Verificando archivos requeridos...")
    for file_path in required_files:
        full_path = os.path.join(base_path, file_path)
        if os.path.exists(full_path):
            success.append(f"✅ {file_path} - Existe")
        else:
            errors.append(f"❌ {file_path} - No encontrado")
    
    # Verificar validez XML
    print("\n🔍 Verificando sintaxis XML...")
    xml_files = [
        'views/medical_consultation_views.xml',
        'reports/medical_certificate_reports.xml', 
        'reports/private_medical_certificate_template.xml',
        'reports/iess_medical_certificate_template.xml'
    ]
    
    for xml_file in xml_files:
        full_path = os.path.join(base_path, xml_file)
        if os.path.exists(full_path):
            try:
                ET.parse(full_path)
                success.append(f"✅ {xml_file} - XML válido")
            except ET.ParseError as e:
                errors.append(f"❌ {xml_file} - Error XML: {e}")
        else:
            errors.append(f"❌ {xml_file} - Archivo no encontrado")
    
    # Verificar contenido del manifiesto
    print("\n🔍 Verificando manifiesto...")
    manifest_path = os.path.join(base_path, '__manifest__.py')
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest_content = f.read()
            
        required_in_manifest = [
            'reports/medical_certificate_reports.xml',
            'reports/private_medical_certificate_template.xml', 
            'reports/iess_medical_certificate_template.xml'
        ]
        
        for required in required_in_manifest:
            if required in manifest_content:
                success.append(f"✅ Manifiesto incluye: {required}")
            else:
                errors.append(f"❌ Manifiesto NO incluye: {required}")
    
    # Verificar campos en modelo
    print("\n🔍 Verificando modelo de consulta...")
    model_path = os.path.join(base_path, 'models/medical_consultation.py')
    if os.path.exists(model_path):
        with open(model_path, 'r', encoding='utf-8') as f:
            model_content = f.read()
            
        required_fields = ['doctor_id', 'doctor_license']
        required_methods = ['action_print_private_certificate', 'action_print_iess_certificate']
        
        for field in required_fields:
            if field in model_content:
                success.append(f"✅ Campo {field} encontrado en modelo")
            else:
                errors.append(f"❌ Campo {field} NO encontrado en modelo")
                
        for method in required_methods:
            if method in model_content:
                success.append(f"✅ Método {method} encontrado en modelo") 
            else:
                errors.append(f"❌ Método {method} NO encontrado en modelo")
    
    # Mostrar resultados
    print("\n" + "="*60)
    print("📊 RESULTADOS DE VALIDACIÓN")
    print("="*60)
    
    if success:
        print(f"\n✅ ÉXITOS ({len(success)}):")
        for item in success:
            print(f"  {item}")
    
    if errors:
        print(f"\n❌ ERRORES ({len(errors)}):")
        for item in errors:
            print(f"  {item}")
    else:
        print(f"\n🎉 ¡IMPLEMENTACIÓN COMPLETA! No se encontraron errores.")
        print("\n📋 Resumen de funcionalidades implementadas:")
        print("  • Campos de doctor agregados al modelo medical.consultation")
        print("  • Botones de certificados agregados a la vista")
        print("  • Plantilla de certificado médico privado")
        print("  • Plantilla de certificado médico IESS")
        print("  • Reportes configurados en el manifiesto")
        print("  • Métodos de impresión implementados")
    
    print("\n" + "="*60)
    return len(errors) == 0

if __name__ == '__main__':
    validate_implementation()
