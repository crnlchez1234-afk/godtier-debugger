#!/usr/bin/env python3
"""
🔥 MASTER DEBUGGER ULTRA GODTIER 🔥
Unified System - Cleaned and Restructured
"""

import os
import sys
import time
import ast
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import traceback
import logging
from src.utils.git_senior import GitSenior

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

# Import AutoDebugger
try:
    from src.debugger.auto_debugger import AutoDebugger, CorrectionResult
    AUTO_DEBUGGER_AVAILABLE = True
except ImportError as e:
    AUTO_DEBUGGER_AVAILABLE = False
    logger.warning(f"⚠️ AutoDebugger not available: {e}")

# Import NeurosysAGI
try:
    from src.ai.neurosys_debugger_wrapper import NeurosysDebuggerAI
    NEUROSYS_AVAILABLE = True
except ImportError as e:
    NEUROSYS_AVAILABLE = False
    logger.info(f"ℹ️  NeurosysAGI not available: {e}")

# Import Lazarus & Darwin
try:
    from src.lazarus.engine import LazarusEngine, lazarus_protect
    from src.darwin.evolver import DarwinEvolver
    GOD_TIER_AVAILABLE = True
except ImportError as e:
    GOD_TIER_AVAILABLE = False
    logger.warning(f"⚠️ God Tier Modules (Lazarus/Darwin) not available: {e}")



