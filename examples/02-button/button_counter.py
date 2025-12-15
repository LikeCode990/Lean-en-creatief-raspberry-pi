#!/usr/bin/env python3
"""
Knop Teller met Event Detection
================================
Geavanceerder voorbeeld met event detection en een teller.

Hardware: Zelfde als button.py
"""

import RPi.GPIO as GPIO
import time

BUTTON_PIN = 17
LED_PIN = 18

# Globale teller
press_count = 0

def button_pressed_callback(channel):
    """Callback functie voor knop druk"""
    global press_count
    press_count += 1
    print(f"Knop ingedrukt! Totaal: {press_count} keer")
    
    # Laat LED kort knipperen
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(LED_PIN, GPIO.LOW)

def setup():
    """Initialiseer GPIO en events"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, GPIO.LOW)
    
    # Event detection op falling edge (knop indrukken)
    # bouncetime in ms voorkomt contact dender
    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, 
                         callback=button_pressed_callback, 
                         bouncetime=300)
    
    print("Knop teller gestart")
    print("Druk op de knop om te tellen (Ctrl+C om te stoppen)")

def main():
    """Hoofdfunctie"""
    setup()
    
    try:
        # Programma blijft draaien en wacht op events
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n\nFinale telling: {press_count} keer gedrukt")
        print("Programma gestopt")
    
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
