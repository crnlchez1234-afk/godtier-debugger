import subprocess
import time
import os
from typing import Tuple, Optional

class JSHandler:
    """
    Maneja la ejecución y optimización de scripts JavaScript (Node.js).
    """
    def __init__(self):
        self.node_cmd = "node"

    def is_available(self) -> bool:
        try:
            subprocess.run([self.node_cmd, "--version"], capture_output=True, check=True)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

    def run_benchmark(self, file_path: str) -> Tuple[float, str]:
        """Ejecuta el script JS y mide el tiempo."""
        start = time.time_ns()
        try:
            result = subprocess.run(
                [self.node_cmd, file_path],
                capture_output=True,
                text=True,
                check=True
            )
            end = time.time_ns()
            return (end - start), result.stdout
        except subprocess.CalledProcessError as e:
            return -1.0, e.stderr

    def create_mutant(self, original_path: str, mutant_code: str) -> str:
        """Crea un archivo temporal con el código mutante."""
        mutant_path = original_path.replace(".js", "_mutant.js")
        with open(mutant_path, "w", encoding="utf-8") as f:
            f.write(mutant_code)
        return mutant_path
