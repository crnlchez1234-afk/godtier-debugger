#!/usr/bin/env python3
"""
🎮 Dashboard Interactivo con WebSocket
Actualización en tiempo real SIN recargar la página
"""

import asyncio
import json
import time
from pathlib import Path
from datetime import datetime
from aiohttp import web
import aiohttp
from src.dashboard.audit import AuditDashboard

PORT = 8080
clients = set()


async def websocket_handler(request):
    """Handler para WebSocket - Envía actualizaciones en tiempo real"""
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    clients.add(ws)
    
    print(f"🔌 Cliente conectado. Total: {len(clients)}")
    
    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print(f'⚠️ WebSocket error: {ws.exception()}')
    finally:
        clients.discard(ws)
        print(f"🔌 Cliente desconectado. Total: {len(clients)}")
    
    return ws


async def index_handler(request):
    """Sirve el dashboard HTML con WebSocket"""
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>NeuroSys AGI - Live Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', sans-serif; 
            background: linear-gradient(135deg, #1a1a1a 0%, #2d1b4e 100%); 
            color: #e0e0e0; 
            padding: 20px; 
            min-height: 100vh;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            animation: fadeIn 1s;
        }
        h1 { 
            color: #00ff9d; 
            font-size: 2.5em;
            text-shadow: 0 0 20px rgba(0, 255, 157, 0.5);
        }
        .status {
            display: inline-block;
            padding: 8px 16px;
            background: #00ff9d;
            color: #1a1a1a;
            border-radius: 20px;
            font-weight: bold;
            animation: pulse 2s infinite;
            margin-top: 10px;
        }
        .card { 
            background: rgba(45, 45, 45, 0.8); 
            padding: 20px; 
            border-radius: 15px; 
            margin-bottom: 20px; 
            box-shadow: 0 8px 16px rgba(0,0,0,0.3);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 255, 157, 0.2);
            transition: transform 0.3s;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 24px rgba(0, 255, 157, 0.2);
        }
        .metric { 
            font-size: 3em; 
            font-weight: bold; 
            background: linear-gradient(45deg, #00ff9d, #00cc7d);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .metric-label { 
            color: #888; 
            font-size: 0.9em; 
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }
        .grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px;
        }
        .update-time {
            text-align: center;
            color: #666;
            font-size: 0.9em;
            margin-top: 20px;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.8; transform: scale(1.05); }
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .connection-status {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 10px 20px;
            border-radius: 25px;
            font-size: 0.85em;
            font-weight: bold;
            z-index: 1000;
        }
        .connected {
            background: #00ff9d;
            color: #1a1a1a;
            animation: pulse 2s infinite;
        }
        .disconnected {
            background: #ff4444;
            color: white;
        }
    </style>
