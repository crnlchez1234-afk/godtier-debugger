import sys
import time
from pathlib import Path

# Setup path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.lazarus.engine import lazarus_protect

print("🧪 INICIANDO PRUEBA DEL PROTOCOLO LÁZARO 🧪")
print("===========================================\n")

@lazarus_protect
def risky_math_operation(a, b):
    print(f"   🔢 Ejecutando división: {a} / {b}")
    # Esto va a fallar si b es 0
    result = a / b
    return result

@lazarus_protect
def access_database(data):
    print("   💾 Intentando acceder a base de datos...")
    # Simulamos un error de acceso a atributo None
    return data['value'] * 2

def run_test():
    print("--- PRUEBA 1: ZeroDivisionError ---")
    try:
        # Intentamos dividir por cero. Normalmente esto mata el programa.
        # Lázaro debería atraparlo, pedirle a la IA que arregle la función
        # (ej: retornando 0 o manejando la excepción) y reintentar.
        val = risky_math_operation(10, 0)
        print(f"✅ Resultado final (post-resurrección): {val}")
    except Exception as e:
        print(f"❌ Murió definitivamente: {e}")

    print("\n--- PRUEBA 2: TypeError/KeyError ---")
    try:
        # Pasamos None, lo cual causará error al intentar acceder ['value']
        val = access_database(None)
        print(f"✅ Resultado final (post-resurrección): {val}")
    except Exception as e:
        print(f"❌ Murió definitivamente: {e}")

if __name__ == "__main__":
    run_test()
