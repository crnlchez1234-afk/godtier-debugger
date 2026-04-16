"""
Módulo de Auto-Corrección Avanzada para Código Generado por IA
================================================================

Este módulo detecta y corrige automáticamente errores comunes en código
generado por modelos de IA, mejorando significativamente la calidad del output.

Características:
- Detección automática de errores comunes
- Corrección iterativa con herramientas del sistema
- Aprendizaje de patrones de error
- Integración con el pipeline de generación
- Logging detallado de correcciones aplicadas
"""

import re
import ast
import sys
import traceback
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import logging
from pathlib import Path

# Import NeuroSymbolic Core
try:
    # Add project root to path to allow imports if needed
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from src.ai.neurosymbolic_agi_core import SymbolicParser
    NEURO_SYMBOLIC_AVAILABLE = True
except Exception:
    NEURO_SYMBOLIC_AVAILABLE = False
    logging.warning("NeuroSymbolic Core not found. Running in classic mode.")

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CorrectionResult:
    """Resultado de una corrección aplicada"""
    original_code: str
    corrected_code: str
    errors_found: List[str]
    corrections_applied: List[str]
    success: bool
    confidence_score: float

class AutoDebugger:
    """
    Sistema avanzado de depuración automática para código generado por IA
    """

    def __init__(self, tool_manager=None):
        self.tool_manager = tool_manager
        
        # Initialize NeuroSymbolic Brain if available
        self.brain = SymbolicParser() if NEURO_SYMBOLIC_AVAILABLE else None
        
        self.correction_patterns = self._load_correction_patterns()
        self.error_history = []
        self.correction_stats = {
            'total_corrections': 0,
            'successful_corrections': 0,
            'error_patterns': {}
        }

    def _load_correction_patterns(self) -> Dict[str, Dict]:
        """Carga patrones de corrección para errores comunes"""
        return {
            'undefined_variable': {
                'pattern': r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b(?!\s*=)',
                'check_func': self._check_undefined_variables,
                'fix_func': self._fix_undefined_variables,
                'description': 'Variables no definidas'
            },
            'missing_imports': {
                'pattern': r'\b([A-Z][a-zA-Z0-9_]*)\(',
                'check_func': self._check_missing_imports,
                'fix_func': self._fix_missing_imports,
                'description': 'Imports faltantes para clases/funciones'
            },
            'syntax_error': {
                'pattern': r'.*',
                'check_func': self._check_syntax_errors,
                'fix_func': self._fix_syntax_errors,
                'description': 'Errores de sintaxis básicos'
            },
            'runtime_risk': {
                'pattern': r'.*',
                'check_func': self._check_runtime_risks,
                'fix_func': self._fix_runtime_risks,
                'description': 'Riesgos de errores en tiempo de ejecucion'
            },
            'logic_inconsistency': {
                'pattern': r'.*',
                'check_func': self._check_logic_inconsistencies,
                'fix_func': self._fix_logic_inconsistencies,
                'description': 'Inconsistencias lógicas en el código'
            },
            'code_quality': {
                'pattern': r'.*',
                'check_func': self._check_code_quality_issues,
                'fix_func': self._fix_code_quality_issues,
                'description': 'Problemas de calidad y mejores prácticas'
            },
            'type_mismatch': {
                'pattern': r'.*',
                'check_func': self._check_type_mismatches,
                'fix_func': self._fix_type_mismatches,
                'description': 'Tipos de datos incompatibles'
            },
            'neurosymbolic_logic': {
                'pattern': r'#\s*IF\s+.+\s+THEN\s+.+',
                'check_func': self._check_neurosymbolic_logic,
                'fix_func': self._fix_neurosymbolic_logic,
                'description': 'Validación de Lógica Neuro-Simbólica'
            }
        }

    def debug_code(self, code: str, context: Dict[str, Any] = None, language: str = 'python') -> CorrectionResult:
        """
        Aplica depuración automática al código generado

        Args:
            code: Código Python a depurar
            context: Contexto adicional (imports disponibles, etc.)

        Returns:
            CorrectionResult con el código corregido y detalles
        """
        logger.info("Iniciando depuración automática de código")

        original_code = code
        corrected_code = code
        errors_found = []
        corrections_applied = []
        confidence_score = 1.0

        # Aplicar correcciones iterativamente
        max_iterations = 3
        for iteration in range(max_iterations):
            logger.info(f"Iteración de corrección {iteration + 1}/{max_iterations}")

            iteration_errors = []
            iteration_corrections = []

            # Verificar cada patrón de error
            for pattern_name, pattern_config in self.correction_patterns.items():
                try:
                    has_error, error_details = pattern_config['check_func'](
                        corrected_code, context or {}
                    )

                    if has_error:
                        logger.info(f"Detectado error: {pattern_name} - {error_details}")
                        iteration_errors.append(f"{pattern_name}: {error_details}")

                        # Intentar corrección
                        fixed_code, correction_details = pattern_config['fix_func'](
                            corrected_code, error_details, context or {}
                        )

                        if fixed_code != corrected_code:
                            corrected_code = fixed_code
                            iteration_corrections.append(f"{pattern_name}: {correction_details}")
                            confidence_score *= 0.9  # Reducir confianza por corrección aplicada
                            logger.info(f"Corrección aplicada: {correction_details}")

                except Exception as e:
                    logger.warning(f"Error procesando patrón {pattern_name}: {e}")
                    continue

            errors_found.extend(iteration_errors)
            corrections_applied.extend(iteration_corrections)

            # Si no se encontraron errores en esta iteración, salir
            if not iteration_errors:
                break

        # Verificación final
        success = self._validate_code(corrected_code)

        # Actualizar estadísticas
        self._update_stats(errors_found, corrections_applied, success)

        result = CorrectionResult(
            original_code=original_code,
            corrected_code=corrected_code,
            errors_found=errors_found,
            corrections_applied=corrections_applied,
            success=success,
            confidence_score=confidence_score
        )

        logger.info(f"Depuración completada. Éxito: {success}, Correcciones: {len(corrections_applied)}")
        return result

    def fix_syntax_error(
        self,
        code: str,
        error: Exception,
        context: Optional[Dict[str, Any]] = None
    ) -> CorrectionResult:
        """
        Corrige un SyntaxError específico y devuelve un CorrectionResult compatible con main.py.

        Args:
            code: Código fuente original.
            error: Excepción de sintaxis capturada (p.ej., SyntaxError).
            context: Contexto opcional para ajustar la corrección (idioma, etc.).

        Returns:
            CorrectionResult con el código corregido y metadatos de la corrección.
        """
        logger.info("Aplicando fix_syntax_error sobre código detectado con SyntaxError")

        ctx: Dict[str, Any] = context or {}
        error_msg = str(error)

        corrected_code = code
        corrections_applied: List[str] = []
        errors_found = [f"SyntaxError: {error_msg}"]

        try:
            corrected_code, correction_details = self._fix_syntax_errors(code, error_msg, ctx)

            # Desglosar correcciones reportadas en lista legible
            for item in correction_details.split(';'):
                item = item.strip()
                if item:
                    corrections_applied.append(item)
        except Exception as fix_exc:
            logger.warning(f"Fallo al aplicar fix_syntax_error: {fix_exc}")
            corrections_applied.append(f"Fix failed: {fix_exc}")

        success = self._validate_code(corrected_code)

        # Ajustar confianza en función del número de correcciones realizadas
        confidence_score = 0.9 ** len(corrections_applied) if corrections_applied else 1.0

        self._update_stats(errors_found, corrections_applied, success)

        return CorrectionResult(
            original_code=code,
            corrected_code=corrected_code,
            errors_found=errors_found,
            corrections_applied=corrections_applied,
            success=success,
            confidence_score=confidence_score
        )

    def _check_indentation(self, code: str, context: Dict) -> Tuple[bool, str]:
        """Verifica errores de indentación"""
        lines = code.split('\n')
        indent_stack = []
        errors = []

        for i, line in enumerate(lines):
            stripped = line.lstrip()
            if not stripped or stripped.startswith('#'):
                continue

            indent_level = len(line) - len(stripped)

            # Lógica básica de indentación Python
            if stripped.startswith(('def ', 'class ', 'if ', 'for ', 'while ', 'try:', 'with ')):
                indent_stack.append(indent_level)
            elif stripped.startswith(('elif ', 'else:', 'except:', 'finally:')):
                if indent_stack and indent_level != indent_stack[-1]:
                    errors.append(f"Línea {i+1}: indentación inconsistente")
            elif indent_level > 0 and (not indent_stack or indent_level <= indent_stack[-1]):
                if not any(stripped.startswith(x) for x in ['elif ', 'else:', 'except:', 'finally:']):
                    errors.append(f"Línea {i+1}: indentación inesperada")

        return len(errors) > 0, "; ".join(errors) if errors else ""

    def _fix_indentation(self, code: str, error_details: str, context: Dict) -> Tuple[str, str]:
        """Corrige errores de indentación"""
        try:
            # Usar autopep8 o similar si está disponible
            if self.tool_manager and hasattr(self.tool_manager, 'format_code'):
                result = self.tool_manager.format_code(code)
                if result.get('success'):
                    return result['formatted_code'], "Indentación corregida automáticamente"
        except:
            pass

        # Corrección manual básica
        lines = code.split('\n')
        corrected_lines = []
        base_indent = 4

        for line in lines:
            stripped = line.lstrip()
            if not stripped or stripped.startswith('#'):
                corrected_lines.append(line)
                continue

            # Calcular indentación correcta
            if stripped.startswith(('def ', 'class ')):
                indent = 0
            elif stripped.startswith(('if ', 'for ', 'while ', 'try:', 'with ')):
                indent = (len(corrected_lines) > 0 and corrected_lines[-1].startswith(' ') and
                         len(corrected_lines[-1]) - len(corrected_lines[-1].lstrip()) or 0)
            else:
                # Mantener indentación relativa
                indent = max(0, len(line) - len(stripped) - base_indent)

            corrected_lines.append(' ' * indent + stripped)

        return '\n'.join(corrected_lines), "Indentación ajustada manualmente"

    def _check_undefined_variables(self, code: str, context: Dict) -> Tuple[bool, str]:
        """Verifica variables no definidas"""
        try:
            tree = ast.parse(code)
            analyzer = VariableAnalyzer()
            analyzer.visit(tree)

            undefined = analyzer.undefined_vars
            if undefined:
                return True, f"Variables no definidas: {', '.join(undefined)}"
        except:
            pass
        return False, ""

    def _fix_undefined_variables(self, code: str, error_details: str, context: Dict) -> Tuple[str, str]:
        """Intenta corregir variables no definidas"""
        # Extraer nombres de variables undefined
        undefined_vars = re.findall(r'Variables no definidas: (.+)', error_details)
        if not undefined_vars:
            return code, "No se pudieron identificar variables específicas"

        vars_list = [v.strip() for v in undefined_vars[0].split(',')]

        # Funciones y variables built-in que no deben inicializarse
        builtin_names = {
            'print', 'len', 'str', 'int', 'float', 'list', 'dict', 'set', 'tuple', 'range',
            'enumerate', 'zip', 'sum', 'max', 'min', 'abs', 'round', 'open', 'input', 'type',
            'isinstance', 'hasattr', 'getattr', 'setattr', 'Exception', 'ValueError', 'TypeError'
        }

        # Filtrar variables que no son built-in
        user_vars = [var for var in vars_list if var not in builtin_names]

        if not user_vars:
            return code, "Solo variables built-in no definidas"

        corrections = []
        lines = code.split('\n')

        for var in user_vars:
            # Buscar dónde se usa la variable
            for i, line in enumerate(lines):
                if var in line and '=' not in line.split(var)[0]:  # Variable usada antes de asignación
                    # Agregar inicialización antes
                    if 'int' in var.lower() or var.endswith('_id') or var.endswith('_count'):
                        init_line = f"{var} = 0"
                    elif 'list' in var.lower() or var.endswith('s') or var.startswith('items'):
                        init_line = f"{var} = []"
                    elif 'dict' in var.lower() or 'data' in var.lower() or var.endswith('_data'):
                        init_line = f"{var} = {{}}"
                    elif 'str' in var.lower() or var.endswith('_name') or var.endswith('_text'):
                        init_line = f"{var} = \"\""
                    else:
                        init_line = f"{var} = None"

                    lines.insert(i, init_line)
                    corrections.append(f"Variable {var} inicializada")
                    break

        return '\n'.join(lines), f"Variables inicializadas: {', '.join(corrections)}"

    def _check_missing_imports(self, code: str, context: Dict) -> Tuple[bool, str]:
        """Verifica imports faltantes"""
        # Clases comunes que requieren imports específicos
        common_classes = {
            'FastAPI': 'fastapi',
            'BaseModel': 'pydantic',
            'HTTPException': 'fastapi',
            'List': 'typing',
            'Dict': 'typing',
            'Optional': 'typing',
            'datetime': 'datetime',
            'json': 'json',
            'requests': 'requests'
        }

        used_classes = set()
        for line in code.split('\n'):
            for class_name in common_classes:
                if re.search(rf'\b{class_name}\b', line):
                    used_classes.add(class_name)

        missing_imports = []
        existing_imports = set()

        # Extraer imports existentes
        for line in code.split('\n'):
            if line.startswith('from ') or line.startswith('import '):
                for module, class_name in common_classes.items():
                    if class_name in line:
                        existing_imports.add(module)

        for class_name in used_classes:
            if class_name not in existing_imports:
                missing_imports.append(f"{class_name} (from {common_classes[class_name]})")

        return len(missing_imports) > 0, f"Imports faltantes: {', '.join(missing_imports)}"

    def _fix_missing_imports(self, code: str, error_details: str, context: Dict) -> Tuple[str, str]:
        """Agrega imports faltantes"""
        import_matches = re.findall(r'(\w+) \(from (\w+)\)', error_details)

        if not import_matches:
            return code, "No se pudieron identificar imports específicos"

        lines = code.split('\n')
        import_lines = []
        code_lines = []

        # Separar imports del código
        for line in lines:
            if line.startswith(('import ', 'from ')):
                import_lines.append(line)
            else:
                code_lines.append(line)

        # Agregar imports faltantes
        added_imports = []
        for class_name, module in import_matches:
            import_line = f"from {module} import {class_name}"
            if import_line not in import_lines:
                import_lines.append(import_line)
                added_imports.append(f"{class_name} from {module}")

        # Reensamblar código
        result = '\n'.join(import_lines + [''] + code_lines) if import_lines else '\n'.join(code_lines)

        return result, f"Imports agregados: {', '.join(added_imports)}"

    def _check_syntax_errors(self, code: str, context: Dict) -> Tuple[bool, str]:
        """Verifica errores de sintaxis básicos"""
        language = context.get('language', 'python')

        if language == 'python':
            try:
                compile(code, '<string>', 'exec')
                return False, ""
            except SyntaxError as e:
                return True, f"SyntaxError: {e.msg} en línea {e.lineno}"
            except Exception as e:
                return True, f"Error de compilación: {str(e)}"
        elif language in ['javascript', 'typescript']:
            # Validación básica de JavaScript
            return self._check_javascript_syntax(code)
        else:
            # Para otros lenguajes, usar validación básica
            return False, ""

    def _check_javascript_syntax(self, code: str) -> Tuple[bool, str]:
        """Verifica errores de sintaxis básicos en JavaScript"""
        try:
            lines = code.split('\n')
            errors = []

            # Verificar imports básicos
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped.startswith('import'):
                    if 'from' in stripped:
                        # Verificar espacio después de 'from'
                        parts = stripped.split('from')
                        if len(parts) > 1 and not parts[1].strip().startswith(' '):
                            errors.append(f"Línea {i+1}: Falta espacio después de 'from'")
                    # Verificar punto y coma
                    if not stripped.endswith(';'):
                        errors.append(f"Línea {i+1}: Import sin punto y coma")

            # Verificar números inválidos
            import re
            for i, line in enumerate(lines):
                # Números seguidos de paréntesis sin sentido
                invalid_numbers = re.findall(r'\b\d+\);', line)
                if invalid_numbers:
                    errors.append(f"Línea {i+1}: Número inválido seguido de paréntesis")

                # Imports malformados
                if 'import plotly.;' in line:
                    errors.append(f"Línea {i+1}: Import inválido")

            # Verificar balance de brackets
            brace_count = code.count('{') - code.count('}')
            paren_count = code.count('(') - code.count(')')
            bracket_count = code.count('[') - code.count(']')

            if brace_count != 0:
                errors.append(f"Desbalance de llaves: {brace_count}")
            if paren_count != 0:
                errors.append(f"Desbalance de paréntesis: {paren_count}")
            if bracket_count != 0:
                errors.append(f"Desbalance de corchetes: {bracket_count}")

            if errors:
                return True, "; ".join(errors[:3])

            return False, ""

        except Exception as e:
            return True, f"Error validando JavaScript: {str(e)}"

    def _fix_syntax_errors(self, code: str, error_details: str, context: Dict) -> Tuple[str, str]:
        """Intenta corregir errores de sintaxis básicos"""
        language = context.get('language', 'python')

        if language == 'python':
            return self._fix_python_syntax_errors(code, error_details, context)
        elif language in ['javascript', 'typescript']:
            return self._fix_javascript_syntax_errors(code, error_details, context)
        else:
            return code, "No se aplicaron correcciones (lenguaje no soportado)"

    def _fix_python_syntax_errors(self, code: str, error_details: str, context: Dict) -> Tuple[str, str]:
        """Intenta corregir errores de sintaxis básicos en Python"""
        corrections = []
        lines = code.split('\n')

        # Corrección de ":" faltante después de def, class, if, for, while, etc.
        for i, line in enumerate(lines):
            stripped = line.strip()
            # Patrones que requieren ":" al final
            if re.match(r'^(def|class|if|elif|else|for|while|try|except|finally|with|async def)\b', stripped):
                if not stripped.endswith(':'):
                    lines[i] = line.rstrip() + ':'
                    corrections.append(f"':' agregado después de '{stripped.split()[0]}' en línea {i+1}")

        code = '\n'.join(lines)

        # Corrección de bloques no indentados después de definiciones
        lines = code.split('\n')
        for i, line in enumerate(lines):
            stripped = line.strip()
            # Si la línea anterior termina con ":" y esta línea no está indentada ni vacía
            if i > 0 and lines[i-1].strip().endswith(':') and line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                # Verificar que no sea una línea de comentario o import
                if not stripped.startswith(('#', 'import', 'from', '@')):
                    lines[i] = '    ' + line  # Agregar indentación de 4 espacios
                    corrections.append(f"Indentación agregada en línea {i+1}")

        code = '\n'.join(lines)

        # Corrección de paréntesis no cerrados
        open_parens = code.count('(') - code.count(')')
        if open_parens > 0:
            code += ')' * open_parens
            corrections.append("Paréntesis faltantes agregados")

        # Corrección de corchetes no cerrados
        open_brackets = code.count('[') - code.count(']')
        if open_brackets > 0:
            code += ']' * open_brackets
            corrections.append("Corchetes faltantes agregados")

        # Corrección de llaves no cerradas
        open_braces = code.count('{') - code.count('}')
        if open_braces > 0:
            code += '}' * open_braces
            corrections.append("Llaves faltantes agregadas")

        # Corrección de strings no cerrados (incluyendo docstrings triples)
        lines = code.split('\n')
        in_triple_quote = False
        triple_quote_type = None

        for i, line in enumerate(lines):
            # Detectar inicio de docstring triple
            if '"""' in line and not in_triple_quote:
                in_triple_quote = True
                triple_quote_type = '"""'
            elif "'''" in line and not in_triple_quote:
                in_triple_quote = True
                triple_quote_type = "'''"

            # Si estamos en un docstring triple, buscar el cierre
            if in_triple_quote:
                if triple_quote_type in line:
                    in_triple_quote = False
                    triple_quote_type = None

        # Si terminamos con un docstring triple abierto, cerrarlo
        if in_triple_quote and triple_quote_type:
            lines.append(triple_quote_type)
            corrections.append(f"Docstring triple no terminado cerrado con {triple_quote_type}")

        # Corrección adicional de comillas simples y dobles en líneas individuales
        for i, line in enumerate(lines):
            if in_triple_quote and triple_quote_type in line:
                continue  # Saltar líneas que ya manejamos arriba

            # Contar comillas simples y dobles (ignorando escapes)
            single_quotes = line.count("'") - line.count("\\'")
            double_quotes = line.count('"') - line.count('\\"')

            if single_quotes % 2 == 1:
                lines[i] += "'"
                corrections.append(f"Comilla simple faltante en línea {i+1}")
            if double_quotes % 2 == 1:
                lines[i] += '"'
                corrections.append(f"Comilla doble faltante en línea {i+1}")

        code = '\n'.join(lines)

        return code, "; ".join(corrections) if corrections else "Errores de sintaxis corregidos"

    def _fix_javascript_syntax_errors(self, code: str, error_details: str, context: Dict) -> Tuple[str, str]:
        """Intenta corregir errores de sintaxis básicos en JavaScript"""
        corrections = []
        lines = code.split('\n')

        # Corregir imports sin espacios después de 'from'
        for i, line in enumerate(lines):
            if 'from' in line and not line.split('from')[1].strip().startswith(' '):
                lines[i] = line.replace('from', 'from ', 1)
                corrections.append(f"Espacio agregado después de 'from' en línea {i+1}")

        # Añadir punto y coma faltante en imports
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('import') and not stripped.endswith(';'):
                lines[i] = line.rstrip() + ';'
                corrections.append(f"Punto y coma agregado en import de línea {i+1}")

        # Remover imports inválidos
        filtered_lines = []
        for i, line in enumerate(lines):
            if 'import plotly.;' in line:
                corrections.append(f"Import inválido removido de línea {i+1}")
                continue
            filtered_lines.append(line)

        lines = filtered_lines

        # Corregir números inválidos seguidos de paréntesis
        for i, line in enumerate(lines):
            original_line = line
            line = re.sub(r'\b(\d+)\);', r'\1;', line)
            if line != original_line:
                corrections.append(f"Número inválido corregido en línea {i+1}")

        # Corregir balance de brackets
        brace_count = code.count('{') - code.count('}')
        paren_count = code.count('(') - code.count(')')
        bracket_count = code.count('[') - code.count(']')

        if brace_count > 0:
            lines.append('}' * brace_count)
            corrections.append(f"Llaves de cierre agregadas ({brace_count})")
        if paren_count > 0:
            lines.append(')' * paren_count)
            corrections.append(f"Paréntesis de cierre agregados ({paren_count})")
        if bracket_count > 0:
            lines.append(']' * bracket_count)
            corrections.append(f"Corchetes de cierre agregados ({bracket_count})")

        code = '\n'.join(lines)

        return code, "; ".join(corrections) if corrections else "Errores de sintaxis JavaScript corregidos"

    def _check_logic_inconsistencies(self, code: str, context: Dict) -> Tuple[bool, str]:
        """Verifica inconsistencias lógicas"""
        errors = []

        try:
            # Usar AST para análisis más preciso
            tree = ast.parse(code)

            # Extraer variables definidas y usadas
            defined_vars = set()
            used_vars = set()

            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    if isinstance(node.ctx, ast.Store):
                        defined_vars.add(node.id)
                    elif isinstance(node.ctx, ast.Load):
                        used_vars.add(node.id)

            # Variables built-in comunes
            builtin_vars = {
                'True', 'False', 'None', 'print', 'len', 'str', 'int', 'float', 'list', 'dict', 'set', 'tuple',
                'range', 'enumerate', 'zip', 'sum', 'max', 'min', 'abs', 'round', 'open', 'close', 'read', 'write',
                'Exception', 'ValueError', 'TypeError', 'KeyError', 'IndexError', 'AttributeError',
                'ImportError', 'OSError', 'IOError', 'EOFError', 'KeyboardInterrupt', 'SystemExit'
            }

            # Verificar variables usadas pero no definidas
            undefined_vars = used_vars - defined_vars - builtin_vars

            if undefined_vars:
                # Filtrar variables que podrían estar en contexto de error (imports faltantes, etc.)
                filtered_undefined = []
                for var in undefined_vars:
                    # Ignorar variables que parecen ser nombres de módulos o clases comunes
                    if not (var[0].isupper() or '.' in var or var in context.get('known_modules', set())):
                        filtered_undefined.append(var)

                if filtered_undefined:
                    errors.extend([f"Variable '{var}' usada pero nunca asignada" for var in filtered_undefined[:10]])  # Limitar a 10

        except SyntaxError:
            # Si hay errores de sintaxis, no podemos analizar con AST
            pass

        return len(errors) > 0, "; ".join(errors)

    def _fix_logic_inconsistencies(self, code: str, error_details: str, context: Dict) -> Tuple[str, str]:
        """Corrige inconsistencias lógicas"""
        # Esta es una corrección compleja, por ahora solo reportamos
        return code, "Inconsistencias lógicas detectadas - requiere revisión manual"

    def _check_code_quality_issues(self, code: str, context: Dict) -> Tuple[bool, str]:
        """Verifica problemas de calidad y mejores prácticas en el código"""
        issues = []

        try:
            tree = ast.parse(code)
            lines = code.split('\n')

            # 1. Detectar variables globales mutables
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    # Verificar si es asignación a nivel global
                    if isinstance(node.targets[0], ast.Name):
                        var_name = node.targets[0].id
                        if isinstance(node.value, ast.List) and not node.value.elts:
                            # Lista vacía global
                            issues.append(f"Variable global mutable '{var_name} = []' - usar lista local o None")
                        elif isinstance(node.value, ast.Dict) and not node.value.keys:
                            # Diccionario vacío global
                            issues.append(f"Variable global mutable '{var_name} = {{}}' - usar dict local o None")

            # 2. Detectar métodos innecesarios en clases Pydantic
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Verificar si hereda de BaseModel
                    inherits_basemodel = any(
                        (isinstance(base, ast.Name) and base.id == 'BaseModel') or
                        (isinstance(base, ast.Attribute) and base.attr == 'BaseModel')
                        for base in node.bases
                    )

                    if inherits_basemodel:
                        for item in node.body:
                            if isinstance(item, ast.FunctionDef) and item.name == 'to_dict':
                                issues.append(f"Método 'to_dict' innecesario en clase Pydantic '{node.name}' - usar .dict()")

            # 3. Detectar imports no utilizados
            imports = set()
            used_names = set()

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.asname if alias.asname else alias.name)
                elif isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        imports.add(alias.asname if alias.asname else alias.name)
                elif isinstance(node, ast.Name):
                    if isinstance(node.ctx, ast.Load):
                        used_names.add(node.id)

            unused_imports = imports - used_names - {'__name__', '__main__'}
            for unused in unused_imports:
                if '.' not in unused:  # Solo reportar imports simples
                    issues.append(f"Import '{unused}' no utilizado")

            # 4. Detectar funciones sin return explícito
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    has_return = any(isinstance(child, ast.Return) for child in ast.walk(node))
                    if not has_return and node.name != '__init__':
                        issues.append(f"Función '{node.name}' no tiene return explícito")

        except SyntaxError:
            pass  # Si hay errores de sintaxis, no podemos analizar

        return len(issues) > 0, "; ".join(issues[:5])  # Limitar a 5 issues

    def _fix_code_quality_issues(self, code: str, error_details: str, context: Dict) -> Tuple[str, str]:
        """Corrige problemas de calidad de código"""
        corrections = []
        lines = code.split('\n')

        # 1. Corregir variables globales mutables
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped in ['tasks = []', 'data = []', 'items = []']:
                lines[i] = line.replace('[]', 'None')
                corrections.append(f"Variable global mutable cambiada a None: {stripped}")

        # 2. Remover métodos to_dict innecesarios en clases Pydantic
        try:
            tree = ast.parse('\n'.join(lines))
            new_lines = []
            skip_lines = 0

            for i, line in enumerate(lines):
                if skip_lines > 0:
                    skip_lines -= 1
                    continue

                # Detectar método to_dict en clases Pydantic
                if 'def to_dict(self):' in line:
                    # Verificar si estamos en una clase Pydantic
                    class_start = i
                    while class_start > 0 and not lines[class_start].strip().startswith('class '):
                        class_start -= 1

                    if class_start >= 0 and 'BaseModel' in lines[class_start]:
                        # Encontrar el final del método
                        method_end = i + 1
                        indent_level = len(line) - len(line.lstrip())
                        while method_end < len(lines):
                            if lines[method_end].strip() == '' or len(lines[method_end]) - len(lines[method_end].lstrip()) <= indent_level:
                                break
                            method_end += 1

                        # Saltar estas líneas
                        skip_lines = method_end - i
                        corrections.append("Método to_dict() innecesario removido de clase Pydantic")
                        continue

                new_lines.append(line)

            lines = new_lines

        except SyntaxError:
            pass

        return '\n'.join(lines), "; ".join(corrections) if corrections else "Problemas de calidad corregidos"

    def _check_type_mismatches(self, code: str, context: Dict) -> Tuple[bool, str]:
        """Verifica mismatches de tipos básicos"""
        issues = []
        
        try:
            tree = ast.parse(code)
            
            # Detectar operaciones con tipos incompatibles
            for node in ast.walk(tree):
                if isinstance(node, ast.BinOp):
                    # Detectar string + number
                    if isinstance(node.op, ast.Add):
                        # Simplificado: buscar pattern común 'x' + 5
                        left_str = isinstance(node.left, ast.Constant) and isinstance(node.left.value, str)
                        right_num = isinstance(node.right, ast.Constant) and isinstance(node.right.value, (int, float))
                        
                        if left_str and right_num:
                            issues.append("String + Number operation detected")
                        elif right_num and left_str:
                            issues.append("Number + String operation detected")
        except:
            pass
        
        return len(issues) > 0, "; ".join(issues)

    def _fix_type_mismatches(self, code: str, error_details: str, context: Dict) -> Tuple[str, str]:
        """Corrige mismatches de tipos - agregar str() conversion"""
        corrections = []
        
        if "String + Number" in error_details or "Number + String" in error_details:
            # Simple fix: add comment suggesting str() conversion
            code = f"# Warning: Type mismatch detected - consider using str() conversion\n{code}"
            corrections.append("Type mismatch warning added")
        
        return code, "; ".join(corrections) if corrections else "Type mismatches require manual fix"
    
    def _check_runtime_risks(self, code: str, context: Dict) -> Tuple[bool, str]:
        """Detecta riesgos potenciales de runtime errors"""
        risks = []
        
        try:
            tree = ast.parse(code)
            
            # 1. Division por zero potencial
            for node in ast.walk(tree):
                if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)):
                    # Detectar divisor literal 0 o variable 'b', 'y' sin validación
                    if isinstance(node.right, ast.Constant) and node.right.value == 0:
                        risks.append("Division by zero (literal 0)")
                    elif isinstance(node.right, ast.Name):
                        divisor = node.right.id
                        # Buscar si hay validación previa
                        has_check = False
                        for check_node in ast.walk(tree):
                            if isinstance(check_node, ast.Compare):
                                # Buscar if divisor != 0 o similar
                                if isinstance(check_node.left, ast.Name) and check_node.left.id == divisor:
                                    has_check = True
                                    break
                        
                        if not has_check:
                            risks.append(f"Potential division by zero (variable '{divisor}' not validated)")
            
            # 2. Index out of range potencial
            for node in ast.walk(tree):
                if isinstance(node, ast.Subscript):
                    if isinstance(node.slice, ast.Constant):
                        index = node.slice.value
                        if isinstance(index, int) and index > 5:  # Index alto sin validación
                            risks.append(f"Potential index error (index {index} without bounds check)")
            
            # 3. Operaciones sobre None sin validación
            for node in ast.walk(tree):
                if isinstance(node, ast.Attribute):
                    if isinstance(node.value, ast.Name):
                        var_name = node.value.id
                        # Verificar si variable podría ser None
                        if var_name in ['result', 'data', 'obj', 'item']:
                            risks.append(f"Potential AttributeError ('{var_name}' might be None)")
        
        except:
            pass
        
        return len(risks) > 0, "; ".join(risks)
    
    def _fix_runtime_risks(self, code: str, error_details: str, context: Dict) -> Tuple[str, str]:
        """Agrega validaciones para prevenir runtime errors"""
        corrections = []
        
        # Para division by zero, agregar comentario de validación
        if "division by zero" in error_details.lower():
            code = f"# Warning: Validate divisor is not zero before division\n{code}"
            corrections.append("Division by zero warning added")
        
        # Para index errors, agregar comentario de validación
        elif "index error" in error_details.lower():
            code = f"# Warning: Check array bounds before accessing elements\n{code}"
            corrections.append("Index bounds check warning added")
        
        # Para AttributeError, agregar None check
        elif "AttributeError" in error_details:
            code = f"# Warning: Validate object is not None before accessing attributes\n{code}"
            corrections.append("None check warning added")
        
        return code, "; ".join(corrections) if corrections else "Runtime risk warnings added"

    def _validate_code(self, code: str) -> bool:
        """Valida que el código se compile correctamente"""
        try:
            compile(code, '<string>', 'exec')
            return True
        except:
            return False

    def _check_neurosymbolic_logic(self, code: str, context: Dict) -> Tuple[bool, str]:
        """
        Verifica la lógica del código usando el parser simbólico.
        Busca comentarios tipo '# IF ... THEN ...' y valida si tienen sentido.
        """
        if not self.brain:
            return False, "NeuroSymbolic Brain not available"

        issues = []
        lines = code.split('\n')
        for i, line in enumerate(lines):
            # Buscar patrones de reglas en comentarios
            match = re.search(r'#\s*(IF\s+.+\s+THEN\s+.+)', line)
            if match:
                rule_text = match.group(1)
                try:
                    parsed = self.brain.parse_logical_expression(rule_text)
                    
                    # Si el parser no lo reconoce como regla, es un problema
                    if parsed.get('type') != 'rule':
                        issues.append(f"Línea {i+1}: Regla lógica ambigua o mal formada: '{rule_text}'")
                    else:
                        # Validación extra: Verificar que los antecedentes no empiecen con operadores
                        # Esto detecta casos como "IF x AND OR y" donde "OR y" se parsea como átomo
                        for cond in parsed.get('antecedent', []):
                            # Obtener el valor crudo o procesado
                            val = cond.get('value') or cond.get('raw') or str(cond)
                            if isinstance(val, str) and val.strip().upper().startswith(('AND ', 'OR ', 'THEN ')):
                                issues.append(f"Línea {i+1}: Condición inválida en regla (operador suelto): '{val}'")
                except Exception as e:
                    issues.append(f"Línea {i+1}: Error de análisis simbólico: {str(e)}")

        if issues:
            return True, "\n".join(issues)
        return False, ""

    def _fix_neurosymbolic_logic(self, code: str, error_msg: str, context: Dict = None) -> Tuple[str, str]:
        """
        Intenta corregir problemas lógicos detectados por el cerebro simbólico.
        """
        lines = code.split('\n')
        new_lines = []
        corrections = []
        
        # Extraer líneas con problemas del mensaje de error
        problematic_lines = []
        for error in error_msg.split('\n'):
            match = re.search(r'Línea (\d+):', error)
            if match:
                problematic_lines.append(int(match.group(1)))

        for i, line in enumerate(lines):
            new_lines.append(line)
            # Si esta línea tuvo un problema, agregamos una advertencia del sistema
            if (i + 1) in problematic_lines:
                indent = re.match(r'^\s*', line).group(0) if re.match(r'^\s*', line) else ""
                warning_msg = f"{indent}# 🧠 NEUROSYS: La regla lógica anterior es ambigua. Revisar sintaxis."
                new_lines.append(warning_msg)
                corrections.append(f"Agregada advertencia en línea {i+1}")

        return "\n".join(new_lines), ", ".join(corrections)

    def _update_stats(self, errors: List[str], corrections: List[str], success: bool):
        """Actualiza estadísticas de corrección"""
        self.correction_stats['total_corrections'] += len(corrections)
        if success:
            self.correction_stats['successful_corrections'] += 1

        for error in errors:
            error_type = error.split(':')[0] if ':' in error else 'unknown'
            self.correction_stats['error_patterns'][error_type] = \
                self.correction_stats['error_patterns'].get(error_type, 0) + 1

    def get_stats(self) -> Dict:
        """Retorna estadísticas de corrección"""
        return self.correction_stats.copy()
    
    def detect_and_fix_errors(self, code: str) -> list:
        """
        Metodo para compatibilidad con benchmark_supremo.py
        
        El benchmark llama: akira.debugger.detect_and_fix_errors(code)
        Este metodo retorna lista de correcciones aplicadas
        
        Args:
            code: Codigo a analizar
            
        Returns:
            Lista de strings describiendo las correcciones
        """
        result = self.debug_code(code)
        return result.corrections_applied

