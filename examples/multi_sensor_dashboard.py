#!/usr/bin/env python3
"""
Multi-Sensor Dashboard
======================
Een uitgebreid voorbeeld dat meerdere sensoren combineert en data logt.

Sensoren:
- DHT22: Temperatuur & Luchtvochtigheid
- HC-SR04: Afstand
- PIR: Beweging

Dit script demonstreert:
- Werken met meerdere sensoren tegelijk
- Data logging naar bestand
- Error handling
- Clean shutdown
"""

import RPi.GPIO as GPIO
import Adafruit_DHT
import time
from datetime import datetime
from gpiozero import MotionSensor
import json
import os

# ====== CONFIGURATIE ======
# DHT22
DHT_PIN = 4
DHT_SENSOR = Adafruit_DHT.DHT22

# HC-SR04
TRIG_PIN = 23
ECHO_PIN = 24

# PIR
PIR_PIN = 17

# Logging
LOG_FILE = "sensor_data.json"
LOG_INTERVAL = 10  # seconden

# ====== GLOBALS ======
motion_detected_flag = False
sensor_data = []

# ====== HC-SR04 FUNCTIES ======
def setup_ultrasonic():
    """Setup HC-SR04 sensor."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    GPIO.output(TRIG_PIN, False)

def measure_distance():
    """Meet afstand met HC-SR04."""
    try:
        GPIO.output(TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(TRIG_PIN, False)
        
        timeout = time.time() + 0.1
        while GPIO.input(ECHO_PIN) == 0:
            pulse_start = time.time()
            if pulse_start > timeout:
                return None
        
        timeout = time.time() + 0.1
        while GPIO.input(ECHO_PIN) == 1:
            pulse_end = time.time()
            if pulse_end > timeout:
                return None
        
        duration = pulse_end - pulse_start
        distance = (duration * 34300) / 2
        
        if 2 <= distance <= 400:
            return round(distance, 1)
        return None
    except:
        return None

# ====== DHT22 FUNCTIES ======
def read_dht22():
    """Lees DHT22 sensor."""
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        return {
            'temperature': round(temperature, 1),
            'humidity': round(humidity, 1)
        }
    return None

# ====== PIR FUNCTIES ======
def on_motion():
    """Callback bij beweging."""
    global motion_detected_flag
    motion_detected_flag = True

def setup_pir():
    """Setup PIR sensor."""
    pir = MotionSensor(PIR_PIN)
    pir.when_motion = on_motion
    return pir

# ====== DATA LOGGING ======
def log_data(data):
    """Log sensor data naar JSON bestand."""
    try:
        # Lees bestaande data
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                existing_data = json.load(f)
        else:
            existing_data = []
        
        # Voeg nieuwe data toe
        existing_data.append(data)
        
        # Behoud alleen laatste 1000 entries
        if len(existing_data) > 1000:
            existing_data = existing_data[-1000:]
        
        # Schrijf terug
        with open(LOG_FILE, 'w') as f:
            json.dump(existing_data, f, indent=2)
            
        return True
    except Exception as e:
        print(f"❌ Log error: {e}")
        return False

# ====== DISPLAY FUNCTIES ======
def clear_screen():
    """Clear terminal."""
    os.system('clear' if os.name == 'posix' else 'cls')

def display_dashboard(data):
    """Toon sensor data op scherm."""
    clear_screen()
    print("=" * 60)
    print("         MULTI-SENSOR DASHBOARD")
    print("=" * 60)
    print(f"\n⏰ Tijd: {data['timestamp']}\n")
    
    # Temperatuur & Luchtvochtigheid
    if data.get('dht22'):
        dht = data['dht22']
        print(f"🌡️  Temperatuur:      {dht['temperature']:.1f}°C")
        print(f"💧 Luchtvochtigheid: {dht['humidity']:.1f}%")
    else:
        print("🌡️  Temperatuur:      Niet beschikbaar")
        print("💧 Luchtvochtigheid: Niet beschikbaar")
    
    # Afstand
    if data.get('distance'):
        print(f"📏 Afstand:          {data['distance']:.1f} cm")
    else:
        print("📏 Afstand:          Niet beschikbaar")
    
    # Beweging
    motion_status = "🔴 JA" if data.get('motion') else "🟢 NEE"
    print(f"👁️  Beweging:         {motion_status}")
    
    print("\n" + "=" * 60)
    print("Druk op Ctrl+C om te stoppen")

# ====== MAIN ======
def main():
    """Hoofdprogramma."""
    global motion_detected_flag
    
    print("Multi-Sensor Dashboard wordt gestart...")
    print("Initialiseren...")
    
    # Setup
    setup_ultrasonic()
    pir = setup_pir()
    time.sleep(2)
    
    print("✅ Alle sensoren geïnitialiseerd!")
    time.sleep(1)
    
    last_log_time = time.time()
    
    try:
        while True:
            # Verzamel data
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            data = {
                'timestamp': timestamp,
                'dht22': read_dht22(),
                'distance': measure_distance(),
                'motion': motion_detected_flag
            }
            
            # Reset motion flag
            motion_detected_flag = False
            
            # Toon dashboard
            display_dashboard(data)
            
            # Log data periodiek
            current_time = time.time()
            if current_time - last_log_time >= LOG_INTERVAL:
                if log_data(data):
                    print(f"\n💾 Data gelogd naar {LOG_FILE}")
                last_log_time = current_time
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Programma gestopt.")
        print(f"📁 Sensor data opgeslagen in: {LOG_FILE}")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