</head>
<body>
    <div id="connectionStatus" class="connection-status disconnected">🔴 Conectando...</div>
    
    <div class="header">
        <h1>🧬 NeuroSys AGI: Live Dashboard</h1>
        <div class="status">🔄 ACTUALIZACIÓN EN TIEMPO REAL</div>
    </div>
    
    <div class="grid">
        <div class="card">
            <div class="metric-label">Total Optimizaciones</div>
            <div id="totalOpts" class="metric">0</div>
        </div>
        <div class="card">
            <div class="metric-label">Factor de Aceleración Promedio</div>
            <div id="avgSpeedup" class="metric">0.0x</div>
        </div>
        <div class="card">
            <div class="metric-label">Ahorro Proyectado (Mensual)</div>
            <div id="savings" class="metric" style="color: #00ff9d;">$0.00</div>
        </div>
    </div>

    <div class="card">
        <canvas id="speedupChart"></canvas>
    </div>

    <div class="update-time">
        Última actualización: <span id="lastUpdate">--:--:--</span>
    </div>

    <script>
        let chart = null;
        let ws = null;
        
        function connectWebSocket() {
            ws = new WebSocket(`ws://${window.location.host}/ws`);
            
            ws.onopen = () => {
                console.log('✅ WebSocket conectado');
                document.getElementById('connectionStatus').className = 'connection-status connected';
                document.getElementById('connectionStatus').textContent = '🟢 Conectado';
            };
            
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                updateDashboard(data);
            };
            
            ws.onerror = (error) => {
                console.error('❌ WebSocket error:', error);
            };
            
            ws.onclose = () => {
                console.log('🔴 WebSocket desconectado. Reconectando en 3s...');
                document.getElementById('connectionStatus').className = 'connection-status disconnected';
                document.getElementById('connectionStatus').textContent = '🔴 Desconectado';
                setTimeout(connectWebSocket, 3000);
            };
        }
        
        function updateDashboard(data) {
            // Actualizar métricas
            document.getElementById('totalOpts').textContent = data.total_opts;
            document.getElementById('avgSpeedup').textContent = data.avg_speedup.toFixed(1) + 'x';
            document.getElementById('savings').textContent = '$' + data.savings.toFixed(2);
            document.getElementById('lastUpdate').textContent = new Date().toLocaleTimeString();
            
            // Actualizar gráfico
            updateChart(data.optimizations);
        }
        
        function updateChart(optimizations) {
            const ctx = document.getElementById('speedupChart').getContext('2d');
            
            if (chart) {
                chart.destroy();
            }
            
            chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: optimizations.map(d => d.name),
                    datasets: [{
                        label: 'Factor de Aceleración (x)',
                        data: optimizations.map(d => d.speedup),
                        backgroundColor: 'rgba(0, 255, 157, 0.7)',
                        borderColor: '#00ff9d',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    animation: {
                        duration: 750,
                        easing: 'easeInOutQuart'
                    },
                    scales: {
                        y: { 
                            beginAtZero: true,
                            grid: { color: '#444' },
                            ticks: { color: '#fff' }
                        },
                        x: { 
                            grid: { display: false },
                            ticks: { color: '#fff' }
                        }
                    },
                    plugins: {
                        legend: { 
                            labels: { color: '#fff', font: { size: 14 } }
                        }
                    }
                }
            });
        }
        
        // Conectar al WebSocket
        connectWebSocket();
    </script>
</body>
</html>
    """
    return web.Response(text=html, content_type='text/html')


async def broadcast_update():
    """Envía actualizaciones periódicas a todos los clientes conectados"""
    while True:
        await asyncio.sleep(3)  # Actualizar cada 3 segundos
        
        if clients:
            # Obtener datos del dashboard
            dashboard = AuditDashboard()
            data = dashboard._fetch_data()
            
            total_opts = len(data)
            avg_speedup = sum(d['speedup'] for d in data) / total_opts if total_opts else 0
            estimated_savings = avg_speedup * 0.01 * 10000
            
            update = {
                'total_opts': total_opts,
                'avg_speedup': avg_speedup,
                'savings': estimated_savings,
                'optimizations': data,
                'timestamp': datetime.now().isoformat()
            }
            
            # Enviar a todos los clientes
            dead_clients = set()
            for ws in clients:
                try:
                    await ws.send_json(update)
                except:
                    dead_clients.add(ws)
            
            # Limpiar clientes muertos
            clients.difference_update(dead_clients)
            
            if clients:
                print(f"📡 Actualización enviada a {len(clients)} cliente(s) - {time.strftime('%H:%M:%S')}")


async def init_app():
    """Inicializa la aplicación web"""
    app = web.Application()
    app.router.add_get('/', index_handler)
    app.router.add_get('/ws', websocket_handler)
    
    # Iniciar broadcast en segundo plano
    asyncio.create_task(broadcast_update())
    
    return app


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎮 DASHBOARD INTERACTIVO CON WEBSOCKET")
    print("="*60)
    print(f"\n✅ Servidor iniciado en: http://localhost:{PORT}")
    print(f"📊 Abre tu navegador en: http://localhost:{PORT}")
    print(f"🔄 Actualización automática: Cada 3 segundos")
    print(f"⚡ Tecnología: WebSocket (sin recargar página)")
    print(f"\n⏹️  Presiona Ctrl+C para detener\n")
    
    web.run_app(init_app(), host='localhost', port=PORT, print=None)
