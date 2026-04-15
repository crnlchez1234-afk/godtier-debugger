import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ai.tier10_router import Tier10Router

def test_router_logic():
    print("🧪 TEST: Tier 10 Router Logic Simulation\n")
    
    router = Tier10Router()
    
    # Test Cases
    scenarios = [
        {
            "name": "Simple Bug Fix",
            "prompt": "Fix this IndexError in the list comprehension.",
            "expected": "light"
        },
        {
            "name": "Complex Refactor",
            "prompt": "Refactor the entire authentication module to use OAuth2 and rewrite the database schema.",
            "expected": "beast"
        },
        {
            "name": "Algorithm Optimization",
            "prompt": "Optimize this O(n^2) sorting algorithm to be O(n log n).",
            "expected": "beast"
        },
        {
            "name": "Tiny Script",
            "prompt": "print('hello world')",
            "expected": "light"
        },
        {
            "name": "Massive Context",
            "prompt": "x" * 2500, # > 2000 chars
            "expected": "beast"
        }
    ]
    
    print(f"{'SCENARIO':<25} | {'DECISION':<10} | {'RESULT':<10}")
    print("-" * 50)
    
    for case in scenarios:
        decision = router.decide_model(case["prompt"])
        result = "✅ PASS" if decision == case["expected"] else "❌ FAIL"
        print(f"{case['name']:<25} | {decision.upper():<10} | {result}")

if __name__ == "__main__":
    test_router_logic()
