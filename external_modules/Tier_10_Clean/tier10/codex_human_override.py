from typing import Any


# -*- coding: utf-8 -*-
"""
TIER 10 - Human Override
=========================
Sistema de aprobación humana para cambios críticos

Advanced Code Governance & Refactoring System
Date: December 6, 2025
"""

from datetime import datetime

class HumanOverride:
    """Requiere aprobación humana para cambios de alto impacto"""

    def __init__(self) -> None:
        self.auto_approve_threshold = 0.30  # Ganancia estimada < 30% -> auto-approve
        self.pending_approvals = {}
        self.approval_history = []

    # TODO: REFACTOR - Función muy larga (54 líneas). Dividir en funciones más pequeñas.
    def request_approval(self, change_description: str, estimated_gain: Any, change_metadata: Any = None) -> Any:
        """
        Solicita aprobación humana para un cambio

        Args:
            change_description (str): Descripción del cambio
            estimated_gain (float): Ganancia estimada (0.0 - 1.0)
            change_metadata (dict): Metadata adicional del cambio

        Returns:
            dict: {
                'approval_id': str,
                'status': 'auto_approved' | 'pending' | 'approved' | 'rejected',
                'requires_human': bool
            }
        """
        change_metadata = change_metadata or {}
        approval_id = f"APR_{int(datetime.now().timestamp())}"

        # Auto-approve low-impact changes
        if estimated_gain < self.auto_approve_threshold:
            result = {
                'approval_id': approval_id,
                'status': 'auto_approved',
                'requires_human': False,
                'reason': f'Low impact (gain={estimated_gain:.2f} < threshold={self.auto_approve_threshold})'
            }

            self.approval_history.append({
                'approval_id': approval_id,
                'timestamp': datetime.now().isoformat(),
                'description': change_description,
                'estimated_gain': estimated_gain,
                'status': 'auto_approved'
            })

            return result

        # High-impact changes require human approval
        else:
            self.pending_approvals[approval_id] = {
                'timestamp': datetime.now().isoformat(),
                'description': change_description,
                'estimated_gain': estimated_gain,
                'metadata': change_metadata or {},
                'status': 'pending'
            }

            result = {
                'approval_id': approval_id,
                'status': 'pending',
                'requires_human': True,
                'reason': f'High impact (gain={estimated_gain:.2f} >= threshold={self.auto_approve_threshold})'
            }

            return result

    def approve(self, approval_id: str) -> int:
        """Aprueba un cambio pendiente (simulado)"""
        if approval_id not in self.pending_approvals:
            return False

        self.pending_approvals[approval_id]['status'] = 'approved'
        self.approval_history.append(self.pending_approvals[approval_id])
        del self.pending_approvals[approval_id]

        return True

    def reject(self, approval_id: str, reason: Any) -> int:
        """Rechaza un cambio pendiente"""
        if approval_id not in self.pending_approvals:
            return False

        self.pending_approvals[approval_id]['status'] = 'rejected'
        self.pending_approvals[approval_id]['rejection_reason'] = reason
        self.approval_history.append(self.pending_approvals[approval_id])
        del self.pending_approvals[approval_id]

        return True

    def get_pending(self) -> Any:
        """Retorna lista de aprobaciones pendientes"""
        return list(self.pending_approvals.values())

    def get_history(self) -> Any:
        """Retorna historial de aprobaciones"""
        return self.approval_history
