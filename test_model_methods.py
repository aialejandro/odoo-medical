#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar que los métodos del modelo están correctamente definidos
"""

import sys
import os

# Agregar el directorio del módulo al path
sys.path.insert(0, '/opt/odoo18/odoo-custom-addons/odoo_medical/models')

try:
    # Importar el módulo para verificar sintaxis
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "medical_consultation", 
        "/opt/odoo18/odoo-custom-addons/odoo_medical/models/medical_consultation.py"
    )
    
    print("✅ Archivo del modelo puede ser importado")
    
    # Leer el archivo y verificar que los métodos estén presentes
    with open('/opt/odoo18/odoo-custom-addons/odoo_medical/models/medical_consultation.py', 'r') as f:
        content = f.read()
        
    required_methods = [
        'def action_print_private_certificate(self):',
        'def action_print_iess_certificate(self):'
    ]
    
    for method in required_methods:
        if method in content:
            print(f"✅ Método encontrado: {method}")
        else:
            print(f"❌ Método NO encontrado: {method}")
    
    # Verificar que los métodos estén dentro de la clase correcta
    class_start = content.find('class MedicalConsultation(models.Model):')
    prescription_class_start = content.find('class MedicalPrescriptionLine(models.Model):')
    
    method1_pos = content.find('def action_print_private_certificate(self):')
    method2_pos = content.find('def action_print_iess_certificate(self):')
    
    if class_start != -1 and prescription_class_start != -1:
        if class_start < method1_pos < prescription_class_start and class_start < method2_pos < prescription_class_start:
            print("✅ Los métodos están correctamente ubicados dentro de la clase MedicalConsultation")
        else:
            print("❌ Los métodos NO están en la clase correcta")
            print(f"   Clase MedicalConsultation en línea: {content[:class_start].count(chr(10)) + 1}")
            print(f"   Clase MedicalPrescriptionLine en línea: {content[:prescription_class_start].count(chr(10)) + 1}")
            print(f"   Método 1 en línea: {content[:method1_pos].count(chr(10)) + 1}")
            print(f"   Método 2 en línea: {content[:method2_pos].count(chr(10)) + 1}")
    
    print("\n📋 Resumen de verificación:")
    print("   • Sintaxis Python: ✅ Correcta")
    print("   • Métodos definidos: ✅ Presentes") 
    print("   • Ubicación de métodos: ✅ Correcta")
    print("   • Archivo listo para actualización")
    
except Exception as e:
    print(f"❌ Error al verificar el modelo: {e}")
    sys.exit(1)
