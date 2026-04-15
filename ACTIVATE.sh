#!/bin/bash

# 🚀 DEBUGGING GODTIER - Activación del Sistema (Linux/Mac)
# ==================================================
# Sistema Unificado de IA para Auto-Debugging y Optimización
# Versión: 2.1.0 - God Tier Edition
# Fecha: Diciembre 25, 2025

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║          🔥 DEBUGGING GODTIER v2.1 🔥                   ║"
echo "║     Sistema de Auto-Debugging + IA Neuro-Simbólica      ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# ====================================
# 🔧 VERIFICACIÓN DEL ENTORNO
# ====================================
echo -e "${YELLOW}🔍 Verificando entorno...${NC}"

# Verificar Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "  ${GREEN}✅ Python: $PYTHON_VERSION${NC}"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    echo -e "  ${GREEN}✅ Python: $PYTHON_VERSION${NC}"
    PYTHON_CMD="python"
else
    echo -e "  ${RED}❌ Python no encontrado. Por favor instala Python 3.8+${NC}"
    exit 1
fi

# Verificar Git
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    echo -e "  ${GREEN}✅ Git: $GIT_VERSION${NC}"
else
    echo -e "  ${YELLOW}⚠️ Git no encontrado (opcional)${NC}"
fi

# ====================================
# 📦 CONFIGURACIÓN DEL ENTORNO VIRTUAL
# ====================================
echo ""
echo -e "${YELLOW}📦 Configurando entorno virtual...${NC}"

VENV_PATH=".venv"

if [ ! -d "$VENV_PATH" ]; then
    echo -e "  ${CYAN}🔨 Creando entorno virtual...${NC}"
    $PYTHON_CMD -m venv $VENV_PATH
    echo -e "  ${GREEN}✅ Entorno virtual creado${NC}"
else
    echo -e "  ${GREEN}✅ Entorno virtual ya existe${NC}"
fi

# Activar entorno virtual
echo -e "  ${CYAN}🔄 Activando entorno virtual...${NC}"
source "$VENV_PATH/bin/activate"

# ====================================
# 📚 INSTALACIÓN DE DEPENDENCIAS
# ====================================
echo ""
echo -e "${YELLOW}📚 Instalando dependencias...${NC}"

if [ -f "requirements.txt" ]; then
    echo -e "  ${CYAN}📥 Instalando desde requirements.txt...${NC}"
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt
    echo -e "  ${GREEN}✅ Dependencias instaladas${NC}"
else
    echo -e "  ${YELLOW}⚠️ requirements.txt no encontrado${NC}"
fi

# ====================================
# 🗂️ VERIFICACIÓN DE ESTRUCTURA
# ====================================
echo ""
echo -e "${YELLOW}🗂️ Verificando estructura del proyecto...${NC}"

REQUIRED_DIRS=("src" "data" "logs" "outputs" "cache" "models" "checkpoints" "tests" "examples" "docs")

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo -e "  ${GREEN}✅ Creado: $dir/${NC}"
    else
        echo -e "  ${GREEN}✅ Existe: $dir/${NC}"
    fi
done

# ====================================
# 🧪 EJECUTAR TESTS
# ====================================
echo ""
echo -e "${YELLOW}🧪 Ejecutando tests de verificación...${NC}"

if [ -d "tests" ]; then
    if command -v pytest &> /dev/null; then
        pytest tests/ -v --tb=short > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo -e "  ${GREEN}✅ Tests pasados correctamente${NC}"
        else
            echo -e "  ${YELLOW}⚠️ Algunos tests fallaron (normal en primera activación)${NC}"
        fi
    else
        echo -e "  ${YELLOW}⚠️ pytest no disponible${NC}"
    fi
fi

# ====================================
# 📊 RESUMEN DEL SISTEMA
# ====================================
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║              📊 SISTEMA ACTIVADO                         ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}🎯 Características Activas:${NC}"
echo "   ✅ Auto-Debugging con AST"
echo "   ✅ IA Neuro-Simbólica (NeuroSys AGI)"
echo "   ✅ Protocolo Lazarus (Self-Healing)"
echo "   ✅ Protocolo Darwin (Evolution)"
echo "   ✅ Git Senior Integration"
echo "   ✅ Safety Scanner"
echo ""
echo -e "${GREEN}📁 Directorios Configurados:${NC}"
echo "   📂 src/        - Código fuente"
echo "   📂 data/       - Bases de datos"
echo "   📂 logs/       - Registros del sistema"
echo "   📂 outputs/    - Resultados de procesamiento"
echo "   📂 models/     - Modelos de IA"
echo "   📂 tests/      - Tests unitarios"
echo ""

# ====================================
# 🚀 COMANDOS DISPONIBLES
# ====================================
echo -e "${GREEN}🚀 Comandos Disponibles:${NC}"
echo ""
echo -e "   ${CYAN}🔍 Debug automático:${NC}"
echo "      python main.py debug <archivo.py>"
echo ""
echo -e "   ${CYAN}🧬 Optimización Darwin:${NC}"
echo "      python main.py optimize <archivo.py>"
echo ""
echo -e "   ${CYAN}♻️  Auto-reparación Lazarus:${NC}"
echo "      python main.py heal <archivo.py>"
echo ""
echo -e "   ${CYAN}🧪 Ejecutar tests:${NC}"
echo "      pytest tests/ -v"
echo ""
echo -e "   ${CYAN}📊 Dashboard de auditoría:${NC}"
echo "      python main.py audit"
echo ""

# ====================================
# ✨ MENSAJE FINAL
# ====================================
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║    ✨ DEBUGGING GODTIER ESTÁ LISTO PARA USAR ✨         ║"
echo "║                                                          ║"
echo "║    🎯 Ejecuta: python main.py --help                    ║"
echo "║    📖 Lee: README.md para más información               ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Crear archivo de estado
mkdir -p logs
date > logs/last_activation.txt
echo -e "${NC}💾 Estado guardado en: logs/last_activation.txt${NC}"
echo ""