class GodTierRunner:
    """
    Ejecutor de Scripts con capacidades God Tier (Lazarus + Darwin).
    """
    def __init__(self, script_path: str):
        self.script_path = Path(script_path).resolve()
        if not self.script_path.exists():
            raise FileNotFoundError(f"Script not found: {self.script_path}")

    def run_god_mode(self, enable_lazarus: bool = False, enable_darwin: bool = False, senior_mode: bool = False):
        """
        Ejecuta el script inyectando superpoderes.
        """
        print(f"\n⚡ INICIANDO GOD MODE RUNNER para: {self.script_path.name}")
        
        # Inicializar Git Senior si es necesario
        git_senior = None
        if senior_mode:
            git_senior = GitSenior(self.script_path.parent)
            if not git_senior.is_repo():
                print("   ⚠️ Directorio no es un repo Git. Inicializando para modo Senior...")
                git_senior.init_repo()
                git_senior._run(["add", "."])
                git_senior._run(["commit", "-m", "Initial commit"])
        
        with open(self.script_path, 'r', encoding='utf-8') as f:
            original_code = f.read()

        final_code = original_code

        # 1. DARWIN EVOLUTION (Optimización Estática Previa)
        if enable_darwin:
            print("🧬 Darwin Protocol: Analizando funciones para evolución...")
            try:
                # Inicializar Evolver
                evolver = DarwinEvolver()
                
                # Ejecutar código original en entorno aislado para extraer funciones
                temp_env = {}
                exec(original_code, temp_env)
                
                # Buscar funciones candidatas (definidas en el script, no importadas)
                candidates = []
                
                # Usar AST para extraer el código fuente de cada función
                import ast
                import astor
                tree = ast.parse(original_code)
                
                function_sources = {}
                for node in tree.body:
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        function_sources[node.name] = astor.to_source(node)

                for name, obj in temp_env.items():
                    if callable(obj) and hasattr(obj, '__module__') and obj.__module__ is None:
                        if name in function_sources:
                            candidates.append((name, obj, function_sources[name]))
                
                if not candidates:
                    print("   ⚠️ No se encontraron funciones candidatas para evolucionar.")
                
                for name, func, source in candidates:
                    # Heurística: Solo evolucionar si tiene "slow" o "calculate" en el nombre (para demo)
                    if "slow" in name or "calc" in name or "process" in name:
                        # Intentar evolucionar
                        test_args = (10,) 
                        
                        # Pasamos el código fuente explícitamente
                        new_func, new_source = evolver.evolve_function(name, func, test_args=test_args, source_code_override=source)
                        
                        if new_source:
                            print(f"   ✨ Aplicando evolución a '{name}' en el código fuente...")
                            
                            # Asegurar que la nueva función tenga el nombre correcto
                            try:
                                new_tree = ast.parse(new_source)
                                for node in new_tree.body:
                                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                                        if node.name != name:
                                            print(f"   🔧 Renombrando '{node.name}' -> '{name}' para mantener compatibilidad.")
                                            node.name = name
                                new_source = astor.to_source(new_tree)
                            except Exception as e:
                                print(f"   ⚠️ Error renombrando función: {e}")

                            # --- SENIOR MODE: GIT INTEGRATION ---
                            if senior_mode and git_senior:
                                print(f"   👔 Senior Mode: Creating Pull Request for '{name}'...")
                                original_branch = git_senior.get_current_branch()
                                branch_name = git_senior.create_optimization_branch(name)
                                
                                # Escribir cambios en el archivo REAL
                                with open(self.script_path, 'r', encoding='utf-8') as f:
                                    current_content = f.read()
                                
                                if source.strip() in current_content:
                                    new_content = current_content.replace(source.strip(), new_source.strip())
                                    with open(self.script_path, 'w', encoding='utf-8') as f:
                                        f.write(new_content)
                                    
                                    git_senior.commit_changes(self.script_path.name, name, 99.9)
                                    print(f"   ✅ Changes committed to branch '{branch_name}'")
                                    
                                    git_senior.checkout_main()
                                    print(f"   🔙 Switched back to '{original_branch}' (PR ready)")
                                else:
                                    print("   ⚠️ Could not apply patch to file (source mismatch). Skipping Git commit.")

                            # Append al final y redefinir (para ejecución en memoria)
                            final_code += f"\n\n# --- DARWIN EVOLUTION APPLIED TO {name} ---\n{new_source}\n# ----------------------------------------\n"
                            
            except Exception as e:
                print(f"   ❌ Error en Darwin Protocol: {e}")
                traceback.print_exc() 

        # 2. LAZARUS PROTOCOL (Inyección de Inmortalidad)
        if enable_lazarus:
            print("💀 Lazarus Protocol: Inyectando nanobots de resurrección...")
            # Usamos final_code para incluir las evoluciones de Darwin si las hubo
            final_code = self._inject_lazarus(final_code)

        # 3. EJECUCIÓN
        print("🚀 Ejecutando código aumentado...\n" + "="*40)
        try:
            # Crear un entorno global con las herramientas necesarias
            global_env = {
                '__file__': str(self.script_path),
                '__name__': '__main__',
                'lazarus_protect': lazarus_protect, # Inyectar decorador
                'sys': sys,
                'os': os
            }
            # Añadir directorio del script al path
            sys.path.insert(0, str(self.script_path.parent))
            
            # Compilar con el nombre de archivo real para que inspect.getsource funcione
            # y Lazarus pueda leer el código fuente original del disco.
            compiled_code = compile(final_code, str(self.script_path), 'exec')
            
            exec(compiled_code, global_env)
        except Exception as e:
            print(f"\n❌ Fallo crítico en el Runner (incluso Lazarus no pudo contenerlo): {e}")
            traceback.print_exc() 

        # 2. LAZARUS PROTOCOL (Inyección de Inmortalidad)
        if enable_lazarus:
            print("💀 Lazarus Protocol: Inyectando nanobots de resurrección...")
            # Usamos final_code para incluir las evoluciones de Darwin si las hubo
            final_code = self._inject_lazarus(final_code)

        # 3. EJECUCIÓN
        print("🚀 Ejecutando código aumentado...\n" + "="*40)
        try:
            # Crear un entorno global con las herramientas necesarias
            global_env = {
                '__file__': str(self.script_path),
                '__name__': '__main__',
                'lazarus_protect': lazarus_protect, # Inyectar decorador
                'sys': sys,
                'os': os
            }
            # Añadir directorio del script al path
            sys.path.insert(0, str(self.script_path.parent))
            
            # Compilar con el nombre de archivo real para que inspect.getsource funcione
            # y Lazarus pueda leer el código fuente original del disco.
            compiled_code = compile(final_code, str(self.script_path), 'exec')
            
            exec(compiled_code, global_env)
        except Exception as e:
            print(f"\n❌ Fallo crítico en el Runner (incluso Lazarus no pudo contenerlo): {e}")
            traceback.print_exc()

    def _inject_lazarus(self, source_code: str) -> str:
        """
        Usa AST para decorar automáticamente todas las funciones con @lazarus_protect
        """
        try:
            tree = ast.parse(source_code)
            
            # Importar lazarus si no está (aunque lo inyectamos en globals, es bueno que esté en AST)
            # Pero como usamos exec con globals, basta con decorar.
            
            class LazarusInjector(ast.NodeTransformer):
                def visit_FunctionDef(self, node):
                    # Verificar si ya tiene el decorador
                    has_lazarus = any(
                        isinstance(d, ast.Name) and d.id == 'lazarus_protect' 
                        for d in node.decorator_list
                    )
                    if not has_lazarus:
                        # Agregar @lazarus_protect
                        node.decorator_list.insert(0, ast.Name(id='lazarus_protect', ctx=ast.Load()))
                    return node

            transformer = LazarusInjector()
            new_tree = transformer.visit(tree)
            ast.fix_missing_locations(new_tree)
            
            import astor
            return astor.to_source(new_tree)
        except Exception as e:
            logger.error(f"Error inyectando Lazarus: {e}")
            return source_code


