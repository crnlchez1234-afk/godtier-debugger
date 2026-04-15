import sys
import os
import json
from pathlib import Path

# Add project root to path to allow imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ai.neurosymbolic_agi_core import SymbolicParser

def run_tests():
    print("🧪 INICIANDO PRUEBAS DEL CEREBRO SIMBÓLICO (GOD TIER) 🧪")
    print("========================================================\n")

    parser = SymbolicParser()

    test_cases = [
        # 1. Hecho simple
        "The variable is null",
        
        # 2. Regla simple
        "IF x is null THEN return None",
        
        # 3. Regla compleja con AND
        "IF user is admin AND access is granted THEN show dashboard",
        
        # 4. Regla con OR (probando la recursividad)
        "IF error is 404 OR error is 500 THEN log error",
        
        # 5. Proposición atómica
        "TRUE",
        
        # 6. Algo que no es regla ni hecho claro
        "Just a random string"
    ]

    for i, case in enumerate(test_cases, 1):
        print(f"🔹 Caso {i}: '{case}'")
        try:
            result = parser.parse_logical_expression(case)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"❌ Error: {e}")
        print("-" * 50)

if __name__ == "__main__":
    run_tests()
