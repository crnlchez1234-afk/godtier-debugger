"""Quick test: verify Aurora LLM connects and responds."""
import sys, time
sys.path.insert(0, r"C:\EVIDENCIA_GENESIS_AURORA")
from core.aurora_llm_engine import get_engine

print("Cargando Aurora LLM (Qwen2.5-14B)...")
engine = get_engine()

for i in range(90):
    if engine.is_ready:
        break
    time.sleep(1)
    if i % 10 == 0:
        print(f"  Esperando... {i}s")

if engine.is_ready:
    elapsed = time.time() - engine._init_time
    print(f"AURORA LLM LISTA en {elapsed:.1f}s")
    print(f"Status: {engine.status()}")
    resp = engine.think("Analiza este error Python: ZeroDivisionError: division by zero en x = 10/0")
    if resp:
        print(f"Respuesta LLM ({len(resp)} chars):")
        print(resp[:500])
    else:
        print("Respuesta: None (modelo no respondio)")
else:
    print("FALLO: Aurora no se conecto en 90s")
    print(f"Status: {engine.status()}")
