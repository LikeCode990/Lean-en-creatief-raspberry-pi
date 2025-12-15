#!/usr/bin/env python3
"""
Basis LED Knipperen
===================
Dit voorbeeld laat een LED knipperen met een interval van 1 seconde.

Hardware:
- LED op GPIO 18
- 220Ω weerstand
- Breadboard en jumper draden

Aansluiting:
GPIO 18 → 220Ω weerstand → LED (+) → LED (-) → GND
"""

import RPi.GPIO as GPIO
import time

# Configuratie
LED_PIN = 18
BLINK_INTERVAL = 1  # seconden

def setup():
    """Initialiseer GPIO"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LED_PIN, GPIO.OUT)
    print("GPIO setup compleet")

def blink():
    """Laat LED knipperen"""
    print("LED knipperen gestart (Ctrl+C om te stoppen)")
    
    try:
        while True:
            GPIO.output(LED_PIN, GPIO.HIGH)
            print("LED AAN")
            time.sleep(BLINK_INTERVAL)
            
            GPIO.output(LED_PIN, GPIO.LOW)
            print("LED UIT")
            time.sleep(BLINK_INTERVAL)
            
    except KeyboardInterrupt:
        print("\nProgramma gestopt door gebruiker")
    
    finally:
        GPIO.cleanup()
        print("GPIO cleanup compleet")

def main():
    """Hoofdfunctie"""
    setup()
    blink()

if __name__ == "__main__":
    main()
