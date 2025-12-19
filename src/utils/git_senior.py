import subprocess
import time
from pathlib import Path
from typing import Tuple, Optional

class GitSenior:
    """
    Maneja la integración con Git para el modo 'Senior'.
    Crea ramas, hace commits y gestiona el flujo de trabajo profesional.
    """
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.git_cmd = "git"

    def _run(self, args: list) -> Tuple[bool, str]:
        try:
            result = subprocess.run(
                [self.git_cmd] + args,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=False
            )
            return result.returncode == 0, result.stdout.strip()
        except FileNotFoundError:
            return False, "Git not installed"

    def is_repo(self) -> bool:
        ok, _ = self._run(["rev-parse", "--is-inside-work-tree"])
        return ok

    def init_repo(self) -> bool:
        """Inicializa un repo si no existe (para demos)."""
        ok, _ = self._run(["init"])
        return ok

    def get_current_branch(self) -> str:
        ok, out = self._run(["branch", "--show-current"])
        return out if ok else "unknown"

    def create_optimization_branch(self, func_name: str) -> str:
        """Crea una rama específica para la optimización."""
        timestamp = int(time.time())
        branch_name = f"darwin/opt-{func_name}-{timestamp}"
        
        # Crear rama y cambiar a ella
        self._run(["checkout", "-b", branch_name])
        return branch_name

    def commit_changes(self, file_path: str, func_name: str, speedup: float) -> bool:
        """Hace commit de los cambios."""
        # Add
        self._run(["add", file_path])
        
        # Commit
        msg = f"⚡ Darwin: Optimized '{func_name}' (🚀 {speedup:.2f}% Speedup)"
        ok, out = self._run(["commit", "-m", msg])
        return ok

    def checkout_main(self):
        """Intenta volver a main o master."""
        # Try main first
        ok, _ = self._run(["checkout", "main"])
        if not ok:
            self._run(["checkout", "master"])
