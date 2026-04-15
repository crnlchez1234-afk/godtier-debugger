#!/usr/bin/env python3
"""
GodTier Debugger CLI
====================
Command-line interface for the AI-powered self-healing debugger.

Usage:
    godtier scan <path>       Scan a directory for bugs
    godtier fix <file>        Auto-fix a Python file
    godtier analyze <file>    AI analysis of a file
    godtier safety <file>     Security audit of a file
    godtier info              Show system status
"""

import argparse
import sys
import os
from pathlib import Path

# Ensure project root on path
_PROJECT_ROOT = Path(__file__).parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))


def _scan(args):
    """Scan a directory for Python bugs."""
    from src.debugger.auto_debugger import AutoDebugger

    target = Path(args.path)
    if not target.exists():
        print(f"Error: path '{target}' not found.")
        return 1

    debugger = AutoDebugger()
    files = list(target.rglob("*.py")) if target.is_dir() else [target]

    if not files:
        print("No Python files found.")
        return 0

    total_errors = 0
    total_fixed = 0

    for f in files:
        code = f.read_text(encoding="utf-8", errors="replace")
        result = debugger.debug_code(code, language="python")
        n_err = len(result.errors_found)
        n_fix = len(result.corrections_applied)
        total_errors += n_err
        total_fixed += n_fix
        if n_err:
            rel = f.relative_to(target) if target.is_dir() else f.name
            status = "FIXED" if result.success else "ISSUES"
            print(f"  [{status}] {rel}  ({n_err} errors, {n_fix} fixed)")

    print(f"\nSummary: {len(files)} files scanned, "
          f"{total_errors} errors found, {total_fixed} auto-fixed.")
    return 0 if total_errors == total_fixed else 1


def _fix(args):
    """Auto-fix a single Python file."""
    from src.debugger.auto_debugger import AutoDebugger

    target = Path(args.file)
    if not target.is_file():
        print(f"Error: file '{target}' not found.")
        return 1

    code = target.read_text(encoding="utf-8", errors="replace")
    debugger = AutoDebugger()
    result = debugger.debug_code(code, language="python")

    if not result.errors_found:
        print(f"No errors found in {target.name}.")
        return 0

    print(f"Errors found: {len(result.errors_found)}")
    for err in result.errors_found:
        print(f"  - {err}")
    print(f"Corrections applied: {len(result.corrections_applied)}")
    for fix in result.corrections_applied:
        print(f"  + {fix}")

    if args.write:
        target.write_text(result.corrected_code, encoding="utf-8")
        print(f"\nFixed code written to {target}")
    else:
        print(f"\nFixed code (use --write to save):")
        print("-" * 60)
        print(result.corrected_code)

    return 0


def _analyze(args):
    """AI analysis of a Python file."""
    from src.ai.neurosys_debugger_wrapper import NeurosysDebuggerAI

    target = Path(args.file)
    if not target.is_file():
        print(f"Error: file '{target}' not found.")
        return 1

    code = target.read_text(encoding="utf-8", errors="replace")
    ai = NeurosysDebuggerAI()

    aurora_status = "Aurora LLM" if ai.llm_ready else "Symbolic (heuristic)"
    print(f"Engine: {ai.name} v{ai.version}")
    print(f"Mode: {aurora_status}\n")

    result = ai.analyze_code(code)
    for key, value in result.items():
        if isinstance(value, list):
            print(f"{key}:")
            for item in value:
                print(f"  - {item}")
        elif isinstance(value, dict):
            print(f"{key}:")
            for k, v in value.items():
                print(f"  {k}: {v}")
        else:
            print(f"{key}: {value}")

    return 0


def _safety(args):
    """Security audit of a Python file."""
    from src.darwin.safety import DarwinSafetyInspector

    target = Path(args.file)
    if not target.is_file():
        print(f"Error: file '{target}' not found.")
        return 1

    code = target.read_text(encoding="utf-8", errors="replace")
    inspector = DarwinSafetyInspector()
    is_safe, issues = inspector.check(code)

    if is_safe:
        print(f"SAFE: {target.name} passed all security checks.")
    else:
        print(f"UNSAFE: {target.name} has {len(issues)} security issue(s):")
        for issue in issues:
            print(f"  ! {issue}")

    return 0 if is_safe else 1


def _info(_args):
    """Show system status."""
    from src.ai.neurosys_debugger_wrapper import NeurosysDebuggerAI

    ai = NeurosysDebuggerAI()
    print("GodTier Debugger v1.0.0")
    print(f"  Engine: {ai.name} v{ai.version}")
    print(f"  Symbolic Core: {'OK' if ai.ready else 'NOT AVAILABLE'}")
    print(f"  Aurora LLM: {'CONNECTED' if ai.llm_ready else 'NOT AVAILABLE'}")
    print(f"  Rules loaded: {len(ai.rules)}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        prog="godtier",
        description="GodTier Debugger - AI-powered self-healing code debugger",
    )
    sub = parser.add_subparsers(dest="command")

    # scan
    p_scan = sub.add_parser("scan", help="Scan a directory for bugs")
    p_scan.add_argument("path", help="Directory or file to scan")
    p_scan.set_defaults(func=_scan)

    # fix
    p_fix = sub.add_parser("fix", help="Auto-fix a Python file")
    p_fix.add_argument("file", help="Python file to fix")
    p_fix.add_argument("--write", "-w", action="store_true",
                       help="Write fixed code back to the file")
    p_fix.set_defaults(func=_fix)

    # analyze
    p_analyze = sub.add_parser("analyze", help="AI analysis of a file")
    p_analyze.add_argument("file", help="Python file to analyze")
    p_analyze.set_defaults(func=_analyze)

    # safety
    p_safety = sub.add_parser("safety", help="Security audit of a file")
    p_safety.add_argument("file", help="Python file to audit")
    p_safety.set_defaults(func=_safety)

    # info
    p_info = sub.add_parser("info", help="Show system status")
    p_info.set_defaults(func=_info)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
