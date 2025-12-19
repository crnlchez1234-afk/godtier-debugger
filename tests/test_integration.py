import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.debugger.auto_debugger import AutoDebugger

def test_neurosymbolic_integration():
    print("🔗 PROBANDO INTEGRACIÓN NEURO-SIMBÓLICA 🔗")
    print("===========================================\n")

    debugger = AutoDebugger()
    
    if not debugger.brain:
        print("❌ Error: El cerebro simbólico no se cargó correctamente.")
        return

    print("✅ Cerebro Simbólico detectado en AutoDebugger.")

    # Código con una regla lógica mal formada (para probar detección)
    bad_code = """
def process_data(data):
    # IF data is valid THEN process
    # IF x AND OR y THEN crash
    if data:
        return True
    """

    print("\n📄 Analizando código con reglas lógicas...")
    result = debugger.debug_code(bad_code)

    print("\n📊 Resultados:")
    print(f"Errores encontrados: {len(result.errors_found)}")
    for error in result.errors_found:
        print(f" - {error}")
    
    print("\n🛠️ Código Corregido:")
    print(result.corrected_code)

    if "NEUROSYS" in result.corrected_code:
        print("\n✅ ¡ÉXITO! El sistema insertó advertencias neuro-simbólicas.")
    else:
        print("\n❌ FALLO: No se insertaron advertencias.")

if __name__ == "__main__":
    test_neurosymbolic_integration()
