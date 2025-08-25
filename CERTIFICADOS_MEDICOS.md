# Certificados Médicos - Implementación

## Resumen
Se han agregado dos botones en el modelo `medical.consultation` para imprimir certificados médicos:
1. **Certificado Médico Particular** - Para uso privado
2. **Certificado Médico IESS** - Formato oficial del Instituto Ecuatoriano de Seguridad Social

## Campos Agregados

### En el modelo `medical.consultation`:
- `doctor_id`: Campo Many2one hacia `res.users` para identificar al médico tratante
- `doctor_license`: Campo de texto para el número de licencia médica del doctor

## Campos Utilizados en los Certificados

### Información del Paciente:
- `patient_id.name`: Nombre completo del paciente
- `patient_vat`: Cédula/RUC del paciente
- `birth_date`: Fecha de nacimiento
- `age`: Edad calculada automáticamente

### Información del Doctor:
- `doctor_id.name`: Nombre del médico
- `doctor_license`: Número de licencia médica

### Información Médica:
- `diagnosis`: Diagnóstico médico
- `cie10_code`: Código CIE-10 con descripción
- `has_symptoms`: Si el paciente presenta síntomas
- `medical_cause`: Causa médica (enfermedad general, accidente laboral, etc.)
- `work_restriction_type`: Tipo de restricción laboral
- `rest_days`: Días de reposo prescritos
- `rest_start_date`: Fecha de inicio del reposo
- `rest_end_date`: Fecha de fin del reposo
- `treatment_description`: Descripción del tratamiento
- `observations`: Observaciones médicas adicionales
- `prescription_line_ids`: Prescripciones médicas detalladas

### Información de la Consulta:
- `consultation_date`: Fecha de la consulta
- `consultation_reason`: Motivo de la consulta
- `evolution`: Evolución del paciente
- `next_appointment_date`: Próxima cita

## Funcionalidades Implementadas

### Botones en la Interfaz:
1. **"Print Private Certificate"** - Disponible solo cuando la consulta está en estado 'finished'
2. **"Print IESS Certificate"** - Disponible solo cuando la consulta está en estado 'finished'

### Métodos en el Modelo:
- `action_print_private_certificate()`: Genera el certificado médico privado
- `action_print_iess_certificate()`: Genera el certificado médico IESS

### Validaciones:
- Los certificados solo pueden generarse para consultas finalizadas (estado 'finished')
- Se muestra un mensaje de error si se intenta generar un certificado para una consulta no finalizada

## Plantillas de Certificados

### Certificado Médico Particular:
- Diseño limpio y profesional
- Información completa del paciente y médico
- Sección detallada de diagnóstico y tratamiento
- Tabla de prescripciones farmacológicas
- Área para firma y sello del médico

### Certificado Médico IESS:
- Formato oficial del IESS con colores institucionales
- Secciones claramente definidas según normativas
- Casillas de verificación para diferentes tipos de restricciones
- Tabla destacada para días de incapacidad
- Información del médico tratante con espacio para firma y sello

## Archivos Creados:

### Modelos:
- Modificaciones en `models/medical_consultation.py`

### Vistas:
- Modificaciones en `views/medical_consultation_views.xml`

### Reportes:
- `reports/medical_certificate_reports.xml` - Definición de reportes
- `reports/private_medical_certificate_template.xml` - Plantilla del certificado privado
- `reports/iess_medical_certificate_template.xml` - Plantilla del certificado IESS

### Manifiesto:
- Actualización de `__manifest__.py` para incluir los nuevos archivos de reportes

## Uso:
1. Crear una consulta médica
2. Completar los campos requeridos (paciente, médico, diagnóstico, etc.)
3. Finalizar la consulta (cambiar estado a 'Finished')
4. Usar los botones "Print Private Certificate" o "Print IESS Certificate" según se requiera

## Notas de Desarrollo:
- Los reportes utilizan QWeb templates de Odoo
- Se aplicó formato HTML con CSS inline para mejor compatibilidad
- Los certificados se pueden imprimir en formato PDF
- La validación de estado previene la generación de certificados incompletos
