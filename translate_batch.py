#!/usr/bin/env python3
"""
Batch Translation Script for Odoo Medical Module
Applies Spanish translations to the most common and important strings
"""

import re
import os

def apply_translations(po_file_path):
    """Apply Spanish translations to the .po file"""
    
    # Define translation mappings
    translations = {
        # UI Elements - High Priority
        "Action Needed": "Acción Requerida",
        "Activities": "Actividades",
        "Activity Exception Decoration": "Decoración de Excepción de Actividad",
        "Activity State": "Estado de Actividad",
        "Activity Type Icon": "Icono de Tipo de Actividad",
        "Active": "Activo",
        "Add": "Agregar",
        "Add a description...": "Agregar una descripción...",
        "Add component description...": "Agregar descripción del componente...",
        "Add detailed instructions...": "Agregar instrucciones detalladas...",
        "Address": "Dirección",
        "Affected Apparatus": "Aparato Afectado",
        "Age": "Edad",
        "All": "Todos",
        "Amount": "Cantidad",
        "Apparatus": "Aparato",
        "Apparatus Description": "Descripción del Aparato",
        "Apparatus Name": "Nombre del Aparato",
        "Archive": "Archivar",
        "Attachment Count": "Contador de Archivos Adjuntos",
        "Available": "Disponible",
        "Cancel": "Cancelar",
        "Cancelled": "Cancelado",
        "Category": "Categoría",
        "Code": "Código",
        "Comment": "Comentario",
        "Comments": "Comentarios",
        "Company": "Empresa",
        "Complete": "Completar",
        "Completed": "Completado",
        "Concentration": "Concentración",
        "Concentration Unit": "Unidad de Concentración",
        "Configuration": "Configuración",
        "Confirm": "Confirmar",
        "Confirmed": "Confirmado",
        "Consultation": "Consulta",
        "Consultation Date": "Fecha de Consulta",
        "Consultation Notes": "Notas de Consulta",
        "Consultations": "Consultas",
        "Contact": "Contacto",
        "Create": "Crear",
        "Create Invoice": "Crear Factura",
        "Created by": "Creado por",
        "Created on": "Creado el",
        "Currency": "Moneda",
        "Date": "Fecha",
        "Delete": "Eliminar",
        "Description": "Descripción",
        "Diagnosis": "Diagnóstico",
        "Display Name": "Nombre a Mostrar",
        "Done": "Realizado",
        "Draft": "Borrador",
        "Duration": "Duración",
        "Duration (minutes)": "Duración (minutos)",
        "Edit": "Editar",
        "Email": "Correo Electrónico",
        "End Date": "Fecha de Fin",
        "Error": "Error",
        "Group": "Grupo",
        "Help": "Ayuda",
        "History": "Historial",
        "ID": "ID",
        "In Progress": "En Progreso",
        "Instructions": "Instrucciones",
        "Last Modified on": "Última Modificación el",
        "Medical": "Médico",
        "Medical Consultation": "Consulta Médica",
        "Medical History": "Historial Médico",
        "Medical Therapy": "Terapia Médica",
        "Name": "Nombre",
        "New": "Nuevo",
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
        "Schedule": "Programar",
        "Scheduled": "Programado",
        "Search": "Buscar",
        "Session": "Sesión",
        "Sessions": "Sesiones",
        "Start Date": "Fecha de Inicio",
        "State": "Estado",
        "Status": "Estado",
        "Therapy": "Terapia",
        "Time": "Tiempo",
        "Total": "Total",
        "Treatment": "Tratamiento",
        "Type": "Tipo",
        "Update": "Actualizar",
        "User": "Usuario",
        "View": "Ver",
        "Work Restriction": "Restricción Laboral",
        
        # Selection Values
        "Capsule": "Cápsula",
        "Cream": "Crema",
        "Drops": "Gotas",
        "Gyneco-Obstetric": "Gineco-Obstétrico",
        "Injection": "Inyección",
        "Liquid": "Líquido",
        "Ointment": "Pomada",
        "Oral": "Oral",
        "Patch": "Parche",
        "Powder": "Polvo",
        "Spray": "Aerosol",
        "Syrup": "Jarabe",
        "Tablet": "Tableta",
        "Topical": "Tópico",
        
        # Medical dosage units
        "g": "g",
        "mg": "mg",
        "mcg": "mcg",
        "ml": "ml",
        "UI": "UI",
        
        # Error Messages and Python Code
        "Concentration must be greater than zero.": "La concentración debe ser mayor que cero.",
        "Consultation Invoice": "Factura de Consulta",
        "Discount percentage must be between 0 and 100.": "El porcentaje de descuento debe estar entre 0 y 100.",
        "Quantity to dispense must be greater than zero.": "La cantidad a dispensar debe ser mayor que cero.",
        "You cannot create recursive group hierarchies.": "No puede crear jerarquías de grupo recursivas.",
        "You must configure the consultation item and journal.": "Debe configurar el item y diario de consulta.",
        
        # Help texts (selection)
        "Actual duration of the session in minutes": "Duración real de la sesión en minutos",
        "Additional description for the apparatus": "Descripción adicional para el aparato",
        "Additional observations from the therapist": "Observaciones adicionales del terapeuta",
        "Apparatus that is being treated": "Aparato que está siendo tratado",
        "Assign this code to a specific ICD-10 group": "Asignar este código a un grupo ICD-10 específico",
    }
    
    # Read the file
    with open(po_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply translations
    translated_count = 0
    for english, spanish in translations.items():
        # Pattern to find msgid with empty msgstr
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
    
    print("Applying Spanish translations...")
    translated_count = apply_translations(po_file)
    print(f"\nCompleted! Applied {translated_count} translations.")
    
    print("\nRunning verification...")
    # Check remaining untranslated strings
    os.system(f'grep -c \'msgstr ""\' {po_file}')

if __name__ == "__main__":
    main()
