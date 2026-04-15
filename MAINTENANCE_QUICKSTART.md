# 🔄 MANTENIMIENTO RÁPIDO - Ejecuta cada mes

## Para que el proyecto NO quede obsoleto en 6 meses:

### 1️⃣ Verificar (1 minuto):
```powershell
python auto_updater.py --check-only
```

### 2️⃣ Actualizar (5 minutos):
```powershell
python auto_updater.py
```

### 3️⃣ Probar (2 minutos):
```powershell
pytest tests/
```

## ✅ Listo! El proyecto está actualizado.

---

### 🤖 AUTOMATIZAR (Una sola vez):

Ejecuta esto UNA VEZ para verificar automáticamente cada mes:

```powershell
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File E:\DEBUGGING_GODTIER\check_updates.ps1"
$trigger = New-ScheduledTaskTrigger -Weekly -At 9AM -DaysOfWeek Monday
Register-ScheduledTask -TaskName "DEBUGGING_GODTIER_Check" -Action $action -Trigger $trigger
```

**¡Ya no tienes que acordarte! Windows lo hará por ti.**

---

Ver guía completa: [docs/MAINTENANCE_GUIDE.md](docs/MAINTENANCE_GUIDE.md)
