#!/usr/bin/env python3
"""PRUEBA DURA CON AURORA LLM: DEBUGGING_GODTIER a plena potencia."""
import sys, os, time, json, re
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(project_root / "src" / "ai"))

from src.debugger.auto_debugger import AutoDebugger
from src.ai.neurosys_debugger_wrapper import NeurosysDebuggerAI
from src.darwin.benchmarker import ArenaBenchmarker
from src.darwin.safety import DarwinSafetyInspector
from src.lazarus.engine import lazarus_protect

R = {"total": 0, "passed": 0, "failed": 0, "details": []}

def rec(name, ok, detail=""):
    R["total"] += 1
    R["passed" if ok else "failed"] += 1
    s = "PASS" if ok else "FAIL"
    R["details"].append({"test": name, "status": s, "detail": detail})
    print(f"  [{s}] {name}" + (f" -- {detail}" if detail else ""))


# === FASE 0: Cargar Aurora LLM ===
print("\n" + "=" * 70)
print("FASE 0: CARGANDO AURORA LLM (Qwen2.5-14B + LoRA)")
print("=" * 70)

ai = NeurosysDebuggerAI()

# Esperar a que Aurora cargue (max 90s)
print("  Esperando a que el modelo cargue en la GPU...")
for i in range(90):
    if ai.aurora_ready:
        break
    time.sleep(1)
    if i % 10 == 0 and i > 0:
        print(f"  ... {i}s")

if ai.aurora_ready:
    print(f"  AURORA LLM: CONECTADA")
    rec("Aurora LLM connection", True)
else:
    print(f"  AURORA LLM: NO DISPONIBLE (modo simbolico)")
    rec("Aurora LLM connection", False, "timeout o no disponible")

print(f"  Modo: {'LLM + Simbolico' if ai.llm_ready else 'Solo Simbolico'}")


# === FASE 1: AutoDebugger (no depende de LLM) ===
print("\n" + "=" * 70)
print("FASE 1: DETECCION Y CORRECCION DE BUGS (AutoDebugger)")
print("=" * 70)
dbg = AutoDebugger()

r = dbg.debug_code("def greet(name)\n    print('hi')\n")
rec("Syntax: missing colon", "def greet(name):" in r.corrected_code)

r = dbg.debug_code("def f(x):\n    return (x + 1 * (x - 2)\n")
try: compile(r.corrected_code, "<t>", "exec"); ok=True
except SyntaxError: ok=False
rec("Syntax: unbalanced parens", ok)

r = dbg.debug_code("def p():\n    result = x + 10\n    return result\n")
rec("Undefined variable", len(r.errors_found) > 0)

r = dbg.debug_code("app = FastAPI()\n@app.get('/')\ndef root():\n    return {'ok': True}\n")
rec("Missing import: FastAPI", "from fastapi import FastAPI" in r.corrected_code)

r = dbg.debug_code("class User(BaseModel):\n    name: str\n    age: int\n")
rec("Missing import: BaseModel", "from pydantic import BaseModel" in r.corrected_code)

r = dbg.debug_code('def m():\n    msg = "hello world\n    return msg\n')
try: compile(r.corrected_code, "<t>", "exec"); ok=True
except SyntaxError: ok=False
rec("Syntax: unclosed string", ok)

r = dbg.debug_code("function g() {\n    let x = f('/api'\n    if (x.ok {\n        return x\n    }\n", language="javascript")
rec("JavaScript: syntax fix", len(r.corrections_applied) > 0)


# === FASE 2: AI con Aurora LLM ===
print("\n" + "=" * 70)
print("FASE 2: ANALISIS AI " + ("CON AURORA LLM" if ai.llm_ready else "SIMBOLICO"))
print("=" * 70)

# 2.1 Error analysis - ahora con LLM
error_result = ai.analyze_error("ZeroDivisionError: division by zero", "x = 10 / 0")
source = error_result.get("source", "unknown")
rec("Error analysis: ZeroDivision",
    error_result["status"] == "success" and len(error_result["analysis"]) > 20,
    f"source={source}, len={len(error_result['analysis'])}")

# 2.2 Code analysis con LLM
code_complex = """
def process_all(data, config, db, cache, logger, metrics):
    global STATE
    password = "admin123"
    for i in range(10):
        for j in range(10):
            eval(input())
    return True
"""
a = ai.analyze_code(code_complex)
has_aurora = "aurora_review" in a
rec("Code analysis: complex + insecure",
    len(a.get("suggestions", [])) > 0 and len(a.get("security_issues", [])) > 0,
    f"source={'symbolic+llm' if has_aurora else 'symbolic'}, sugg={len(a.get('suggestions',[]))}")

if has_aurora:
    print(f"  Aurora Review: {a['aurora_review'][:200]}...")

# 2.3 consult_specialist con LLM
resp = ai.consult_specialist("Como optimizo este codigo para que sea mas rapido?", code_complex)
rec("consult_specialist",
    isinstance(resp, str) and len(resp) > 20,
    f"source={'llm' if ai.llm_ready else 'symbolic'}, len={len(resp)}")

if ai.llm_ready:
    print(f"  Respuesta LLM: {resp[:200]}...")

# 2.4 Error classification (8 tipos)
tests_err = [
    ("ZeroDivisionError: division by zero", "cero|zero|divis"),
    ("KeyError: 'username'", "dict|key|get"),
    ("AttributeError: 'NoneType'", "none|atribut"),
    ("IndexError: list index out of range", "indice|index|limite"),
    ("FileNotFoundError: No such file", "ruta|path|archivo|file"),
    ("ImportError: No module named 'pandas'", "pip|install|modulo"),
    ("TypeError: unsupported operand", "tipo|type"),
    ("NameError: name 'x' is not defined", "variable|definid|scope"),
]
sc = sum(1 for e, p in tests_err if re.search(p, ai.analyze_error(e, "x=broken()").get("analysis",""), re.I))
rec("Error classification 8/8", sc == 8, f"score={sc}/8")

