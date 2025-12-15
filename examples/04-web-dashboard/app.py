#!/usr/bin/env python3
"""
Web Dashboard voor Raspberry Pi
================================
Flask web applicatie om sensor data te bekijken en GPIO te besturen.

Functies:
- Bekijk sensor data (temperatuur, luchtvochtigheid)
- Bestuur LEDs via web interface
- Real-time data updates
- Eenvoudige installatie en gebruik

Hardware:
- DHT22 sensor op GPIO 4 (optioneel)
- LED op GPIO 18
- LED op GPIO 23

Installatie:
pip3 install flask

Gebruik:
python3 app.py
Open browser: http://raspberrypi.local:5000
"""

from flask import Flask, render_template, jsonify, request
import RPi.GPIO as GPIO
from datetime import datetime
import time

# GPIO Configuration
LED1_PIN = 18
LED2_PIN = 23
DHT_PIN = 4

app = Flask(__name__)

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED1_PIN, GPIO.OUT)
GPIO.setup(LED2_PIN, GPIO.OUT)

# Initial LED states
led1_state = False
led2_state = False

def read_sensor_data():
    """
    Lees sensor data (DHT22)
    Als sensor niet beschikbaar is, return dummy data
    """
    try:
        import Adafruit_DHT
        sensor = Adafruit_DHT.DHT22
        humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT_PIN)
        
        if humidity is not None and temperature is not None:
            return {
                'temperature': round(temperature, 1),
                'humidity': round(humidity, 1),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'success'
            }
    except ImportError:
        pass
    except Exception as e:
        print(f"Sensor error: {e}")
    
    # Dummy data als sensor niet beschikbaar
    return {
        'temperature': 21.5,
        'humidity': 45.0,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'demo'
    }

@app.route('/')
def index():
    """Hoofdpagina"""
    return render_template('index.html')

@app.route('/api/sensor')
def get_sensor_data():
    """API endpoint voor sensor data"""
    data = read_sensor_data()
    return jsonify(data)

@app.route('/api/led/<int:led_num>/toggle', methods=['POST'])
def toggle_led(led_num):
    """Toggle LED aan/uit"""
    global led1_state, led2_state
    
    if led_num == 1:
        led1_state = not led1_state
        GPIO.output(LED1_PIN, GPIO.HIGH if led1_state else GPIO.LOW)
        return jsonify({'led': 1, 'state': led1_state})
    elif led_num == 2:
        led2_state = not led2_state
        GPIO.output(LED2_PIN, GPIO.HIGH if led2_state else GPIO.LOW)
        return jsonify({'led': 2, 'state': led2_state})
    
    return jsonify({'error': 'Invalid LED number'}), 400

@app.route('/api/led/<int:led_num>/state', methods=['POST'])
def set_led_state(led_num):
    """Zet LED naar specifieke state"""
    global led1_state, led2_state
    
    data = request.get_json()
    state = data.get('state', False)
    
    if led_num == 1:
        led1_state = state
        GPIO.output(LED1_PIN, GPIO.HIGH if state else GPIO.LOW)
        return jsonify({'led': 1, 'state': led1_state})
    elif led_num == 2:
        led2_state = state
        GPIO.output(LED2_PIN, GPIO.HIGH if state else GPIO.LOW)
        return jsonify({'led': 2, 'state': led2_state})
    
    return jsonify({'error': 'Invalid LED number'}), 400

@app.route('/api/status')
def get_status():
    """Status van alle GPIO pins"""
    return jsonify({
        'led1': led1_state,
        'led2': led2_state,
        'uptime': time.time()
    })

def cleanup():
    """Cleanup GPIO bij afsluiten"""
    GPIO.cleanup()
    print("GPIO cleanup compleet")

if __name__ == '__main__':
    try:
        print("=" * 50)
        print("Raspberry Pi Web Dashboard")
        print("=" * 50)
        print(f"LED 1: GPIO {LED1_PIN}")
        print(f"LED 2: GPIO {LED2_PIN}")
        print(f"DHT Sensor: GPIO {DHT_PIN}")
        print("=" * 50)
        print("\nServer gestart op http://0.0.0.0:5000")
        print("Druk Ctrl+C om te stoppen\n")
        
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\n\nServer gestopt")
    finally:
        cleanup()
