import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ai.neurosys_debugger_wrapper import NeurosysDebuggerAI


def test_god_tier_wrapper():
    """Test the NeurosysDebuggerAI symbolic analysis pipeline."""
    ai = NeurosysDebuggerAI()

    assert ai.ready is True, "Symbolic core should initialize"
    assert ai.llm_ready is False, "LLM should not be loaded"

    # Test code analysis
    code = """
def process(x):
    return x * 2
"""
    result = ai.analyze_code(code)
    assert result["status"] == "success"
    assert isinstance(result["facts_extracted"], int)

    # Test error analysis
    error_result = ai.analyze_error("ZeroDivisionError: division by zero", "x = 1/0")
    assert error_result["status"] == "success"
    assert "cero" in error_result["analysis"].lower() or "zero" in error_result["analysis"].lower()

    # Test security check
    dangerous = "password = 'admin123'"
    sec_result = ai.analyze_code(dangerous)
    assert len(sec_result.get("security_issues", [])) > 0
