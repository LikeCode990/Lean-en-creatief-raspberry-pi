#!/usr/bin/env python3
"""
HC-SR04 Sensor Web Monitor - All-in-One
========================================
Complete sensor monitoring systeem in één bestand!

Geen externe dependencies nodig - alleen Python standard library.

Gebruik:
    python3 hc_sr04_simple_web.py
    
Open browser: http://localhost:8080

Hardware Setup:
- VCC  → 5V
- GND  → Ground
- TRIG → GPIO 23
- ECHO → GPIO 24 (met voltage divider: 1kΩ + 2kΩ)
"""

import RPi.GPIO as GPIO
import time
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import threading

# ===== CONFIGURATIE =====
TRIG_PIN = 23
ECHO_PIN = 24
PORT = 8080

# ===== SENSOR DATA =====
sensor_data = {
    'distance': None,
    'status': 'starting',
    'timestamp': None,
    'history': [],
    'total': 0,
    'success': 0
}

# ===== GPIO FUNCTIES =====
def setup_gpio():
    """Initialiseer GPIO."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.1)

def measure():
    """Meet afstand."""
    try:
        GPIO.output(TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(TRIG_PIN, False)
        
        timeout = time.time() + 0.1
        while GPIO.input(ECHO_PIN) == 0:
            start = time.time()
            if start > timeout:
                return None, 'timeout'
        
        timeout = time.time() + 0.1
        while GPIO.input(ECHO_PIN) == 1:
            end = time.time()
            if end > timeout:
                return None, 'timeout'
        
        distance = ((end - start) * 34300) / 2
        
        if 2 <= distance <= 400:
            return round(distance, 1), 'success'
        return None, 'out_of_range'
    except:
        return None, 'error'

def sensor_loop():
    """Background thread voor sensor."""
    setup_gpio()
    print("✓ Sensor actief\n")
    
    while True:
        distance, status = measure()
        
        sensor_data['distance'] = distance
        sensor_data['status'] = status
        sensor_data['timestamp'] = datetime.now().strftime("%H:%M:%S")
        sensor_data['total'] += 1
        
        if status == 'success':
            sensor_data['success'] += 1
            sensor_data['history'].append(distance)
        else:
            sensor_data['history'].append(None)
        
        if len(sensor_data['history']) > 30:
            sensor_data['history'].pop(0)
        
        if distance:
            print(f"[{sensor_data['timestamp']}] {distance:.1f} cm")
        
        time.sleep(0.5)

# ===== HTML INTERFACE =====
HTML_PAGE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HC-SR04 Monitor</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 800px; margin: 0 auto; }
        .card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        h1 {
            color: #667eea;
            text-align: center;
            font-size: 2em;
            margin-bottom: 30px;
        }
        .distance {
            text-align: center;
            font-size: 5em;
            font-weight: bold;
            color: #667eea;
            margin: 30px 0;
            font-family: 'Courier New', monospace;
        }
        .status {
            text-align: center;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            font-size: 1.2em;
        }
        .status.ok { background: #d4edda; color: #155724; }
        .status.error { background: #f8d7da; color: #721c24; }
        .led {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 10px;
            animation: pulse 1s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .led.green { background: #28a745; }
        .led.yellow { background: #ffc107; }
        .led.red { background: #dc3545; }
        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 20px;
        }
        .stat {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label {
            color: #666;
            margin-top: 5px;
            font-size: 0.9em;
        }
        .chart {
            height: 150px;
            display: flex;
            align-items: flex-end;
            justify-content: space-around;
            background: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
        }
        .bar {
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
            width: 12px;
            border-radius: 6px 6px 0 0;
            transition: height 0.3s;
        }
        .time {
            text-align: center;
            color: #999;
            margin-top: 10px;
            font-family: 'Courier New', monospace;
        }
        @media (max-width: 600px) {
            .distance { font-size: 3em; }
            .stats { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>🎯 HC-SR04 Afstandsmeter</h1>
            
            <div class="distance" id="distance">-- cm</div>
            
            <div class="status" id="status">
                <span class="led" id="led"></span>
                <span id="statusText">Laden...</span>
            </div>
            
            <div class="time" id="time">--</div>
        </div>
        
        <div class="card">
            <h2 style="color: #667eea; margin-bottom: 15px;">📊 Statistieken</h2>
            <div class="stats">
                <div class="stat">
                    <div class="stat-value" id="total">0</div>
                    <div class="stat-label">Totaal</div>
                </div>
                <div class="stat">
                    <div class="stat-value" id="success">0</div>
                    <div class="stat-label">Succesvol</div>
                </div>
                <div class="stat">
                    <div class="stat-value" id="rate">0%</div>
                    <div class="stat-label">Success Rate</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2 style="color: #667eea; margin-bottom: 15px;">📈 Geschiedenis</h2>
            <div class="chart" id="chart"></div>
        </div>
    </div>
    
    <script>
        function update() {
            fetch('/data')
                .then(r => r.json())
                .then(d => {
                    // Distance
                    const dist = d.distance;
                    document.getElementById('distance').textContent = 
                        dist ? dist.toFixed(1) + ' cm' : '-- cm';
                    
                    // LED color
                    const led = document.getElementById('led');
                    if (dist && dist < 10) {
                        led.className = 'led red';
                    } else if (dist && dist < 30) {
                        led.className = 'led yellow';
                    } else {
                        led.className = 'led green';
                    }
                    
                    // Status
                    const status = document.getElementById('status');
                    const statusText = document.getElementById('statusText');
                    if (d.status === 'success') {
                        status.className = 'status ok';
                        statusText.textContent = '✓ Actief';
                    } else {
                        status.className = 'status error';
                        statusText.textContent = '✗ ' + d.status;
                    }
                    
                    // Time
                    document.getElementById('time').textContent = 
                        'Update: ' + d.timestamp;
                    
                    // Stats
                    document.getElementById('total').textContent = d.total;
                    document.getElementById('success').textContent = d.success;
                    const rate = d.total > 0 ? ((d.success/d.total)*100).toFixed(0) : 0;
                    document.getElementById('rate').textContent = rate + '%';
                    
                    // Chart
                    const chart = document.getElementById('chart');
                    chart.innerHTML = '';
                    const vals = d.history.filter(v => v !== null);
                    if (vals.length > 0) {
                        const max = Math.max(...vals, 100);
                        d.history.forEach(v => {
                            const bar = document.createElement('div');
                            bar.className = 'bar';
                            bar.style.height = v ? ((v/max)*120) + 'px' : '0px';
                            chart.appendChild(bar);
                        });
                    }
                });
        }
        
        setInterval(update, 500);
        update();
    </script>
</body>
</html>"""

# ===== HTTP SERVER =====
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode())
        elif self.path == '/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(sensor_data).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress logs

# ===== MAIN =====
def main():
    print("="*50)
    print("    HC-SR04 SENSOR WEB MONITOR")
    print("="*50)
    print("\n🚀 Starten...")
    
    # Start sensor thread
    thread = threading.Thread(target=sensor_loop, daemon=True)
    thread.start()
    time.sleep(1)
    
    # Start web server
    print(f"\n🌐 Server actief op:")
    print(f"   → http://localhost:{PORT}")
    print(f"\n⏹️  Druk Ctrl+C om te stoppen\n")
    print("="*50 + "\n")
    
    try:
        server = HTTPServer(('', PORT), Handler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n⏹️  Gestopt")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
