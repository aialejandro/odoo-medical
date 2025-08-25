#!/usr/bin/env python3
"""
Test simple para verificar que el modelo puede ser cargado correctamente
"""

import ast
import sys

def test_python_syntax():
    """Verifica la sintaxis Python del archivo del modelo"""
    model_file = '/opt/odoo18/odoo-custom-addons/odoo_medical/models/medical_consultation.py'
    
    try:
        with open(model_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parsear el AST para verificar sintaxis
        tree = ast.parse(content, model_file)
        
        print("✅ Sintaxis Python válida")
        
        # Encontrar la clase MedicalConsultation
        medical_class = None
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == 'MedicalConsultation':
                medical_class = node
                break
        
        if medical_class:
            print("✅ Clase MedicalConsultation encontrada")
            
            # Buscar los métodos específicos
            target_methods = ['action_print_private_certificate', 'action_print_iess_certificate']
            found_methods = []
            
            for node in medical_class.body:
                if isinstance(node, ast.FunctionDef) and node.name in target_methods:
                    found_methods.append(node.name)
                    print(f"✅ Método encontrado: {node.name}")
            
            if len(found_methods) == len(target_methods):
                print("✅ Todos los métodos requeridos están presentes")
                return True
            else:
                print(f"❌ Faltan métodos. Encontrados: {found_methods}")
                return False
        else:
            print("❌ Clase MedicalConsultation no encontrada")
            return False
            
    except SyntaxError as e:
        print(f"❌ Error de sintaxis: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == '__main__':
    if test_python_syntax():
        print("\n🎉 ¡El modelo está correctamente estructurado!")
        sys.exit(0)
    else:
        print("\n❌ Hay problemas con el modelo.")
        sys.exit(1)
