"""
🔥 PROJECT LAZARUS: RUNTIME RESURRECTION PROTOCOL 🔥
=====================================================
Sistema de auto-sanación en tiempo de ejecución.
Permite que el código se reescriba a sí mismo cuando falla y continúe ejecutándose.
"""

import sys
import traceback
import inspect
import textwrap
from functools import wraps
from typing import Any, Callable, Dict, Optional
from pathlib import Path

# Importar el cerebro (NeuroSys)
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.ai.neurosys_debugger_wrapper import NeurosysDebuggerAI

class LazarusEngine:
    def __init__(self):
        self.ai = NeurosysDebuggerAI()
        self.resurrection_count = 0
        self.max_resurrections = 3

    def heal_and_retry(self, func: Callable, args, kwargs, exception: Exception) -> Any:
        """
        Intenta curar la función dañada y re-ejecutarla.
        """
        self.resurrection_count += 1
        if self.resurrection_count > self.max_resurrections:
            raise exception  # Ya intentamos demasiado, dejar morir.

        print(f"\n💀 LAZARUS PROTOCOL ACTIVATED 💀")
        print(f"   Error detectado: {type(exception).__name__}: {exception}")
        print(f"   Intentando resurrección ({self.resurrection_count}/{self.max_resurrections})...")

        # 1. Obtener código fuente y contexto
        try:
            source_code = inspect.getsource(func)
            source_code = textwrap.dedent(source_code)
        except OSError:
            print("   ❌ No se pudo acceder al código fuente. Abortando.")
            raise exception

        # 2. Consultar al Especialista Tier 10
        # Prompt estilo "Completion" para Phi-2 (más efectivo para código)
        prompt = f"""{source_code}

# Fixed version of the function above that handles {type(exception).__name__} ("{exception}"):
# IMPORTANT: Return ONLY the function definition. Do NOT raise the error again. Handle it gracefully (return None or 0).
def"""
        
        print("   🧠 Consultando al Especialista Tier 10 para Hot-Fix...")
        # Usamos el wrapper existente
        if self.ai.llm_ready:
            # raw_mode=True para evitar el formato "Instruct:"
            fixed_code_raw = self.ai.consult_specialist(prompt, raw_mode=True)
            
            # Si la respuesta no empieza con def, lo agregamos (porque el prompt termina en def)
            if not fixed_code_raw.strip().startswith("def "):
                fixed_code_raw = "def " + fixed_code_raw
                
            print(f"   🔍 [DEBUG] Respuesta Raw IA: {fixed_code_raw[:100]}...") # Debug
        else:
            print("   ⚠️ IA no disponible. Usando heurística básica (Mock).")
            # Fallback básico para pruebas si la IA falla o tarda
            fixed_code_raw = self._heuristic_fix(source_code, exception)

        # Limpiar respuesta (extraer código)
        fixed_code = self._extract_code(fixed_code_raw)
        
        if not fixed_code:
            print("   ❌ La IA no devolvió código válido. Intentando fallback heurístico.")
            fixed_code = self._heuristic_fix(source_code, exception)

        print("   💉 Inyectando código corregido en memoria...")
        print(f"   📜 [DEBUG] Código Final a Inyectar:\n---\n{fixed_code}\n---")
        
        # 3. Hot-Patching (Reemplazo en caliente)
        try:
            # Compilar el nuevo código en el contexto del módulo original
            module = sys.modules[func.__module__]
            
            # Detectar nombre de la nueva función generada por la IA
            import ast
            tree = ast.parse(fixed_code)
            new_func_def_name = None
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    new_func_def_name = node.name
                    break
            
            if not new_func_def_name:
                raise ValueError("No function definition found in fixed code")

            # Ejecutar para crear la función en el módulo
            exec(fixed_code, module.__dict__)
            
            # Recuperar la nueva función usando su nombre real (el que puso la IA)
            new_func_obj = module.__dict__[new_func_def_name]
            
            # Sobrescribir la función ORIGINAL en el módulo con la NUEVA
            # Esto es crucial si la IA cambió el nombre (ej: risky -> safe)
            original_name = func.__name__
            if new_func_def_name != original_name:
                print(f"   ⚠️ La IA renombró la función: '{original_name}' -> '{new_func_def_name}'. Re-vinculando...")
                module.__dict__[original_name] = new_func_obj
            
            # Actualizar referencia local para ejecutarla ahora
            new_func = module.__dict__[original_name]
            
            print("   ⚡ ¡CÓDIGO RESUCITADO! Re-ejecutando...")
            return new_func(*args, **kwargs)
            
        except Exception as e:
            print(f"   ❌ Falló la inyección de código: {e}")
            raise exception

    def _heuristic_fix(self, code: str, exception: Exception) -> str:
        """Fix tonto por si la IA no responde (solo para demo)"""
        if isinstance(exception, ZeroDivisionError):
            # Reemplazar división por cero con una segura
            return code.replace(" / ", " / (1 if 0 else 1) # Lazarus Fix ").replace("/ b", "/ (b if b else 1)")
        if isinstance(exception, TypeError) and "'NoneType'" in str(exception):
            # Agregar check de None
            lines = code.split('\n')
            new_lines = []
            for line in lines:
                if "def " in line:
                    new_lines.append(line)
                    new_lines.append("    if not data: return 0 # Lazarus Fallback")
                else:
                    new_lines.append(line)
            return "\n".join(new_lines)
        return code

    def _extract_code(self, text: str) -> Optional[str]:
        """Limpia la salida del LLM usando AST para garantizar validez."""
        code = text
        
        # 1. Extraer bloques de código Markdown si existen
        if "```python" in text:
            code = text.split("```python")[1].split("```")[0]
        elif "```" in text:
            code = text.split("```")[1].split("```")[0]
            
        # 2. Limpieza básica de líneas
        lines = []
        for l in code.split('\n'):
            stripped = l.strip()
            if stripped.startswith('Instruct:') or stripped.startswith('Output:'):
                continue
            lines.append(l)
        final_code = "\n".join(lines).strip()
        
        # Fallback: Si está vacío, buscar 'def'
        if not final_code and "def " in text:
            final_code = text[text.find("def "):]

        # 3. Validación y Extracción vía AST (Robustez God Tier)
        import ast
        try:
            # Intentar parsear
            tree = ast.parse(final_code)
            
            # Filtrar solo definiciones de funciones e imports
            new_body = []
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Import, ast.ImportFrom)):
                    new_body.append(node)
            
            if not new_body:
                raise SyntaxError("No function definition found")
                
            # Reconstruir código limpio
            import astor
            return astor.to_source(ast.Module(body=new_body, type_ignores=[]))
            
        except (SyntaxError, ImportError):
            # Fallback: Truncado progresivo (para eliminar basura al final)
            lines = final_code.split('\n')
            for i in range(len(lines) - 1, 0, -1):
                subset = "\n".join(lines[:i])
                try:
                    ast.parse(subset)
                    return subset
                except SyntaxError:
                    continue
            
        return final_code if final_code else None

# Instancia global
_engine = LazarusEngine()

def lazarus_protect(func):
    """
    Decorador que hace inmortal a una función.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Invocar al motor de resurrección
            return _engine.heal_and_retry(func, args, kwargs, e)
    return wrapper
