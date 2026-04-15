# 🔄 DEBUGGING GODTIER - Modo Watch con Auto-Actualización
# ==================================================
# Ejecuta tests continuamente y muestra dashboard en tiempo real
# Uso: .\ACTIVATE_WATCH.ps1

param(
    [int]$Interval = 5  # Intervalo en segundos entre ejecuciones
)

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                          ║" -ForegroundColor Cyan
Write-Host "║       🔄 DEBUGGING GODTIER - MODO WATCH 🔄              ║" -ForegroundColor Cyan
Write-Host "║     Auto-Actualización Continua de Tests                ║" -ForegroundColor Cyan
Write-Host "║                                                          ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$projectRoot = $PSScriptRoot
Set-Location $projectRoot

# Activar entorno virtual
Write-Host "🔄 Activando entorno virtual..." -ForegroundColor Yellow
& ".venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "⏰ Intervalo de actualización: $Interval segundos" -ForegroundColor Green
Write-Host "⏹️  Presiona Ctrl+C para detener" -ForegroundColor Yellow
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""

$runCount = 0

# Bucle infinito de monitoreo
while ($true) {
    $runCount++
    $timestamp = Get-Date -Format "HH:mm:ss"
    
    # Limpiar pantalla cada 10 ejecuciones para mantener legibilidad
    if ($runCount % 10 -eq 0) {
        Clear-Host
        Write-Host "🔄 MODO WATCH ACTIVO - Ejecución #$runCount" -ForegroundColor Cyan
        Write-Host ""
    }
    
    Write-Host "[$timestamp] 🧪 Ejecutando tests (Run #$runCount)..." -ForegroundColor Yellow
    
    # Ejecutar tests
    try {
        $testOutput = pytest tests/ -v --tb=short 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[$timestamp] ✅ Tests PASADOS - Todo OK" -ForegroundColor Green
        } else {
            Write-Host "[$timestamp] ❌ Tests FALLIDOS - Revisar errores" -ForegroundColor Red
            # Mostrar últimas líneas de error
            $testOutput | Select-Object -Last 5 | ForEach-Object {
                Write-Host "   $_" -ForegroundColor DarkRed
            }
        }
    } catch {
        Write-Host "[$timestamp] ⚠️ Error ejecutando tests: $_" -ForegroundColor Red
    }
    
    # Generar dashboard si está disponible
    if (Test-Path "src/dashboard/audit.py") {
        try {
            python -c "from src.dashboard.audit import AuditDashboard; AuditDashboard().generate_report('AUDIT_REPORT.html')" 2>&1 | Out-Null
            if ($LASTEXITCODE -eq 0) {
                Write-Host "[$timestamp] 📊 Dashboard actualizado: AUDIT_REPORT.html" -ForegroundColor Cyan
            }
        } catch {
            # Silenciar errores del dashboard
        }
    }
    
    # Mostrar estado del sistema
    $filesChanged = (git status --short 2>&1 | Measure-Object).Count
    if ($filesChanged -gt 0) {
        Write-Host "[$timestamp] 📝 Archivos modificados: $filesChanged" -ForegroundColor Magenta
    }
    
    Write-Host "[$timestamp] ⏳ Esperando $Interval segundos..." -ForegroundColor DarkGray
    Write-Host ""
    
    # Esperar intervalo
    Start-Sleep -Seconds $Interval
}
