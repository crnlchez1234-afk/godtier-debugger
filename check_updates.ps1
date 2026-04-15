# 🔄 DEBUGGING GODTIER - Auto-Update Scheduler
# Ejecuta auto-actualización periódicamente

param(
    [int]$DaysInterval = 30,  # Verificar cada 30 días por defecto
    [switch]$RunNow,          # Ejecutar inmediatamente
    [switch]$AutoUpdate       # Actualizar sin preguntar
)

$projectRoot = $PSScriptRoot
Set-Location $projectRoot

# Activar entorno virtual
& ".venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                          ║" -ForegroundColor Cyan
Write-Host "║     🔄 AUTO-UPDATE SCHEDULER - DEBUGGING GODTIER        ║" -ForegroundColor Cyan
Write-Host "║                                                          ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$lastCheckFile = "logs/last_update_check.txt"

# Verificar última actualización
$needsCheck = $false

if (-not (Test-Path $lastCheckFile)) {
    $needsCheck = $true
    Write-Host "📅 Primera verificación - No hay registro previo" -ForegroundColor Yellow
} else {
    $lastCheck = Get-Content $lastCheckFile
    $lastCheckDate = [DateTime]::Parse($lastCheck)
    $daysSince = (Get-Date) - $lastCheckDate
    
    Write-Host "📅 Última verificación: $($lastCheckDate.ToString('yyyy-MM-dd HH:mm:ss'))" -ForegroundColor Gray
    Write-Host "⏱️  Días desde última verificación: $([math]::Floor($daysSince.TotalDays))" -ForegroundColor Gray
    
    if ($daysSince.TotalDays -ge $DaysInterval -or $RunNow) {
        $needsCheck = $true
        Write-Host "✅ Es hora de verificar actualizaciones" -ForegroundColor Green
    } else {
        Write-Host "⏭️  Aún no es necesario verificar (faltan $([math]::Ceiling($DaysInterval - $daysSince.TotalDays)) días)" -ForegroundColor Yellow
    }
}

if ($needsCheck -or $RunNow) {
    Write-Host ""
    Write-Host "🔍 Iniciando verificación de obsolescencia..." -ForegroundColor Cyan
    Write-Host ""
    
    # Ejecutar auto-updater
    if ($AutoUpdate) {
        python auto_updater.py --auto
    } else {
        python auto_updater.py
    }
    
    # Actualizar marca de tiempo
    New-Item -ItemType Directory -Force -Path "logs" | Out-Null
    Get-Date -Format "yyyy-MM-dd HH:mm:ss" | Out-File $lastCheckFile
    
    Write-Host ""
    Write-Host "✅ Verificación completada y registrada" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "ℹ️  No es necesario verificar actualizaciones en este momento" -ForegroundColor Cyan
    Write-Host "   Usa -RunNow para forzar verificación" -ForegroundColor Gray
}

Write-Host ""
Write-Host "💡 Tip: Agrega este script a Task Scheduler para verificación automática" -ForegroundColor Yellow
Write-Host ""
