import sqlite3
import hashlib
import time
from pathlib import Path
from typing import Optional, Tuple

# Base de datos local para la memoria genética
DB_PATH = Path("darwin_gene_memory.db")

class GeneMemory:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Inicializa la tabla de memoria si no existe."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS evolutions (
                function_name TEXT,
                original_hash TEXT,
                optimized_code TEXT,
                speedup_factor REAL,
                timestamp REAL,
                PRIMARY KEY (function_name, original_hash)
            )
        ''')
        conn.commit()
        conn.close()

    def _compute_hash(self, source_code: str) -> str:
        """Calcula el hash SHA-256 del código fuente normalizado."""
        # Normalizar: eliminar espacios en blanco extra para evitar falsos negativos por formato
        normalized = "".join(source_code.split())
        return hashlib.sha256(normalized.encode('utf-8')).hexdigest()

    def recall_optimization(self, function_name: str, original_source: str) -> Optional[Tuple[str, float]]:
        """
        Busca si ya existe una optimización para esta función específica.
        Retorna: (código_optimizado, factor_speedup) o None
        """
        code_hash = self._compute_hash(original_source)
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            "SELECT optimized_code, speedup_factor FROM evolutions WHERE function_name=? AND original_hash=?",
            (function_name, code_hash)
        )
        result = c.fetchone()
        conn.close()
        
        if result:
            return result[0], result[1]
        return None

    def save_optimization(self, function_name: str, original_source: str, optimized_source: str, speedup: float):
        """Guarda una mutación exitosa en la memoria genética."""
        code_hash = self._compute_hash(original_source)
        timestamp = time.time()
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute(
                "INSERT OR REPLACE INTO evolutions VALUES (?, ?, ?, ?, ?)",
                (function_name, code_hash, optimized_source, speedup, timestamp)
            )
            conn.commit()
        except Exception as e:
            print(f"⚠️ Error guardando en memoria genética: {e}")
        finally:
            conn.close()
