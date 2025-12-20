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

    def commit_changes(self, file_path: str, message: str) -> bool:
        """Hace commit de los cambios con un mensaje personalizado."""
        # Add
        self._run(["add", file_path])
        
        # Commit
        # Usamos -m para el mensaje completo (git soporta multiline en -m o múltiples -m)
        # Para seguridad, pasamos el mensaje como un solo argumento
        ok, out = self._run(["commit", "-m", message])
        return ok

    def checkout_main(self):
        """Intenta volver a main o master."""
        # Try main first
        ok, _ = self._run(["checkout", "main"])
        if not ok:
            self._run(["checkout", "master"])
            
    def merge_branch(self, branch_name: str) -> bool:
        """Fusiona una rama en la actual (usualmente main)."""
        print(f"   🔀 Merging {branch_name} into current branch...")
        ok, out = self._run(["merge", branch_name])
        if ok:
            print("   ✅ Merge successful.")
            # Delete branch after merge
            self._run(["branch", "-d", branch_name])
            return True
        else:
            print(f"   ❌ Merge failed: {out}")
            self._run(["merge", "--abort"])
            return False
