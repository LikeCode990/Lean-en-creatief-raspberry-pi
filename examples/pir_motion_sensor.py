#!/usr/bin/env python3
"""
PIR Motion Sensor
=================
Detecteer beweging met een PIR (Passive Infrared) sensor.

Hardware:
- PIR sensor (HC-SR501 of vergelijkbaar)

Aansluiting:
- VCC → Pin 2 (5V)
- GND → Pin 6 (Ground)  
- OUT → Pin 11 (GPIO 17)

Opmerking: Sommige PIR sensoren hebben potentiometers voor:
- Sensitivity (gevoeligheid)
- Time delay (hoe lang output HIGH blijft)
"""

from gpiozero import MotionSensor
from datetime import datetime
from signal import pause
import time

# GPIO configuratie
PIR_PIN = 17

# Statistieken
detection_count = 0
start_time = time.time()

def log_event(message):
    """Print event met timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def motion_detected():
    """Callback functie wanneer beweging wordt gedetecteerd."""
    global detection_count
    detection_count += 1
    log_event(f"🔴 Beweging gedetecteerd! (#{detection_count})")

def no_motion():
    """Callback functie wanneer beweging stopt."""
    log_event("🟢 Geen beweging meer")

def print_statistics():
    """Print statistieken over detecties."""
    elapsed = time.time() - start_time
    elapsed_minutes = elapsed / 60
    print(f"\n📊 Statistieken:")
    print(f"   Aantal detecties: {detection_count}")
    print(f"   Looptijd: {elapsed_minutes:.1f} minuten")
    if elapsed_minutes > 0:
        print(f"   Detecties/minuut: {detection_count/elapsed_minutes:.1f}")

def main():
    """Hoofdprogramma voor bewegingsdetectie."""
    print("PIR Bewegingssensor Monitor")
    print("=" * 50)
    print("Wacht op sensor initialisatie (±30 seconden)...")
    
    # Initialiseer PIR sensor
    pir = MotionSensor(PIR_PIN)
    
    # Wacht tot sensor gestabiliseerd is
    time.sleep(2)
    
    # Registreer callback functies
    pir.when_motion = motion_detected
    pir.when_no_motion = no_motion
    
    log_event("✅ PIR sensor actief en klaar!")
    print("Druk op Ctrl+C om te stoppen\n")
    
    try:
        pause()  # Wacht op events
    except KeyboardInterrupt:
        print("\n\nProgramma gestopt.")
        print_statistics()

if __name__ == "__main__":
    main()