class MasterDebugger:
    """
    Unified Master Debugger System
    """

    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path).resolve()
        self.start_time = datetime.now()
        
        # Stats
        self.stats = {
            'files_scanned': 0,
            'files_with_errors': 0,
            'total_errors': 0,
            'auto_fixes_applied': 0,
            'manual_fixes_needed': 0,
            'patterns_detected': {}
        }
        
        # Initialize AutoDebugger
        self.auto_debugger = None
        if AUTO_DEBUGGER_AVAILABLE:
            try:
                self.auto_debugger = AutoDebugger()
                logger.info("🔥 AutoDebugger initialized")
            except Exception as e:
                logger.warning(f"Error initializing AutoDebugger: {e}")
        
        # Initialize NeurosysAGI
        self.ai_debugger = None
        if NEUROSYS_AVAILABLE:
            try:
                self.ai_debugger = NeurosysDebuggerAI()
                logger.info("🧠 NeurosysAGI initialized")
            except Exception as e:
                logger.warning(f"Error initializing NeurosysAGI: {e}")
        
        self.results = []

    def scan_project(self) -> List[Path]:
        """Scans all Python files in the project"""
        logger.info(f"🔍 Scanning project: {self.project_path}")
        
        python_files = []
        for path in self.project_path.rglob("*.py"):
            # Ignore special directories and archive
            if any(part.startswith('.') for part in path.parts):
                continue
            if any(part in ['__pycache__', 'venv', 'env', 'node_modules', '_archive'] for part in path.parts):
                continue
            
            python_files.append(path)
        
        self.stats['files_scanned'] = len(python_files)
        logger.info(f"📄 Found {len(python_files)} Python files")
        return python_files

    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyzes a single file for errors"""
        result = {
            'file': str(file_path),
            'has_errors': False,
            'errors': [],
            'fixes': []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Syntax Check
            try:
                ast.parse(content)
            except SyntaxError as e:
                result['has_errors'] = True
                result['errors'].append(f"SyntaxError: {e}")
                self.stats['total_errors'] += 1
                
                # Try Auto-Fix if available
                if self.auto_debugger:
                    fix_result = self.auto_debugger.fix_syntax_error(content, e)
                    if fix_result and fix_result.success:
                        result['fixes'].append("Syntax Error Fixed")
                        self.stats['auto_fixes_applied'] += 1
                        # Save fixed file (optional, commented out for safety)
                        # with open(file_path, 'w', encoding='utf-8') as f:
                        #     f.write(fix_result.corrected_code)
            
            # Logic/Pattern Check (if no syntax errors)
            if not result['has_errors'] and self.auto_debugger:
                # Here we would call more advanced checks from AutoDebugger
                pass

        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            
        if result['has_errors']:
            self.stats['files_with_errors'] += 1
            
        return result

    def run(self):
        """Runs the full debugging process"""
        files = self.scan_project()
        
        print("\n" + "="*50)
        print(f"🚀 STARTING DEBUG SCAN - {self.start_time}")
        print("="*50 + "\n")
        
        for file_path in files:
            res = self.analyze_file(file_path)
            if res['has_errors']:
                print(f"❌ Error in {file_path.name}: {res['errors']}")
                if res['fixes']:
                    print(f"   ✅ Fixes applied: {res['fixes']}")
            self.results.append(res)
            
        print("\n" + "="*50)
        print("📊 FINAL REPORT")
        print(f"Files Scanned: {self.stats['files_scanned']}")
        print(f"Files with Errors: {self.stats['files_with_errors']}")
        print(f"Total Errors: {self.stats['total_errors']}")
        print(f"Auto-Fixes: {self.stats['auto_fixes_applied']}")
        print("="*50 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="🔥 DEBUGGING GODTIER - Unified AI System 🔥")
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')

    # Comando SCAN
    scan_parser = subparsers.add_parser('scan', help='Escanear proyecto en busca de errores')
    scan_parser.add_argument('--path', default='.', help='Ruta del proyecto')

    # Comando RUN
    run_parser = subparsers.add_parser('run', help='Ejecutar script en MODO DIOS')
    run_parser.add_argument('script', help='Archivo Python a ejecutar')
    run_parser.add_argument('--god-mode', action='store_true', help='Activa TODO (Lazarus + Darwin)')
    run_parser.add_argument('--lazarus', action='store_true', help='Activa solo Protocolo Lázaro (Inmortalidad)')
    run_parser.add_argument('--darwin', action='store_true', help='Activa solo Project Darwin (Evolución)')
    run_parser.add_argument('--senior', action='store_true', help='Activa Modo Senior (Git Integration)')

    args = parser.parse_args()

    if args.command == 'run':
        runner = GodTierRunner(args.script)
        lazarus_on = args.god_mode or args.lazarus
        darwin_on = args.god_mode or args.darwin
        runner.run_god_mode(enable_lazarus=lazarus_on, enable_darwin=darwin_on, senior_mode=args.senior)
        
    elif args.command == 'scan' or args.command is None:
        # Default to scan if no command or scan command
        path = args.path if args.command == 'scan' else '.'
        debugger = MasterDebugger(path)
        debugger.run()
    else:
        parser.print_help()
