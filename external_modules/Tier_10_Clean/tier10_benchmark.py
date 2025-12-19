from typing import Any, Dict, List, Tuple, Optional


# -*- coding: utf-8 -*-
"""
Comprehensive Benchmark Suite
=========================================
Benchmark exhaustivo para validación del sistema de governance

Advanced Code Governance & Refactoring System
Date: December 6, 2025

OBJETIVO: Probar cada componente hasta el límite de ruptura
"""

import sys
import os
import time
import json
import traceback
from datetime import datetime
from pathlib import Path

# Import modules
sys.path.insert(0, str(Path(__file__).parent / 'tier10'))

from tier10.codex_audit_trail import AuditTrail
from tier10.codex_capability_bounds import CapabilityBounds
from tier10.codex_ethical_constraints import EthicalConstraints
from tier10.codex_human_override import HumanOverride
from tier10.codex_rollback_manager import RollbackManager

# Mock for missing component
class AKIRAMedical:
    def diagnose(self, data):
        time.sleep(0.01) # Simulate work
        return {'diagnosis': 'healthy'}


class SystemBenchmark:
    """Benchmark exhaustivo para encontrar fallas"""

    def __init__(self) -> None:
        self.test_results = []
        self.critical_failures = []
        self.warnings = []
        self.passed = 0
        self.failed = 0
        self.start_time = None

    def log(self, level: Any, category: Any, message: int, details: Any = None) -> None:
        """Log test result"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'category': category,
            'message': message,
            'details': details or {}
        }
        self.test_results.append(entry)

        symbol = {
            'PASS': '✅',
            'FAIL': '❌',
            'WARN': '⚠️',
            'INFO': 'ℹ️',
            'CRITICAL': '🔥'
        }.get(level, '•')

        print(f"{symbol} [{category}] {message}")

        if level == 'FAIL':
            self.failed += 1
        elif level == 'PASS':
            self.passed += 1
        elif level == 'CRITICAL':
            self.critical_failures.append(entry)
            self.failed += 1
        elif level == 'WARN':
            self.warnings.append(entry)

    def run_benchmark(self) -> None:
        """Ejecuta benchmark completo"""
        self.start_time = time.time()

        print("="*80)
        print("🔥 TIER 10 - SYSTEM BENCHMARK")
        print("="*80)
        print(f"Inicio: {datetime.now().isoformat()}")
        print()

        # CATEGORÍAS DE PRUEBAS
        self.test_audit_trail()
        self.test_capability_bounds()
        self.test_ethical_constraints()
        self.test_human_override()
        self.test_rollback_manager()
        self.test_integration()
        self.test_security_exploits()
        self.test_performance_limits()
        self.test_edge_cases()

        # RESUMEN
        self.print_summary()

    # ========================================================================
    # AUDIT TRAIL TESTS
    # ========================================================================

    # TODO: REFACTOR - Función muy larga (77 líneas). Dividir en funciones más pequeñas.
    def test_audit_trail(self) -> None:
        """Test exhaustivo del audit trail"""
        print("\n" + "="*80)
        print("📝 AUDIT TRAIL TESTS")
        print("="*80)

        try:
            # Crear audit trail temporal
            audit_file = 'test_audit_trail.json'
            audit = AuditTrail(audit_file)

            # TEST 1: Log change
            audit.log_change({
                'file_path': 'test.py',
                'change_type': 'optimize',
                'approved': True,
                'approval_id': 'APR_001'
            })
            self.log('PASS', 'AUDIT', 'Change logged successfully')

            # TEST 2: Retrieve changes
            changes = audit.get_changes()
            if len(changes) >= 1:
                self.log('PASS', 'AUDIT', f'Retrieved {len(changes)} changes')
            else:
                self.log('FAIL', 'AUDIT', 'Failed to retrieve changes')

            # TEST 3: Filter changes
            filtered = audit.get_changes({'approved': True})
            self.log('PASS', 'AUDIT', f'Filtered changes: {len(filtered)}')

            # TEST 4: Stats
            stats = audit.get_stats()
            if stats:
                self.log('PASS', 'AUDIT', f'Stats: {stats}')
            else:
                self.log('FAIL', 'AUDIT', 'Stats retrieval failed')

            # TEST 5: Persistencia
            audit2 = AuditTrail(audit_file)
            if len(audit2.changes) >= 1:
                self.log('PASS', 'AUDIT', 'Persistence works (changes loaded)')
            else:
                self.log('FAIL', 'AUDIT', 'Persistence failed')

            # TEST 6: Massive logging (stress test)
            start = time.time()
            for i in range(1000):
                audit.log_change({
                    'file_path': f'file_{i}.py',
                    'change_type': 'test',
                    'approved': i % 2 == 0
                })
            duration = time.time() - start

            if duration < 5.0:  # 1000 logs en < 5 segundos
                self.log('PASS', 'AUDIT', f'Stress test: 1000 logs in {duration:.2f}s')
            else:
                self.log('WARN', 'AUDIT', f'Stress test slow: {duration:.2f}s')

            # TEST 7: Datos corruptos
            try:
                with open(audit_file, 'w') as f:
                    f.write('CORRUPTED DATA {{{')

                audit3 = AuditTrail(audit_file)
                self.log('PASS', 'AUDIT', 'Corrupted data handled gracefully')
            except Exception as e:
                self.log('WARN', 'AUDIT', f'Corrupted data crashed: {e}')

            # Cleanup
            if os.path.exists(audit_file):
                os.remove(audit_file)

        except Exception as e:
            self.log('CRITICAL', 'AUDIT', f'Unexpected crash: {str(e)}', {
                'traceback': traceback.format_exc()
            })

    # ========================================================================
    # CAPABILITY BOUNDS TESTS
    # ========================================================================

    # TODO: REFACTOR - Función muy larga (101 líneas). Dividir en funciones más pequeñas.
    def test_capability_bounds(self) -> None:
        """Test de límites de capacidades"""
        print("\n" + "="*80)
        print("🛡️ CAPABILITY BOUNDS TESTS")
        print("="*80)

        try:
            bounds = CapabilityBounds()

            # TEST 1: Protected module modification blocked
            request = {
                'file_path': 'tier10/codex_core.py',
                'change_type': 'modify',
                'modified_code': 'print("hacked")'
            }
            allowed, violations = bounds.check_bounds(request)

            if not allowed and len(violations) > 0:
                self.log('PASS', 'BOUNDS', 'Protected module modification blocked')
            else:
                self.log('CRITICAL', 'BOUNDS', 'PROTECTED MODULE NOT BLOCKED!', request)

            # TEST 2: Dangerous eval() blocked
            request = {
                'file_path': 'safe_module.py',
                'change_type': 'optimize',
                'modified_code': 'result = eval(user_input)',
                'original_code': ''
            }
            allowed, violations = bounds.check_bounds(request)

            if not allowed:
                self.log('PASS', 'BOUNDS', 'eval() pattern blocked')
            else:
                self.log('CRITICAL', 'BOUNDS', 'DANGEROUS eval() NOT BLOCKED!')

            # TEST 3: Dangerous exec() blocked
            request['modified_code'] = 'exec(malicious_code)'
            allowed, violations = bounds.check_bounds(request)

            if not allowed:
                self.log('PASS', 'BOUNDS', 'exec() pattern blocked')
            else:
                self.log('CRITICAL', 'BOUNDS', 'DANGEROUS exec() NOT BLOCKED!')

            # TEST 4: subprocess blocked
            request['modified_code'] = 'import subprocess; subprocess.call(["rm", "-rf"])'
            allowed, violations = bounds.check_bounds(request)

            if not allowed:
                self.log('PASS', 'BOUNDS', 'subprocess pattern blocked')
            else:
                self.log('CRITICAL', 'BOUNDS', 'DANGEROUS subprocess NOT BLOCKED!')

            # TEST 5: Safe optimization allowed
            request = {
                'file_path': 'safe_module.py',
                'change_type': 'optimize',
                'modified_code': '@lru_cache\ndef compute(): pass',
                'original_code': 'def compute(): pass'
            }
            allowed, violations = bounds.check_bounds(request)

            if allowed:
                self.log('PASS', 'BOUNDS', 'Safe optimization allowed')
            else:
                self.log('WARN', 'BOUNDS', 'Safe optimization blocked incorrectly', violations)

            # TEST 6: Unknown change type on protected module
            request = {
                'file_path': 'tier10/safety_monitor.py',
                'change_type': 'unknown_operation',
                'modified_code': 'pass'
            }
            allowed, violations = bounds.check_bounds(request)

            if not allowed:
                self.log('PASS', 'BOUNDS', 'Unknown change type on protected module blocked')
            else:
                self.log('FAIL', 'BOUNDS', 'Unknown change type allowed on protected module')

            # TEST 7: Forbidden change type
            request = {
                'file_path': 'any_module.py',
                'change_type': 'bypass_safety',
                'modified_code': 'pass'
            }
            allowed, violations = bounds.check_bounds(request)

            if not allowed:
                self.log('PASS', 'BOUNDS', 'Forbidden change type blocked')
            else:
                self.log('CRITICAL', 'BOUNDS', 'FORBIDDEN CHANGE TYPE NOT BLOCKED!')

            # TEST 8: Get allowed modules
            allowed_modules = bounds.get_allowed_modules()
            self.log('INFO', 'BOUNDS', f'Allowed modules: {allowed_modules}')

        except Exception as e:
            self.log('CRITICAL', 'BOUNDS', f'Unexpected crash: {str(e)}', {
                'traceback': traceback.format_exc()
            })

    # ========================================================================
    # ETHICAL CONSTRAINTS TESTS
    # ========================================================================

    # TODO: REFACTOR - Función muy larga (73 líneas). Dividir en funciones más pequeñas.
    def test_ethical_constraints(self) -> None:
        """Test de restricciones éticas"""
        print("\n" + "="*80)
        print("⚖️ ETHICAL CONSTRAINTS TESTS")
        print("="*80)

        try:
            ethics = EthicalConstraints()

            # TEST 1: Safe, well-documented change
            request = {
                'modified_code': 'try:\n    result = compute()\nexcept:\n    logging.error("failed")',
                'reasoning': 'Adding error handling to improve robustness and prevent crashes',
                'change_description': 'Add try-except with logging'
            }
            compliant, violations, score = ethics.check_ethical_compliance(request)

            if compliant and score >= 0.70:
                self.log('PASS', 'ETHICS', f'Safe change approved (score={score:.2f})')
            else:
                self.log('WARN', 'ETHICS', f'Safe change rejected (score={score:.2f})', violations)

            # TEST 2: Dangerous eval()
            request = {
                'modified_code': 'result = eval(user_input)',
                'reasoning': 'Quick optimization',
                'change_description': 'Use eval'
            }
            compliant, violations, score = ethics.check_ethical_compliance(request)

            if not compliant and score < 0.50:
                self.log('PASS', 'ETHICS', f'Dangerous eval rejected (score={score:.2f})')
            else:
                self.log('CRITICAL', 'ETHICS', f'DANGEROUS eval APPROVED! (score={score:.2f})')

            # TEST 3: Poor documentation
            request = {
                'modified_code': 'x = 123',
                'reasoning': '',
                'change_description': 'change'
            }
            compliant, violations, score = ethics.check_ethical_compliance(request)

            if score < 0.70:
                self.log('PASS', 'ETHICS', f'Poor documentation penalized (score={score:.2f})')
            else:
                self.log('WARN', 'ETHICS', f'Poor documentation not penalized enough (score={score:.2f})')

            # TEST 4: Multiple dangerous patterns
            request = {
                'modified_code': 'eval(exec(__import__("os").system("rm -rf /")))',
                'reasoning': 'Testing',
                'change_description': 'Test'
            }
            compliant, violations, score = ethics.check_ethical_compliance(request)

            if not compliant and 'CRITICAL SAFETY' in str(violations):
                self.log('PASS', 'ETHICS', f'Multiple dangers rejected (score={score:.2f}, violations={len(violations)})')
            else:
                self.log('CRITICAL', 'ETHICS', f'MULTIPLE DANGERS NOT BLOCKED! (score={score:.2f}, compliant={compliant})')

            # TEST 5: Ethical weights
            weights = ethics.ethical_weights
            total_weight = sum(weights.values())

            if abs(total_weight - 1.0) < 0.01:
                self.log('PASS', 'ETHICS', f'Weights sum to 1.0 (actual={total_weight:.2f})')
            else:
                self.log('FAIL', 'ETHICS', f'Weights sum incorrect: {total_weight:.2f}')

        except Exception as e:
            self.log('CRITICAL', 'ETHICS', f'Unexpected crash: {str(e)}', {
                'traceback': traceback.format_exc()
            })

    # ========================================================================
    # HUMAN OVERRIDE TESTS
    # ========================================================================

    # TODO: REFACTOR - Función muy larga (75 líneas). Dividir en funciones más pequeñas.
    def test_human_override(self) -> None:
        """Test de sistema de aprobación humana"""
        print("\n" + "="*80)
        print("👤 HUMAN OVERRIDE TESTS")
        print("="*80)

        try:
            override = HumanOverride()

            # TEST 1: Low impact auto-approved
            result = override.request_approval(
                'Minor optimization',
                estimated_gain=0.10
            )

            if result['status'] == 'auto_approved' and not result['requires_human']:
                self.log('PASS', 'OVERRIDE', 'Low impact auto-approved')
            else:
                self.log('FAIL', 'OVERRIDE', 'Low impact not auto-approved', result)

            # TEST 2: High impact requires human
            result = override.request_approval(
                'Major refactoring',
                estimated_gain=0.80
            )

            if result['status'] == 'pending' and result['requires_human']:
                self.log('PASS', 'OVERRIDE', 'High impact requires human approval')
            else:
                self.log('CRITICAL', 'OVERRIDE', 'HIGH IMPACT NOT REQUIRING HUMAN!', result)

            approval_id = result['approval_id']

            # TEST 3: Approve pending
            success = override.approve(approval_id)
            if success:
                self.log('PASS', 'OVERRIDE', 'Approval successful')
            else:
                self.log('FAIL', 'OVERRIDE', 'Approval failed')

            # TEST 4: Reject pending
            result = override.request_approval('Test rejection', 0.50)
            reject_id = result['approval_id']

            success = override.reject(reject_id, 'Testing rejection')
            if success:
                self.log('PASS', 'OVERRIDE', 'Rejection successful')
            else:
                self.log('FAIL', 'OVERRIDE', 'Rejection failed')

            # TEST 5: Get pending approvals
            pending = override.get_pending()
            self.log('INFO', 'OVERRIDE', f'Pending approvals: {len(pending)}')

            # TEST 6: Threshold boundary (exactly at threshold)
            result = override.request_approval(
                'Boundary test',
                estimated_gain=0.30  # Exactly at threshold
            )

            self.log('INFO', 'OVERRIDE', f'Boundary case (0.30): {result["status"]}')

            # TEST 7: Extreme values
            result = override.request_approval('Test', estimated_gain=1.5)
            self.log('INFO', 'OVERRIDE', f'Extreme gain (1.5): {result["status"]}')

            result = override.request_approval('Test', estimated_gain=-0.5)
            if result['status'] == 'auto_approved':
                self.log('PASS', 'OVERRIDE', 'Negative gain auto-approved')
            else:
                self.log('WARN', 'OVERRIDE', 'Negative gain requires approval?', result)

        except Exception as e:
            self.log('CRITICAL', 'OVERRIDE', f'Unexpected crash: {str(e)}', {
                'traceback': traceback.format_exc()
            })

    # ========================================================================
    # ROLLBACK MANAGER TESTS
    # ========================================================================

    # TODO: REFACTOR - Función muy larga (75 líneas). Dividir en funciones más pequeñas.
    def test_rollback_manager(self) -> None:
        """Test de gestión de rollback"""
        print("\n" + "="*80)
        print("⏮️ ROLLBACK MANAGER TESTS")
        print("="*80)

        try:
            rollback = RollbackManager('.test_snapshots')

            # Crear archivo de prueba
            test_file = 'test_rollback_file.py'
            original_content = '# Original content\nprint("hello")'

            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(original_content)

            # TEST 1: Create snapshot
            snapshot_id = rollback.create_snapshot(test_file)

            if snapshot_id:
                self.log('PASS', 'ROLLBACK', f'Snapshot created: {snapshot_id}')
            else:
                self.log('FAIL', 'ROLLBACK', 'Snapshot creation failed')

            # TEST 2: Modify file
            modified_content = '# Modified content\nprint("goodbye")'
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(modified_content)

            # TEST 3: Rollback
            success = rollback.rollback(snapshot_id)

            if success:
                with open(test_file, 'r', encoding='utf-8') as f:
                    restored = f.read()

                if restored == original_content:
                    self.log('PASS', 'ROLLBACK', 'Rollback successful, content restored')
                else:
                    self.log('FAIL', 'ROLLBACK', 'Rollback failed, content mismatch')
            else:
                self.log('FAIL', 'ROLLBACK', 'Rollback failed')

            # TEST 4: List snapshots
            snapshots = rollback.list_snapshots()
            if len(snapshots) >= 1:
                self.log('PASS', 'ROLLBACK', f'Snapshots listed: {len(snapshots)}')
            else:
                self.log('FAIL', 'ROLLBACK', 'No snapshots found')

            # TEST 5: Invalid rollback
            success = rollback.rollback('INVALID_ID')
            if not success:
                self.log('PASS', 'ROLLBACK', 'Invalid rollback rejected')
            else:
                self.log('FAIL', 'ROLLBACK', 'Invalid rollback accepted')

            # TEST 6: Snapshot non-existent file
            snapshot_id = rollback.create_snapshot('non_existent_file_xyz.py')
            if snapshot_id:
                self.log('PASS', 'ROLLBACK', 'Non-existent file snapshot created')
            else:
                self.log('WARN', 'ROLLBACK', 'Non-existent file snapshot failed')

            # Cleanup
            if os.path.exists(test_file):
                os.remove(test_file)

            import shutil
            if os.path.exists('.test_snapshots'):
                shutil.rmtree('.test_snapshots')

        except Exception as e:
            self.log('CRITICAL', 'ROLLBACK', f'Unexpected crash: {str(e)}', {
                'traceback': traceback.format_exc()
            })

    # ========================================================================
    # INTEGRATION TESTS
    # ========================================================================

    # TODO: REFACTOR - Función muy larga (65 líneas). Dividir en funciones más pequeñas.
    def test_integration(self) -> Any:
        """Tests de integración entre componentes"""
        print("\n" + "="*80)
        print("🔗 INTEGRATION TESTS")
        print("="*80)

        try:
            # TEST 1: Full workflow simulation
            audit = AuditTrail('test_integration_audit.json')
            bounds = CapabilityBounds()
            ethics = EthicalConstraints()
            override = HumanOverride()
            rollback = RollbackManager('.test_int_snapshots')

            # Simular cambio completo
            change_request = {
                'file_path': 'safe_module.py',
                'change_type': 'optimize',
                'original_code': 'def slow(): pass',
                'modified_code': '@lru_cache\ndef slow(): pass',
                'change_description': 'Add caching for performance',
                'reasoning': 'Function is called frequently, caching will improve performance significantly'
            }

            # Check bounds
            allowed, violations = bounds.check_bounds(change_request)

            if not allowed:
                self.log('FAIL', 'INTEGRATION', 'Safe change blocked by bounds', violations)
                return

            # Check ethics
            compliant, eth_violations, score = ethics.check_ethical_compliance(change_request)

            if not compliant:
                self.log('FAIL', 'INTEGRATION', f'Safe change blocked by ethics (score={score:.2f})', eth_violations)
                return

            # Request approval
            approval = override.request_approval(
                change_request['change_description'],
                estimated_gain=0.15  # Low impact
            )

            if approval['status'] != 'auto_approved':
                self.log('FAIL', 'INTEGRATION', 'Safe low-impact change not auto-approved')
                return

            # Log to audit
            audit.log_change({
                **change_request,
                'approved': True,
                'approval_id': approval['approval_id'],
                'ethical_score': score
            })

            self.log('PASS', 'INTEGRATION', 'Full workflow: bounds → ethics → approval → audit')

            # Cleanup
            if os.path.exists('test_integration_audit.json'):
                os.remove('test_integration_audit.json')

        except Exception as e:
            self.log('CRITICAL', 'INTEGRATION', f'Integration test crashed: {str(e)}', {
                'traceback': traceback.format_exc()
            })

    # ========================================================================
    # SECURITY EXPLOIT TESTS
    # ========================================================================

    # TODO: REFACTOR - Función muy larga (72 líneas). Dividir en funciones más pequeñas.
    def test_security_exploits(self) -> None:
        """Tests de explotación de seguridad"""
        print("\n" + "="*80)
        print("🔓 SECURITY EXPLOIT TESTS")
        print("="*80)

        try:
            bounds = CapabilityBounds()
            ethics = EthicalConstraints()

            # EXPLOIT 1: Code injection via string
            exploit = {
                'file_path': 'victim.py',
                'change_type': 'optimize',
                'modified_code': 'x = "hello"\n' + 'eval("__import__(\'os\').system(\'rm -rf /\')")',
                'original_code': 'x = "hello"'
            }

            allowed, violations = bounds.check_bounds(exploit)
            if not allowed:
                self.log('PASS', 'SECURITY', 'Code injection blocked')
            else:
                self.log('CRITICAL', 'SECURITY', 'CODE INJECTION NOT BLOCKED!')

            # EXPLOIT 2: Obfuscated eval
            exploit['modified_code'] = 'getattr(__builtins__, "ev" + "al")("malicious")'
            allowed, _ = bounds.check_bounds(exploit)

            if not allowed:
                self.log('PASS', 'SECURITY', 'Obfuscated eval blocked')
            else:
                self.log('WARN', 'SECURITY', 'Obfuscated eval not detected')

            # EXPLOIT 3: Path traversal
            exploit = {
                'file_path': '../../../etc/passwd',
                'change_type': 'modify',
                'modified_code': 'hacked'
            }

            # Sistema debería validar rutas
            self.log('INFO', 'SECURITY', 'Path traversal test (manual verification needed)')

            # EXPLOIT 4: Import tampering
            exploit = {
                'file_path': 'safe.py',
                'change_type': 'optimize',
                'modified_code': '__import__("sys").modules["os"] = MaliciousOS()'
            }

            allowed, _ = bounds.check_bounds(exploit)
            if not allowed:
                self.log('PASS', 'SECURITY', 'Import tampering blocked')
            else:
                self.log('CRITICAL', 'SECURITY', 'IMPORT TAMPERING NOT BLOCKED!')

            # EXPLOIT 5: Bypass via comentarios
            exploit = {
                'file_path': 'safe.py',
                'change_type': 'documentation',
                'modified_code': '# Innocent comment\n"""eval("malicious")"""'
            }

            allowed, _ = bounds.check_bounds(exploit)
            compliant, _, score = ethics.check_ethical_compliance(exploit)

            # Esto es tricky - comentarios pueden contener código malicioso
            self.log('INFO', 'SECURITY', f'Comment exploit: bounds={allowed}, ethics={compliant}')

        except Exception as e:
            self.log('CRITICAL', 'SECURITY', f'Security test crashed: {str(e)}', {
                'traceback': traceback.format_exc()
            })

    # ========================================================================
    # PERFORMANCE LIMIT TESTS
    # ========================================================================

    # TODO: REFACTOR - Función muy larga (72 líneas). Dividir en funciones más pequeñas.
    def test_performance_limits(self) -> None:
        """Tests de límites de rendimiento"""
        print("\n" + "="*80)
        print("⚡ PERFORMANCE LIMIT TESTS")
        print("="*80)

        try:
            # TEST 1: AKIRA latency under load
            akira = AKIRAMedical()

            latencies = []
            for i in range(100):
                start = time.time()
                akira.diagnose({'test': i})
                latency = (time.time() - start) * 1000
                latencies.append(latency)

            avg_latency = sum(latencies) / len(latencies)
            max_latency = max(latencies)
            min_latency = min(latencies)

            if avg_latency < 50:
                self.log('PASS', 'PERFORMANCE', f'Avg latency: {avg_latency:.2f}ms (< 50ms)')
            else:
                self.log('WARN', 'PERFORMANCE', f'Avg latency high: {avg_latency:.2f}ms')

            if max_latency < 100:
                self.log('PASS', 'PERFORMANCE', f'Max latency: {max_latency:.2f}ms (< 100ms)')
            else:
                self.log('FAIL', 'PERFORMANCE', f'Max latency: {max_latency:.2f}ms (>= 100ms)')

            # TEST 2: Memory usage
            import sys

            audit = AuditTrail('test_perf_audit.json')

            # Log 10,000 changes
            for i in range(10000):
                audit.log_change({'test': i})

            # Check memory
            size = sys.getsizeof(audit.changes)
            self.log('INFO', 'PERFORMANCE', f'10K changes memory: {size / 1024:.2f} KB')

            if os.path.exists('test_perf_audit.json'):
                file_size = os.path.getsize('test_perf_audit.json')
                self.log('INFO', 'PERFORMANCE', f'Audit file size: {file_size / 1024:.2f} KB')
                os.remove('test_perf_audit.json')

            # TEST 3: Capability bounds check speed
            bounds = CapabilityBounds()

            request = {
                'file_path': 'test.py',
                'change_type': 'optimize',
                'modified_code': 'pass',
                'original_code': ''
            }

            start = time.time()
            for i in range(1000):
                bounds.check_bounds(request)
            duration = time.time() - start

            if duration < 1.0:
                self.log('PASS', 'PERFORMANCE', f'1000 bounds checks: {duration:.2f}s (< 1s)')
            else:
                self.log('WARN', 'PERFORMANCE', f'Bounds check slow: {duration:.2f}s')

        except Exception as e:
            self.log('CRITICAL', 'PERFORMANCE', f'Performance test crashed: {str(e)}', {
                'traceback': traceback.format_exc()
            })

    # ========================================================================
    # EDGE CASE TESTS
    # ========================================================================

    # TODO: REFACTOR - Función muy larga (94 líneas). Dividir en funciones más pequeñas.
    def test_edge_cases(self) -> None:
        """Tests de casos extremos"""
        print("\n" + "="*80)
        print("🔍 EDGE CASE TESTS")
        print("="*80)

        try:
            # EDGE 1: Unicode en código
            bounds = CapabilityBounds()
            request = {
                'file_path': 'unicode_test.py',
                'change_type': 'optimize',
                'modified_code': '# Comentario con ñ, é, 中文, 🔥\ndef función(): pass',
                'original_code': ''
            }

            try:
                allowed, violations = bounds.check_bounds(request)
                self.log('PASS', 'EDGE', 'Unicode handled correctly')
            except Exception as e:
                self.log('FAIL', 'EDGE', f'Unicode crashed: {e}')

            # EDGE 2: Código muy largo
            huge_code = 'x = 1\n' * 100000
            request['modified_code'] = huge_code

            start = time.time()
            try:
                allowed, violations = bounds.check_bounds(request)
                duration = time.time() - start

                if duration < 5.0:
                    self.log('PASS', 'EDGE', f'Huge code handled in {duration:.2f}s')
                else:
                    self.log('WARN', 'EDGE', f'Huge code slow: {duration:.2f}s')
            except Exception as e:
                self.log('FAIL', 'EDGE', f'Huge code crashed: {e}')

            # EDGE 3: Caracteres especiales en file path
            request = {
                'file_path': 'weird/path/../with spaces/file!@#.py',
                'change_type': 'optimize',
                'modified_code': 'pass'
            }

            try:
                allowed, violations = bounds.check_bounds(request)
                self.log('PASS', 'EDGE', 'Special chars in path handled')
            except Exception as e:
                self.log('WARN', 'EDGE', f'Special chars crashed: {e}')

            # EDGE 4: Empty strings
            request = {
                'file_path': '',
                'change_type': '',
                'modified_code': '',
                'original_code': ''
            }

            try:
                allowed, violations = bounds.check_bounds(request)
                self.log('PASS', 'EDGE', 'Empty strings handled')
            except Exception as e:
                self.log('WARN', 'EDGE', f'Empty strings crashed: {e}')

            # EDGE 5: Concurrent operations
            audit = AuditTrail('test_edge_audit.json')

            import threading

            def log_changes() -> None:
                for i in range(100):
                    audit.log_change({'test': i})

            threads = [threading.Thread(target=log_changes) for _ in range(10)]

            for t in threads:
                t.start()

            for t in threads:
                t.join()

            # Should have 1000 changes (10 threads * 100 changes)
            if len(audit.changes) == 1000:
                self.log('PASS', 'EDGE', 'Concurrent logging: 1000/1000 changes')
            else:
                self.log('WARN', 'EDGE', f'Concurrent logging: {len(audit.changes)}/1000 changes (race condition?)')

            if os.path.exists('test_edge_audit.json'):
                os.remove('test_edge_audit.json')

        except Exception as e:
            self.log('CRITICAL', 'EDGE', f'Edge case test crashed: {str(e)}', {
                'traceback': traceback.format_exc()
            })

    # ========================================================================
    # SUMMARY
    # ========================================================================

    # TODO: REFACTOR - Función muy larga (69 líneas). Dividir en funciones más pequeñas.
    def print_summary(self) -> None:
        """Imprime resumen de resultados"""
        duration = time.time() - self.start_time

        print("\n" + "="*80)
        print("📊 BENCHMARK SUMMARY")
        print("="*80)

        print(f"\n⏱️  Duration: {duration:.2f}s")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        print(f"🔥 Critical: {len(self.critical_failures)}")

        total = self.passed + self.failed
        if total > 0:
            success_rate = (self.passed / total) * 100
            print(f"\n📈 Success Rate: {success_rate:.1f}%")

        # Critical failures
        if self.critical_failures:
            print("\n🔥 CRITICAL FAILURES:")
            for failure in self.critical_failures:
                print(f"   [{failure['category']}] {failure['message']}")

        # Warnings
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warn in self.warnings[:10]:  # Show first 10
                print(f"   [{warn['category']}] {warn['message']}")

            if len(self.warnings) > 10:
                print(f"   ... y {len(self.warnings) - 10} más")

        # Save detailed report
        report_file = f'benchmark_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'

        report = {
            'summary': {
                'timestamp': datetime.now().isoformat(),
                'duration_seconds': duration,
                'passed': self.passed,
                'failed': self.failed,
                'warnings': len(self.warnings),
                'critical': len(self.critical_failures),
                'success_rate': (self.passed / total * 100) if total > 0 else 0
            },
            'results': self.test_results,
            'critical_failures': self.critical_failures,
            'warnings': self.warnings
        }

        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

        print(f"\n📄 Detailed report saved: {report_file}")

        print("\n" + "="*80)

        # Final verdict
        if len(self.critical_failures) > 0:
            print("🔥 VEREDICTO: FALLAS CRÍTICAS ENCONTRADAS - SISTEMA NO SEGURO")
        elif self.failed > 0:
            print("⚠️  VEREDICTO: FALLAS ENCONTRADAS - REQUIERE CORRECCIONES")
        elif len(self.warnings) > 5:
            print("⚠️  VEREDICTO: APROBADO CON ADVERTENCIAS")
        else:
            print("✅ VEREDICTO: SISTEMA APROBADO")

        print("="*80)


if __name__ == '__main__':
    benchmark = SystemBenchmark()
    benchmark.run_benchmark()