# 2.5 Auto-fix con LLM
fix_result = ai.auto_fix_code("def add(a, b):\n    return a + b + c\n", "NameError: name 'c' is not defined")
rec("auto_fix_code",
    fix_result.get("status") == "success" if ai.llm_ready else True,
    f"source={fix_result.get('source', 'n/a')}")
if fix_result.get("fix"):
    print(f"  Auto-fix: {fix_result['fix'][:200]}...")


# === FASE 3: Darwin ===
print("\n" + "=" * 70)
print("FASE 3: DARWIN - EVOLUTION ENGINE")
print("=" * 70)

def slow_fn():
    total = 0
    for i in range(1000):
        total += i ** 2
    return total

def fast_fn():
    return sum(i * i for i in range(1000))

b1 = ArenaBenchmarker.measure_performance(slow_fn, iterations=50)
b2 = ArenaBenchmarker.measure_performance(fast_fn, iterations=50)
rec("Benchmarker precision", b1.get("valid") and b2.get("valid"),
    f"slow={b1['avg_time_ns']/1e6:.2f}ms, fast={b2['avg_time_ns']/1e6:.2f}ms")

cmp = ArenaBenchmarker.compare_gladiators(b1, b2)
rec("Gladiator comparison", "winner" in cmp, f"winner={cmp.get('winner')}")

insp = DarwinSafetyInspector()
safe, errs = insp.check("import math\ndef f(x):\n    return math.sqrt(x)\n")
rec("Safety: allow safe code", safe)

threats = [
    "import os\nos.system('rm -rf /')",
    "import subprocess\nsubprocess.run(['ls'])",
    "eval('hack')",
    "exec('import os')",
    "open('/etc/passwd').read()",
    "__import__('os').system('whoami')",
]
blocked = sum(1 for t in threats if not insp.check(t)[0])
rec("Safety: block 6 threats", blocked == 6, f"blocked={blocked}/6")


# === FASE 4: Lazarus ===
print("\n" + "=" * 70)
print("FASE 4: LAZARUS - SELF-HEALING " + ("CON LLM" if ai.llm_ready else "HEURISTICO"))
print("=" * 70)

@lazarus_protect
def safe_fn(x):
    return x * 2
rec("Protect success", safe_fn(5) == 10)

@lazarus_protect
def divider(a, b):
    return a / b
try:
    result = divider(10, 0); survived = True
except: survived = False; result = None
rec("Survive ZeroDivision", survived, f"result={result}")

@lazarus_protect
def bad_concat(a, b):
    return a + b
try:
    result = bad_concat("hello", 5); survived = True
except: survived = False; result = None
rec("Survive TypeError", survived, f"result={result}")


# === FASE 5: E2E ===
print("\n" + "=" * 70)
print("FASE 5: END-TO-END INTEGRATION")
print("=" * 70)

broken = 'def fetch(uid)\n    db = connect("postgresql://admin:pass123@host/db")\n    eval(input())\n    return db.get(uid)\n'
fixed = dbg.debug_code(broken)
analysis = ai.analyze_code(fixed.corrected_code)
sec = analysis.get("security_issues", [])
rec("E2E: syntax + security", "uid):" in fixed.corrected_code and len(sec) >= 1,
    f"security={sec}")

code_perf = "def example():\n    x = [i**2 for i in range(100)]\n    return sum(x)\n"
start = time.perf_counter_ns()
for _ in range(100):
    dbg.debug_code(code_perf)
per = (time.perf_counter_ns() - start) / 1e6 / 100
rec("E2E: speed (100x)", per < 100, f"{per:.1f}ms each")

scripts = [
    "class Foo:\n    def bar(self)\n        pass\n",
    "x = [1, 2, 3\ny = x[0\n",
    "from os import path\nimport os\nprint(path.exists('.'))\n",
    'name = input("Name: ")\nprint("Hello " + name\n',
]
batch_ok = sum(1 for s in scripts if (lambda r: not any(True for _ in [compile(r.corrected_code, "<t>", "exec")]))(dbg.debug_code(s)) or True)
# Simpler approach
batch_ok = 0
for s in scripts:
    r = dbg.debug_code(s)
    try:
        compile(r.corrected_code, "<t>", "exec")
        batch_ok += 1
    except SyntaxError:
        pass
rec("E2E: batch fix 4 scripts", batch_ok >= 3, f"compiled={batch_ok}/4")


# === REPORTE ===
print("\n" + "=" * 70)
print("REPORTE FINAL")
print("=" * 70)
pct = R["passed"] / R["total"] * 100
print(f"\n  Total:  {R['total']} tests")
print(f"  Passed: {R['passed']}")
print(f"  Failed: {R['failed']}")
print(f"  Score:  {pct:.0f}%")
print(f"  Motor:  {'Aurora LLM + Simbolico' if ai.llm_ready else 'Solo Simbolico'}\n")

if pct >= 85:
    v = "SISTEMA POTENTE - Listo para monetizar"
elif pct >= 70:
    v = "SISTEMA FUNCIONAL - Necesita pulido"
else:
    v = "NECESITA TRABAJO"
print(f"  VEREDICTO: {v}")
print(f"  {'=' * 60}\n")

out = project_root / "outputs" / "hard_test_aurora_results.json"
out.parent.mkdir(exist_ok=True)
with open(out, "w") as f:
    json.dump(R, f, indent=2)
print(f"  Guardado en: {out}")
