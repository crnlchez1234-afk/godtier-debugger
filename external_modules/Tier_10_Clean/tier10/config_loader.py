import yaml
import os
from typing import Any, Dict

class ConfigLoader:
    _config = None

    @staticmethod
    def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
        if ConfigLoader._config is None:
            if not os.path.exists(config_path):
                # Fallback defaults if config is missing
                return {
                    "llm": {"provider": "ollama", "model": "llama3.1:8b"},
                    "evolution": {"max_generations": 100, "improvement_threshold": 0.05, "auto_approve_threshold": 0.3},
                    "paths": {"memory_db": "evolution_memory.db", "audit_log": "evolution_audit.jsonl", "snapshots": ".snapshots"}
                }
            
            with open(config_path, 'r') as f:
                ConfigLoader._config = yaml.safe_load(f)
        
        return ConfigLoader._config
