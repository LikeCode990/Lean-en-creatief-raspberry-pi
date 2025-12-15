#!/usr/bin/env python3
"""
HC-SR04 Sensor API Server
=========================
Lightweight Python HTTP server die sensor data als JSON serveert.
Geen Flask nodig - gebruikt alleen Python standard library!

Gebruik:
    python3 hc_sr04_api_server.py
    
De web interface kan dan data ophalen van: http://localhost:8080/api/sensor
"""

import RPi.GPIO as GPIO
import time
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import threading

# GPIO Configuration
TRIG_PIN = 23
ECHO_PIN = 24
SOUND_SPEED = 34300

# Global sensor data
sensor_data = {
    'distance': None,
    'status': 'initializing',
    'timestamp': None,
    'history': [],
    'stats': {
        'total': 0,
        'success': 0,
        'errors': 0,
        'min': None,
        'max': None,
        'avg': None
    }
}

def setup_gpio():
    """Initialize GPIO pins."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.1)
    print("✓ GPIO initialized")

def measure_distance():
    """
    Measure distance with HC-SR04.
    Returns: (distance, status)
    """
    try:
        # Send trigger pulse
        GPIO.output(TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(TRIG_PIN, False)
        
        # Wait for echo start
        timeout = time.time() + 0.1
        while GPIO.input(ECHO_PIN) == 0:
            pulse_start = time.time()
            if pulse_start > timeout:
                return None, 'timeout_start'
        
        # Wait for echo end
        timeout = time.time() + 0.1
        while GPIO.input(ECHO_PIN) == 1:
            pulse_end = time.time()
            if pulse_end > timeout:
                return None, 'timeout_end'
        
        # Calculate distance
        duration = pulse_end - pulse_start
        distance = (duration * SOUND_SPEED) / 2
        
        if 2 <= distance <= 400:
            return round(distance, 1), 'success'
        else:
            return round(distance, 1), 'out_of_range'
            
    except Exception as e:
        return None, f'error: {str(e)}'

def update_statistics(distance):
    """Update statistics with new distance measurement."""
    stats = sensor_data['stats']
    
    if distance is not None:
        # Update min/max
        if stats['min'] is None or distance < stats['min']:
            stats['min'] = distance
        if stats['max'] is None or distance > stats['max']:
            stats['max'] = distance
        
        # Calculate average
        valid_history = [d for d in sensor_data['history'] if d is not None]
        if valid_history:
            stats['avg'] = round(sum(valid_history) / len(valid_history), 1)

def sensor_loop():
    """Background thread that continuously reads sensor."""
    global sensor_data
    
    setup_gpio()
    sensor_data['status'] = 'active'
    print("✓ Sensor thread started\n")
    
    while True:
        try:
            distance, status = measure_distance()
            
            # Update data
            sensor_data['distance'] = distance
            sensor_data['status'] = status
            sensor_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sensor_data['stats']['total'] += 1
            
            if status == 'success':
                sensor_data['stats']['success'] += 1
                sensor_data['history'].append(distance)
                update_statistics(distance)
            else:
                sensor_data['stats']['errors'] += 1
                sensor_data['history'].append(None)
            
            # Keep last 50 measurements
            if len(sensor_data['history']) > 50:
                sensor_data['history'].pop(0)
            
            # Console output
            if distance is not None:
                print(f"[{sensor_data['timestamp']}] {distance:.1f} cm - {status}")
            else:
                print(f"[{sensor_data['timestamp']}] ERROR - {status}")
            
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Sensor error: {e}")
            time.sleep(1)

class SensorAPIHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for sensor API."""
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/api/sensor':
            # Return sensor data as JSON
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')  # Enable CORS
            self.end_headers()
            
            response = json.dumps(sensor_data)
            self.wfile.write(response.encode())
            
        elif self.path == '/':
            # Simple info page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head><title>HC-SR04 API Server</title></head>
            <body style="font-family: Arial; padding: 40px; background: #f5f5f5;">
                <h1>🎯 HC-SR04 Sensor API Server</h1>
                <p><strong>Status:</strong> Active ✅</p>
                <h2>API Endpoints:</h2>
                <ul>
                    <li><a href="/api/sensor">/api/sensor</a> - Get sensor data (JSON)</li>
                </ul>
                <h2>Web Interface:</h2>
                <p>Open <code>sensor_dashboard.html</code> in your browser to view the dashboard.</p>
                <hr>
                <pre id="data">Loading...</pre>
                <script>
                    fetch('/api/sensor')
                        .then(r => r.json())
                        .then(d => {
                            document.getElementById('data').textContent = 
                                JSON.stringify(d, null, 2);
                        });
                    setInterval(() => {
                        fetch('/api/sensor')
                            .then(r => r.json())
                            .then(d => {
                                document.getElementById('data').textContent = 
                                    JSON.stringify(d, null, 2);
                            });
                    }, 1000);
                </script>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
            
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass

def main():
    """Start API server and sensor thread."""
    print("="*60)
    print("         HC-SR04 SENSOR API SERVER")
    print("="*60)
    print("\n📡 Starting sensor thread...")
    
    # Start sensor in background thread
    sensor_thread = threading.Thread(target=sensor_loop, daemon=True)
    sensor_thread.start()
    
    time.sleep(2)
    
    # Start HTTP server
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, SensorAPIHandler)
    
    print("\n🌐 API Server running on:")
    print(f"   → http://localhost:8080")
    print(f"   → http://localhost:8080/api/sensor (JSON data)")
    print("\n💡 Open sensor_dashboard.html in your browser")
    print("   to view the web interface!")
    print("\n⏹️  Press Ctrl+C to stop\n")
    print("="*60 + "\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n⏹️  Server stopped")
    finally:
        GPIO.cleanup()
        print("✓ GPIO cleanup complete")

if __name__ == "__main__":
    main()
