#!/usr/bin/env python3
"""
PWM LED Fade
============
Dit voorbeeld laat een LED geleidelijk in en uit faden met PWM.

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
PWM_FREQUENCY = 100  # Hz
FADE_STEPS = 100
FADE_DELAY = 0.02  # seconden per stap

def setup():
    """Initialiseer GPIO en PWM"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LED_PIN, GPIO.OUT)
    
    # Maak PWM object
    pwm = GPIO.PWM(LED_PIN, PWM_FREQUENCY)
    pwm.start(0)  # Start met 0% duty cycle (uit)
    
    print("PWM setup compleet")
    return pwm

def fade_in(pwm):
    """Fade LED geleidelijk aan"""
    for duty_cycle in range(0, 101, 1):
        pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(FADE_DELAY)

def fade_out(pwm):
    """Fade LED geleidelijk uit"""
    for duty_cycle in range(100, -1, -1):
        pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(FADE_DELAY)

def pulse(pwm):
    """Laat LED pulseren (in en uit)"""
    fade_in(pwm)
    fade_out(pwm)

def main():
    """Hoofdfunctie"""
    pwm = setup()
    
    print("LED fade gestart (Ctrl+C om te stoppen)")
    
    try:
        while True:
            print("Fade in...")
            fade_in(pwm)
            
            print("Fade out...")
            fade_out(pwm)
            
            time.sleep(0.5)  # Korte pauze tussen pulsen
            
    except KeyboardInterrupt:
        print("\nProgramma gestopt door gebruiker")
    
    finally:
        pwm.stop()
        GPIO.cleanup()
        print("PWM gestopt en GPIO cleanup compleet")

if __name__ == "__main__":
    main()
