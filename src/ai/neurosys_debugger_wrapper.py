#!/usr/bin/env python3
"""
🧠 NEUROSYS AGI DEBUGGER WRAPPER 🧠
Integra el LLM NeurosysAGI con el sistema de debugging.
Version 7.0: Enhanced Symbolic Reasoning
"""

import sys
import os
import ast
from pathlib import Path
from typing import Dict, List, Optional, Any

# Agregar path para importar neurosys
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))


class NeurosysDebuggerAI:
    """
    Wrapper para usar NeurosysAGI como motor de debugging inteligente.
    Utiliza razonamiento simbólico para analizar la estructura del código.
    """

    def __init__(self):
        self.name = "NeurosysAGI Debugger"
        self.version = "8.0 (God Tier - Hybrid)"
        self.ready = False
        self.llm_ready = False
        self.parser = None
        self.model = None
        self.tokenizer = None
        self.device = "cpu"
        self.rules = [
            "IF is_long_function THEN suggest_refactor",
            "IF has_many_arguments THEN suggest_dataclass",
            "IF has_nested_loops THEN check_complexity",
            "IF uses_global_variables THEN warn_side_effects"
        ]
        self._initialize()

    def _initialize(self):
        """Inicializa el sistema NeurosysAGI y el Modelo Especialista"""
        # 1. Inicializar Core Simbólico
        try:
            from neurosymbolic_agi_core import SymbolicParser
            self.parser = SymbolicParser()
            self.ready = True
            print(f"✅ {self.name} v{self.version} - Core Simbólico: ACTIVO")
        except ImportError as e:
            print(f"⚠️  NeurosysAGI Core no disponible: {e}")
            self.ready = False

        # 2. Inicializar LLM Especialista (Tier 10)
        self.llm_ready = False
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
            from peft import PeftModel
            
            print("⏳ Cargando Especialista Tier 10 (Phi-2 + LoRA)...")
            
            # Rutas
            base_model_id = "microsoft/phi-2"
            # Ajustar ruta relativa al workspace
            workspace_root = Path(__file__).parent.parent.parent
            adapter_path = workspace_root / "external_modules" / "Tier_10_Clean" / "TIER10_UPDATE_PACKAGE" / "Tier10-Specialist-v1"
            
            if adapter_path.exists():
                # Configuración de dispositivo
                self.device = "cuda" if torch.cuda.is_available() else "cpu"
                dtype = torch.float16 if torch.cuda.is_available() else torch.float32
                
                # Configuración de Memoria (Estabilidad)
                max_memory = None
                if self.device == "cuda":
                    # Reservar solo 8GB para el modelo, dejar el resto para el sistema/otros procesos
                    # Tienes 12GB, así que 8GB es seguro.
                    max_memory = {0: "8GB"} 
                
                # Cargar Tokenizer
                try:
                    self.tokenizer = AutoTokenizer.from_pretrained(str(adapter_path), trust_remote_code=True)
                except:
                    self.tokenizer = AutoTokenizer.from_pretrained(base_model_id, trust_remote_code=True)
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
                # Cargar Modelo Base con gestión de memoria
                self.model = AutoModelForCausalLM.from_pretrained(
                    base_model_id,
                    torch_dtype=dtype,
                    trust_remote_code=True,
                    device_map="auto" if self.device == "cuda" else None,
                    max_memory=max_memory,
                    offload_folder="offload_weights" # Usar disco/RAM si falta VRAM
                )
                if self.device == "cpu":
                    self.model = self.model.to(self.device)
                
                # Cargar Adaptador
                self.model = PeftModel.from_pretrained(self.model, str(adapter_path))
                self.llm_ready = True
                print(f"✅ Especialista Tier 10: ACTIVO ({self.device} - Memory Optimized)")
            else:
                print(f"⚠️  Adaptador Tier 10 no encontrado en: {adapter_path}")
                
        except Exception as e:
            print(f"⚠️  No se pudo cargar el LLM Especialista: {e}")
            self.llm_ready = False

    def analyze_code(self, code: str, context: str = "") -> Dict[str, Any]:
        """
        Analiza código usando razonamiento simbólico.
        Convierte el AST del código en 'hechos' y aplica reglas lógicas.
        """
        if not self.ready:
            return {
                "status": "unavailable",
                "message": "NeurosysAGI no está disponible",
                "suggestions": [],
            }

        try:
            # 1. Extraer Hechos del Código (Code-to-Symbolic)
            facts = self._extract_code_facts(code)
            
            # 2. Razonamiento Simbólico (Aplicar Reglas)
            reasoning = self._apply_symbolic_reasoning(facts)

            analysis = {
                "status": "success",
                "facts_extracted": len(facts),
                "code_quality": self._assess_code_quality(code),
                "reasoning_output": reasoning,
                "suggestions": reasoning.get("suggestions", []),
                "security_issues": self._check_security(code)
            }

            return analysis

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error en análisis: {str(e)}",
                "suggestions": [],
            }

    def _extract_code_facts(self, code: str) -> List[Dict[str, str]]:
        """
        Convierte el código en una lista de hechos simbólicos.
        Ejemplo: {"subject": "func_x", "predicate": "is_long_function"}
        """
        facts = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                # Hechos sobre Funciones
                if isinstance(node, ast.FunctionDef):
                    facts.append({"subject": node.name, "predicate": "is_function"})
                    
                    # Check length
                    if len(node.body) > 15:
                        facts.append({"subject": node.name, "predicate": "is_long_function"})
                    
                    # Check arguments
                    if len(node.args.args) > 4:
                        facts.append({"subject": node.name, "predicate": "has_many_arguments"})

                # Hechos sobre Bucles
                if isinstance(node, (ast.For, ast.While)):
                    for child in ast.walk(node):
                        if isinstance(child, (ast.For, ast.While)) and child != node:
                            facts.append({"subject": "loop", "predicate": "has_nested_loops"})
                            break
                
                # Hechos sobre Globales
                if isinstance(node, ast.Global):
                    facts.append({"subject": "code", "predicate": "uses_global_variables"})

        except Exception:
            pass # Si falla el parseo, retornamos lo que tengamos
        return facts

    def _apply_symbolic_reasoning(self, facts: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Aplica el motor de reglas simbólicas a los hechos extraídos.
        """
        suggestions = []
        inferences = []

        for fact in facts:
            subject = fact["subject"]
            predicate = fact["predicate"]

            # Regla: Funciones largas
            if predicate == "is_long_function":
                suggestions.append(f"⚡ Función '{subject}' es muy larga (>15 líneas). Sugerencia: Dividir en sub-funciones.")
                inferences.append(f"COMPLEXITY_HIGH({subject})")

            # Regla: Muchos argumentos
            if predicate == "has_many_arguments":
                suggestions.append(f"📦 Función '{subject}' tiene muchos argumentos. Sugerencia: Usar Dataclass o diccionario.")
                inferences.append(f"INTERFACE_BLOAT({subject})")

            # Regla: Bucles anidados
            if predicate == "has_nested_loops":
                suggestions.append(f"🔄 Bucles anidados detectados. Verificar complejidad O(n^2).")
                inferences.append("PERFORMANCE_RISK")

            # Regla: Variables globales
            if predicate == "uses_global_variables":
                suggestions.append(f"🌐 Uso de 'global' detectado. Puede causar efectos secundarios difíciles de rastrear.")
                inferences.append("SIDE_EFFECT_RISK")

        return {
            "suggestions": list(set(suggestions)), # Eliminar duplicados
            "inferences": list(set(inferences))
        }

    def consult_specialist(self, query: str, context_code: str = "", raw_mode: bool = False) -> str:
        """Consulta al modelo especialista Tier 10"""
        if not self.llm_ready:
            return "Especialista no disponible."
            
        if raw_mode:
            prompt = query
        else:
            prompt = f"Instruct: {query}\nContext Code:\n{context_code}\nOutput:"
        
        try:
            import torch
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs, 
                    max_new_tokens=200, 
                    do_sample=True, 
                    temperature=0.7,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            full_output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            if raw_mode:
                # Intentamos devolver solo lo generado nuevo
                # Una heurística simple es quitar el prompt del inicio
                if full_output.startswith(prompt):
                    return full_output[len(prompt):].strip()
                return full_output # Fallback
            else:
                return full_output.split("Output:")[-1].strip()
        except Exception as e:
            return f"Error consultando especialista: {e}"

    def auto_fix_code(self, code: str, error_msg: str = "") -> Dict[str, Any]:
        """Intenta corregir código automáticamente usando el Especialista"""
        if self.llm_ready:
            fix_prompt = f"Fix the following Python code which has this error: {error_msg}"
            fixed_code = self.consult_specialist(fix_prompt, code)
            return {
                "status": "success", 
                "fixed_code": fixed_code,
                "source": "Tier10-Specialist"
            }
        
        return {"status": "unavailable", "message": "Auto-fix avanzado requiere modelo especialista"}

    def _assess_code_quality(self, code: str) -> str:
        """Evalúa calidad del código (Heurística simple)"""
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
        """Revisa problemas de seguridad básicos"""
        issues = []
        if "password" in code.lower() and "=" in code:
            issues.append("⚠️  Posible contraseña hardcodeada")
        if "eval(" in code or "exec(" in code:
            issues.append("⚠️  Uso peligroso de eval/exec")
        return issues

# Demo
if __name__ == "__main__":
    debugger = NeurosysDebuggerAI()
    
    code_sample = """
def process_data(a, b, c, d, e, f):
    global state
    for i in range(100):
        for j in range(100):
            print(i, j)
            # ... many lines ...
            # ... many lines ...
            # ... many lines ...
            # ... many lines ...
            # ... many lines ...
            # ... many lines ...
            # ... many lines ...
            # ... many lines ...
            # ... many lines ...
            # ... many lines ...
            # ... many lines ...
            # ... many lines ...
            # ... many lines ...
            # ... many lines ...
            # ... many lines ...
            # ... many lines ...
    return True
"""
    print("\nAnalizando código de prueba...")
    result = debugger.analyze_code(code_sample)
    print("\nResultados del Razonamiento Simbólico:")
    for suggestion in result["suggestions"]:
        print(suggestion)
