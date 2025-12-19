from tier10.codex_recursion_detector import detect_recursion

with open('sujeto_de_prueba.py', 'r', encoding='utf-8') as f:
    code = f.read()

print(f"Code length: {len(code)}")
results = detect_recursion(code)
print(f"Results: {results}")
