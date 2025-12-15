#!/usr/bin/env python3
"""
PWM LED Fade - Pulse Width Modulation
======================================

Dit script gebruikt PWM om een LED vloeiend te laten in- en uitfaden.
Demonstreert analoge output simulatie met digitale signalen.

Hardware:
- LED verbonden aan GPIO 18 (PWM capable pin)
- 220Ω weerstand in serie met LED
- LED kathode naar GND

PWM Frequentie: 1000 Hz
Duty Cycle: 0-100%

Creatief principe: Gebruik van PWM voor vloeiende overgangen
"""

import RPi.GPIO as GPIO
import time

# GPIO pin configuratie
LED_PIN = 18

# PWM parameters
PWM_FREQUENCY = 1000  # 1000 Hz

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# PWM setup
pwm = GPIO.PWM(LED_PIN, PWM_FREQUENCY)
pwm.start(0)  # Start met 0% duty cycle (uit)

print("PWM LED Fade gestart (druk Ctrl+C om te stoppen)")

try:
    while True:
        # Fade in (0% naar 100%)
        print("Fading in...")
        for duty_cycle in range(0, 101, 1):
            pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(0.02)  # 20ms per stap
        
        time.sleep(0.5)  # Pauze op maximale helderheid
        
        # Fade out (100% naar 0%)
        print("Fading out...")
        for duty_cycle in range(100, -1, -1):
            pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(0.02)
        
        time.sleep(0.5)  # Pauze op minimale helderheid

except KeyboardInterrupt:
    print("\nProgramma gestopt door gebruiker")

finally:
    pwm.stop()
    GPIO.cleanup()
    print("GPIO cleanup voltooid")
