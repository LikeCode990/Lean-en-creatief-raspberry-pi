#!/usr/bin/env python3
"""
RGB LED Control - Geavanceerde PWM
===================================

Dit script bestuurt een RGB LED met PWM voor kleurmenging.
Demonstreert gebruik van meerdere PWM kanalen en kleurentheorie.

Hardware:
- Common cathode RGB LED
- GPIO 17 (Rood)
- GPIO 27 (Groen)  
- GPIO 22 (Blauw)
- 3x 220Ω weerstanden (één per kleur)

Creatief principe: Kleurmenging voor visuele feedback
"""

import RPi.GPIO as GPIO
import time

# GPIO pin configuratie
RED_PIN = 17
GREEN_PIN = 27
BLUE_PIN = 22

# PWM setup
PWM_FREQ = 1000  # 1000 Hz

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

# PWM objecten
red_pwm = GPIO.PWM(RED_PIN, PWM_FREQ)
green_pwm = GPIO.PWM(GREEN_PIN, PWM_FREQ)
blue_pwm = GPIO.PWM(BLUE_PIN, PWM_FREQ)

red_pwm.start(0)
green_pwm.start(0)
blue_pwm.start(0)

def set_color(red, green, blue):
    """Zet RGB kleur (waarden 0-100)"""
    red_pwm.ChangeDutyCycle(red)
    green_pwm.ChangeDutyCycle(green)
    blue_pwm.ChangeDutyCycle(blue)

def color_demo():
    """Demonstreer verschillende kleuren"""
    colors = [
        ("Rood", 100, 0, 0),
        ("Groen", 0, 100, 0),
        ("Blauw", 0, 0, 100),
        ("Geel", 100, 100, 0),
        ("Cyaan", 0, 100, 100),
        ("Magenta", 100, 0, 100),
        ("Wit", 100, 100, 100),
        ("Oranje", 100, 50, 0),
        ("Paars", 50, 0, 100),
    ]
    
    for name, r, g, b in colors:
        print(f"Kleur: {name}")
        set_color(r, g, b)
        time.sleep(1)

def rainbow_cycle():
    """Vloeiende regenboog overgang"""
    print("Rainbow cycle...")
    steps = 360
    for i in range(steps):
        # HSV naar RGB conversie (vereenvoudigd)
        if i < 60:
            r, g, b = 100, i * 100 // 60, 0
        elif i < 120:
            r, g, b = 100 - (i - 60) * 100 // 60, 100, 0
        elif i < 180:
            r, g, b = 0, 100, (i - 120) * 100 // 60
        elif i < 240:
            r, g, b = 0, 100 - (i - 180) * 100 // 60, 100
        elif i < 300:
            r, g, b = (i - 240) * 100 // 60, 0, 100
        else:
            r, g, b = 100, 0, 100 - (i - 300) * 100 // 60
        
        set_color(r, g, b)
        time.sleep(0.02)

try:
    print("RGB LED Control gestart (druk Ctrl+C om te stoppen)")
    
    while True:
        color_demo()
        rainbow_cycle()

except KeyboardInterrupt:
    print("\nProgramma gestopt door gebruiker")

finally:
    red_pwm.stop()
    green_pwm.stop()
    blue_pwm.stop()
    GPIO.cleanup()
    print("GPIO cleanup voltooid")
