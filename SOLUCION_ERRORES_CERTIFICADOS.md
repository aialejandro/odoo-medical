# Solución de Problemas - Certificados Médicos

## Error: "action_print_private_certificate no es una acción válida"

### 🔍 Problema Identificado
El error indica que Odoo no puede encontrar los métodos `action_print_private_certificate` y `action_print_iess_certificate` en el modelo `medical.consultation`.

### ✅ Soluciones Implementadas

#### 1. **Verificación de Sintaxis**
- ✅ Los métodos están correctamente definidos en la clase `MedicalConsultation`
- ✅ La sintaxis Python es válida 
- ✅ La indentación es correcta

#### 2. **Limpieza de Cache**
```bash
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +
```

#### 3. **Métodos Mejorados**
Los métodos ahora incluyen:
- Validación de estado (solo consultas finalizadas)
- Búsqueda dinámica de reportes
- Fallback con notificación si los reportes no están disponibles

#### 4. **Orden de Carga Corregido**
En `__manifest__.py`, los reportes se cargan antes que las vistas:
```python
'data': [
    # ... otros archivos ...
    'reports/medical_certificate_reports.xml',
    'reports/private_medical_certificate_template.xml',
    'reports/iess_medical_certificate_template.xml',
    'views/medical_consultation_views.xml',  # Después de los reportes
    # ... otras vistas ...
],
```

### 🔧 Pasos para Actualizar el Módulo

1. **Limpiar Cache de Python:**
```bash
cd /opt/odoo18/odoo-custom-addons/odoo_medical
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +
```

2. **Verificar Archivos:**
```bash
python3 validate_certificates.py
```

3. **Actualizar Módulo en Odoo:**
```bash
cd /opt/odoo18
python3 -u odoo/odoo-bin -c /opt/odoo18/odoo.conf -d odoo18_db --update=odoo_medical --stop-after-init
```

4. **Si persiste el error, reiniciar completamente:**
```bash
# Desinstalar módulo
python3 -u odoo/odoo-bin -c /opt/odoo18/odoo.conf -d odoo18_db --update=odoo_medical --uninstall=odoo_medical --stop-after-init

# Instalar nuevamente
python3 -u odoo/odoo-bin -c /opt/odoo18/odoo.conf -d odoo18_db --update=odoo_medical --stop-after-init
```

### 🎯 Funcionalidades de los Métodos

#### `action_print_private_certificate()`
- Verifica que la consulta esté finalizada
- Busca el reporte dinámicamente
- Genera certificado médico privado
- Muestra notificación si no encuentra el reporte

#### `action_print_iess_certificate()`
- Verifica que la consulta esté finalizada  
- Busca el reporte dinámicamente
- Genera certificado médico IESS
- Muestra notificación si no encuentra el reporte

### 📋 Verificaciones Adicionales

Si el problema persiste, verificar:

1. **Modelo cargado correctamente:**
```python
# En shell de Odoo
model = env['medical.consultation']
print(hasattr(model, 'action_print_private_certificate'))
```

2. **Reportes disponibles:**
```python
# En shell de Odoo
reports = env['ir.actions.report'].search([('model', '=', 'medical.consultation')])
print(reports.mapped('name'))
```

3. **Vista sin errores XML:**
```bash
python3 -c "import xml.etree.ElementTree as ET; ET.parse('views/medical_consultation_views.xml')"
```

### 🔄 Estado Actual
- ✅ Métodos definidos correctamente
- ✅ Sintaxis Python válida
- ✅ Archivos XML válidos
- ✅ Orden de carga corregido
- ✅ Cache limpiado
- ✅ Fallbacks implementados

El módulo debería actualizar correctamente ahora.
