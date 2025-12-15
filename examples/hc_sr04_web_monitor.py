#!/usr/bin/env python3
"""
HC-SR04 Distance Sensor - Web Monitor
======================================
Real-time web interface voor het monitoren van de afstandssensor.

Installatie:
    pip install flask

Gebruik:
    python3 hc_sr04_web_monitor.py
    Open browser: http://localhost:5000

Hardware:
- HC-SR04 ultrasone sensor
- Voltage divider (1kΩ + 2kΩ)
"""

import RPi.GPIO as GPIO
import time
from datetime import datetime
from flask import Flask, render_template_string, jsonify
import threading
import json

# GPIO pins
TRIG_PIN = 23
ECHO_PIN = 24
SOUND_SPEED = 34300

# Data storage
sensor_data = {
    'current_distance': None,
    'status': 'initializing',
    'timestamp': None,
    'history': [],
    'stats': {
        'total_readings': 0,
        'successful_readings': 0,
        'errors': 0
    }
}

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>HC-SR04 Monitor</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
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
            margin-bottom: 10px;
            font-size: 2em;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        .distance-display {
            text-align: center;
            font-size: 4em;
            font-weight: bold;
            color: #667eea;
            margin: 30px 0;
            font-family: 'Courier New', monospace;
        }
        .status {
            text-align: center;
            font-size: 1.2em;
            padding: 10px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .status.success { background: #d4edda; color: #155724; }
        .status.error { background: #f8d7da; color: #721c24; }
        .status.warning { background: #fff3cd; color: #856404; }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .stat-box {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
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
            margin-top: 20px;
            height: 200px;
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            position: relative;
        }
        .chart-bar {
            position: absolute;
            bottom: 15px;
            background: #667eea;
            width: 8px;
            border-radius: 4px 4px 0 0;
            transition: height 0.3s;
        }
        .timestamp {
            text-align: center;
            color: #999;
            font-size: 0.9em;
            margin-top: 10px;
        }
        .indicator {
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
        .indicator.green { background: #28a745; }
        .indicator.yellow { background: #ffc107; }
        .indicator.red { background: #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>🎯 HC-SR04 Distance Monitor</h1>
            <p class="subtitle">Real-time Ultrasone Afstandsmeting</p>
            
            <div class="distance-display" id="distance">-- cm</div>
            
            <div class="status" id="status">
                <span class="indicator green"></span>
                <span id="status-text">Laden...</span>
            </div>
            
            <div class="timestamp" id="timestamp">--</div>
        </div>
        
        <div class="card">
            <h2 style="color: #667eea; margin-bottom: 15px;">📊 Statistieken</h2>
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-value" id="total-readings">0</div>
                    <div class="stat-label">Totaal Metingen</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" id="success-readings">0</div>
                    <div class="stat-label">Succesvol</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" id="error-count">0</div>
                    <div class="stat-label">Errors</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" id="success-rate">0%</div>
                    <div class="stat-label">Success Rate</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2 style="color: #667eea; margin-bottom: 15px;">📈 Geschiedenis (laatste 20)</h2>
            <div class="chart" id="chart"></div>
        </div>
    </div>
    
    <script>
        function updateData() {
            fetch('/api/sensor')
                .then(response => response.json())
                .then(data => {
                    // Update distance
                    const distanceEl = document.getElementById('distance');
                    if (data.current_distance !== null) {
                        distanceEl.textContent = data.current_distance.toFixed(1) + ' cm';
                        
                        // Update indicator color
                        const indicator = document.querySelector('.indicator');
                        if (data.current_distance < 10) {
                            indicator.className = 'indicator red';
                        } else if (data.current_distance < 30) {
                            indicator.className = 'indicator yellow';
                        } else {
                            indicator.className = 'indicator green';
                        }
                    } else {
                        distanceEl.textContent = '-- cm';
                    }
                    
                    // Update status
                    const statusEl = document.getElementById('status');
                    const statusText = document.getElementById('status-text');
                    statusText.textContent = data.status;
                    
                    if (data.status.includes('success') || data.status === 'active') {
                        statusEl.className = 'status success';
                    } else if (data.status.includes('timeout')) {
                        statusEl.className = 'status error';
                    } else {
                        statusEl.className = 'status warning';
                    }
                    
                    // Update timestamp
                    document.getElementById('timestamp').textContent = 
                        'Laatste update: ' + data.timestamp;
                    
                    // Update stats
                    document.getElementById('total-readings').textContent = 
                        data.stats.total_readings;
                    document.getElementById('success-readings').textContent = 
                        data.stats.successful_readings;
                    document.getElementById('error-count').textContent = 
                        data.stats.errors;
                    
                    const successRate = data.stats.total_readings > 0 
                        ? (data.stats.successful_readings / data.stats.total_readings * 100).toFixed(1)
                        : 0;
                    document.getElementById('success-rate').textContent = successRate + '%';
                    
                    // Update chart
                    updateChart(data.history);
                })
                .catch(error => console.error('Error:', error));
        }
        
        function updateChart(history) {
            const chart = document.getElementById('chart');
            chart.innerHTML = '';
            
            const validData = history.filter(d => d !== null);
            if (validData.length === 0) return;
            
            const maxDistance = Math.max(...validData, 100);
            const chartHeight = 170;
            const barWidth = 8;
            const gap = 4;
            const totalWidth = validData.length * (barWidth + gap);
            
            validData.forEach((distance, index) => {
                const bar = document.createElement('div');
                bar.className = 'chart-bar';
                bar.style.height = (distance / maxDistance * chartHeight) + 'px';
                bar.style.left = (index * (barWidth + gap)) + 15 + 'px';
                chart.appendChild(bar);
            });
        }
        
        // Update every 500ms
        setInterval(updateData, 500);
        updateData();
    </script>
</body>
</html>
"""

def setup_gpio():
    """Setup GPIO pins."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.1)

def measure_distance():
    """Meet afstand."""
    try:
        GPIO.output(TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(TRIG_PIN, False)
        
        timeout = time.time() + 0.1
        while GPIO.input(ECHO_PIN) == 0:
            pulse_start = time.time()
            if pulse_start > timeout:
                return None, 'timeout'
        
        timeout = time.time() + 0.1
        while GPIO.input(ECHO_PIN) == 1:
            pulse_end = time.time()
            if pulse_end > timeout:
                return None, 'timeout'
        
        duration = pulse_end - pulse_start
        distance = (duration * SOUND_SPEED) / 2
        
        if 2 <= distance <= 400:
            return distance, 'success'
        else:
            return distance, 'out_of_range'
    except Exception as e:
        return None, f'error: {str(e)}'

def sensor_thread():
    """Thread voor sensor reading."""
    global sensor_data
    
    setup_gpio()
    sensor_data['status'] = 'active'
    
    while True:
        try:
            distance, status = measure_distance()
            
            sensor_data['current_distance'] = distance
            sensor_data['status'] = status
            sensor_data['timestamp'] = datetime.now().strftime("%H:%M:%S")
            sensor_data['stats']['total_readings'] += 1
            
            if status == 'success':
                sensor_data['stats']['successful_readings'] += 1
                sensor_data['history'].append(distance)
            else:
                sensor_data['stats']['errors'] += 1
                sensor_data['history'].append(None)
            
            # Behoud laatste 20 metingen
            if len(sensor_data['history']) > 20:
                sensor_data['history'].pop(0)
            
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Sensor thread error: {e}")
            time.sleep(1)

@app.route('/')
def index():
    """Hoofdpagina."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/sensor')
def api_sensor():
    """API endpoint voor sensor data."""
    return jsonify(sensor_data)

def main():
    """Start web server en sensor thread."""
    print("="*60)
    print("         HC-SR04 WEB MONITOR")
    print("="*60)
    print("\n🚀 Server wordt gestart...")
    print("\n📡 Sensor thread starten...")
    
    # Start sensor thread
    thread = threading.Thread(target=sensor_thread, daemon=True)
    thread.start()
    
    time.sleep(1)
    
    print("\n✅ Sensor actief!")
    print("\n🌐 Open je browser en ga naar:")
    print("   → http://localhost:5000")
    print("   → http://raspberrypi.local:5000 (vanaf andere computer)")
    print("\n⏹️  Druk Ctrl+C om te stoppen\n")
    print("="*60 + "\n")
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n\n⏹️  Server gestopt")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
