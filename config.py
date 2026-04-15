# 🔧 DEBUGGING GODTIER - Configuración del Sistema
# Fecha: Diciembre 25, 2025
# Sistema Unificado de IA para Auto-Debugging y Optimización

# ====================================
# 🎯 CONFIGURACIÓN GENERAL
# ====================================
PROJECT_NAME = "DEBUGGING_GODTIER"
VERSION = "2.1.0"
ENVIRONMENT = "production"  # development, staging, production

# ====================================
# 📁 RUTAS DEL PROYECTO
# ====================================
from pathlib import Path
ROOT_DIR = Path(__file__).parent.absolute()

PATHS = {
    "root": str(ROOT_DIR),
    "src": str(ROOT_DIR / "src"),
    "data": str(ROOT_DIR / "data"),
    "logs": str(ROOT_DIR / "logs"),
    "outputs": str(ROOT_DIR / "outputs"),
    "cache": str(ROOT_DIR / "cache"),
    "models": str(ROOT_DIR / "models"),
    "checkpoints": str(ROOT_DIR / "checkpoints"),
    "tests": str(ROOT_DIR / "tests"),
    "examples": str(ROOT_DIR / "examples"),
}

# ====================================
# 🧠 CONFIGURACIÓN IA
# ====================================
AI_CONFIG = {
    "neuro_symbolic_enabled": True,
    "meta_learning_enabled": True,
    "knowledge_graph_enabled": True,
    "multi_agent_enabled": True,
    
    # Modelos
    "primary_model": "deepseek-coder",
    "fallback_model": "gpt-4",
    "embedding_model": "text-embedding-ada-002",
    
    # Capacidades
    "max_reasoning_depth": 5,
    "max_iterations": 10,
    "temperature": 0.7,
    "top_p": 0.95,
}

# ====================================
# 🔍 CONFIGURACIÓN AUTO-DEBUGGER
# ====================================
DEBUGGER_CONFIG = {
    "enabled": True,
    "auto_fix": True,
    "max_attempts": 3,
    "severity_threshold": "medium",  # low, medium, high, critical
    
    # Análisis
    "static_analysis": True,
    "dynamic_analysis": True,
    "security_scanning": True,
    "performance_profiling": True,
    
    # Lenguajes soportados
    "supported_languages": ["python", "javascript", "typescript", "java", "cpp"],
}

# ====================================
# ♻️ PROTOCOLO LAZARUS (Self-Healing)
# ====================================
LAZARUS_CONFIG = {
    "enabled": True,
    "auto_restart": True,
    "max_restart_attempts": 5,
    "restart_delay": 2,  # segundos
    
    # Monitoreo
    "monitor_cpu": True,
    "monitor_memory": True,
    "monitor_disk": True,
    "monitor_network": False,
    
    # Thresholds
    "cpu_threshold": 90,  # %
    "memory_threshold": 85,  # %
    "disk_threshold": 90,  # %
    
    # Backup
    "auto_backup": True,
    "backup_interval": 3600,  # segundos (1 hora)
}

# ====================================
# 🧬 PROTOCOLO DARWIN (Evolution)
# ====================================
DARWIN_CONFIG = {
    "enabled": True,
    "auto_optimize": True,
    "genetic_algorithm": True,
    
    # Evolución
    "population_size": 20,
    "generations": 10,
    "mutation_rate": 0.1,
    "crossover_rate": 0.7,
    "elitism_rate": 0.1,
    
    # Benchmark
    "benchmark_iterations": 100,
    "benchmark_timeout": 30,  # segundos
    
    # Gene Memory
    "gene_memory_enabled": True,
    "gene_memory_db": "data/darwin_gene_memory.db",
    "keep_top_genes": 100,
}

