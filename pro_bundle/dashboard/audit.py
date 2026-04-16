import sqlite3
import json
from pathlib import Path
from datetime import datetime

class AuditDashboard:
    def __init__(self, db_path: str = "darwin_gene_memory.db"):
        self.db_path = db_path

    def generate_report(self, output_file: str = "AUDIT_REPORT.html"):
        data = self._fetch_data()
        html = self._build_html(data)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"   📊 Dashboard generated: {output_file}")

    def _fetch_data(self):
        data = {
            'optimizations': [],
            'upgrades': []
        }
        
        # 1. Fetch Darwin Optimizations
        if Path(self.db_path).exists():
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT function_name, speedup_factor, timestamp FROM gene_memory")
                rows = cursor.fetchall()
                data['optimizations'] = [{"name": r[0], "speedup": r[1], "date": r[2]} for r in rows]
                conn.close()
            except sqlite3.OperationalError:
                pass

        # 2. Fetch Auto-Upgrades
        log_path = Path("logs/code_upgrades.jsonl")
        if log_path.exists():
            with open(log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        if entry.get('success'):
                            data['upgrades'].append({
                                'pattern': entry.get('pattern'),
                                'action': entry.get('action'),
                                'timestamp': entry.get('timestamp')
                            })
                    except json.JSONDecodeError:
                        continue
            
        return data

    def _build_html(self, data):
        # Calcular métricas
        optimizations = data.get('optimizations', [])
        upgrades = data.get('upgrades', [])
        
        total_opts = len(optimizations)
        total_upgrades = len(upgrades)
        avg_speedup = sum(d['speedup'] for d in optimizations) / total_opts if total_opts else 0
        
        # Simulación de costos
        estimated_savings_per_run = avg_speedup * 0.01 
        
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>NeuroSys AGI - God Tier Dashboard</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #1a1a1a; color: #e0e0e0; margin: 0; padding: 20px; }}
        .card {{ background: #2d2d2d; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }}
        .metric {{ font-size: 2.5em; font-weight: bold; color: #4CAF50; }}
        .metric-label {{ color: #888; font-size: 0.9em; text-transform: uppercase; letter-spacing: 1px; }}
        h1 {{ color: #fff; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }}
        h2 {{ color: #4CAF50; margin-top: 0; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th, td {{ text-align: left; padding: 12px; border-bottom: 1px solid #404040; }}
        th {{ color: #888; }}
        tr:hover {{ background: #333; }}
        .badge {{ padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }}
        .badge-opt {{ background: #2196F3; color: white; }}
        .badge-upg {{ background: #9C27B0; color: white; }}
    </style>
</head>
<body>
    <h1>🔥 DEBUGGING GOD TIER - LIVE STATUS 🔥</h1>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
        <div class="card">
            <div class="metric">{total_opts}</div>
            <div class="metric-label">Darwin Evolutions</div>
        </div>
        <div class="card">
            <div class="metric">{avg_speedup:.2f}x</div>
            <div class="metric-label">Avg Speedup</div>
        </div>
        <div class="card">
            <div class="metric">{total_upgrades}</div>
            <div class="metric-label">Auto-Upgrades Applied</div>
        </div>
        <div class="card">
            <div class="metric">ACTIVE</div>
            <div class="metric-label">System Status</div>
        </div>
    </div>

    <div class="card">
        <h2>🧬 Recent Auto-Upgrades</h2>
        <table>
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>Pattern</th>
                    <th>Action</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {''.join(f'<tr><td>{u["timestamp"][:19]}</td><td><span class="badge badge-upg">{u["pattern"]}</span></td><td>{u["action"]}</td><td>✅ Applied</td></tr>' for u in upgrades[-10:])}
            </tbody>
        </table>
    </div>

    <div class="card">
        <h2>🚀 Evolution History</h2>
        <table>
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>Function</th>
                    <th>Speedup</th>
                </tr>
            </thead>
            <tbody>
                {''.join(f'<tr><td>{o["date"]}</td><td>{o["name"]}</td><td><span class="badge badge-opt">{o["speedup"]:.2f}x</span></td></tr>' for o in optimizations[-10:])}
            </tbody>
        </table>
    </div>
</body>
</html>
"""

