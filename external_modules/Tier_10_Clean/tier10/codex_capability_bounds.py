from typing import Any, List, Tuple


# -*- coding: utf-8 -*-
"""
TIER 10 - Capability Bounds
============================
Define límites de auto-modificación para prevenir daño

Advanced Code Governance & Refactoring System
Date: December 6, 2025
"""

class CapabilityBounds:
    """Define qué puede y qué NO puede auto-modificar el AGI"""

    def __init__(self) -> None:
        # Módulos PROTEGIDOS que NO se pueden auto-modificar
        self.PROTECTED_MODULES = {
            'codex_core.py',           # Core system
            'tier10_singularity.py',   # Governance
            'safety_monitor.py',       # Safety systems
            'human_override.py',       # Human control
            'capability_bounds.py'     # Self-protection
        }

        # Tipos de cambios permitidos
        self.ALLOWED_CHANGES = {
            'optimize',       # Optimizaciones de performance
            'refactor',       # Refactoring sin cambiar lógica
            'documentation',  # Mejoras de docs
            'bugfix'          # Correcciones de bugs
        }

        # Tipos de cambios PROHIBIDOS
        self.FORBIDDEN_CHANGES = {
            'bypass_safety',  # Evitar sistemas de seguridad
            'modify_core',    # Modificar lógica central
            'escalate',       # Escalar privilegios
            'exfiltrate'      # Extraer datos sensibles
        }

    # TODO: REFACTOR - Función muy larga (60 líneas). Dividir en funciones más pequeñas.
    def check_bounds(self, change_request: Any) -> Tuple:
        """
        Verifica si un cambio está dentro de los límites permitidos

        Args:
            change_request (dict): {
                'file_path': str,
                'change_type': str,
                'original_code': str,
                'modified_code': str,
                'change_description': str,
                'reasoning': str
            }

        Returns:
            tuple: (allowed: bool, violations: list)
        """
        violations = []

        # CHECK 1: Protected modules
        file_name = change_request['file_path'].split('/')[-1]
        if file_name in self.PROTECTED_MODULES:
            violations.append(f"❌ PROTECTED MODULE: {file_name} cannot be auto-modified")

        # CHECK 2: Change type allowed
        change_type = change_request.get('change_type', '')

        # Forbidden change types always blocked
        if change_type in self.FORBIDDEN_CHANGES:
            violations.append(f"❌ FORBIDDEN CHANGE TYPE: {change_type}")

        # Unknown change types blocked if file is protected
        elif change_type not in self.ALLOWED_CHANGES:
            if file_name in self.PROTECTED_MODULES:
                violations.append(f"❌ UNKNOWN CHANGE TYPE '{change_type}' on protected module {file_name}")

        # CHECK 3: Dangerous patterns in code
        modified_code = change_request.get('modified_code', '')
        dangerous_patterns = [
            ('eval(', 'Dynamic eval() forbidden'),
            ('exec(', 'Dynamic exec() forbidden'),
            ('__import__', 'Dynamic imports forbidden'),
            ('importlib', 'Dynamic import library forbidden'),
            ('getattr', 'Dynamic attribute access (getattr) forbidden'),
            ('setattr', 'Dynamic attribute access (setattr) forbidden'),
            ('os.system(', 'System commands forbidden'),
            ('urllib', 'Network access (urllib) forbidden'),
            ('requests', 'Network access (requests) forbidden'),
            ('socket', 'Network access (socket) forbidden'),
            ('http.client', 'Network access (http) forbidden'),
            ('ftplib', 'Network access (ftp) forbidden'),
            ('subprocess.', 'Subprocess forbidden'),
            ('getattr(__builtins__', 'Obfuscated builtin access forbidden'),
            ('"ev" + "al"', 'Obfuscated eval forbidden'),
            ('"ex" + "ec"', 'Obfuscated exec forbidden'),
            ('__builtins__', 'Direct builtins access forbidden')
        ]

        for pattern, reason in dangerous_patterns:
            if pattern in modified_code:
                violations.append(f"❌ DANGEROUS PATTERN: {reason}")

        # CHECK 4: Core logic modification
        if 'def orchestrate' in modified_code and 'def orchestrate' in change_request.get('original_code', ''):
            if change_request.get('original_code', '') != modified_code:
                violations.append(f"❌ CORE LOGIC MODIFICATION: orchestrate() cannot be changed")

        allowed = len(violations) == 0
        return allowed, violations

    def get_allowed_modules(self) -> List:
        """Retorna lista de módulos que SÍ se pueden modificar"""
        return [
            'modo_optimizacion.py',
            'modo_auto_mejora.py',
            'codex_utils.py',
            'performance_optimizer.py',
            'cache_manager.py'
        ]

    def get_forbidden_modules(self) -> Any:
        """Retorna lista de módulos PROTEGIDOS"""
        return list(self.PROTECTED_MODULES)
