#!/usr/bin/env python3
"""
HC-SR04 Distance Sensor - Enhanced Terminal Debug
==================================================
Uitgebreide debug versie met gedetailleerde logging voor troubleshooting.

Hardware:
- HC-SR04 ultrasone sensor
- Voltage divider (1kΩ + 2kΩ)

Aansluiting:
- VCC  → Pin 2 (5V)
- GND  → Pin 6 (Ground)
- TRIG → Pin 16 (GPIO 23)
- ECHO → Voltage Divider → Pin 18 (GPIO 24)
"""

import RPi.GPIO as GPIO
import time
from datetime import datetime
import statistics

# GPIO pins
TRIG_PIN = 23
ECHO_PIN = 24

# Constanten
SOUND_SPEED = 34300  # cm/s bij 20°C

# Debug statistieken
measurements = []
errors = {"timeout": 0, "out_of_range": 0}
total_readings = 0

def setup():
    """Initialiseer GPIO pins met debug output."""
    print("🔧 GPIO Setup wordt gestart...")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    GPIO.output(TRIG_PIN, False)
    
    print(f"   ✓ TRIG pin (GPIO {TRIG_PIN}) geconfigureerd als OUTPUT")
    print(f"   ✓ ECHO pin (GPIO {ECHO_PIN}) geconfigureerd als INPUT")
    print("   ⏳ Wacht 2 seconden voor sensor stabilisatie...")
    time.sleep(2)
    print("   ✓ Sensor gestabiliseerd\n")

def measure_distance_debug():
    """
    Meet afstand met uitgebreide debug informatie.
    
    Returns:
        dict: {'distance': float, 'pulse_duration': float, 'status': str}
    """
    result = {
        'distance': None,
        'pulse_duration': None,
        'status': 'unknown',
        'timestamp': datetime.now().strftime("%H:%M:%S.%f")[:-3]
    }
    
    # Stuur trigger pulse
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    
    # Wacht op echo start
    timeout_start = time.time() + 0.1
    pulse_start = time.time()
    
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
        if pulse_start > timeout_start:
            result['status'] = 'timeout_waiting_echo_start'
            return result
    
    # Wacht op echo einde
    timeout_end = time.time() + 0.1
    pulse_end = time.time()
    
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()
        if pulse_end > timeout_end:
            result['status'] = 'timeout_waiting_echo_end'
            return result
    
    # Bereken afstand
    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * SOUND_SPEED) / 2
    
    result['pulse_duration'] = pulse_duration * 1000000  # microseconden
    result['distance'] = distance
    
    if 2 <= distance <= 400:
        result['status'] = 'success'
    else:
        result['status'] = 'out_of_range'
    
    return result

def print_measurement(result, show_details=True):
    """Print meting met kleuren en details."""
    global total_readings, measurements, errors
    
    total_readings += 1
    timestamp = result['timestamp']
    
    if result['status'] == 'success':
        distance = result['distance']
        measurements.append(distance)
        
        # Behoud laatste 50 metingen
        if len(measurements) > 50:
            measurements.pop(0)
        
        # Kleur indicatie
        if distance < 10:
            indicator = "🔴 ZEER DICHTBIJ"
        elif distance < 30:
            indicator = "🟡 DICHTBIJ"
        elif distance < 100:
            indicator = "🟢 NORMAAL"
        else:
            indicator = "🔵 VER WEG"
        
        print(f"[{timestamp}] 📏 {distance:6.1f} cm  |  {indicator}", end="")
        
        if show_details and result['pulse_duration']:
            print(f"  |  Pulse: {result['pulse_duration']:.1f}μs", end="")
        
        print()
        
    elif 'timeout' in result['status']:
        errors['timeout'] += 1
        print(f"[{timestamp}] ❌ TIMEOUT: {result['status']}")
        print(f"             💡 Controleer: Is er een object binnen bereik?")
        
    elif result['status'] == 'out_of_range':
        errors['out_of_range'] += 1
        print(f"[{timestamp}] ⚠️  BUITEN BEREIK: {result['distance']:.1f} cm")
        print(f"             💡 Bereik moet tussen 2-400 cm zijn")
    
    else:
        print(f"[{timestamp}] ❓ ONBEKENDE STATUS: {result['status']}")

def print_statistics():
    """Print statistieken over metingen."""
    print("\n" + "="*70)
    print("📊 STATISTIEKEN")
    print("="*70)
    print(f"Totaal metingen:     {total_readings}")
    print(f"Succesvolle metingen: {len(measurements)}")
    print(f"Timeout errors:      {errors['timeout']}")
    print(f"Buiten bereik:       {errors['out_of_range']}")
    
    if measurements:
        print(f"\n📈 AFSTAND STATISTIEKEN (laatste {len(measurements)} metingen):")
        print(f"   Min:      {min(measurements):.1f} cm")
        print(f"   Max:      {max(measurements):.1f} cm")
        print(f"   Gemiddeld: {statistics.mean(measurements):.1f} cm")
        print(f"   Mediaan:  {statistics.median(measurements):.1f} cm")
        if len(measurements) > 1:
            print(f"   Std Dev:  {statistics.stdev(measurements):.1f} cm")
    
    success_rate = (len(measurements) / total_readings * 100) if total_readings > 0 else 0
    print(f"\n✓ Success Rate: {success_rate:.1f}%")
    print("="*70 + "\n")

def cleanup():
    """Ruim GPIO resources op."""
    GPIO.cleanup()
    print("\n🔧 GPIO cleanup voltooid")

def main():
    """Hoofdprogramma met debug interface."""
    print("="*70)
    print("         HC-SR04 DISTANCE SENSOR - DEBUG MODE")
    print("="*70)
    print("\n⚡ Debug features:")
    print("   • Uitgebreide error logging")
    print("   • Pulse duration metingen")
    print("   • Real-time statistieken")
    print("   • Timestamp per meting")
    print("\n💡 Tips:")
    print("   • Controleer voltage divider (1kΩ + 2kΩ)")
    print("   • Zorg voor vrij zicht (geen obstakels)")
    print("   • Sensor werkt best tussen 10-300 cm")
    print("\n" + "="*70 + "\n")
    
    setup()
    
    measurement_count = 0
    
    try:
        print("🚀 Start metingen... (Ctrl+C om te stoppen)\n")
        
        while True:
            result = measure_distance_debug()
            print_measurement(result, show_details=True)
            
            measurement_count += 1
            
            # Toon statistieken elke 20 metingen
            if measurement_count % 20 == 0:
                print_statistics()
            
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Programma gestopt door gebruiker")
        print_statistics()
    
    except Exception as e:
        print(f"\n\n💥 ONVERWACHTE FOUT: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        cleanup()

if __name__ == "__main__":
    main()
