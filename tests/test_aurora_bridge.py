import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.aurora_bridge import AuroraBridge

def test_aurora_integration():
    print("🌉 TEST: Aurora Governance Bridge Integration\n")
    
    bridge = AuroraBridge()
    
    if not bridge.ready:
        print("❌ Bridge failed to initialize.")
        return

    print("\n--- SCENARIO 1: Safe Optimization ---")
    safe_proposal = {
        "max_threads": 5, # Safe limit
        "optimization_level": "O2"
    }
    result_safe = bridge.validate_action("safe_config_update", safe_proposal)
    print(f"Result: {'✅ PASS' if result_safe else '❌ FAIL'}")

    print("\n--- SCENARIO 2: Dangerous Configuration (Thread Bomb) ---")
    dangerous_proposal = {
        "max_threads": 1000, # Exceeds limit of 50
        "optimization_level": "O3"
    }
    result_danger = bridge.validate_action("dangerous_config_update", dangerous_proposal)
    
    # We expect this to fail (return False)
    if not result_danger:
        print("Result: ✅ PASS (Correctly Blocked)")
    else:
        print("Result: ❌ FAIL (Should have been blocked!)")

if __name__ == "__main__":
    test_aurora_integration()
