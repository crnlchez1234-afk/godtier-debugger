# Tier 10 Engine: AI-Assisted Code Optimization & Governance System

**Version:** 1.0.0 (Hardened Release)
**Date:** December 16, 2025
**Author:** Cruz Sanchez

---

## 🔍 Overview

**Tier 10** is a deterministic, secure, and honest code optimization engine designed to automate the refactoring and assurance of Python scripts. Unlike traditional "AI coding agents" that operate as black boxes, Tier 10 implements a strict **Observer-Subject Architecture** that separates the creative capability of Large Language Models (LLMs) from the rigid safety requirements of production engineering.

It is **not** an AGI. It is a specialized engineering tool that uses Llama 3.1 as an inference engine and Python's Abstract Syntax Tree (AST) as a governance layer.

## 🛡️ Key Features

### 1. Honest Optimization
- **Real Benchmarking:** The system executes code in a controlled environment to measure actual performance gains. If the code isn't faster, it reports `+0.00%` improvement.
- **Logic Verification:** Ensures that optimized functions return the exact same results as the original code.

### 2. "Hard Governance" (Security)
The system enforces a **Zero Trust** policy on all AI-generated code. It does not "trust" the LLM; it verifies every token using Static Analysis (AST).

**Blocked Vectors:**
- 🚫 **RCE Attempts:** Blocks `os.system`, `subprocess`, `eval`, `exec`.
- 🚫 **Obfuscation:** Blocks metaprogramming tools like `importlib`, `getattr`, `__import__` used to hide malicious intent.
- 🚫 **Data Exfiltration:** Blocks network libraries (`urllib`, `requests`, `socket`) to prevent silent data leaks.
- 🚫 **Intent Violation:** Prevents the removal of logic marked as intentional (e.g., `time.sleep` for rate limiting).

### 3. Local Intelligence
- Uses **Ollama** running **Llama 3.1 (8B)** locally for privacy and speed.
- No code leaves your machine. All inference and analysis happen on-premise.

---

## ⚙️ Architecture

The system operates on a **Separation of Powers** model:

1.  **The Subject (Cortex):**
    *   *Engine:* Llama 3.1
    *   *Role:* Proposes creative optimizations and refactors.
    *   *Permissions:* Read-Only on source, Write-Only on proposals.

2.  **The Observer (Governance):**
    *   *Engine:* Python AST & `tier10_engine.py`
    *   *Role:* Validates syntax, security, and performance.
    *   *Permissions:* Veto power. Can block any change regardless of the LLM's "confidence".

---

## 🚀 Installation & Usage

### Prerequisites
1.  **Python 3.8+**
2.  **Ollama** installed and running.
3.  **Llama 3.1 Model:** Run `ollama pull llama3.1:8b`

### Setup
```bash
# Install dependencies
pip install astor ollama
```

### Running the Engine
To optimize a specific file:

```bash
python tier10_engine.py --targets my_script.py --generations 1
```

### Interpreting Results
- **✅ Applied successfully:** The code was safe, correct, and faster.
- **⛔ Blocked by governance:** The AI proposed unsafe code or tried to violate security rules.
- **🛡️ EVOLUTION HALTED:** A critical security risk was detected (e.g., RCE attempt).

---

## 🔒 Security Policy

The Tier 10 Engine adheres to the **"Hardened"** standard. It assumes that any generated code could be potentially malicious or flawed.

| Category | Status | Action |
| :--- | :--- | :--- |
| **System Calls** | 🔴 Forbidden | Immediate Block |
| **Network I/O** | 🔴 Forbidden | Immediate Block |
| **Dynamic Imports** | 🔴 Forbidden | Immediate Block |
| **Recursion** | 🟡 Allowed | Must be memoized (`@lru_cache`) |
| **Complex Logic** | 🟢 Allowed | Subject to correctness tests |

---

## 📝 Disclaimer

This tool is an assistant for software engineers. While it implements rigorous safety checks, it is recommended to always review the changes (diffs) produced by the engine before deploying to production environments.

**Tier 10 is a tool for code quality, not a replacement for human oversight.**
