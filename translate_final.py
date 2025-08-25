#!/usr/bin/env python3
"""
Simplified script to handle remaining translations efficiently
"""

import re
import subprocess

def copy_spanish_msgid_to_msgstr(po_file_path):
    """Copy Spanish msgid entries to their msgstr when msgstr is empty"""
    
    with open(po_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    translated_count = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Look for msgid lines
        if line.startswith('msgid "') and i + 1 < len(lines):
            msgid_content = line[7:-2]  # Remove 'msgid "' and '"\n'
            next_line = lines[i + 1]
            
            # Check if next line is empty msgstr and msgid contains Spanish characters
            if (next_line.startswith('msgstr ""') and 
                any(char in msgid_content for char in 'áéíóúñüÁÉÍÓÚÑÜ¿¡') and
                len(msgid_content) > 3):  # Avoid very short strings
                
                # Replace empty msgstr with the Spanish content
                lines[i + 1] = f'msgstr "{msgid_content}"\n'
                translated_count += 1
                print(f"Copied Spanish: '{msgid_content}'")
        
        i += 1
    
    # Write back the file
    with open(po_file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    return translated_count

def apply_common_translations(po_file_path):
    """Apply remaining common translations"""
    
    with open(po_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Common translations for remaining terms
    translations = {
        "Apparatus": "Aparato",
        "Category": "Categoría", 
        "Code": "Código",
        "Comment": "Comentario",
        "Comments": "Comentarios",
        "Company": "Empresa",
        "Configuration": "Configuración",
        "Contact": "Contacto",
        "Description": "Descripción",
        "Display Name": "Nombre a Mostrar",
        "Duration": "Duración",
        "Email": "Correo Electrónico",
        "Name": "Nombre",
        "Notes": "Notas",
        "Phone": "Teléfono",
        "Price": "Precio",
        "Priority": "Prioridad",
        "Progress": "Progreso",
        "Quantity": "Cantidad",
        "State": "Estado",
        "Status": "Estado",
        "Time": "Tiempo",
        "Total": "Total",
        "Type": "Tipo",
        "User": "Usuario",
        "View": "Ver",
        "Available": "Disponible",
        "Done": "Realizado",
        "Error": "Error",
        "All": "Todos",
        "Address": "Dirección",
        "Age": "Edad",
        "Amount": "Cantidad",
        "Help": "Ayuda",
        "Archive": "Archivar",
        "Confirm": "Confirmar",
        "Confirmed": "Confirmado",
        "Create": "Crear",
        "Save": "Guardar",
        "Search": "Buscar",
        "Update": "Actualizar",
        "Next": "Siguiente",
        "Medical": "Médico",
        "Patient": "Paciente",
        "Treatment": "Tratamiento",
        "Diagnosis": "Diagnóstico",
        "Instructions": "Instrucciones",
        "Observations": "Observaciones",
        "Session": "Sesión",
        "Currency": "Moneda",
        "Concentration": "Concentración",
        "Liquid": "Líquido",
        "Oral": "Oral",
        "Patch": "Parche",
        "Topical": "Tópico",
    }
    
    translated_count = 0
    for english, spanish in translations.items():
        pattern = f'msgid "{re.escape(english)}"\nmsgstr ""'
        if re.search(pattern, content):
            content = re.sub(pattern, f'msgid "{english}"\nmsgstr "{spanish}"', content)
            translated_count += 1
            print(f"Translated: '{english}' -> '{spanish}'")
    
    with open(po_file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return translated_count

def main():
    po_file = '/opt/odoo18/odoo-custom-addons/odoo_medical/i18n/es.po'
    
    print("Step 1: Copying Spanish msgid to empty msgstr...")
    spanish_count = copy_spanish_msgid_to_msgstr(po_file)
    print(f"Copied {spanish_count} Spanish entries")
    
    print("\nStep 2: Applying common translations...")
    common_count = apply_common_translations(po_file)
    print(f"Applied {common_count} common translations")
    
    print(f"\nTotal translations applied: {spanish_count + common_count}")
    
    print("\nChecking remaining untranslated strings...")
    result = subprocess.run(['grep', '-c', 'msgstr ""', po_file], 
                          capture_output=True, text=True)
    print(f"Remaining untranslated: {result.stdout.strip()}")

if __name__ == "__main__":
    main()
