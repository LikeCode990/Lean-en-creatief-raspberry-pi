#!/usr/bin/env python3
"""
Ultrasonic Distance Sensor - HC-SR04
=====================================

Dit script leest afstand met een ultrasone sensor.
Demonstreert timing-kritische operaties en sensor interfacing.

Hardware:
- HC-SR04 Ultrasonic sensor
- TRIGGER pin -> GPIO 23
- ECHO pin -> GPIO 24 (via voltage divider: 1kΩ + 2kΩ)
- VCC -> 5V
- GND -> GND

Let op: ECHO pin geeft 5V output, gebruik voltage divider!

Lean principe: Herbruikbare sensor classe, modulair design
"""

import RPi.GPIO as GPIO
import time

class UltrasonicSensor:
    """Klasse voor HC-SR04 ultrasone afstandssensor"""
    
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        
        # Zorg dat trigger laag is
        GPIO.output(self.trigger_pin, GPIO.LOW)
        time.sleep(0.1)
    
    def get_distance(self):
        """
        Meet afstand in centimeters.
        Returns: afstand in cm, of None bij timeout
        """
        # Stuur trigger pulse (10μs)
        GPIO.output(self.trigger_pin, GPIO.HIGH)
        time.sleep(0.00001)  # 10 microseconden
        GPIO.output(self.trigger_pin, GPIO.LOW)
        
        # Wacht op echo start
        timeout = time.time() + 0.5  # 0.5s timeout
        while GPIO.input(self.echo_pin) == GPIO.LOW:
            pulse_start = time.time()
            if pulse_start > timeout:
                return None
        
        # Wacht op echo einde
        timeout = time.time() + 0.5
        while GPIO.input(self.echo_pin) == GPIO.HIGH:
            pulse_end = time.time()
            if pulse_end > timeout:
                return None
        
        # Bereken afstand
        pulse_duration = pulse_end - pulse_start
        # Geluidssnelheid: 343 m/s = 34300 cm/s
        # Afstand = (tijd × snelheid) / 2 (heen en terug)
        distance = (pulse_duration * 34300) / 2
        
        return round(distance, 2)
    
    def cleanup(self):
        """Cleanup GPIO"""
        GPIO.cleanup()

# Main programma
if __name__ == "__main__":
    TRIGGER_PIN = 23
    ECHO_PIN = 24
    
    sensor = UltrasonicSensor(TRIGGER_PIN, ECHO_PIN)
    
    print("Ultrasonic Distance Sensor gestart")
    print("Afstand wordt continu gemeten (druk Ctrl+C om te stoppen)")
    print()
    
    try:
        while True:
            distance = sensor.get_distance()
            
            if distance is not None:
                # Visuele indicator met sterren
                bars = int(distance / 5)  # 1 ster per 5 cm
                bar_display = '*' * min(bars, 50)
                
                print(f"Afstand: {distance:6.2f} cm | {bar_display}")
                
                # Waarschuwing bij korte afstand
                if distance < 10:
                    print("  ⚠️  OBJECT DICHTBIJ!")
            else:
                print("Fout: Geen echo ontvangen")
            
            time.sleep(0.5)  # Meet 2x per seconde
    
    except KeyboardInterrupt:
        print("\nProgramma gestopt door gebruiker")
    
    finally:
        sensor.cleanup()
        print("GPIO cleanup voltooid")
