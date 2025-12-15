#!/usr/bin/env python3
"""
LED Blink - Basis GPIO Voorbeeld
=================================

Dit script laat een LED knipperen met een regelmatig interval.
Dit is het "Hello World" van embedded programmering!

Hardware:
- LED verbonden aan GPIO 17
- 220Ω weerstand in serie met LED
- LED kathode (-) naar GND

Lean principe: Start simpel, test snel, itereer
"""

import RPi.GPIO as GPIO
import time

# GPIO pin configuratie
LED_PIN = 17

# GPIO setup
GPIO.setmode(GPIO.BCM)  # Gebruik BCM pin nummering
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    print("LED Blink gestart (druk Ctrl+C om te stoppen)")
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)  # LED aan
        print("LED AAN")
        time.sleep(1)  # Wacht 1 seconde
        
        GPIO.output(LED_PIN, GPIO.LOW)   # LED uit
        print("LED UIT")
        time.sleep(1)  # Wacht 1 seconde

except KeyboardInterrupt:
    print("\nProgramma gestopt door gebruiker")

finally:
    # Cleanup: zet GPIO pins terug naar default state
    GPIO.cleanup()
    print("GPIO cleanup voltooid")
