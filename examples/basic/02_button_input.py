#!/usr/bin/env python3
"""
Button Input - Input Verwerking
================================

Dit script leest een drukknop en gebruikt de input om een LED te besturen.
Demonstreert basis input/output interactie.

Hardware:
- LED verbonden aan GPIO 17
- 220Ω weerstand in serie met LED
- Drukknop verbonden aan GPIO 27
- 10kΩ pull-down weerstand op button pin
- Button tussen GPIO 27 en 3.3V

Lean principe: Eenvoudige feedback loop, directe response
"""

import RPi.GPIO as GPIO
import time

# GPIO pin configuratie
LED_PIN = 17
BUTTON_PIN = 27

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# LED state
led_state = False

print("Button Input gestart (druk Ctrl+C om te stoppen)")
print("Druk op de knop om LED aan/uit te schakelen")

try:
    previous_button_state = False
    
    while True:
        # Lees button state
        button_state = GPIO.input(BUTTON_PIN)
        
        # Detecteer button press (rising edge)
        if button_state and not previous_button_state:
            led_state = not led_state  # Toggle LED
            GPIO.output(LED_PIN, led_state)
            
            if led_state:
                print("Button ingedrukt - LED AAN")
            else:
                print("Button ingedrukt - LED UIT")
            
            time.sleep(0.2)  # Debounce delay
        
        previous_button_state = button_state
        time.sleep(0.01)  # Kleine delay om CPU te sparen

except KeyboardInterrupt:
    print("\nProgramma gestopt door gebruiker")

finally:
    GPIO.cleanup()
    print("GPIO cleanup voltooid")
