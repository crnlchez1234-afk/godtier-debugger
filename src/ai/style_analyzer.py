import ast
import re
from typing import Dict, Any

class StyleAnalyzer:
    """
    Analiza código fuente para extraer convenciones de estilo (ADN del programador).
    """
    
    def analyze(self, source_code: str) -> Dict[str, Any]:
        return {
            "indentation": self._detect_indentation(source_code),
            "naming": self._detect_naming_convention(source_code),
            "typing": self._detect_typing_usage(source_code),
            "docstrings": self._detect_docstring_style(source_code)
        }

    def get_style_prompt(self, source_code: str) -> str:
        """Genera una instrucción en lenguaje natural para el LLM basada en el estilo detectado."""
        style = self.analyze(source_code)
        
        prompt = "STRICT STYLE GUIDELINES (MIMIC USER STYLE):\n"
        
        # Indentación
        if style["indentation"] == "tabs":
            prompt += "- Use TABS for indentation.\n"
        else:
            spaces = style["indentation"]
            prompt += f"- Use {spaces} SPACES for indentation.\n"
            
        # Naming
        prompt += f"- Variable Naming: {style['naming']['variables']}.\n"
        prompt += f"- Function Naming: {style['naming']['functions']}.\n"
        
        # Typing
        if style["typing"]:
            prompt += "- USE Python Type Hints (e.g., def func(x: int) -> str:).\n"
        else:
            prompt += "- DO NOT use Type Hints (keep it dynamic).\n"
            
        # Docstrings
        if style["docstrings"]:
            prompt += "- Include docstrings for functions.\n"
            
        return prompt

    def _detect_indentation(self, code: str) -> Any:
        lines = code.split('\n')
        for line in lines:
            if line.startswith(' ') and len(line.strip()) > 0:
                # Contar espacios iniciales
                spaces = len(line) - len(line.lstrip(' '))
                # Asumimos que el primer nivel de indentación define el estilo (heurística simple)
                if spaces > 0:
                    return spaces
            if line.startswith('\t'):
                return "tabs"
        return 4 # Default standard

    def _detect_naming_convention(self, code: str) -> Dict[str, str]:
        # Heurística simple basada en regex sobre el código
        snake_case = len(re.findall(r'[a-z]+_[a-z]+', code))
        camelCase = len(re.findall(r'[a-z]+[A-Z][a-z]+', code))
        
        style = "snake_case" if snake_case >= camelCase else "camelCase"
        return {"variables": style, "functions": style}

    def _detect_typing_usage(self, code: str) -> bool:
        # Busca sintaxis de tipo : int, -> str, etc.
        return bool(re.search(r':\s*[a-zA-Z_\[\]]+\s*[=,)]', code)) or "->" in code

    def _detect_docstring_style(self, code: str) -> bool:
        return '"""' in code or "'''" in code
