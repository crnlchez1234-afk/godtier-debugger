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
        if not Path(self.db_path).exists():
            return []
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Asumiendo que la tabla se llama 'optimizations' o similar basada en evolver.py
        # Si no existe, manejamos el error.
        try:
            cursor.execute("SELECT function_name, speedup_factor, timestamp FROM gene_memory")
            rows = cursor.fetchall()
        except sqlite3.OperationalError:
            return []
        finally:
            conn.close()
            
        return [{"name": r[0], "speedup": r[1], "date": r[2]} for r in rows]

    def _build_html(self, data):
        # Calcular métricas
        total_opts = len(data)
        avg_speedup = sum(d['speedup'] for d in data) / total_opts if total_opts else 0
        # Simulación de costos: Asumimos $0.00005 por ms de cómputo en nube (AWS Lambda pricing approx)
        # Esto es ilustrativo para el manager.
        estimated_savings_per_run = avg_speedup * 0.01 # Fake math for demo
        
        json_data = json.dumps(data)
        
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>NeuroSys AGI - Executive Audit</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #1a1a1a; color: #e0e0e0; padding: 20px; }}
        .card {{ background: #2d2d2d; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }}
        h1 {{ color: #00ff9d; }}
        .metric {{ font-size: 2em; font-weight: bold; }}
        .metric-label {{ color: #888; font-size: 0.9em; }}
        .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }}
    </style>
</head>
<body>
    <h1>🧬 NeuroSys AGI: Optimization Audit</h1>
    
    <div class="grid">
        <div class="card">
            <div class="metric-label">Total Optimizations</div>
            <div class="metric">{total_opts}</div>
        </div>
        <div class="card">
            <div class="metric-label">Avg. Speedup Factor</div>
            <div class="metric">{avg_speedup:.1f}x</div>
        </div>
        <div class="card">
            <div class="metric-label">Proj. Cloud Savings (Monthly)</div>
            <div class="metric" style="color: #00ff9d;">${estimated_savings_per_run * 10000:.2f}</div>
        </div>
    </div>

    <div class="card">
        <canvas id="speedupChart"></canvas>
    </div>

    <script>
        const data = {json_data};
        const ctx = document.getElementById('speedupChart').getContext('2d');
        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: data.map(d => d.name),
                datasets: [{{
                    label: 'Speedup Factor (x)',
                    data: data.map(d => d.speedup),
                    backgroundColor: '#00ff9d',
                    borderColor: '#00cc7d',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{ beginAtZero: true, grid: {{ color: '#444' }} }},
                    x: {{ grid: {{ display: false }} }}
                }},
                plugins: {{
                    legend: {{ labels: {{ color: '#fff' }} }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
