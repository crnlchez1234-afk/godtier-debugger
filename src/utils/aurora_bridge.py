import sys
import os
from pathlib import Path
import importlib.util
import logging

# Configurar logger
logger = logging.getLogger("AuroraBridge")

class AuroraBridge:
    """
    🌉 PUENTE DE GOBERNANZA (DEBUGGING GODTIER <-> AURORA)
    Permite que el sistema de depuración utilice el motor de gobernanza de Aurora.
    """
    
    def __init__(self, aurora_path: str = r"E:\Aurora_Clean_Backup"):
        self.aurora_path = Path(aurora_path)
        self.governance = None
        self.ready = False
        
        if not self.aurora_path.exists():
            logger.error(f"❌ No se encuentra Aurora en: {self.aurora_path}")
            return

        self._connect()

    def _connect(self):
        """Carga dinámicamente el módulo de gobernanza de Aurora."""
        try:
            print(f"🔌 Conectando con Aurora Core en {self.aurora_path}...")
            
            # Añadir Aurora al path temporalmente
            sys.path.insert(0, str(self.aurora_path))
            
            # Importar GovernanceSystem
            # Nota: Aurora espera estar en el root, así que importamos como src.analysis.governance
            spec = importlib.util.spec_from_file_location(
                "src.analysis.governance",
                self.aurora_path / "src" / "analysis" / "governance.py"
            )
            module = importlib.util.module_from_spec(spec)
            sys.modules["src.analysis.governance"] = module
            spec.loader.exec_module(module)
            
            # Instanciar
            self.governance = module.GovernanceSystem()
            self.ready = True
            print("✅ Puente de Gobernanza Establecido.")
            
        except Exception as e:
            print(f"⚠️ Error conectando con Aurora: {e}")
            self.ready = False
        finally:
            # Limpiar path para no ensuciar
            if str(self.aurora_path) in sys.path:
                sys.path.remove(str(self.aurora_path))

    def validate_action(self, action_type: str, details: dict) -> bool:
        """
        Consulta a Aurora si una acción es segura.
        """
        if not self.ready:
            print("⚠️ Puente no listo. Aprobando por defecto (Modo Inseguro).")
            return True

        print(f"🛡️ Consultando Gobernanza Aurora para: {action_type}...")
        
        # Adaptar la solicitud al formato que Aurora espera (validate_evolution)
        # Aurora espera un diccionario plano con las claves de configuración
        proposal = details.copy()
        proposal["_reasoning"] = f"Solicitud externa de DEBUGGING_GODTIER para {action_type}"
        
        try:
            approved, message = self.governance.validate_evolution(proposal)
            if approved:
                print(f"✅ APROBADO por Aurora: {message}")
                return True
            else:
                print(f"⛔ BLOQUEADO por Aurora: {message}")
                return False
        except Exception as e:
            print(f"❌ Error durante validación: {e}")
            return False

if __name__ == "__main__":
    # Prueba rápida
    bridge = AuroraBridge()
    if bridge.ready:
        # Caso 1: Seguro
        bridge.validate_action("optimize_loop", {"target": "main.py", "risk": "low"})
        
        # Caso 2: Peligroso (Simulado)
        bridge.validate_action("delete_database", {"target": "users.db", "risk": "critical"})
