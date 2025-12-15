#!/usr/bin/env python3
"""
GPIO Zero LED Knipperen
=======================
Alternatieve implementatie van LED knipperen met GPIO Zero library.
Veel simpeler dan RPi.GPIO!

Hardware:
- LED op GPIO 18
- 220Ω weerstand

Aansluiting:
GPIO 18 → 220Ω weerstand → LED (+) → LED (-) → GND
"""

from gpiozero import LED
from time import sleep
from signal import pause

LED_PIN = 18
BLINK_INTERVAL = 1  # seconden

def method_1_manual():
    """Handmatig knipperen met loop"""
    print("Methode 1: Handmatig knipperen")
    led = LED(LED_PIN)
    
    try:
        while True:
            led.on()
            print("LED AAN")
            sleep(BLINK_INTERVAL)
            
            led.off()
            print("LED UIT")
            sleep(BLINK_INTERVAL)
            
    except KeyboardInterrupt:
        print("\nGestopt")
        led.close()

def method_2_blink():
    """Automatisch knipperen met blink() methode"""
    print("Methode 2: Automatisch met blink()")
    led = LED(LED_PIN)
    
    # blink(on_time, off_time)
    led.blink(on_time=BLINK_INTERVAL, off_time=BLINK_INTERVAL)
    
    print("LED knippert automatisch (Ctrl+C om te stoppen)")
    
    try:
        pause()  # Wacht oneindig
    except KeyboardInterrupt:
        print("\nGestopt")
        led.close()

def method_3_toggle():
    """Knipperen met toggle"""
    print("Methode 3: Toggle methode")
    led = LED(LED_PIN)
    
    try:
        while True:
            led.toggle()  # Schakel LED om (aan→uit of uit→aan)
            status = "AAN" if led.is_lit else "UIT"
            print(f"LED {status}")
            sleep(BLINK_INTERVAL)
            
    except KeyboardInterrupt:
        print("\nGestopt")
        led.close()

def main():
    """Hoofdfunctie - kies een methode"""
    print("GPIO Zero LED Knipperen")
    print("=" * 40)
    print("\nKies een methode:")
    print("1. Handmatig knipperen")
    print("2. Automatisch blink()")
    print("3. Toggle methode")
    
    choice = input("\nKeuze (1-3): ")
    
    if choice == "1":
        method_1_manual()
    elif choice == "2":
        method_2_blink()
    elif choice == "3":
        method_3_toggle()
    else:
        print("Ongeldige keuze")

if __name__ == "__main__":
    main()
