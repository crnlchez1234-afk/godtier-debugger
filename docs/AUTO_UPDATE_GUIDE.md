# 🔄 Guía de Auto-Actualización - DEBUGGING GODTIER

## ✨ Nuevas Funcionalidades de Auto-Actualización

Hemos agregado **3 modos de auto-actualización** para monitorear tu sistema en tiempo real:

---

## 🎯 Opción 1: Dashboard con Meta Refresh (Simple)

**Archivo**: `serve_dashboard.py`

El dashboard HTML se recarga automáticamente cada 5 segundos usando meta-refresh.

### Uso:
```powershell
python serve_dashboard.py
```

Luego abre: `http://localhost:8080/AUDIT_REPORT.html`

✅ **Ventajas**: Simple, no requiere dependencias adicionales
❌ **Desventajas**: Recarga completa de la página (parpadeo)

---

## 🚀 Opción 2: Dashboard con WebSocket (Recomendado)

**Archivo**: `serve_dashboard_live.py`

Dashboard interactivo que se actualiza en tiempo real **SIN recargar la página** usando WebSocket.

### Uso:
```powershell
python serve_dashboard_live.py
```

Luego abre: `http://localhost:8080`

✅ **Ventajas**: 
- Actualización en tiempo real sin parpadeos
- Transiciones suaves
- Indicador de conexión
- Auto-reconexión si se pierde la conexión

❌ **Desventajas**: Requiere `aiohttp` (ya instalado)

---

## 🧪 Opción 3: Modo Watch para Tests

**Archivo**: `ACTIVATE_WATCH.ps1`

Ejecuta tests automáticamente cada N segundos y actualiza el dashboard.

### Uso:
```powershell
# Ejecutar cada 5 segundos (default)
.\ACTIVATE_WATCH.ps1

# Ejecutar cada 10 segundos
.\ACTIVATE_WATCH.ps1 -Interval 10
```

✅ **Ventajas**:
- Monitoreo continuo de tests
- Detecta cambios automáticamente
- Muestra estado en consola
- Actualiza dashboard HTML

❌ **Desventajas**: Solo en PowerShell

---

## 📊 Comparación Rápida

| Característica | Meta Refresh | WebSocket | Watch Mode |
|---|---|---|---|
| **Auto-actualización** | ✅ Cada 5s | ✅ Cada 3s | ✅ Configurable |
| **Sin recargar página** | ❌ | ✅ | N/A (consola) |
| **Ejecuta tests** | ❌ | ❌ | ✅ |
| **Visualización** | Navegador | Navegador | Consola |
| **Dependencias** | Ninguna | aiohttp | PowerShell |

---

## 🎮 Ejemplo de Uso Completo

### Escenario 1: Desarrollo Activo
```powershell
# Terminal 1: Tests en loop
.\ACTIVATE_WATCH.ps1 -Interval 3

# Terminal 2: Dashboard en vivo
python serve_dashboard_live.py

# Navegador: http://localhost:8080
```

### Escenario 2: Demostración Simple
```powershell
python serve_dashboard.py
# Abre: http://localhost:8080/AUDIT_REPORT.html
```

---

## 🔧 Personalización

### Cambiar intervalo de actualización en WebSocket:
Edita `serve_dashboard_live.py`:
```python
await asyncio.sleep(3)  # Cambiar a 5, 10, etc.
```

### Cambiar meta-refresh:
Edita `src/dashboard/audit.py`:
```html
<meta http-equiv="refresh" content="5">  # Cambiar a 10, 15, etc.
```

---

## 🎯 Recomendación

Para **desarrollo activo**: Usa `serve_dashboard_live.py` (WebSocket)
Para **demos rápidas**: Usa `serve_dashboard.py` (Meta Refresh)  
Para **testing continuo**: Usa `ACTIVATE_WATCH.ps1`

---

**¡Disfruta del monitoreo en tiempo real!** 🚀
