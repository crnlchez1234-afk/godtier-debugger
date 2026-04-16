#!/usr/bin/env python3
"""PRUEBA DURA: DEBUGGING_GODTIER con bugs reales."""
import sys, os, time, json, re
from pathlib import Path

os.environ["AURORA_PROJECT_PATH"] = r"C:\NONEXISTENT"

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


# === FASE 1: AutoDebugger ===
print("\n" + "=" * 70)
print("FASE 1: DETECCION Y CORRECCION DE BUGS (AutoDebugger)")
print("=" * 70)
dbg = AutoDebugger()

# 1.1 Missing colon
r = dbg.debug_code("def greet(name)\n    print('hi')\n")
rec("Syntax: missing colon", "def greet(name):" in r.corrected_code)

# 1.2 Unbalanced parens
r = dbg.debug_code("def f(x):\n    return (x + 1 * (x - 2)\n")
try:
    compile(r.corrected_code, "<t>", "exec"); ok=True
except SyntaxError:
    ok=False
rec("Syntax: unbalanced parens", ok)

# 1.3 Undefined variable
r = dbg.debug_code("def p():\n    result = x + 10\n    return result\n")
rec("Undefined variable", len(r.errors_found) > 0)

# 1.4 Missing import FastAPI
r = dbg.debug_code("app = FastAPI()\n@app.get('/')\ndef root():\n    return {'ok': True}\n")
rec("Missing import: FastAPI", "from fastapi import FastAPI" in r.corrected_code)

# 1.5 Missing import BaseModel
r = dbg.debug_code("class User(BaseModel):\n    name: str\n    age: int\n")
rec("Missing import: BaseModel", "from pydantic import BaseModel" in r.corrected_code)

# 1.6 Unclosed string
r = dbg.debug_code('def m():\n    msg = "hello world\n    return msg\n')
try:
    compile(r.corrected_code, "<t>", "exec"); ok=True
except SyntaxError:
    ok=False
rec("Syntax: unclosed string", ok)

# 1.7 Multi-bug: colon + undefined
r = dbg.debug_code("def calc(data, threshold)\n    for item in dta:\n        pass\n")
rec("Multi-bug: colon + undefined", "threshold):" in r.corrected_code, f"fixes={len(r.corrections_applied)}")

# 1.8 JavaScript
r = dbg.debug_code("function g() {\n    let x = f('/api'\n    if (x.ok {\n        return x\n    }\n", language="javascript")
rec("JavaScript: syntax fix", len(r.corrections_applied) > 0)

# 1.9 Unused imports
r = dbg.debug_code("import os\nimport sys\nimport json\n\ndef hello():\n    return 'hi'\n")
found = any("import" in str(e).lower() for e in r.errors_found)
rec("Code quality: unused imports", found)

# 1.10 HARD: complex real-world broken
code10 = "import requests\nfrom typing import List\n\ndef fetch_users(api_url, timeout)\n    response = requests.get(api_url)\n    data = response.json(\n    users = []\n    for user in data['results']:\n        users.append(user\n    return users\n"
r = dbg.debug_code(code10)
try:
    compile(r.corrected_code, "<t>", "exec"); ok=True
except SyntaxError:
    ok=False
rec("HARD: real-world multi-bug", ok, f"fixes={len(r.corrections_applied)}")


# === FASE 2: AI Simbolico ===
print("\n" + "=" * 70)
print("FASE 2: ANALISIS AI SIMBOLICO (NeurosysDebuggerAI)")
print("=" * 70)
ai = NeurosysDebuggerAI()

# 2.1 Complexity
code_c = """
def process_all(data, config, db, cache, logger, metrics):
    global STATE
    for i in range(10):
        for j in range(10):
            for k in range(10):
                pass
    return True
"""
a = ai.analyze_code(code_c)
rec("AI: detect complexity", len(a.get("suggestions", [])) > 0 and a.get("facts_extracted", 0) > 0,
    f"facts={a.get('facts_extracted')}, sugg={len(a.get('suggestions',[]))}")

# 2.2 Security
a = ai.analyze_code('password = "admin123"\neval(input())\n')
rec("AI: detect security issues", len(a.get("security_issues", [])) >= 2, f"issues={a.get('security_issues')}")

# 2.3 Error classification 8/8
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
rec("AI: error classification 8/8", sc == 8, f"score={sc}/8")

# 2.4 consult_specialist
resp = ai.consult_specialist("optimize this", code_c)
rec("AI: consult_specialist", isinstance(resp, str) and len(resp) > 5, f"len={len(resp)}")


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

# 3.1 Benchmarker
b1 = ArenaBenchmarker.measure_performance(slow_fn, iterations=50)
b2 = ArenaBenchmarker.measure_performance(fast_fn, iterations=50)
rec("Darwin: benchmarker works", b1.get("valid") and b2.get("valid"),
    f"slow={b1['avg_time_ns']/1e6:.2f}ms, fast={b2['avg_time_ns']/1e6:.2f}ms")

