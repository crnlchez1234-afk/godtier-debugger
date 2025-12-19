import sys
import time
from pathlib import Path

# Setup path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.darwin.evolver import DarwinEvolver

def slow_function(n):
    """
    A deliberately slow function: Sum of squares using a slow loop and sleep.
    """
    result = 0
    # Inefficient loop
    for i in range(n):
        time.sleep(0.0001) # Artificial delay to simulate heavy work
        result += i * i
    return result

def test_darwin_evolution():
    print("🏟️ BIENVENIDO A LA ARENA DE DARWIN 🏟️")
    print("======================================\n")

    evolver = DarwinEvolver()
    
    print("📜 Función Original: 'slow_function'")
    print("   (Contiene un sleep artificial y un bucle lento)")

    # Run Evolution
    # We pass n=100 as test argument
    evolved_func = evolver.evolve(slow_function, test_args=(100,), iterations=10)

    if evolved_func and evolved_func != slow_function:
        print("\n✨ ¡EVOLUCIÓN COMPLETADA! ✨")
        print("Probando la nueva función...")
        start = time.time()
        res = evolved_func(100)
        end = time.time()
        print(f"Resultado: {res} (Tiempo: {(end-start)*1000:.4f} ms)")
        
        # Verify correctness (simple check)
        expected = sum(i*i for i in range(100))
        if res == expected:
            print("✅ La lógica se mantiene correcta.")
        else:
            print(f"❌ ALERTA: El resultado cambió (Esperado: {expected}, Obtenido: {res})")
    else:
        print("\n🦕 La evolución no produjo un espécimen superior esta vez.")

if __name__ == "__main__":
    test_darwin_evolution()
