import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ai.neurosys_debugger_wrapper import NeurosysDebuggerAI

def test_god_tier_wrapper():
    print("⚡ PROBANDO WRAPPER GOD TIER (HÍBRIDO) ⚡")
    print("=========================================\n")

    ai = NeurosysDebuggerAI()
    
    if not ai.llm_ready:
        print("❌ El modelo especialista no cargó. Revisa los logs anteriores.")
        return

    print("\n🧠 Consultando al Especialista...")
    code_snippet = """
    def calculate_risk(data):
        # Intentional delay
        import time
        time.sleep(5)
        return data * 0.5
    """
    
    query = "Analyze this code for performance issues but respect intentional delays."
    response = ai.consult_specialist(query, code_snippet)
    
    print(f"\n🤖 Respuesta del Especialista:\n{response}")
    print("\n✅ Prueba completada.")

if __name__ == "__main__":
    test_god_tier_wrapper()
