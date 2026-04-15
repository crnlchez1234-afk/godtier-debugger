# 📅 DEBUGGING_GODTIER - Mantener Actualizado en 6 Meses

## 🎯 Sistema de Auto-Actualización Implementado

Para evitar que el proyecto quede obsoleto, hemos implementado un sistema automático de mantenimiento:

---

## 🔄 Archivos Creados

### 1. **auto_updater.py** - Verificador y Actualizador Principal
Realiza las siguientes verificaciones:

✅ **Paquetes desactualizados** - Detecta y actualiza dependencias
✅ **Versión de Python** - Advierte si Python está obsoleto  
✅ **Código deprecated** - Busca patrones de código obsoleto
✅ **Vulnerabilidades** - Escanea seguridad con pip-audit
✅ **Requirements.txt** - Actualiza versiones automáticamente

### 2. **check_updates.ps1** - Scheduler Automático
Script de PowerShell que:
- Verifica automáticamente cada 30 días
- Guarda registro de última verificación
- Se puede ejecutar manualmente o programar

---

## 🚀 Cómo Usar

### Verificación Manual (Recomendado mensualmente):

```powershell
# Solo verificar sin actualizar
python auto_updater.py --check-only

# Verificar y preguntar antes de actualizar
python auto_updater.py

# Actualizar TODO automáticamente
python auto_updater.py --auto
```

### Verificación Programada:

```powershell
# Verificar si han pasado 30 días
.\check_updates.ps1

# Forzar verificación ahora
.\check_updates.ps1 -RunNow

# Auto-actualizar sin preguntar
.\check_updates.ps1 -RunNow -AutoUpdate

# Verificar cada 15 días
.\check_updates.ps1 -DaysInterval 15
```

---

## 🤖 Automatización con Task Scheduler (Windows)

Para que se ejecute automáticamente cada mes:

### Opción 1: PowerShell (Fácil)
```powershell
# Crear tarea programada
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File E:\DEBUGGING_GODTIER\check_updates.ps1"
$trigger = New-ScheduledTaskTrigger -Daily -At 3AM
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable
Register-ScheduledTask -TaskName "DEBUGGING_GODTIER_AutoUpdate" -Action $action -Trigger $trigger -Settings $settings
```

### Opción 2: Task Scheduler GUI
1. Abre "Task Scheduler" (Programador de Tareas)
2. Crear Tarea Básica
3. Nombre: "DEBUGGING_GODTIER Auto-Update"
4. Disparador: Mensual (primer día del mes, 3:00 AM)
5. Acción: Iniciar programa
   - Programa: `PowerShell.exe`
   - Argumentos: `-File E:\DEBUGGING_GODTIER\check_updates.ps1 -AutoUpdate`

---

## 📊 Reportes Generados

Cada verificación genera un reporte JSON en:
```
logs/update_report_YYYYMMDD_HHMMSS.json
```

Contiene:
- Paquetes desactualizados
- Código obsoleto encontrado
- Versión de Python
- Timestamp de verificación

---

## ⚠️ Qué se Actualiza Automáticamente

### ✅ SÍ se actualiza automáticamente:
- Dependencias de Python (pip packages)
- requirements.txt
- Detección de código obsoleto

### ❌ Requiere acción manual:
- Versión de Python (avisos solamente)
- Cambios en código fuente (solo avisos)
- Migraciones de sintaxis

---

## 🎯 Calendario Recomendado de Mantenimiento

| Frecuencia | Acción | Comando |
|---|---|---|
| **Mensual** | Verificar actualizaciones | `python auto_updater.py --check-only` |
| **Trimestral** | Actualizar dependencias | `python auto_updater.py` |
| **Semestral** | Revisar código obsoleto | `python auto_updater.py --check-only` + revisar logs |
| **Anual** | Actualizar Python | Verificar nueva versión estable |

---

## 🔧 Personalización

### Cambiar intervalo de verificación:
```powershell
.\check_updates.ps1 -DaysInterval 15  # Cada 15 días
```

### Agregar patrones de código obsoleto:
Edita `auto_updater.py`:
```python
deprecated_patterns = {
    r'tu_patron_aqui': 'Mensaje de advertencia',
    # Agregar más patrones...
}
```

---

## 📋 Checklist de Mantenimiento Semestral

- [ ] Ejecutar `python auto_updater.py --check-only`
- [ ] Revisar reporte en `logs/update_report_*.json`
- [ ] Actualizar paquetes críticos
- [ ] Ejecutar tests: `pytest tests/`
- [ ] Verificar compatibilidad con nueva versión de Python
- [ ] Actualizar documentación si es necesario
- [ ] Commit y push cambios

---

## 🚨 Señales de Alerta (Revisar Inmediatamente)

⚠️ Python < 3.10 → **OBSOLETO**  
⚠️ Más de 10 paquetes desactualizados → **Actualizar**  
⚠️ Vulnerabilidades de seguridad → **Actualizar urgente**  
⚠️ Tests fallando después de actualizar → **Revisar compatibilidad**

---

## ✨ Beneficios

✅ **Sin obsolescencia** - El proyecto se mantiene moderno  
✅ **Seguridad** - Detección de vulnerabilidades  
✅ **Automatizado** - No requiere memoria, se ejecuta solo  
✅ **Reportes** - Historial de cambios y actualizaciones  
✅ **Flexible** - Puedes controlar qué y cuándo actualizar

---

**¡Tu proyecto DEBUGGING_GODTIER no quedará obsoleto en 6 meses!** 🚀

Última actualización: 25 de Diciembre, 2025
