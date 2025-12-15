#!/usr/bin/env python3
"""
HC-SR04 Ultrasonic Distance Sensor
===================================
Een eenvoudig voorbeeld van het uitlezen van een HC-SR04 afstandssensor.

⚠️ BELANGRIJK: ECHO pin geeft 5V output! Gebruik een voltage divider:
   ECHO → 1kΩ → GPIO 24 → 2kΩ → GND

Hardware:
- HC-SR04 ultrasone sensor
- 1kΩ resistor
- 2kΩ resistor (voor voltage divider)

Aansluiting:
- VCC  → Pin 2 (5V)
- GND  → Pin 6 (Ground)
- TRIG → Pin 16 (GPIO 23)
- ECHO → Voltage Divider → Pin 18 (GPIO 24)
"""

import RPi.GPIO as GPIO
import time

# GPIO pins
TRIG_PIN = 23
ECHO_PIN = 24

# Constanten
SOUND_SPEED = 34300  # cm/s bij 20°C

def setup():
    """Initialiseer GPIO pins."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.1)  # Laat sensor stabiliseren

def read_sensor():
    """
    Meet de afstand met de HC-SR04 sensor.
    
    Returns:
        float: Afstand in centimeters, of None bij timeout
    """
    # Stuur 10μs trigger pulse
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    
    # Wacht op echo start
    timeout = time.time() + 0.1  # 100ms timeout
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
        if pulse_start > timeout:
            return None
    
    # Wacht op echo einde
    timeout = time.time() + 0.1
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()
        if pulse_end > timeout:
            return None
    
    # Bereken afstand
    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * SOUND_SPEED) / 2
    
    return distance

def cleanup():
    """Ruim GPIO resources op."""
    GPIO.cleanup()

def main():
    """Hoofdprogramma voor continue afstandsmeting."""
    print("HC-SR04 Afstandssensor Monitor")
    print("=" * 40)
    print("Bereik: 2-400 cm")
    print("Druk op Ctrl+C om te stoppen\n")
    
    setup()
    
    try:
        while True:
            distance = read_sensor()
            
            if distance is not None:
                if 2 <= distance <= 400:
                    print(f"Afstand: {distance:.1f} cm", end="")
                    
                    # Visuele indicator
                    if distance < 10:
                        print("  🔴 ZEER DICHTBIJ!")
                    elif distance < 30:
                        print("  🟡 Dichtbij")
                    else:
                        print("  🟢")
                else:
                    print(f"⚠️  Afstand buiten bereik: {distance:.1f} cm")
            else:
                print("❌ Timeout - Geen object gedetecteerd")
            
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\n\nProgramma gestopt.")
    finally:
        cleanup()

if __name__ == "__main__":
    main()
