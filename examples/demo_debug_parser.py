import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
from src.ai.neurosymbolic_agi_core import SymbolicParser
import json

p = SymbolicParser()
res = p.parse_logical_expression("IF x AND OR y THEN crash")
print(json.dumps(res, indent=2))
