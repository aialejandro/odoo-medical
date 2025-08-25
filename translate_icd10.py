#!/usr/bin/env python3
"""
Script to handle ICD10 descriptions and remaining common translations
"""

import re
import os

def translate_icd10_descriptions(po_file_path):
    """Translate ICD10 descriptions that are already in Spanish"""
    
    with open(po_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to find ICD10 descriptions that are already in Spanish
    # These have Spanish text as msgid but empty msgstr
    pattern = r'(#: model:medical\.icd10,description:[^\n]+\n)(msgid "([^"]+)"\nmsgstr "")'
    
    def replace_icd10(match):
        prefix = match.group(1)
        msgid_line = match.group(2)
        spanish_text = match.group(3)
        
        # If the msgid contains Spanish text, copy it to msgstr
        if any(char in spanish_text for char in 'áéíóúñüÁÉÍÓÚÑÜ¿¡'):
            return prefix + f'msgid "{spanish_text}"\nmsgstr "{spanish_text}"'
        else:
            return match.group(0)  # Return unchanged if not Spanish
    
    content = re.sub(pattern, replace_icd10, content)
    
    # Additional common medical translations
    additional_translations = {
        # Medical terms
        "Affected Apparatus": "Aparato Afectado",
        "Consultation Date": "Fecha de Consulta", 
        "Consultation Notes": "Notas de Consulta",
        "Diagnosis": "Diagnóstico",
        "Duration (minutes)": "Duración (minutos)",
        "Instructions": "Instrucciones",
        "Medical": "Médico",
        "Medical Consultation": "Consulta Médica",
        "Medical Therapy": "Terapia Médica",
        "Observations": "Observaciones",
        "Patient": "Paciente",
        "Treatment": "Tratamiento",
        "Work Restriction": "Restricción Laboral",
        
        # Form fields
        "Apparatus": "Aparato",
        "Apparatus Description": "Descripción del Aparato", 
        "Apparatus Name": "Nombre del Aparato",
        "Category": "Categoría",
        "Code": "Código",
        "Comment": "Comentario",
        "Comments": "Comentarios",
        "Company": "Empresa",
        "Concentration": "Concentración",
        "Concentration Unit": "Unidad de Concentración",
        "Configuration": "Configuración",
        "Contact": "Contacto",
        "Currency": "Moneda",
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
        "Session": "Sesión",
        "State": "Estado",
        "Status": "Estado",
        "Time": "Tiempo",
        "Total": "Total",
        "Type": "Tipo",
        "User": "Usuario",
        
        # UI actions
        "Archive": "Archivar",
        "Confirm": "Confirmar",
        "Confirmed": "Confirmado",
        "Create": "Crear",
        "Save": "Guardar",
        "Search": "Buscar",
        "Update": "Actualizar",
        "View": "Ver",
        
        # Status values
        "Available": "Disponible",
        "Done": "Realizado",
        "Error": "Error",
        
        # Time periods
        "Next": "Siguiente",
        "All": "Todos",
        
        # Common words
        "Address": "Dirección",
        "Age": "Edad",
        "Amount": "Cantidad",
        "Help": "Ayuda",
        "Last Modified on": "Última Modificación el",
        
        # Medical dosage forms  
        "Liquid": "Líquido",
        "Oral": "Oral",
        "Patch": "Parche",
        "Topical": "Tópico",
        "g": "g",
        "UI": "UI",
    }
    
    translated_count = 0
    for english, spanish in additional_translations.items():
        pattern = f'msgid "{re.escape(english)}"\nmsgstr ""'
        replacement = f'msgid "{english}"\nmsgstr "{spanish}"'
        
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            translated_count += 1
            print(f"Translated: '{english}' -> '{spanish}'")
    
    # Write back the file
    with open(po_file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return translated_count

def main():
    po_file = '/opt/odoo18/odoo-custom-addons/odoo_medical/i18n/es.po'
    
    print("Translating ICD10 descriptions and additional terms...")
    translated_count = translate_icd10_descriptions(po_file)
    print(f"\nCompleted! Applied {translated_count} additional translations.")
    
    print("\nChecking remaining untranslated strings...")
    os.system(f'grep -c \'msgstr ""\' {po_file}')

if __name__ == "__main__":
    main()
