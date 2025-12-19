#!/usr/bin/env python3
"""
🧠 AURORA LONG-TERM MEMORY - TIER 2 AGI Feature
Sistema de memoria contextual profunda para recordar contexto por semanas/meses

Features:
- Almacenamiento persistente de interacciones
- Recuperación semántica de contexto relevante
- Detección de patrones de largo plazo
- Limpieza automática de memoria antigua
- Indexación para búsqueda rápida
"""

import sqlite3
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# Alias para compatibilidad con benchmark
class AuroraMemory:
    """Wrapper class para compatibilidad con benchmark"""

    def __init__(self, db_path: str) -> None:
        self.memory = LongTermMemory(db_path)

    def store(self, key: str, value: Any, category: str = "general") -> bool:
        """Store a key-value pair in memory"""
        context = {
            'key': key,
            'value': value,
            'category': category,
            'event': 'store'
        }
        return self.memory.store_context(context)

    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve a value by key"""
        results = self.memory.search_context({'key': key})
        if results:
            event_data_str = results[0].get('event_data', '{}')
            if isinstance(event_data_str, str):
                event_data = json.loads(event_data_str)
            else:
                event_data = event_data_str
            return event_data.get('value')
        return None

class LongTermMemory:
    """Sistema de memoria de largo plazo para Aurora"""

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self._init_database()

    def search_context(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search for contexts matching query"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Búsqueda simple por clave
                if 'key' in query:
                    cursor.execute("""
                        SELECT * FROM memory_contexts
                        WHERE keywords LIKE ?
                        ORDER BY importance_score DESC
                        LIMIT 100
                    """, (f'%{query["key"]}%',))
                else:
                    cursor.execute("""
                        SELECT * FROM memory_contexts
                        ORDER BY timestamp DESC
                        LIMIT 100
                    """)

                rows = cursor.fetchall()
                results = []
                for row in rows:
                    results.append({
                        'id': row[0],
                        'context_hash': row[1],
                        'event_type': row[2],
                        'event_data': row[3],
                        'keywords': row[4],
                        'timestamp': row[5],
                        'importance_score': row[6]
                    })
                return results
        except:
            return []

    def _init_database(self) -> None:
        """Inicializa base de datos de memoria"""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS memory_contexts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    context_hash TEXT UNIQUE,
                    event_type TEXT,
                    event_data TEXT,  -- JSON
                    keywords TEXT,  -- JSON array para búsqueda
                    timestamp TEXT,
                    importance_score REAL DEFAULT 0.5,
                    access_count INTEGER DEFAULT 0,
                    last_accessed TEXT
                );

                CREATE TABLE IF NOT EXISTS memory_associations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    memory_id INTEGER,
                    associated_memory_id INTEGER,
                    association_type TEXT,
                    strength REAL DEFAULT 0.5,
                    FOREIGN KEY (memory_id) REFERENCES memory_contexts(id),
                    FOREIGN KEY (associated_memory_id) REFERENCES memory_contexts(id)
                );

                CREATE TABLE IF NOT EXISTS memory_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_type TEXT,
                    pattern_data TEXT,  -- JSON
                    frequency INTEGER,
                    first_seen TEXT,
                    last_seen TEXT,
                    confidence REAL
                );

                CREATE INDEX IF NOT EXISTS idx_keywords ON memory_contexts(keywords);
                CREATE INDEX IF NOT EXISTS idx_timestamp ON memory_contexts(timestamp);
                CREATE INDEX IF NOT EXISTS idx_importance ON memory_contexts(importance_score);
            """)

    # TODO: REFACTOR - Función muy larga (63 líneas). Dividir en funciones más pequeñas.
    def store_context(self, context: Dict[str, Any], importance: float = 0.5) -> bool:
        """
        Almacena contexto en memoria de largo plazo

        Args:
            context: Diccionario con información del evento
            importance: Score de importancia (0.0-1.0)

        Returns:
            True si se almacenó exitosamente
        """
        try:
            # Generar hash único
            context_str = json.dumps(context, sort_keys=True)
            context_hash = hashlib.sha256(context_str.encode()).hexdigest()

            # Extraer keywords para búsqueda
            keywords = self._extract_keywords(context)

            # Determinar tipo de evento
            event_type = context.get('event', 'general')

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Verificar si ya existe
                cursor.execute("""
                    SELECT id FROM memory_contexts WHERE context_hash = ?
                """, (context_hash,))

                existing = cursor.fetchone()

                if existing:
                    # Actualizar acceso
                    cursor.execute("""
                        UPDATE memory_contexts
                        SET access_count = access_count + 1,
                            last_accessed = ?
                        WHERE id = ?
                    """, (datetime.now().isoformat(), existing[0]))
                else:
                    # Insertar nuevo contexto
                    cursor.execute("""
                        INSERT INTO memory_contexts
                        (context_hash, event_type, event_data, keywords, timestamp,
                         importance_score, last_accessed)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        context_hash,
                        event_type,
                        json.dumps(context),
                        json.dumps(keywords),
                        datetime.now().isoformat(),
                        importance,
                        datetime.now().isoformat()
                    ))

                conn.commit()

            return True

        except Exception as e:
            print(f"Error storing context: {e}")
            return False

    # TODO: REFACTOR - Función muy larga (70 líneas). Dividir en funciones más pequeñas.
    def retrieve_relevant_context(self, query: str, days_back: int = 90,
                                  limit: int = 20) -> List[Dict[str, Any]]:
        """
        Recupera contextos relevantes basados en query

        Args:
            query: Búsqueda semántica
            days_back: Días hacia atrás para buscar (default: 90 días)
            limit: Máximo número de resultados (default: 20)

        Returns:
            Lista de contextos relevantes ordenados por relevancia
        """
        try:
            # Extraer keywords del query
            query_keywords = self._extract_keywords({'query': query})

            # Calcular fecha límite
            cutoff_date = (datetime.now() - timedelta(days=days_back)).isoformat()

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Recuperar contextos recientes
                cursor.execute("""
                    SELECT id, event_type, event_data, keywords, timestamp,
                           importance_score, access_count
                    FROM memory_contexts
                    WHERE timestamp >= ?
                    ORDER BY importance_score DESC, timestamp DESC
                """, (cutoff_date,))

                contexts = []

                for row in cursor.fetchall():
                    mem_id, event_type, event_data, keywords, timestamp, importance, access_count = row

                    # Calcular relevancia
                    relevance = self._calculate_relevance(
                        query_keywords,
                        json.loads(keywords),
                        importance,
                        access_count
                    )

                    if relevance > 0.1:  # Umbral mínimo de relevancia
                        context_data = json.loads(event_data)
                        context_data['memory_id'] = mem_id
                        context_data['relevance'] = relevance
                        context_data['timestamp'] = timestamp
                        contexts.append(context_data)

                # Ordenar por relevancia y limitar
                contexts.sort(key=lambda x: x['relevance'], reverse=True)

                # Actualizar access_count de los contextos recuperados
                for context in contexts[:limit]:
                    cursor.execute("""
                        UPDATE memory_contexts
                        SET access_count = access_count + 1,
                            last_accessed = ?
                        WHERE id = ?
                    """, (datetime.now().isoformat(), context['memory_id']))

                conn.commit()

                return contexts[:limit]

        except Exception as e:
            print(f"Error retrieving context: {e}")
            return []

    def _extract_keywords(self, context: Dict[str, Any]) -> List[str]:
        """Extrae keywords relevantes del contexto"""
        # Obtener texto completo del contexto
        text_parts = []

        for key, value in context.items():
            if isinstance(value, str):
                text_parts.append(value.lower())
            elif isinstance(value, (list, dict)):
                text_parts.append(str(value).lower())

        full_text = ' '.join(text_parts)

        # Filtrar palabras comunes (stopwords simplificado)
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
                    'to', 'for', 'of', 'with', 'by', 'from', 'is', 'was', 'are'}

        # Extraer palabras únicas
        words = full_text.split()
        keywords = [
            word.strip('.,!?;:"()[]{}')
            for word in words
            if len(word) > 3 and word not in stopwords
        ]

        # Retornar keywords únicos
        return list(set(keywords))[:20]  # Máximo 20 keywords

    def _calculate_relevance(self, query_keywords: List[str],
                            context_keywords: List[str],
                            importance: float,
                            access_count: int) -> float:
        """Calcula score de relevancia mejorado (0.0-1.0)"""
        if not query_keywords or not context_keywords:
            return 0.0

        # Factor 1: Coincidencia exacta de keywords (35%)
        exact_matches = sum(1 for kw in query_keywords if kw in context_keywords)
        keyword_score = (exact_matches / len(query_keywords)) * 0.35

        # Factor 2: Coincidencias parciales (20%)
        partial_score = 0
        for qk in query_keywords:
            for ck in context_keywords:
                if len(qk) > 3 and len(ck) > 3:
                    if qk in ck or ck in qk:
                        partial_score += 0.5
        partial_score = min(partial_score / len(query_keywords), 1.0) * 0.20

        # Factor 3: Importancia del contexto (25%)
        importance_score = importance * 0.25

        # Factor 4: Frecuencia de acceso (20% con decay)
        access_score = min(access_count / 20, 1.0) * 0.20

        return keyword_score + partial_score + importance_score + access_score

    def detect_patterns(self, pattern_type: str = None,
                       min_frequency: int = 3) -> List[Dict[str, Any]]:
        """
        Detecta patrones recurrentes en la memoria

        Args:
            pattern_type: Tipo de patrón específico a buscar
            min_frequency: Frecuencia mínima para considerar patrón

        Returns:
            Lista de patrones detectados
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Agrupar por tipo de evento
                cursor.execute("""
                    SELECT event_type, COUNT(*) as frequency,
                           MIN(timestamp) as first_seen,
                           MAX(timestamp) as last_seen
                    FROM memory_contexts
                    WHERE 1=1
                    """ + ("AND event_type = ?" if pattern_type else "") + """
                    GROUP BY event_type
                    HAVING frequency >= ?
                    ORDER BY frequency DESC
                """, (pattern_type, min_frequency) if pattern_type else (min_frequency,))

                patterns = []

                for event_type, frequency, first_seen, last_seen in cursor.fetchall():
                    # Calcular confianza basada en frecuencia y recencia
                    days_span = (datetime.fromisoformat(last_seen) -
                               datetime.fromisoformat(first_seen)).days + 1
                    confidence = min(frequency / (days_span / 7), 1.0)  # Normalizar por semana

                    patterns.append({
                        'pattern_type': event_type,
                        'frequency': frequency,
                        'first_seen': first_seen,
                        'last_seen': last_seen,
                        'confidence': confidence
                    })

                return patterns

        except Exception as e:
            print(f"Error detecting patterns: {e}")
            return []

    def cleanup_old_memories(self, days_to_keep: int = 90,
                            min_importance: float = 0.3) -> int:
        """
        Limpia memorias antiguas de baja importancia

        Args:
            days_to_keep: Días de retención
            min_importance: Importancia mínima para mantener

        Returns:
            Número de memorias eliminadas
        """
        try:
            cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).isoformat()

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Eliminar memorias antiguas de baja importancia
                cursor.execute("""
                    DELETE FROM memory_contexts
                    WHERE timestamp < ?
                    AND importance_score < ?
                    AND access_count < 2
                """, (cutoff_date, min_importance))

                deleted = cursor.rowcount

                conn.commit()

                return deleted

        except Exception as e:
            print(f"Error cleaning memories: {e}")
            return 0

    def get_memory_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de la memoria"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Total de memorias
                cursor.execute("SELECT COUNT(*) FROM memory_contexts")
                total_memories = cursor.fetchone()[0]

                # Memorias por tipo
                cursor.execute("""
                    SELECT event_type, COUNT(*)
                    FROM memory_contexts
                    GROUP BY event_type
                """)
                by_type = dict(cursor.fetchall())

                # Promedio de importancia
                cursor.execute("SELECT AVG(importance_score) FROM memory_contexts")
                avg_importance = cursor.fetchone()[0] or 0.0

                # Memoria más antigua
                cursor.execute("SELECT MIN(timestamp) FROM memory_contexts")
                oldest = cursor.fetchone()[0]

                # Memoria más reciente
                cursor.execute("SELECT MAX(timestamp) FROM memory_contexts")
                newest = cursor.fetchone()[0]

                return {
                    'total_memories': total_memories,
                    'by_type': by_type,
                    'average_importance': round(avg_importance, 2),
                    'oldest_memory': oldest,
                    'newest_memory': newest,
                    'storage_path': self.db_path
                }

        except Exception as e:
            print(f"Error getting stats: {e}")
            return {}