# 3.2 Compare gladiators
cmp = ArenaBenchmarker.compare_gladiators(b1, b2)
rec("Darwin: gladiator comparison", "winner" in cmp, f"winner={cmp.get('winner')}")

# 3.3 Safety: allow safe code
insp = DarwinSafetyInspector()
safe, errs = insp.check("import math\ndef f(x):\n    return math.sqrt(x)\n")
rec("Darwin: allow safe code", safe, str(errs)[:60] if errs else "OK")

# 3.4 Safety: block 6 threats
threats = [
    "import os\nos.system('rm -rf /')",
    "import subprocess\nsubprocess.run(['ls'])",
    "eval('hack')",
    "exec('import os')",
    "open('/etc/passwd').read()",
    "__import__('os').system('whoami')",
]
blocked = sum(1 for t in threats if not insp.check(t)[0])
rec("Darwin: block 6 threats", blocked == 6, f"blocked={blocked}/6")


# === FASE 4: Lazarus ===
print("\n" + "=" * 70)
print("FASE 4: LAZARUS - SELF-HEALING")
print("=" * 70)

# 4.1 Protect success
@lazarus_protect
def safe_fn(x):
    return x * 2

rec("Lazarus: protect success", safe_fn(5) == 10)

# 4.2 Survive ZeroDivision
@lazarus_protect
def divider(a, b):
    return a / b

try:
    result = divider(10, 0); survived = True
except:
    survived = False; result = None
rec("Lazarus: survive ZeroDivision", survived, f"result={result}")

# 4.3 Survive TypeError
@lazarus_protect
def bad_concat(a, b):
    return a + b

try:
    result = bad_concat("hello", 5); survived = True
except:
    survived = False; result = None
rec("Lazarus: survive TypeError", survived, f"result={result}")


# === FASE 5: E2E Integration ===
print("\n" + "=" * 70)
print("FASE 5: END-TO-END INTEGRATION")
print("=" * 70)

# 5.1 Fix syntax + detect security
broken = 'def fetch(uid)\n    db = connect("postgresql://admin:pass123@host/db")\n    eval(input())\n    return db.get(uid)\n'
fixed = dbg.debug_code(broken)
analysis = ai.analyze_code(fixed.corrected_code)
sec = analysis.get("security_issues", [])
has_colon = "uid):" in fixed.corrected_code
rec("E2E: syntax + security", has_colon and len(sec) >= 1, f"colon={'Y' if has_colon else 'N'}, security={sec}")

# 5.2 Performance: 100 analyses
code_perf = "def example():\n    x = [i**2 for i in range(100)]\n    return sum(x)\n"
start = time.perf_counter_ns()
for _ in range(100):
    dbg.debug_code(code_perf)
ms = (time.perf_counter_ns() - start) / 1e6
per = ms / 100
rec("E2E: speed (100 analyses)", per < 100, f"{per:.1f}ms each")

# 5.3 Idempotent on clean code
clean = "def add(a, b):\n    return a + b\n"
r = dbg.debug_code(clean)
rec("E2E: idempotent on clean code", "def add" in r.corrected_code and "return a + b" in r.corrected_code)

# 5.4 Batch: 5 different broken scripts
scripts = [
    "class Foo:\n    def bar(self)\n        pass\n",
    "x = [1, 2, 3\ny = x[0\n",
    "from os import path\nimport os\nprint(path.exists('.'))\n",
    "def f(a, b, c):\n    return a + b + c\nresult = f(1, 2)\n",
    'name = input("Name: ")\nprint("Hello " + name\n',
]
batch_ok = 0
for s in scripts:
    r = dbg.debug_code(s)
    try:
        compile(r.corrected_code, "<t>", "exec")
        batch_ok += 1
    except SyntaxError:
        pass
rec("E2E: batch fix 5 scripts", batch_ok >= 3, f"compiled={batch_ok}/5")


# === REPORTE ===
print("\n" + "=" * 70)
print("REPORTE FINAL")
print("=" * 70)
pct = R["passed"] / R["total"] * 100
print(f"\n  Total:  {R['total']} tests")
print(f"  Passed: {R['passed']}")
print(f"  Failed: {R['failed']}")
print(f"  Score:  {pct:.0f}%\n")

if pct >= 80:
    v = "SISTEMA FUNCIONAL - Base solida para monetizar"
elif pct >= 60:
    v = "NECESITA TRABAJO - Potencial pero gaps visibles"
else:
    v = "NO LISTO - Demasiadas fallas"
print(f"  VEREDICTO: {v}")
print(f"  {'=' * 60}\n")

out = project_root / "outputs" / "hard_test_results.json"
out.parent.mkdir(exist_ok=True)
with open(out, "w") as f:
    json.dump(R, f, indent=2)
print(f"  Guardado en: {out}")