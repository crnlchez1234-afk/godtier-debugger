#!/usr/bin/env python3
"""
🔄 Auto-Updater para DEBUGGING_GODTIER
Mantiene el proyecto actualizado automáticamente
Evita obsolescencia de dependencias, código y prácticas
"""

import subprocess
import json
import re
from pathlib import Path
from datetime import datetime
import sys

class ProjectUpdater:
    """Actualiza dependencias y detecta código obsoleto"""
    
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path(__file__).parent
        self.report = []
        
    def check_outdated_packages(self):
        """Verifica paquetes desactualizados"""
        print("\n🔍 Verificando paquetes desactualizados...")
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "list", "--outdated", "--format=json"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0 and result.stdout:
                outdated = json.loads(result.stdout)
                
                if outdated:
                    print(f"\n⚠️  Encontrados {len(outdated)} paquetes desactualizados:")
                    for pkg in outdated:
                        print(f"   📦 {pkg['name']}: {pkg['version']} → {pkg['latest_version']}")
                        self.report.append({
                            'type': 'outdated_package',
                            'name': pkg['name'],
                            'current': pkg['version'],
                            'latest': pkg['latest_version']
                        })
                else:
                    print("   ✅ Todos los paquetes están actualizados")
                
                return outdated
            else:
                print("   ⚠️  No se pudo verificar paquetes")
                return []
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return []
    
    def update_packages(self, packages: list = None, auto: bool = False):
        """Actualiza paquetes específicos o todos"""
        
        if not packages:
            outdated = self.check_outdated_packages()
            if not outdated:
                return
            
            if not auto:
                response = input("\n¿Actualizar TODOS los paquetes? (y/n): ")
                if response.lower() != 'y':
                    return
            
            packages = [pkg['name'] for pkg in outdated]
        
        print(f"\n🔄 Actualizando {len(packages)} paquete(s)...")
        
        for pkg in packages:
            try:
                print(f"   📦 Actualizando {pkg}...")
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "--upgrade", pkg],
                    capture_output=True,
                    cwd=self.project_root
                )
                print(f"   ✅ {pkg} actualizado")
            except Exception as e:
                print(f"   ❌ Error actualizando {pkg}: {e}")
    
    def check_python_version(self):
        """Verifica versión de Python"""
        print("\n🐍 Verificando versión de Python...")
        
        current = sys.version_info
        current_str = f"{current.major}.{current.minor}.{current.micro}"
        print(f"   📍 Versión actual: Python {current_str}")
        
        # Python 3.10 es estable, 3.11+ son versiones nuevas
        if current.minor < 10:
            print(f"   ⚠️  OBSOLETO: Python 3.{current.minor} está desactualizado")
            print(f"   💡 Recomendado: Actualizar a Python 3.10+")
            self.report.append({
                'type': 'python_version',
                'current': current_str,
                'recommended': '3.10+'
            })
        elif current.minor >= 12:
            print(f"   ✅ Python 3.{current.minor} - Versión moderna")
        else:
            print(f"   ✅ Python 3.{current.minor} - Versión estable")
    
    def check_deprecated_code(self):
        """Busca código obsoleto en el proyecto"""
        print("\n🔍 Buscando código obsoleto...")
        
        deprecated_patterns = {
            r'import\s+imp\b': 'imp está deprecated, usar importlib',
            r'\.warn\(': 'warnings.warn es mejor práctica',
            r'os\.path\.walk': 'os.walk es el reemplazo moderno',
            r'asyncore|asynchat': 'asyncore/asynchat removidos en Python 3.12+, usar asyncio',
            r'from\s+collections\s+import\s+(Callable|Iterable|Mapping)': 
                'Mover a collections.abc en Python 3.10+',
        }
        
        py_files = list(self.project_root.rglob("*.py"))
        issues_found = []
        
        for file_path in py_files:
            if '.venv' in str(file_path) or '__pycache__' in str(file_path):
                continue
                
            try:
                content = file_path.read_text(encoding='utf-8')
                
                for pattern, message in deprecated_patterns.items():
                    matches = re.finditer(pattern, content)
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        issues_found.append({
                            'file': str(file_path.relative_to(self.project_root)),
                            'line': line_num,
                            'pattern': pattern,
                            'message': message
                        })
            except:
                continue
        
        if issues_found:
            print(f"\n⚠️  Encontradas {len(issues_found)} advertencias de código obsoleto:")
            for issue in issues_found[:10]:  # Mostrar primeras 10
                print(f"   📄 {issue['file']}:{issue['line']}")
                print(f"      💡 {issue['message']}")
            
            self.report.extend(issues_found)
        else:
            print("   ✅ No se encontró código obsoleto")
    
    def update_requirements(self):
        """Actualiza requirements.txt con versiones actuales"""
        print("\n📝 Actualizando requirements.txt...")
        
        req_file = self.project_root / "requirements.txt"
        if not req_file.exists():
            print("   ⚠️  requirements.txt no encontrado")
            return
        
        # Generar nuevo requirements.txt con versiones actuales
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "freeze"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                # Leer requirements actuales
                current_reqs = req_file.read_text().strip().split('\n')
                base_packages = [line.split('>=')[0].split('==')[0] for line in current_reqs if line and not line.startswith('#')]
                
                # Filtrar solo los paquetes que están en requirements
                installed = result.stdout.strip().split('\n')
                updated_reqs = []
                
                for pkg in base_packages:
                    for installed_pkg in installed:
                        if installed_pkg.lower().startswith(pkg.lower() + '=='):
                            # Convertir == a >= para flexibilidad
                            pkg_name, version = installed_pkg.split('==')
                            updated_reqs.append(f"{pkg_name}>={version}")
                            break
                
                if updated_reqs:
                    backup = self.project_root / f"requirements.txt.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    req_file.rename(backup)
                    print(f"   💾 Backup guardado: {backup.name}")
                    
                    req_file.write_text('\n'.join(updated_reqs) + '\n')
                    print(f"   ✅ requirements.txt actualizado con {len(updated_reqs)} paquetes")
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    def check_security_vulnerabilities(self):
        """Verifica vulnerabilidades de seguridad"""
        print("\n🔒 Verificando vulnerabilidades de seguridad...")
        
        try:
            # Intentar usar pip-audit si está disponible
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "pip-audit"],
                capture_output=True,
                cwd=self.project_root
            )
            
            result = subprocess.run(
                [sys.executable, "-m", "pip_audit"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if "No known vulnerabilities found" in result.stdout:
                print("   ✅ No se encontraron vulnerabilidades conocidas")
            else:
                print("   ⚠️  Se encontraron posibles vulnerabilidades")
                print(result.stdout[:500])  # Mostrar primeros 500 caracteres
                
        except:
            print("   ℹ️  pip-audit no disponible (opcional)")
    
    def generate_report(self):
        """Genera reporte de obsolescencia"""
        report_path = self.project_root / "logs" / f"update_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'issues': self.report,
                'total_issues': len(self.report)
            }, f, indent=2)
        
        print(f"\n📊 Reporte guardado: {report_path}")
        return report_path
    
    def run_full_check(self, auto_update: bool = False):
        """Ejecuta verificación completa"""
        print("\n" + "="*60)
        print("🔄 DEBUGGING_GODTIER - Auto-Updater")
        print("="*60)
        
        self.check_python_version()
        self.check_outdated_packages()
        self.check_deprecated_code()
        self.check_security_vulnerabilities()
        
        if auto_update:
            self.update_packages(auto=True)
            self.update_requirements()
        
        self.generate_report()
        
        print("\n" + "="*60)
        print("✅ Verificación completada")
        print("="*60 + "\n")


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Auto-actualización de DEBUGGING_GODTIER')
    parser.add_argument('--auto', action='store_true', help='Actualizar automáticamente sin preguntar')
    parser.add_argument('--check-only', action='store_true', help='Solo verificar, no actualizar')
    
    args = parser.parse_args()
    
    updater = ProjectUpdater()
    
    if args.check_only:
        updater.run_full_check(auto_update=False)
    else:
        updater.run_full_check(auto_update=args.auto)


if __name__ == "__main__":
    main()
