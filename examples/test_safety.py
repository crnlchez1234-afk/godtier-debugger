from src.darwin.safety import validate_mutant_safety

def test_safety_scanner():
    print("🛡️ Testing Darwin Safety Scanner...")

    # Case 1: Safe Code
    safe_code = """
def safe_calc(n):
    import math
    return math.sqrt(n) + 10
"""
    is_safe, errors = validate_mutant_safety(safe_code)
    print(f"\n[Case 1] Safe Code: {'✅ PASS' if is_safe else '❌ FAIL'}")
    if not is_safe: print(errors)

    # Case 2: Dangerous Import
    dangerous_import = """
def hack(n):
    import os
    return os.getcwd()
"""
    is_safe, errors = validate_mutant_safety(dangerous_import)
    print(f"\n[Case 2] Dangerous Import (os): {'✅ PASS' if is_safe else '❌ BLOCKED'}")
    if not is_safe: 
        for e in errors: print(f"   - {e}")

    # Case 3: Dangerous Call (eval)
    dangerous_eval = """
def dynamic(n):
    return eval("2 + 2")
"""
    is_safe, errors = validate_mutant_safety(dangerous_eval)
    print(f"\n[Case 3] Dangerous Call (eval): {'✅ PASS' if is_safe else '❌ BLOCKED'}")
    if not is_safe: 
        for e in errors: print(f"   - {e}")

    # Case 4: Dangerous Attribute (subprocess.run)
    # Note: Even if 'subprocess' was imported (which is blocked), checking attributes is a second layer.
    dangerous_attr = """
def run_cmd(n):
    import subprocess
    subprocess.run(["echo", "hack"])
"""
    is_safe, errors = validate_mutant_safety(dangerous_attr)
    print(f"\n[Case 4] Dangerous Attribute (subprocess.run): {'✅ PASS' if is_safe else '❌ BLOCKED'}")
    if not is_safe: 
        for e in errors: print(f"   - {e}")

if __name__ == "__main__":
    test_safety_scanner()