# ====================================
# 🔐 SEGURIDAD Y SAFETY
# ====================================
SAFETY_CONFIG = {
    "enabled": True,
    "strict_mode": True,
    
    # Escaneo de seguridad
    "scan_dangerous_imports": True,
    "scan_system_calls": True,
    "scan_file_operations": True,
    "scan_network_operations": True,
    
    # Operaciones bloqueadas
    "blocked_imports": ["os.system", "subprocess.Popen", "eval", "exec"],
    "blocked_patterns": [r"rm\s+-rf", r"format\s+c:", r"del\s+/f"],
    
    # Sandbox
    "use_sandbox": True,
    "sandbox_timeout": 10,  # segundos
}

# ====================================
# 📊 LOGGING Y AUDITORÍA
# ====================================
LOGGING_CONFIG = {
    "level": "INFO",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "date_format": "%Y-%m-%d %H:%M:%S",
    
    # Archivos
    "log_to_file": True,
    "log_file": "logs/debugging_godtier.log",
    "max_bytes": 10485760,  # 10 MB
    "backup_count": 5,
    
    # Auditoría
    "audit_enabled": True,
    "audit_file": "logs/audit.log",
    "audit_sensitive_operations": True,
}

# ====================================
# 🔧 GIT INTEGRATION
# ====================================
GIT_CONFIG = {
    "enabled": True,
    "auto_commit": False,
    "auto_push": False,
    
    # Commits inteligentes
    "smart_commits": True,
    "commit_message_template": "[{type}] {description}",
    
    # Branch management
    "default_branch": "main",
    "feature_branch_prefix": "feature/",
    "fix_branch_prefix": "fix/",
}

# ====================================
# 🌐 API Y SERVICIOS
# ====================================
API_CONFIG = {
    "enabled": False,
    "host": "0.0.0.0",
    "port": 8000,
    "workers": 4,
    
    # Autenticación
    "auth_enabled": True,
    "api_key_required": True,
    
    # Rate limiting
    "rate_limit_enabled": True,
    "requests_per_minute": 60,
}

# ====================================
# ⚡ PERFORMANCE Y OPTIMIZACIÓN
# ====================================
PERFORMANCE_CONFIG = {
    "max_workers": 4,
    "async_enabled": True,
    "cache_enabled": True,
    "cache_ttl": 3600,  # segundos
    
    # GPU
    "use_gpu": True,
    "gpu_memory_fraction": 0.8,
    
    # Multiprocessing
    "use_multiprocessing": True,
    "max_processes": 4,
}

# ====================================
# 🔔 NOTIFICACIONES
# ====================================
NOTIFICATIONS_CONFIG = {
    "enabled": False,
    "slack_webhook": None,
    "email_enabled": False,
    "email_smtp": None,
    
    # Alertas
    "alert_on_error": True,
    "alert_on_critical": True,
    "alert_on_success": False,
}

# ====================================
# 🧪 TESTING Y DESARROLLO
# ====================================
TESTING_CONFIG = {
    "test_mode": False,
    "verbose": True,
    "coverage_enabled": True,
    "coverage_threshold": 80,  # %
    
    # Pytest
    "pytest_args": ["-v", "--tb=short", "--cov=src"],
}

# ====================================
# 📦 EXPORTAR CONFIGURACIÓN
# ====================================
CONFIG = {
    "project": {
        "name": PROJECT_NAME,
        "version": VERSION,
        "environment": ENVIRONMENT,
    },
    "paths": PATHS,
    "ai": AI_CONFIG,
    "debugger": DEBUGGER_CONFIG,
    "lazarus": LAZARUS_CONFIG,
    "darwin": DARWIN_CONFIG,
    "safety": SAFETY_CONFIG,
    "logging": LOGGING_CONFIG,
    "git": GIT_CONFIG,
    "api": API_CONFIG,
    "performance": PERFORMANCE_CONFIG,
    "notifications": NOTIFICATIONS_CONFIG,
    "testing": TESTING_CONFIG,
}

# Función helper para obtener configuración
def get_config(key_path: str, default=None):
    """
    Obtiene un valor de configuración usando dot notation.
    Ejemplo: get_config('ai.primary_model')
    """
    keys = key_path.split('.')
    value = CONFIG
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default
    return value
