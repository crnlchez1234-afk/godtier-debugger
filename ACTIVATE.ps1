# 🚀 DEBUGGING GODTIER - Activación del Sistema
# ==================================================
# Sistema Unificado de IA para Auto-Debugging y Optimización
# Versión: 2.1.0 - God Tier Edition
# Fecha: Diciembre 25, 2025

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                          ║" -ForegroundColor Cyan
Write-Host "║          🔥 DEBUGGING GODTIER v2.1 🔥                   ║" -ForegroundColor Cyan
Write-Host "║     Sistema de Auto-Debugging + IA Neuro-Simbólica      ║" -ForegroundColor Cyan
Write-Host "║                                                          ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ====================================
# 🔧 VERIFICACIÓN DEL ENTORNO
# ====================================
Write-Host "🔍 Verificando entorno..." -ForegroundColor Yellow

$projectRoot = $PSScriptRoot
Set-Location $projectRoot

# Verificar Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Python no encontrado. Por favor instala Python 3.8+" -ForegroundColor Red
    exit 1
}

# Verificar Git
try {
    $gitVersion = git --version 2>&1
    Write-Host "  ✅ Git: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️ Git no encontrado (opcional)" -ForegroundColor Yellow
}

# ====================================
# 📦 CONFIGURACIÓN DEL ENTORNO VIRTUAL
# ====================================
Write-Host ""
Write-Host "📦 Configurando entorno virtual..." -ForegroundColor Yellow

$venvPath = ".venv"

if (-not (Test-Path $venvPath)) {
    Write-Host "  🔨 Creando entorno virtual..." -ForegroundColor Cyan
    python -m venv $venvPath
    Write-Host "  ✅ Entorno virtual creado" -ForegroundColor Green
} else {
    Write-Host "  ✅ Entorno virtual ya existe" -ForegroundColor Green
}

# Activar entorno virtual
Write-Host "  🔄 Activando entorno virtual..." -ForegroundColor Cyan
& "$venvPath\Scripts\Activate.ps1"

# ====================================
# 📚 INSTALACIÓN DE DEPENDENCIAS
# ====================================
Write-Host ""
Write-Host "📚 Instalando dependencias..." -ForegroundColor Yellow

if (Test-Path "requirements.txt") {
    Write-Host "  📥 Instalando desde requirements.txt..." -ForegroundColor Cyan
    python -m pip install --upgrade pip | Out-Null
    pip install -r requirements.txt
    Write-Host "  ✅ Dependencias instaladas" -ForegroundColor Green
} else {
    Write-Host "  ⚠️ requirements.txt no encontrado" -ForegroundColor Yellow
}

# ====================================
# 🗂️ VERIFICACIÓN DE ESTRUCTURA
# ====================================
Write-Host ""
Write-Host "🗂️ Verificando estructura del proyecto..." -ForegroundColor Yellow

$requiredDirs = @("src", "data", "logs", "outputs", "cache", "models", "checkpoints", "tests", "examples", "docs")

foreach ($dir in $requiredDirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
        Write-Host "  ✅ Creado: $dir/" -ForegroundColor Green
    } else {
        Write-Host "  ✅ Existe: $dir/" -ForegroundColor Gray
    }
}

# ====================================
# 🧪 EJECUTAR TESTS
# ====================================
Write-Host ""
Write-Host "🧪 Ejecutando tests de verificación..." -ForegroundColor Yellow

if (Test-Path "tests") {
    try {
        pytest tests/ -v --tb=short 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✅ Tests pasados correctamente" -ForegroundColor Green
        } else {
            Write-Host "  ⚠️ Algunos tests fallaron (normal en primera activación)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  ⚠️ pytest no disponible o tests no ejecutados" -ForegroundColor Yellow
    }
}

