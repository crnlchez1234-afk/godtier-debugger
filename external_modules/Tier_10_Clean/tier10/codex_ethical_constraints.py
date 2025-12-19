from typing import Any, Tuple


# -*- coding: utf-8 -*-
"""
TIER 10 - Ethical Constraints
==============================
Validación ética de cambios auto-generados

Advanced Code Governance & Refactoring System
Date: December 6, 2025
"""


class EthicalConstraints:
    """Valida que los cambios sean éticos y seguros"""

    def __init__(self) -> None:
        self.ethical_weights = {
            'safety': 0.30,         # Seguridad del sistema
            'transparency': 0.25,   # Transparencia del código
            'reversibility': 0.20,  # Facilidad de revertir
            'user_benefit': 0.15,   # Beneficio al usuario
            'simplicity': 0.10      # Simplicidad vs complejidad
        }

    def check_ethical_compliance(self, change_request: Any) -> Tuple:
        """
        Evalúa compliance ético de un cambio

        Returns:
            tuple: (compliant: bool, violations: list, ethical_score: float)
        """
        violations = []
        scores = {}

        # SAFETY CHECK
        safety_score = self._check_safety(change_request)
        scores['safety'] = safety_score
        if safety_score < 0.50:
            violations.append(f"⚠️ SAFETY: Score {safety_score:.2f} below threshold 0.50")

        # TRANSPARENCY CHECK
        transparency_score = self._check_transparency(change_request)
        scores['transparency'] = transparency_score
        if transparency_score < 0.60:
            violations.append(f"⚠️ TRANSPARENCY: Insufficient documentation")

        # REVERSIBILITY CHECK
        reversibility_score = self._check_reversibility(change_request)
        scores['reversibility'] = reversibility_score

        # USER BENEFIT CHECK
        benefit_score = self._check_user_benefit(change_request)
        scores['user_benefit'] = benefit_score

        # SIMPLICITY CHECK
        simplicity_score = self._check_simplicity(change_request)
        scores['simplicity'] = simplicity_score

        # Calculate weighted ethical score
        ethical_score = sum(
            scores[dimension] * weight
            for dimension, weight in self.ethical_weights.items()
        )

        # CRITICAL FIX: Reject if safety score is critically low (multiple dangers)
        if scores.get('safety', 1.0) == 0.0:
            violations.append(f"🔥 CRITICAL SAFETY: Multiple dangerous patterns detected")
            compliant = False
        else:
            compliant = (ethical_score >= 0.70 and len(violations) == 0)

        return compliant, violations, ethical_score

    def _check_safety(self, change: Any) -> float:
        """Evalúa seguridad del cambio"""
        code = change.get('modified_code', '')

        # Dangerous patterns reduce safety
        dangerous = ['eval(', 'exec(', '__import__', 'os.system', 'subprocess']
        danger_count = sum(1 for pattern in dangerous if pattern in code)

        # CRITICAL FIX: Multiple dangers = complete rejection
        if danger_count >= 2:
            return 0.0  # Complete rejection for multiple dangers
        elif danger_count == 1:
            return 0.20  # Very unsafe

        # Safe patterns increase score
        safe_patterns = ['@lru_cache', 'if cache:', 'try:', 'except:', 'logging.']
        safe_count = sum(1 for pattern in safe_patterns if pattern in code)

        return min(1.0, 0.70 + (safe_count * 0.10))

    def _check_transparency(self, change: Any) -> float:
        """Evalúa transparencia (documentación, claridad)"""
        reasoning = change.get('reasoning', '')
        description = change.get('change_description', '')

        # Good documentation
        if len(reasoning) > 50 and len(description) > 20:
            return 0.90
        elif len(reasoning) > 20:
            return 0.70
        else:
            return 0.40

    def _check_reversibility(self, change: Any) -> float:
        """Evalúa facilidad de revertir el cambio"""
        change_type = change.get('change_type', '')

        # Reversible changes
        if change_type in ['optimize', 'refactor', 'documentation']:
            return 0.90
        elif change_type in ['bugfix']:
            return 0.75
        else:
            return 0.50

    def _check_user_benefit(self, change: Any) -> Any:
        """Evalúa beneficio al usuario"""
        reasoning = change.get('reasoning', '').lower()

        # Keywords indicating user benefit
        benefit_keywords = ['improve', 'faster', 'performance', 'reduce', 'optimize']
        benefit_count = sum(1 for kw in benefit_keywords if kw in reasoning)

        return min(1.0, 0.50 + (benefit_count * 0.15))

    def _check_simplicity(self, change: Any) -> float:
        """Evalúa simplicidad vs complejidad añadida"""
        original = change.get('original_code', '')
        modified = change.get('modified_code', '')

        # Simple changes preferred
        lines_added = len(modified.split('\n')) - len(original.split('\n'))

        if lines_added <= 3:
            return 0.90
        elif lines_added <= 10:
            return 0.70
        else:
            return 0.50
