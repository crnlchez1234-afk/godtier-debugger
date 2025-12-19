from typing import Any, Dict


# -*- coding: utf-8 -*-
"""
TIER 10 - Audit Trail
======================
Registro auditable de todos los cambios auto-generados

Advanced Code Governance & Refactoring System
Date: December 6, 2025
"""

import json
from datetime import datetime
from pathlib import Path

class AuditTrail:
    """Mantiene registro auditable de cambios"""

    def __init__(self, audit_file: Any) -> None:
        self.audit_file = Path(audit_file)
        self.changes = []
        self.pending_writes = []  # PERFORMANCE FIX: Batch writes
        self.batch_size = 100  # Save every 100 changes

        # Load existing audit trail if exists
        if self.audit_file.exists():
            try:
                with open(self.audit_file, 'r', encoding='utf-8') as f:
                    self.changes = json.load(f)
            except:
                self.changes = []

    def log_change(self, change_metadata: Any) -> None:
        """
        Registra un cambio en el audit trail

        Args:
            change_metadata (dict): Metadata del cambio {
                'file_path': str,
                'change_type': str,
                'approved': bool,
                'approval_id': str,
                'timestamp': str (optional),
                ...
            }
        """
        entry = {
            'timestamp': change_metadata.get('timestamp', datetime.now().isoformat()),
            'file_path': change_metadata.get('file_path', 'unknown'),
            'change_type': change_metadata.get('change_type', 'unknown'),
            'approved': change_metadata.get('approved', False),
            'approval_id': change_metadata.get('approval_id', None),
            'metadata': change_metadata
        }

        self.changes.append(entry)
        self.pending_writes.append(entry)

        # PERFORMANCE FIX: Batch writes to reduce I/O
        if len(self.pending_writes) >= self.batch_size:
            self._save()
            self.pending_writes = []

    def _save(self) -> None:
        """Guarda audit trail a archivo"""
        try:
            with open(self.audit_file, 'w', encoding='utf-8') as f:
                json.dump(self.changes, f, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to save audit trail: {e}")

    def get_changes(self, filter_by: Any = None) -> Any:
        """
        Obtiene cambios del audit trail

        Args:
            filter_by (dict): Filtros opcionales {
                'file_path': str,
                'change_type': str,
                'approved': bool
            }

        Returns:
            list: Lista de cambios que coinciden con filtros
        """
        if not filter_by:
            return self.changes

        filtered = self.changes

        if 'file_path' in filter_by:
            filtered = [c for c in filtered if c['file_path'] == filter_by['file_path']]

        if 'change_type' in filter_by:
            filtered = [c for c in filtered if c['change_type'] == filter_by['change_type']]

        if 'approved' in filter_by:
            filtered = [c for c in filtered if c['approved'] == filter_by['approved']]

        return filtered

    def flush(self) -> None:
        """Fuerza guardado de cambios pendientes"""
        if self.pending_writes:
            self._save()
            self.pending_writes = []

    def get_stats(self) -> Dict:
        """Obtiene estadísticas del audit trail"""
        # Ensure all changes are saved
        self.flush()

        total = len(self.changes)
        approved = len([c for c in self.changes if c['approved']])
        rejected = total - approved

        change_types = {}
        for change in self.changes:
            ct = change['change_type']
            change_types[ct] = change_types.get(ct, 0) + 1

        return {
            'total_changes': total,
            'approved': approved,
            'rejected': rejected,
            'by_type': change_types
        }

    def clear(self) -> None:
        """Limpia audit trail (usar con precaución)"""
        self.changes = []
        self._save()
