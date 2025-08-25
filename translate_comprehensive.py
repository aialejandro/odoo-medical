#!/usr/bin/env python3
"""
Comprehensive translation script for all remaining strings
"""

import re
import subprocess

def apply_comprehensive_translations(po_file_path):
    """Apply comprehensive translations for all remaining strings"""
    
    with open(po_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Comprehensive translation dictionary
    translations = {
        # Placeholder texts
        "Add session description...": "Agregar descripción de la sesión...",
        "Add therapist observations...": "Agregar observaciones del terapeuta...",
        "Add treatment description...": "Agregar descripción del tratamiento...",
        "Additional observations...": "Observaciones adicionales...",
        "Apparatus name...": "Nombre del aparato...",
        
        # Medical conditions and categories
        "Allergy": "Alergia",
        "Amebiasis": "Amebiasis",
        "Amebiasis, no especificada": "Amebiasis, no especificada",
        "Ameboma intestinal": "Ameboma intestinal",
        "Artritis por Salmonella": "Artritis por Salmonella",
        "Artritis tifoidea": "Artritis tifoidea",
        "Balantidiasis": "Balantidiasis",
        "Catastrophic Illness": "Enfermedad Catastrófica",
        
        # Status and state values
        "Archived": "Archivado",
        "By Category": "Por Categoría",
        "By Patient": "Por Paciente", 
        "By State": "Por Estado",
        
        # Medical categories (already in Spanish - copy to msgstr)
        "CIERTAS ENFERMEDADES INFECCIOSAS Y PARASITARIAS": "CIERTAS ENFERMEDADES INFECCIOSAS Y PARASITARIAS",
        "CIERTAS ZOONOSIS BACTERIANAS": "CIERTAS ZOONOSIS BACTERIANAS",
        
        # Form fields and labels
        "Apparatus Name": "Nombre del Aparato",
        "Apparatus Description": "Descripción del Aparato",
        "Affected Apparatus": "Aparato Afectado",
        "Consultation Date": "Fecha de Consulta",
        "Consultation Notes": "Notas de Consulta", 
        "Work Restriction": "Restricción Laboral",
        "Duration (minutes)": "Duración (minutos)",
        "Medical Consultation": "Consulta Médica",
        "Medical History": "Historial Médico",
        "Medical Therapy": "Terapia Médica",
        
        # Common UI elements  
        "Archive": "Archivar",
        "Available": "Disponible",
        "By": "Por",
        "Category": "Categoría",
        "Code": "Código",
        "Comment": "Comentario",
        "Comments": "Comentarios",
        "Company": "Empresa",
        "Complete": "Completar",
        "Completed": "Completado",
        "Configuration": "Configuración",
        "Confirm": "Confirmar",
        "Confirmed": "Confirmado",
        "Contact": "Contacto",
        "Create": "Crear",
        "Currency": "Moneda",
        "Description": "Descripción",
        "Display Name": "Nombre a Mostrar",
        "Done": "Realizado",
        "Duration": "Duración",
        "Email": "Correo Electrónico",
        "Error": "Error",
        "Help": "Ayuda",
        "Instructions": "Instrucciones",
        "Last Modified on": "Última Modificación el",
        "Medical": "Médico",
        "Name": "Nombre",
        "Next": "Siguiente",
        "Notes": "Notas",
        "Observations": "Observaciones",
        "Patient": "Paciente",
        "Phone": "Teléfono",
        "Price": "Precio",
        "Priority": "Prioridad",
        "Progress": "Progreso",
        "Quantity": "Cantidad",
        "Save": "Guardar",
        "Search": "Buscar",
        "Session": "Sesión",
        "State": "Estado",
        "Status": "Estado",
        "Time": "Tiempo",
        "Total": "Total",
        "Treatment": "Tratamiento",
        "Type": "Tipo",
        "Update": "Actualizar",
        "User": "Usuario",
        "View": "Ver",
        
        # Address and contact
        "Address": "Dirección",
        "Age": "Edad",
        "All": "Todos",
        "Amount": "Cantidad",
        
        # Medical terminology
        "Concentration": "Concentración",
        "Concentration Unit": "Unidad de Concentración",
        "Diagnosis": "Diagnóstico",
        "Liquid": "Líquido",
        "Oral": "Oral",
        "Patch": "Parche",
        "Topical": "Tópico",
        
        # Dosage units (keep as is)
        "g": "g",
        "UI": "UI",
        
        # Help texts
        "Additional description for the apparatus": "Descripción adicional para el aparato",
        "Additional observations from the therapist": "Observaciones adicionales del terapeuta",
        "Apparatus that is being treated": "Aparato que está siendo tratado",
        "Assign this code to a specific ICD-10 group": "Asignar este código a un grupo ICD-10 específico",
        
        # Selection values
        "Cardiovascular": "Cardiovascular",
        "Dermatologic": "Dermatológico",
        "Endocrine": "Endocrino",
        "Gastrointestinal": "Gastrointestinal",
        "Hematologic": "Hematológico",
        "Musculoskeletal": "Musculoesquelético",
        "Neurologic": "Neurológico",
        "Oncologic": "Oncológico",
        "Ophthalmologic": "Oftalmológico",
        "Psychiatric": "Psiquiátrico",
        "Pulmonary": "Pulmonar",
        "Renal": "Renal",
        "Rheumatologic": "Reumatológico",
        "Urologic": "Urológico",
        
        # Common medical terms
        "Chronic": "Crónico",
        "Acute": "Agudo",
        "Moderate": "Moderado",
        "Severe": "Severo",
        "Mild": "Leve",
        "High": "Alto",
        "Low": "Bajo",
        "Normal": "Normal",
        
        # Time-related
        "Daily": "Diario",
        "Weekly": "Semanal",
        "Monthly": "Mensual",
        "Hourly": "Por Hora",
        
        # Common actions
        "Add": "Agregar",
        "Remove": "Remover",
        "Delete": "Eliminar",
        "Duplicate": "Duplicar",
        "Print": "Imprimir",
        "Export": "Exportar",
        "Import": "Importar",
    }
    
    translated_count = 0
    for english, spanish in translations.items():
        pattern = f'msgid "{re.escape(english)}"\nmsgstr ""'
        if re.search(pattern, content):
            content = re.sub(pattern, f'msgid "{english}"\nmsgstr "{spanish}"', content)
            translated_count += 1
            print(f"✓ {english} -> {spanish}")
    
    with open(po_file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return translated_count

def copy_all_spanish_entries(po_file_path):
    """Copy all Spanish msgid entries to msgstr where empty"""
    
    with open(po_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to find Spanish msgid with empty msgstr
    spanish_chars = 'áéíóúñüÁÉÍÓÚÑÜ¿¡'
    
    def replace_spanish(match):
        msgid_text = match.group(1)
        if any(char in msgid_text for char in spanish_chars) and len(msgid_text.strip()) > 2:
            return f'msgid "{msgid_text}"\nmsgstr "{msgid_text}"'
        return match.group(0)
    
    pattern = r'msgid "([^"]+)"\nmsgstr ""'
    content = re.sub(pattern, replace_spanish, content)
    
    with open(po_file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    po_file = '/opt/odoo18/odoo-custom-addons/odoo_medical/i18n/es.po'
    
    print("Step 1: Copying all Spanish entries...")
    copy_all_spanish_entries(po_file)
    print("✓ Spanish entries copied")
    
    print("\nStep 2: Applying comprehensive translations...")
    count = apply_comprehensive_translations(po_file)
    print(f"\n✓ Applied {count} translations")
    
    print("\nStep 3: Checking final status...")
    try:
        result = subprocess.run(['grep', '-c', 'msgstr ""', po_file], 
                              capture_output=True, text=True)
        remaining = int(result.stdout.strip())
        
        total_result = subprocess.run(['grep', '-c', '^msgid', po_file],
                                    capture_output=True, text=True)
        total = int(total_result.stdout.strip()) - 1  # Subtract the empty msgid at top
        
        translated = total - remaining
        percentage = (translated / total) * 100 if total > 0 else 0
        
        print(f"📊 Translation Status:")
        print(f"   Total strings: {total}")
        print(f"   Translated: {translated}")
        print(f"   Remaining: {remaining}")
        print(f"   Progress: {percentage:.1f}%")
        
        if remaining < 50:
            print(f"\n🎉 Great progress! Only {remaining} strings left to translate manually.")
        
    except Exception as e:
        print(f"Error checking status: {e}")

if __name__ == "__main__":
    main()
