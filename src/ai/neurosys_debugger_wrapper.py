#!/usr/bin/env python3
"""
NEUROSYS AGI DEBUGGER WRAPPER v10.0
Motor de debugging con puente a Aurora LLM Engine (Qwen2.5-14B + LoRA).
Analisis simbolico (AST) como base + inferencia LLM cuando Aurora esta disponible.
"""

import sys
import ast
import os
from pathlib import Path
from typing import Dict, List, Any, Optional

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# --- Ruta al proyecto Aurora ---
_AURORA_PROJECT = os.environ.get(
    "AURORA_PROJECT_PATH",
    r"C:\EVIDENCIA_GENESIS_AURORA"
)


def _try_import_aurora():
    """Intenta importar el motor LLM de Aurora. Retorna (engine, True) o (None, False)."""
    aurora_path = Path(_AURORA_PROJECT)
    if not aurora_path.exists():
        return None, False
    try:
        if str(aurora_path) not in sys.path:
            sys.path.insert(0, str(aurora_path))
        from core.aurora_llm_engine import get_engine
        engine = get_engine()
        return engine, True
    except Exception:
        return None, False


class NeurosysDebuggerAI:
    """
    Motor de debugging inteligente con puente Aurora LLM.
    - Base: razonamiento simbolico (AST) + heuristicas.
    - Mejorado: inferencia LLM via Aurora Engine cuando esta disponible.
    """

    def __init__(self):
        self.name = "NeurosysAGI Debugger"
        self.version = "10.0 (Aurora Bridge)"
        self.ready = False
        self.llm_ready = False
        self.parser = None
        self._aurora_engine = None
        self._aurora_imported = False
        self.rules = [
            "IF is_long_function THEN suggest_refactor",
            "IF has_many_arguments THEN suggest_dataclass",
            "IF has_nested_loops THEN check_complexity",
            "IF uses_global_variables THEN warn_side_effects"
        ]
        self._initialize()

    def _initialize(self):
        """Inicializa Core Simbolico + conexion Aurora LLM."""
        # 1. Core Simbolico (siempre disponible)
        try:
            from neurosymbolic_agi_core import SymbolicParser
            self.parser = SymbolicParser()
            self.ready = True
        except Exception as e:
            print(f"[WARN] NeurosysAGI Core no disponible: {e}")
            self.ready = False

        # 2. Puente Aurora LLM (opcional)
        engine, imported = _try_import_aurora()
        self._aurora_engine = engine
        self._aurora_imported = imported
        if imported and engine is not None and engine.is_ready:
            self.llm_ready = True
            print(f"[OK] {self.name} v{self.version} - Aurora LLM: CONECTADO")
        elif imported:
            print(f"[OK] {self.name} v{self.version} - Aurora LLM: importado (cargando modelo...)")
        else:
            print(f"[OK] {self.name} v{self.version} - Modo simbolico (Aurora no disponible)")

    @property
    def aurora_ready(self) -> bool:
        """Verifica en tiempo real si Aurora LLM esta lista."""
        if self._aurora_engine is not None:
            ready = self._aurora_engine.is_ready
            self.llm_ready = ready
            return ready
        return False

    def analyze_error(self, error_trace: str, code_context: str) -> Dict[str, Any]:
        """Analiza un error. Usa Aurora LLM si esta disponible, si no, heuristicas."""
        if not self.ready:
            return {"status": "error", "message": "Neurosys Core not ready"}

        # Analisis heuristico base
        heuristic = self._heuristic_error_analysis(error_trace, code_context)

        # Enriquecer con Aurora LLM si esta lista
        if self.aurora_ready:
            llm_analysis = self._aurora_query(
                f"Analiza este error de Python y sugiere la correccion:\n"
                f"Error: {error_trace}\nCodigo: {code_context}"
            )
            if llm_analysis:
                return {
                    "status": "success",
                    "analysis": llm_analysis,
                    "heuristic_fallback": heuristic,
                    "source": "aurora_llm",
                    "confidence": 0.9
                }

        return {
            "status": "success",
            "analysis": heuristic,
            "source": "heuristic",
            "confidence": 0.7
        }

    def _heuristic_error_analysis(self, error_trace: str, code_context: str) -> str:
        """Analisis de errores basado en patrones conocidos."""
        trace_lower = error_trace.lower()
        suggestions = []

        if "zerodivisionerror" in trace_lower:
            suggestions.append("Agregar validacion: verificar que el divisor no sea cero antes de dividir.")
        if "indexerror" in trace_lower:
            suggestions.append("Verificar limites del indice antes de acceder a la lista/tupla.")
        if "keyerror" in trace_lower:
            suggestions.append("Usar dict.get(key, default) en lugar de dict[key].")
        if "attributeerror" in trace_lower:
            suggestions.append("Verificar que el objeto no sea None antes de acceder a sus atributos.")
        if "typeerror" in trace_lower:
            suggestions.append("Verificar los tipos de los argumentos. Posible None o tipo incorrecto.")
        if "importerror" in trace_lower or "modulenotfounderror" in trace_lower:
            suggestions.append("Verificar que el modulo este instalado (pip install) y el nombre sea correcto.")
        if "filenotfounderror" in trace_lower:
            suggestions.append("Verificar que la ruta del archivo exista. Usar pathlib.Path para rutas portables.")
        if "valueerror" in trace_lower:
            suggestions.append("Validar el valor de entrada antes de procesarlo.")
        if "syntaxerror" in trace_lower:
            suggestions.append("Revisar sintaxis: parentesis, dos puntos, indentacion.")
        if "nameerror" in trace_lower:
            suggestions.append("Variable no definida. Verificar scope y ortografia.")

        if not suggestions:
            suggestions.append("Error no reconocido. Revisar el traceback completo para mas contexto.")

        return "\n".join(f"- {s}" for s in suggestions)

    def analyze_code(self, code: str, context: str = "") -> Dict[str, Any]:
        """Analiza codigo usando razonamiento simbolico + Aurora LLM."""
        if not self.ready:
            return {
                "status": "unavailable",
                "message": "NeurosysAGI no esta disponible",
                "suggestions": [],
            }

        try:
            facts = self._extract_code_facts(code)
            reasoning = self._apply_symbolic_reasoning(facts)

            analysis = {
                "status": "success",
                "facts_extracted": len(facts),
                "code_quality": self._assess_code_quality(code),
                "reasoning_output": reasoning,
                "suggestions": reasoning.get("suggestions", []),
                "security_issues": self._check_security(code)
            }

            # Enriquecer con Aurora LLM si esta lista
            if self.aurora_ready:
                llm_review = self._aurora_query(
                    f"Revisa este codigo Python y da sugerencias de mejora:\n{code[:500]}"
                )
                if llm_review:
                    analysis["aurora_review"] = llm_review
                    analysis["source"] = "symbolic+aurora_llm"

            return analysis

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error en analisis: {str(e)}",
                "suggestions": [],
            }

    def _extract_code_facts(self, code: str) -> List[Dict[str, str]]:
        """Convierte el codigo en una lista de hechos simbolicos."""
        facts = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    facts.append({"subject": node.name, "predicate": "is_function"})
                    if len(node.body) > 15:
                        facts.append({"subject": node.name, "predicate": "is_long_function"})
                    if len(node.args.args) > 4:
                        facts.append({"subject": node.name, "predicate": "has_many_arguments"})

                if isinstance(node, (ast.For, ast.While)):
                    for child in ast.walk(node):
                        if isinstance(child, (ast.For, ast.While)) and child != node:
                            facts.append({"subject": "loop", "predicate": "has_nested_loops"})
                            break

                if isinstance(node, ast.Global):
                    facts.append({"subject": "code", "predicate": "uses_global_variables"})

        except Exception:
            pass
        return facts

    def _apply_symbolic_reasoning(self, facts: List[Dict[str, str]]) -> Dict[str, Any]:
        """Aplica reglas simbolicas a los hechos extraidos."""
        suggestions = []
        inferences = []

        for fact in facts:
            subject = fact["subject"]
            predicate = fact["predicate"]

            if predicate == "is_long_function":
                suggestions.append(f"Funcion '{subject}' es muy larga (>15 lineas). Sugerencia: Dividir en sub-funciones.")
                inferences.append(f"COMPLEXITY_HIGH({subject})")
            if predicate == "has_many_arguments":
                suggestions.append(f"Funcion '{subject}' tiene muchos argumentos. Sugerencia: Usar Dataclass o diccionario.")
                inferences.append(f"INTERFACE_BLOAT({subject})")
            if predicate == "has_nested_loops":
                suggestions.append("Bucles anidados detectados. Verificar complejidad O(n^2).")
                inferences.append("PERFORMANCE_RISK")
            if predicate == "uses_global_variables":
                suggestions.append("Uso de 'global' detectado. Puede causar efectos secundarios.")
                inferences.append("SIDE_EFFECT_RISK")

        return {
            "suggestions": list(set(suggestions)),
            "inferences": list(set(inferences))
        }

    def consult_specialist(self, query: str, context_code: str = "", raw_mode: bool = False) -> str:
        """
        Consulta al motor. Usa Aurora LLM si esta disponible, si no, analisis simbolico.
        Mantiene la API para compatibilidad con Lazarus y Darwin.
        """
        if raw_mode and context_code == "":
            return ""

        # Intentar con Aurora LLM primero
        if self.aurora_ready:
            prompt = query
            if context_code:
                prompt = f"{query}\n\nCodigo:\n{context_code[:500]}"
            llm_response = self._aurora_query(prompt)
            if llm_response:
                return llm_response

        # Fallback: analisis simbolico
        if context_code:
            result = self.analyze_code(context_code)
            if result.get("suggestions"):
                return "\n".join(result["suggestions"])

        return "Analisis simbolico: sin sugerencias especificas para esta consulta."

    def auto_fix_code(self, code: str, error_msg: str = "") -> Dict[str, Any]:
        """Intenta corregir codigo. Usa Aurora LLM si esta disponible."""
        if self.aurora_ready:
            prompt = f"Corrige este codigo Python:\n{code[:500]}"
            if error_msg:
                prompt += f"\nError: {error_msg}"
            llm_fix = self._aurora_query(prompt)
            if llm_fix:
                return {"status": "success", "fix": llm_fix, "source": "aurora_llm"}

        return {"status": "unavailable", "message": "Auto-fix requiere Aurora LLM o analisis manual."}

    def _aurora_query(self, question: str) -> Optional[str]:
        """Envia consulta directa a Aurora LLM Engine."""
        if self._aurora_engine is None or not self._aurora_engine.is_ready:
            return None
        try:
            from core.aurora_llm_engine import aurora_query
            return aurora_query(question)
        except Exception:
            return None

    def _assess_code_quality(self, code: str) -> str:
        """Evalua calidad del codigo."""
        lines = code.strip().split("\n")
        score = 100
        if len(lines) > 300: score -= 10
        if "TODO" in code: score -= 5
        if not any('"""' in line for line in lines): score -= 10

        if score >= 90: return "Excelente"
        elif score >= 70: return "Buena"
        elif score >= 50: return "Aceptable"
        else: return "Necesita mejoras"

    def _check_security(self, code: str) -> List[str]:
        """Revisa problemas de seguridad basicos."""
        issues = []
        if "password" in code.lower() and "=" in code:
            issues.append("Posible contrasena hardcodeada")
        if "eval(" in code or "exec(" in code:
            issues.append("Uso peligroso de eval/exec")
        return issues

    def status(self) -> Dict[str, Any]:
        """Estado completo del motor."""
        s = {
            "name": self.name,
            "version": self.version,
            "symbolic_ready": self.ready,
            "aurora_llm_ready": self.aurora_ready,
            "aurora_imported": self._aurora_imported,
        }
        if self._aurora_engine is not None:
            try:
                s["aurora_status"] = self._aurora_engine.status()
            except Exception:
                pass
        return s


if __name__ == "__main__":
    debugger = NeurosysDebuggerAI()
    print(f"\nEstado: {debugger.status()}")

    code_sample = """
def process_data(a, b, c, d, e, f):
    global state
    for i in range(100):
        for j in range(100):
            print(i, j)
    return True
"""
    print("\nAnalizando codigo de prueba...")
    result = debugger.analyze_code(code_sample)
    print("\nResultados:")
    for suggestion in result["suggestions"]:
        print(f"  {suggestion}")
    if result.get("aurora_review"):
        print(f"\nAurora LLM Review:\n  {result['aurora_review']}")