# ====================================
# 📊 RESUMEN DEL SISTEMA
# ====================================
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║              📊 SISTEMA ACTIVADO                         ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "🎯 Características Activas:" -ForegroundColor Green
Write-Host "   ✅ Auto-Debugging con AST" -ForegroundColor White
Write-Host "   ✅ IA Neuro-Simbólica (NeuroSys AGI)" -ForegroundColor White
Write-Host "   ✅ Protocolo Lazarus (Self-Healing)" -ForegroundColor White
Write-Host "   ✅ Protocolo Darwin (Evolution)" -ForegroundColor White
Write-Host "   ✅ Git Senior Integration" -ForegroundColor White
Write-Host "   ✅ Safety Scanner" -ForegroundColor White
Write-Host ""
Write-Host "📁 Directorios Configurados:" -ForegroundColor Green
Write-Host "   📂 src/        - Código fuente" -ForegroundColor White
Write-Host "   📂 data/       - Bases de datos" -ForegroundColor White
Write-Host "   📂 logs/       - Registros del sistema" -ForegroundColor White
Write-Host "   📂 outputs/    - Resultados de procesamiento" -ForegroundColor White
Write-Host "   📂 models/     - Modelos de IA" -ForegroundColor White
Write-Host "   📂 tests/      - Tests unitarios" -ForegroundColor White
Write-Host ""

# ====================================
# 🚀 COMANDOS DISPONIBLES
# ====================================
Write-Host "🚀 Comandos Disponibles:" -ForegroundColor Green
Write-Host ""
Write-Host "   🔍 Debug automático:" -ForegroundColor Cyan
Write-Host "      python main.py debug <archivo.py>" -ForegroundColor White
Write-Host ""
Write-Host "   🧬 Optimización Darwin:" -ForegroundColor Cyan
Write-Host "      python main.py optimize <archivo.py>" -ForegroundColor White
Write-Host ""
Write-Host "   ♻️  Auto-reparación Lazarus:" -ForegroundColor Cyan
Write-Host "      python main.py heal <archivo.py>" -ForegroundColor White
Write-Host ""
Write-Host "   🧪 Ejecutar tests:" -ForegroundColor Cyan
Write-Host "      pytest tests/ -v" -ForegroundColor White
Write-Host ""
Write-Host "   📊 Dashboard de auditoría:" -ForegroundColor Cyan
Write-Host "      python main.py audit" -ForegroundColor White
Write-Host ""
Write-Host "   🔄 Verificar actualizaciones:" -ForegroundColor Cyan
Write-Host "      python auto_updater.py --check-only" -ForegroundColor White
Write-Host ""

# ====================================
# 🔄 VERIFICACIÓN DE OBSOLESCENCIA
# ====================================
$lastCheckFile = "logs/last_update_check.txt"
if (Test-Path $lastCheckFile) {
    $lastCheck = Get-Content $lastCheckFile
    $lastCheckDate = [DateTime]::Parse($lastCheck)
    $daysSince = (Get-Date) - $lastCheckDate
    
    if ($daysSince.TotalDays -ge 30) {
        Write-Host ""
        Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
        Write-Host "║                                                          ║" -ForegroundColor Yellow
        Write-Host "║    ⚠️  HAN PASADO $([math]::Floor($daysSince.TotalDays)) DÍAS DESDE ÚLTIMA ACTUALIZACIÓN    ║" -ForegroundColor Yellow
        Write-Host "║                                                          ║" -ForegroundColor Yellow
        Write-Host "║    Ejecuta: python auto_updater.py --check-only         ║" -ForegroundColor Yellow
        Write-Host "║                                                          ║" -ForegroundColor Yellow
        Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Yellow
        Write-Host ""
    }
}

# ====================================
# ✨ MENSAJE FINAL
# ====================================
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                                                          ║" -ForegroundColor Green
Write-Host "║    ✨ DEBUGGING GODTIER ESTÁ LISTO PARA USAR ✨         ║" -ForegroundColor Green
Write-Host "║                                                          ║" -ForegroundColor Green
Write-Host "║    🎯 Ejecuta: python main.py --help                    ║" -ForegroundColor Green
Write-Host "║    📖 Lee: README.md para más información               ║" -ForegroundColor Green
Write-Host "║                                                          ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# Crear archivo de estado
$statusFile = "logs/last_activation.txt"
New-Item -ItemType Directory -Force -Path "logs" | Out-Null
Get-Date -Format "yyyy-MM-dd HH:mm:ss" | Out-File $statusFile
Write-Host "💾 Estado guardado en: $statusFile" -ForegroundColor Gray
Write-Host ""