# ========== FUNCIONES DE UTILIDAD ==========

def test_memory() -> None:
    """Test rápido del sistema de memoria"""
    memory = LongTermMemory()

    print("🧠 Aurora Long-Term Memory - TIER 2\n")

    # Test 1: Almacenar contextos
    print("Test 1: Almacenando contextos...")
    test_contexts = [
        {"event": "tier2_validation", "data": "Aurora TIER 2 validation started", "timestamp": datetime.now().isoformat()},
        {"event": "deployment", "data": "Deployed Aurora to production", "status": "success"},
        {"event": "tier2_validation", "data": "Multi-step planner tested successfully", "result": "pass"},
        {"event": "user_interaction", "data": "User requested TIER 2 implementation", "priority": "high"},
    ]

    for ctx in test_contexts:
        importance = 0.8 if 'priority' in ctx else 0.5
        result = memory.store_context(ctx, importance)
        print(f"  {'✅' if result else '❌'} Stored: {ctx.get('event', 'unknown')}")

    # Test 2: Recuperar contexto
    print("\nTest 2: Recuperando contexto relevante...")
    query = "validation tier2"
    results = memory.retrieve_relevant_context(query, days_back=7, limit=5)
    print(f"  Encontrados {len(results)} contextos relevantes para '{query}'")
    for i, result in enumerate(results, 1):
        print(f"    {i}. {result.get('data', 'N/A')} (relevancia: {result.get('relevance', 0):.2f})")

    # Test 3: Detectar patrones
    print("\nTest 3: Detectando patrones...")
    patterns = memory.detect_patterns(min_frequency=1)
    print(f"  Detectados {len(patterns)} patrones")
    for pattern in patterns:
        print(f"    - {pattern['pattern_type']}: {pattern['frequency']} veces (confianza: {pattern['confidence']:.2f})")

    # Test 4: Estadísticas
    print("\nTest 4: Estadísticas de memoria...")
    stats = memory.get_memory_stats()
    print(f"  Total de memorias: {stats['total_memories']}")
    print(f"  Importancia promedio: {stats['average_importance']}")
    print(f"  Tipos: {stats['by_type']}")

if __name__ == "__main__":
    test_memory()
