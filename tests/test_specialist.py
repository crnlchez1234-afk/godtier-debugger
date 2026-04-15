import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ai.neurosys_debugger_wrapper import NeurosysDebuggerAI


def test_specialist():
    """Test symbolic analysis engine (replaces old LLM specialist test)."""
    ai = NeurosysDebuggerAI()

    code = """
def calculate_risk(data, alpha, beta, gamma, delta):
    global state
    for i in range(100):
        for j in range(100):
            pass
    return data * 0.5
"""
    result = ai.analyze_code(code)
    assert result["status"] == "success"
    assert result["facts_extracted"] > 0
    assert len(result["suggestions"]) > 0
    assert result["code_quality"] in ("Excelente", "Buena", "Aceptable", "Necesita mejoras")

    # consult_specialist should return something (backwards-compat API)
    response = ai.consult_specialist("analyze this", code)
    assert isinstance(response, str)
    assert len(response) > 0
