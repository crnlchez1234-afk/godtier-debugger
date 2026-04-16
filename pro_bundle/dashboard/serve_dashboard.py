#!/usr/bin/env python3
"""
🌐 Dashboard Server con Auto-Actualización
Sirve el dashboard y lo regenera automáticamente cada 5 segundos
"""

import http.server
import socketserver
import threading
import time
from pathlib import Path
from src.dashboard.audit import AuditDashboard

PORT = 8080
REPORT_FILE = "AUDIT_REPORT.html"

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    """Handler personalizado para servir el dashboard"""
    
    def do_GET(self):
        # Si se solicita la raíz o el dashboard, regenerar y servir
        if self.path in ['/', '/AUDIT_REPORT.html', '/dashboard']:
            # Regenerar el reporte antes de servirlo
            try:
                dashboard = AuditDashboard()
                dashboard.generate_report(REPORT_FILE)
            except Exception as e:
                print(f"⚠️ Error generando reporte: {e}")
            
            # Servir el archivo generado
            self.path = '/' + REPORT_FILE
        
        return super().do_GET()
    
    def log_message(self, format, *args):
        """Silenciar logs de HTTP (opcional)"""
        pass  # Comentar esta línea para ver los logs de acceso


def auto_regenerate_dashboard():
    """Thread que regenera el dashboard cada 5 segundos"""
    while True:
        try:
            dashboard = AuditDashboard()
            dashboard.generate_report(REPORT_FILE)
            print(f"🔄 Dashboard actualizado: {time.strftime('%H:%M:%S')}", end='\r')
        except Exception as e:
            print(f"\n⚠️ Error en auto-regeneración: {e}")
        time.sleep(5)


def start_server():
    """Inicia el servidor web del dashboard"""
    # Generar reporte inicial
    print("📊 Generando dashboard inicial...")
    dashboard = AuditDashboard()
    dashboard.generate_report(REPORT_FILE)
    
    # Iniciar thread de auto-regeneración
    print("🔄 Iniciando auto-actualización (cada 5s)...")
    regen_thread = threading.Thread(target=auto_regenerate_dashboard, daemon=True)
    regen_thread.start()
    
    # Iniciar servidor HTTP
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        print(f"\n✅ Dashboard Server ACTIVO en http://localhost:{PORT}")
        print(f"   📊 Abre tu navegador en: http://localhost:{PORT}/AUDIT_REPORT.html")
        print(f"   🔄 Auto-refresh activado: La página se actualiza cada 5 segundos")
        print(f"   ⏹️  Presiona Ctrl+C para detener\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Servidor detenido. ¡Adiós!")


if __name__ == "__main__":
    start_server()
