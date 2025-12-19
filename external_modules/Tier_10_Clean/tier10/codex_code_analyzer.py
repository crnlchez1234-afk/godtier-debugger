# ═══════════════════════════════════════════════════════════════════════
# Copyright © 2025 Cruz Sanchez. All Rights Reserved.
#
# PROPRIETARY AND CONFIDENTIAL
# Unauthorized copying, distribution, modification, or use of this software,
# via any medium, is strictly prohibited without explicit written permission.
#
# Licensed under Proprietary License - See LICENSE.txt for full terms.
# Commercial use requires separate licensing agreement.
#
# codex AGI System - Advanced Artificial General Intelligence
# ═══════════════════════════════════════════════════════════════════════
#!/usr/bin/env python3
"""
🔍 codex CODE ANALYZER - TIER 9
Analiza y comprende el código fuente de codex para auto-mejora

Capabilities:
- Abstract Syntax Tree (AST) parsing
- Code complexity analysis
- Performance bottleneck detection
- Dependency mapping
- Function call graph generation
"""

import ast
import inspect
import importlib
from pathlib import Path
import json
from typing import Dict, List, Any, Tuple, Optional

class CodexCodeAnalyzer:
    """Analiza código Python para identificar oportunidades de mejora"""

    def __init__(self, target_dir: str) -> None:
        self.target_dir = Path(target_dir)
        self.analyzed_files = {}
        self.complexity_scores = {}
        self.bottlenecks = []
        self.improvement_opportunities = []

    def analyze_file(self, filepath: str) -> Dict[str, Any]:
        """Analiza un archivo Python completo"""
        filepath = Path(filepath)

        if not filepath.exists():
            return {'error': f'File not found: {filepath}'}

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source_code = f.read()

            # Parse AST
            tree = ast.parse(source_code)

            # Análisis estructural
            analysis = {
                'filepath': str(filepath),
                'lines_of_code': len(source_code.split('\n')),
                'functions': self._extract_functions(tree),
                'classes': self._extract_classes(tree),
                'imports': self._extract_imports(tree),
                'complexity': self._calculate_complexity(tree),
                'bottlenecks': self._detect_bottlenecks(tree, source_code),
                'security_issues': self._detect_security_issues(tree, source_code),
                'optimization_hints': []
            }

            # Generar sugerencias de optimización
            analysis['optimization_hints'] = self._generate_optimization_hints(analysis)

            self.analyzed_files[str(filepath)] = analysis
            return analysis

        except Exception as e:
            return {'error': str(e), 'filepath': str(filepath)}

    def _extract_functions(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extrae información de todas las funciones"""
        functions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    'name': node.name,
                    'args': [arg.arg for arg in node.args.args],
                    'line_number': node.lineno,
                    'decorators': [d.id if isinstance(d, ast.Name) else str(d) for d in node.decorator_list],
                    'complexity': self._function_complexity(node),
                    'has_docstring': ast.get_docstring(node) is not None
                }
                functions.append(func_info)

        return functions

    def _extract_classes(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extrae información de todas las clases"""
        classes = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = [m.name for m in node.body if isinstance(m, ast.FunctionDef)]

                class_info = {
                    'name': node.name,
                    'line_number': node.lineno,
                    'methods': methods,
                    'method_count': len(methods),
                    'bases': [b.id if isinstance(b, ast.Name) else str(b) for b in node.bases],
                    'has_docstring': ast.get_docstring(node) is not None
                }
                classes.append(class_info)

        return classes

    def _extract_imports(self, tree: ast.AST) -> List[str]:
        """Extrae todos los imports"""
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}" if module else alias.name)

        return list(set(imports))

    def _calculate_complexity(self, tree: ast.AST) -> int:
        """Calcula complejidad ciclomática aproximada"""
        complexity = 1  # Base complexity

        for node in ast.walk(tree):
            # Cada punto de decisión aumenta complejidad
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1

        return complexity

    def _function_complexity(self, func_node: ast.FunctionDef) -> int:
        """Complejidad de una función específica"""
        complexity = 1

        for node in ast.walk(func_node):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1

        return complexity

    def _detect_bottlenecks(self, tree: ast.AST, source_code: str) -> List[Dict[str, Any]]:
        """Detecta posibles cuellos de botella"""
        bottlenecks = []

        # Detectar loops anidados
        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                nested_loops = [n for n in ast.walk(node) if isinstance(n, ast.For) and n != node]
                if nested_loops:
                    bottlenecks.append({
                        'type': 'nested_loops',
                        'line': node.lineno,
                        'severity': 'medium',
                        'description': f'Nested loop detected (depth: {len(nested_loops) + 1})'
                    })

        # Detectar operaciones costosas en loops
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                for inner in ast.walk(node):
                    if isinstance(inner, ast.Call):
                        if isinstance(inner.func, ast.Attribute):
                            # Operaciones como .append() en loops son OK, pero DB queries no
                            if any(keyword in str(inner.func.attr).lower() for keyword in ['query', 'execute', 'fetch']):
                                bottlenecks.append({
                                    'type': 'expensive_operation_in_loop',
                                    'line': inner.lineno,
                                    'severity': 'high',
                                    'description': 'Database operation inside loop - consider batch operations'
                                })

        return bottlenecks

    def _detect_security_issues(self, tree: ast.AST, source_code: str) -> List[Dict[str, Any]]:
        """Detecta problemas de seguridad (Hard Governance)"""
        issues = []
        
        # 1. Critical System Calls (RCE Risk)
        dangerous_calls = ['os.system', 'subprocess.call', 'subprocess.Popen', 'eval', 'exec', 'shutil.rmtree']
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    # Check for module.function calls (e.g. os.system)
                    # This is a simple heuristic, a full type inference is harder
                    name = f"{getattr(node.func.value, 'id', '')}.{node.func.attr}"
                    if any(dc in name for dc in dangerous_calls):
                         issues.append({
                            'type': 'critical_rce_risk',
                            'line': node.lineno,
                            'severity': 'critical',
                            'description': f'Dangerous system call detected: {name}'
                        })
                elif isinstance(node.func, ast.Name):
                    # Check for direct calls (e.g. eval, exec)
                    if node.func.id in dangerous_calls:
                        issues.append({
                            'type': 'critical_rce_risk',
                            'line': node.lineno,
                            'severity': 'critical',
                            'description': f'Dangerous function call detected: {node.func.id}'
                        })

        # 2. SQL Injection Patterns
        if "f\"SELECT" in source_code or "f'SELECT" in source_code:
             issues.append({
                'type': 'sql_injection',
                'line': 0, # Global check
                'severity': 'high',
                'description': 'Potential SQL Injection: f-string used in SELECT statement'
            })
        
        if ".format(" in source_code and "SELECT" in source_code:
             issues.append({
                'type': 'sql_injection',
                'line': 0,
                'severity': 'high',
                'description': 'Potential SQL Injection: .format() used with SELECT'
            })

        return issues

    def _generate_optimization_hints(self, analysis: Dict[str, Any]) -> List[str]:
        """Genera sugerencias de optimización basadas en análisis"""
        hints = []

        # Complejidad alta
        if analysis['complexity'] > 50:
            hints.append(f"High complexity ({analysis['complexity']}) - consider refactoring into smaller modules")

        # Funciones muy complejas
        complex_functions = [f for f in analysis['functions'] if f['complexity'] > 10]
        if complex_functions:
            hints.append(f"Found {len(complex_functions)} complex functions - consider simplification")

        # Muchas clases sin documentación
        undocumented_classes = [c for c in analysis['classes'] if not c['has_docstring']]
        if len(undocumented_classes) > 3:
            hints.append(f"{len(undocumented_classes)} classes lack docstrings - add documentation")

        # Bottlenecks críticos
        critical_bottlenecks = [b for b in analysis['bottlenecks'] if b['severity'] == 'high']
        if critical_bottlenecks:
            hints.append(f"Found {len(critical_bottlenecks)} critical performance bottlenecks")

        # Archivo muy grande
        if analysis['lines_of_code'] > 1000:
            hints.append(f"Large file ({analysis['lines_of_code']} lines) - consider splitting into modules")

        return hints

    def analyze_module_performance(self, module_name: str) -> Dict[str, Any]:
        """Analiza performance de un módulo en runtime"""
        try:
            # Importar módulo dinámicamente
            module = importlib.import_module(module_name)

            performance_data = {
                'module': module_name,
                'functions': {},
                'total_time': 0
            }

            # Analizar funciones del módulo
            for name, obj in inspect.getmembers(module):
                if inspect.isfunction(obj) and obj.__module__ == module_name:
                    # Medir tiempo de ejecución (simulado - en producción usar profiler)
                    performance_data['functions'][name] = {
                        'callable': True,
                        'args': len(inspect.signature(obj).parameters),
                        'source_available': inspect.getsource(obj) is not None
                    }

            return performance_data

        except Exception as e:
            return {'error': str(e), 'module': module_name}

    def get_improvement_priorities(self) -> List[Dict[str, Any]]:
        """Identifica prioridades de mejora basado en todos los análisis"""
        priorities = []

        for filepath, analysis in self.analyzed_files.items():
            if 'error' in analysis:
                continue

            # Calcular score de prioridad
            priority_score = 0
            reasons = []

            # Complejidad alta = alta prioridad
            if analysis['complexity'] > 50:
                priority_score += 30
                reasons.append(f"High complexity: {analysis['complexity']}")

            # Bottlenecks críticos
            critical_bottlenecks = [b for b in analysis['bottlenecks'] if b['severity'] == 'high']
            priority_score += len(critical_bottlenecks) * 20
            if critical_bottlenecks:
                reasons.append(f"{len(critical_bottlenecks)} critical bottlenecks")

            # Archivo grande
            if analysis['lines_of_code'] > 1000:
                priority_score += 10
                reasons.append(f"Large file: {analysis['lines_of_code']} LOC")

            if priority_score > 0:
                priorities.append({
                    'filepath': filepath,
                    'priority_score': priority_score,
                    'reasons': reasons,
                    'optimization_hints': analysis['optimization_hints']
                })

        # Ordenar por prioridad
        priorities.sort(key=lambda x: x['priority_score'], reverse=True)

        return priorities

    def generate_analysis_report(self) -> str:
        """Genera reporte completo de análisis"""
        report_lines = [
            "=" * 80,
            "🔍 codex CODE ANALYZER - ANALYSIS REPORT",
            "=" * 80,
            f"\nTotal files analyzed: {len(self.analyzed_files)}",
            ""
        ]

        # Estadísticas generales
        total_loc = sum(a.get('lines_of_code', 0) for a in self.analyzed_files.values() if 'error' not in a)
        total_functions = sum(len(a.get('functions', [])) for a in self.analyzed_files.values() if 'error' not in a)
        total_classes = sum(len(a.get('classes', [])) for a in self.analyzed_files.values() if 'error' not in a)

        report_lines.extend([
            f"Total lines of code: {total_loc:,}",
            f"Total functions: {total_functions}",
            f"Total classes: {total_classes}",
            ""
        ])

        # Prioridades de mejora
        priorities = self.get_improvement_priorities()

        if priorities:
            report_lines.extend([
                "=" * 80,
                "📊 IMPROVEMENT PRIORITIES (Top 5)",
                "=" * 80,
                ""
            ])

            for i, priority in enumerate(priorities[:5], 1):
                report_lines.extend([
                    f"{i}. {priority['filepath']} (Priority Score: {priority['priority_score']})",
                    f"   Reasons: {', '.join(priority['reasons'])}",
                    ""
                ])

        report_lines.append("=" * 80)

        return "\n".join(report_lines)


