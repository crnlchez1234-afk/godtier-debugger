from typing import Any


# -*- coding: utf-8 -*-
"""
TIER 10 - Rollback Manager
===========================
Gestiona snapshots y rollback de cambios en código

Advanced Code Governance & Refactoring System
Date: December 6, 2025
"""

import os
import hashlib
import json
from datetime import datetime
from pathlib import Path

class RollbackManager:
    """Gestiona snapshots y rollback de código"""

    def __init__(self, snapshots_dir: Any) -> None:
        self.snapshots_dir = Path(snapshots_dir)
        self.snapshots_dir.mkdir(exist_ok=True)
        self.snapshots = {}  # {snapshot_id: {metadata}}

    def create_snapshot(self, file_path: str) -> Any:
        """
        Crea snapshot de un archivo antes de modificarlo

        Returns:
            str: snapshot_id único
        """
        try:
            # Generate snapshot ID
            timestamp = datetime.now().isoformat()
            content_hash = hashlib.sha256(file_path.encode()).hexdigest()[:8]
            snapshot_id = f"snap_{content_hash}_{int(datetime.now().timestamp())}"

            # Save snapshot metadata
            self.snapshots[snapshot_id] = {
                'file_path': file_path,
                'timestamp': timestamp,
                'status': 'created'
            }

            # Si el archivo existe, guardamos su contenido
            if os.path.exists(file_path):
                snapshot_file = self.snapshots_dir / f"{snapshot_id}.snap"
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                with open(snapshot_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        'file_path': file_path,
                        'timestamp': timestamp,
                        'content': content
                    }, f)

            return snapshot_id

        except Exception as e:
            print(f"⚠️ Snapshot creation failed: {e}")
            return None

    def rollback(self, snapshot_id: str) -> int:
        """
        Revierte cambios usando un snapshot

        Returns:
            bool: True si rollback exitoso
        """
        if snapshot_id not in self.snapshots:
            return False

        try:
            snapshot_file = self.snapshots_dir / f"{snapshot_id}.snap"

            if not snapshot_file.exists():
                return False

            with open(snapshot_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Restore file content
            file_path = data['file_path']
            content = data['content']

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            self.snapshots[snapshot_id]['status'] = 'restored'
            return True

        except Exception as e:
            print(f"⚠️ Rollback failed: {e}")
            return False

    def list_snapshots(self) -> Any:
        """Lista todos los snapshots disponibles"""
        return list(self.snapshots.keys())

    def get_snapshot_info(self, snapshot_id: str) -> Any:
        """Obtiene información de un snapshot"""
        return self.snapshots.get(snapshot_id, {})
