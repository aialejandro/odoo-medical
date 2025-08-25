#!/usr/bin/env python3
"""
Final comprehensive translation script for remaining strings
"""

import re
import subprocess

def apply_final_translations(po_file_path):
    """Apply final comprehensive translations"""
    
    with open(po_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Final comprehensive translation dictionary
    translations = {
        # Help texts and descriptions
        "Cause of the medical condition": "Causa de la condición médica",
        "Chapter (Legacy)": "Capítulo (Heredado)",
        "Check this box if this contact is a medical patient": "Marque esta casilla si este contacto es un paciente médico",
        "Child Groups": "Grupos Hijo",
        "Components": "Componentes",
        "Components Count": "Conteo de Componentes",
        "Components that make up this session": "Componentes que componen esta sesión",
        "Computed name for the session record": "Nombre calculado para el registro de sesión",
        "Configure default parameters for medical consultations": "Configurar parámetros predeterminados para consultas médicas",
        "Consultation Count": "Conteo de Consultas",
        "Consultation Duration (min)": "Duración de Consulta (min)",
        "Current state of the therapy": "Estado actual de la terapia",
        "Date and time when the session ended": "Fecha y hora cuando terminó la sesión",
        "Date and time when the session started": "Fecha y hora cuando inició la sesión",
        "Date when the therapy is scheduled": "Fecha cuando está programada la terapia",
        
        # UI Messages and actions
        "Create a new affected apparatus": "Crear un nuevo aparato afectado",
        "Create a new medical therapy": "Crear una nueva terapia médica",
        "Create a new medical treatment": "Crear un nuevo tratamiento médico",
        "Create a new session record": "Crear un nuevo registro de sesión",
        "Create a new treatment component": "Crear un nuevo componente de tratamiento",
        "Create a new treatment session": "Crear una nueva sesión de tratamiento",
        "Create your first ICD-10 code!": "¡Cree su primer código ICD-10!",
        "Create your first ICD-10 group!": "¡Cree su primer grupo ICD-10!",
        "Create your first medical consultation!": "¡Cree su primera consulta médica!",
        
        # Placeholders
        "Component name...": "Nombre del componente...",
        
        # Medical conditions (Spanish entries)
        "Ciclosporosis": "Ciclosporosis",
        "Cistitis amebiana": "Cistitis amebiana",
        "Criptosporidiosis": "Criptosporidiosis",
        
        # Status and counts
        "Completed Sessions": "Sesiones Completadas",
        
        # Field labels
        "Default pricelist for medical consultations": "Lista de precios predeterminada para consultas médicas",
        "Default product for consultation billing": "Producto predeterminado para facturación de consultas",
        "Default tax for consultation billing": "Impuesto predeterminado para facturación de consultas",
        "Default journal for consultation invoices": "Diario predeterminado para facturas de consulta",
        "Details": "Detalles",
        "Diagnosis Code": "Código de Diagnóstico",
        "Disentería amebiana aguda": "Disentería amebiana aguda",
        "Doctor": "Doctor",
        "Doctor/Therapist": "Doctor/Terapeuta",
        "Duration in Minutes": "Duración en Minutos",
        
        # Form actions
        "Enable medical features for this contact": "Habilitar funciones médicas para este contacto",
        "End Date": "Fecha de Fin",
        "End Time": "Hora de Fin",
        "Equipment": "Equipo",
        "Equipment and apparatus used": "Equipo y aparatos utilizados",
        "Expected duration of the session": "Duración esperada de la sesión",
        
        # More field descriptions
        "Follow Up": "Seguimiento",
        "Follow Up Date": "Fecha de Seguimiento",
        "Followers": "Seguidores",
        "Form": "Formulario",
        "Full name of the affected apparatus": "Nombre completo del aparato afectado",
        "General": "General",
        "Group by...": "Agrupar por...",
        "Has Message": "Tiene Mensaje",
        "Has attachments": "Tiene archivos adjuntos",
        
        # ICD codes
        "ICD-10": "CIE-10",
        "ICD-10 Code": "Código CIE-10",
        "ICD-10 Group": "Grupo CIE-10",
        "ICD-10 Groups": "Grupos CIE-10",
        "ICD10 Code": "Código CIE10",
        "ICD10 Group": "Grupo CIE10",
        
        # Status fields
        "Is Medical Patient": "Es Paciente Médico",
        "Is Unread": "No Leído",
        "Journal": "Diario",
        "Last Message Date": "Fecha del Último Mensaje",
        "Last Update": "Última Actualización",
        "Medical Patient": "Paciente Médico",
        "Medical Settings": "Configuraciones Médicas",
        "Message Attachment Count": "Conteo de Archivos Adjuntos de Mensaje",
        "Message Has Error": "El Mensaje Tiene Error",
        "Message Has Error Counter": "Contador de Errores de Mensaje",
        "Message Has SMS Error": "El Mensaje Tiene Error SMS",
        "Message Is Follower": "El Mensaje Es Seguidor",
        "Message Main Attachment Id": "ID del Archivo Adjunto Principal del Mensaje",
        "Message Partner Ids": "IDs de Socios del Mensaje",
        "Message Unread": "Mensaje No Leído",
        "Messages": "Mensajes",
        "Model": "Modelo",
        
        # Navigation and views
        "Kanban": "Kanban",
        "List": "Lista",
        "Tree": "Árbol",
        "Calendar": "Calendario",
        "Graph": "Gráfico",
        "Pivot": "Tabla Dinámica",
        "Activity": "Actividad",
        
        # Time and scheduling
        "Next Activity Deadline": "Fecha Límite de Próxima Actividad",
        "Next Activity Summary": "Resumen de Próxima Actividad",
        "Next Activity Type": "Tipo de Próxima Actividad",
        "Number of Actions": "Número de Acciones",
        "Number of errors": "Número de errores",
        "Number of messages with delivery error": "Número de mensajes con error de entrega",
        "Number of unread messages": "Número de mensajes no leídos",
        
        # Parent/child relationships  
        "Parent Group": "Grupo Padre",
        "Parent ICD-10 group for creating hierarchies": "Grupo CIE-10 padre para crear jerarquías",
        "Partner": "Socio",
        "Patient Information": "Información del Paciente",
        "Patient Name": "Nombre del Paciente",
        "Planned duration of the session in minutes": "Duración planificada de la sesión en minutos",
        "Pricelist": "Lista de Precios",
        
        # Record management
        "Rating Last Image": "Última Imagen de Calificación",
        "Rating Last Text": "Último Texto de Calificación",
        "Rating Last Value": "Último Valor de Calificación",
        "Record Name": "Nombre del Registro",
        "Remaining sessions to complete the therapy": "Sesiones restantes para completar la terapia",
        "Responsible": "Responsable",
        "Responsible for this therapy": "Responsable de esta terapia",
        
        # Session details
        "Session Count": "Conteo de Sesiones",
        "Session Description": "Descripción de la Sesión",
        "Session End": "Fin de Sesión",
        "Session Notes": "Notas de Sesión",
        "Session Records": "Registros de Sesión",
        "Session Start": "Inicio de Sesión",
        "Sessions Completed": "Sesiones Completadas",
        "Sessions Remaining": "Sesiones Restantes",
        "Sessions Total": "Total de Sesiones",
        "Short description of the component": "Descripción breve del componente",
        "Start Date": "Fecha de Inicio",
        "Start Time": "Hora de Inicio",
        
        # System fields
        "Technical field for UX purpose.": "Campo técnico para propósito de UX.",
        "The consultation journal for billing": "El diario de consulta para facturación",
        "The consultation product for billing": "El producto de consulta para facturación",
        "The consultation tax for billing": "El impuesto de consulta para facturación",
        "The pricelist for consultation": "La lista de precios para consulta",
        "Therapist": "Terapeuta",
        "Therapist Notes": "Notas del Terapeuta",
        "Therapist assigned to this session": "Terapeuta asignado a esta sesión",
        "Total number of sessions planned for this therapy": "Número total de sesiones planificadas para esta terapia",
        "Total sessions for this therapy": "Total de sesiones para esta terapia",
        "Treatment Component": "Componente de Tratamiento",
        "Treatment Components": "Componentes de Tratamiento",
        "Treatment Session": "Sesión de Tratamiento",
        "Treatment Sessions": "Sesiones de Tratamiento",
        
        # Workflow states
        "Unread Messages": "Mensajes No Leídos",
        "Unread Messages Counter": "Contador de Mensajes No Leídos",
        "Website Message Ids": "IDs de Mensaje del Sitio Web",
        
        # Work restriction values
        "Work Restriction Type": "Tipo de Restricción Laboral",
        "light_duty": "trabajo_ligero",
        "modified_duty": "trabajo_modificado", 
        "no_restriction": "sin_restricción",
        "Light Duty": "Trabajo Ligero",
        "Modified Duty": "Trabajo Modificado",
        "No Restriction": "Sin Restricción",
        
        # Additional common terms
        "Filters": "Filtros",
        "Group By": "Agrupar Por",
        "More": "Más",
        "Options": "Opciones",
        "Settings": "Configuraciones",
        "Tools": "Herramientas",
        "Reports": "Reportes",
        "Favorites": "Favoritos",
        "Export Data": "Exportar Datos",
        "Import Data": "Importar Datos",
        "Duplicate": "Duplicar",
        "Archive": "Archivar",
        "Unarchive": "Desarchivar",
    }
    
    translated_count = 0
    for english, spanish in translations.items():
        pattern = f'msgid "{re.escape(english)}"\nmsgstr ""'
        if re.search(pattern, content):
            content = re.sub(pattern, f'msgid "{english}"\nmsgstr "{spanish}"', content)
            translated_count += 1
            print(f"✓ {english}")
    
    with open(po_file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return translated_count

def main():
    po_file = '/opt/odoo18/odoo-custom-addons/odoo_medical/i18n/es.po'
    
    print("Applying final comprehensive translations...")
    count = apply_final_translations(po_file)
    print(f"\n✅ Applied {count} final translations")
    
    print("\nChecking final status...")
    try:
        result = subprocess.run(['grep', '-c', 'msgstr ""', po_file], 
                              capture_output=True, text=True)
        remaining = int(result.stdout.strip())
        
        total_result = subprocess.run(['grep', '-c', '^msgid', po_file],
                                    capture_output=True, text=True)
        total = int(total_result.stdout.strip()) - 1  # Subtract empty msgid
        
        translated = total - remaining
        percentage = (translated / total) * 100 if total > 0 else 0
        
        print(f"\n📊 FINAL TRANSLATION STATUS:")
        print(f"   Total strings: {total}")
        print(f"   Translated: {translated}")
        print(f"   Remaining: {remaining}")
        print(f"   Progress: {percentage:.1f}%")
        
        if percentage >= 80:
            print(f"\n🎉 Excellent! Translation is {percentage:.1f}% complete!")
            print("   The module is now ready for Spanish users.")
        elif percentage >= 60:
            print(f"\n👍 Good progress! Translation is {percentage:.1f}% complete!")
            print("   Most important strings should be translated.")
        else:
            print(f"\n📝 Translation is {percentage:.1f}% complete.")
            print(f"   Consider translating the remaining {remaining} strings for full coverage.")
        
    except Exception as e:
        print(f"Error checking status: {e}")

if __name__ == "__main__":
    main()