if __name__ == "__main__":
    print("\n🔍 codex CODE ANALYZER - TIER 9")
    print("=" * 60)

    analyzer = CodeAnalyzer()

    # Analizar archivos core de codex
    core_files = [
        'codex_meta_reflection.py',
        'codex_consciousness_monitor.py',
        'prometheus_scientific_discovery.py',
        'quantum_scale_memory.py',
        'tree_of_thoughts.py',
        'swarm_intelligence.py'
    ]

    print("\n📁 Analyzing core codex files...")
    for filepath in core_files:
        if Path(filepath).exists():
            print(f"   Analyzing {filepath}...")
            analysis = analyzer.analyze_file(filepath)

            if 'error' not in analysis:
                print(f"   ✅ {filepath}: {analysis['lines_of_code']} LOC, "
                      f"{len(analysis['functions'])} functions, "
                      f"complexity {analysis['complexity']}")
            else:
                print(f"   ⚠️ {filepath}: {analysis['error']}")

    # Generar reporte
    print("\n" + analyzer.generate_analysis_report())

    # Guardar resultados
    results_file = "codex_code_analysis.json"
    with open(results_file, 'w') as f:
        json.dump(analyzer.analyzed_files, f, indent=2)

    print(f"\n💾 Analysis results saved to: {results_file}")