class VariableAnalyzer(ast.NodeVisitor):
    """Analizador de variables para AST"""

    def __init__(self):
        self.defined_vars = set()
        self.undefined_vars = set()
        self.current_scope = []

    def visit_FunctionDef(self, node):
        self.current_scope.append(node.name)
        self.generic_visit(node)
        self.current_scope.pop()

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.defined_vars.add(target.id)
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load) and node.id not in self.defined_vars:
            # Verificar si es una variable built-in o importada
            if node.id not in dir(__builtins__) and not any(node.id in scope for scope in self.current_scope):
                self.undefined_vars.add(node.id)
        self.generic_visit(node)

# Función de integración con el sistema principal
def integrate_auto_debugger(tool_manager=None):
    """
    Integra el AutoDebugger con el sistema de herramientas existente
    """
    debugger = AutoDebugger(tool_manager)

    # Agregar como herramienta del sistema
    if tool_manager:
        tool_manager.tools['auto_debug_code'] = debugger.debug_code
        tool_manager.tool_descriptions['auto_debug_code'] = {
            'description': 'Depura automáticamente errores comunes en código Python generado por IA',
            'parameters': {
                'code': 'str - Código Python a depurar',
                'context': 'dict opcional - Contexto adicional para la depuración'
            }
        }

    return debugger

if __name__ == "__main__":
    # Demo del AutoDebugger
    debugger = AutoDebugger()

    # Código de ejemplo con errores
    test_code = '''
def hello_world()
    print("Hola Mundo"
    undefined_var + 1
    return result
'''

    print("Código original con errores:")
    print(test_code)
    print("\n" + "="*50)

    result = debugger.debug_code(test_code)

    print("Resultado de la depuración:")
    print(f"Éxito: {result.success}")
    print(f"Errores encontrados: {len(result.errors_found)}")
    print(f"Correcciones aplicadas: {len(result.corrections_applied)}")
    print(f"Puntuación de confianza: {result.confidence_score:.2f}")
    print("\nCódigo corregido:")
    print(result.corrected_code)

    print("\nEstadísticas:")
    print(debugger.get_stats())