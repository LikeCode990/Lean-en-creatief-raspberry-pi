#!/usr/bin/env python3
"""
Knop en LED
===========
Dit voorbeeld toont hoe je een knop uitleest en een LED aanstuurt.
Wanneer de knop wordt ingedrukt, gaat de LED aan.

Hardware:
- LED op GPIO 18
- Knop op GPIO 17
- 220Ω weerstand voor LED
- Pull-up weerstand (intern gebruikt)

Aansluiting Knop:
GPIO 17 → Knop → GND
(Interne pull-up weerstand wordt gebruikt)

Aansluiting LED:
GPIO 18 → 220Ω weerstand → LED (+) → LED (-) → GND
"""

import RPi.GPIO as GPIO
import time

# Configuratie
BUTTON_PIN = 17
LED_PIN = 18
DEBOUNCE_TIME = 0.01  # 10ms debounce

def setup():
    """Initialiseer GPIO"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Knop als input met pull-up weerstand
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # LED als output
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, GPIO.LOW)
    
    print("GPIO setup compleet")
    print("Druk op de knop om de LED te bedienen")

def main():
    """Hoofdfunctie"""
    setup()
    
    try:
        while True:
            # Lees knop status (LOW = ingedrukt vanwege pull-up)
            button_state = GPIO.input(BUTTON_PIN)
            
            if button_state == GPIO.LOW:
                GPIO.output(LED_PIN, GPIO.HIGH)
                print("Knop INGEDRUKT - LED AAN")
            else:
                GPIO.output(LED_PIN, GPIO.LOW)
                print("Knop LOSGELATEN - LED UIT")
            
            time.sleep(DEBOUNCE_TIME)
            
    except KeyboardInterrupt:
        print("\nProgramma gestopt door gebruiker")
    
    finally:
        GPIO.cleanup()
        print("GPIO cleanup compleet")

if __name__ == "__main__":
    main()
