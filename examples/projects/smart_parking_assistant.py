#!/usr/bin/env python3
"""
Smart Parking Assistant - Complete Project
===========================================

Een slim parkeerhulp systeem dat afstand meet en visuele + audio feedback geeft.
Combineert ultrasone sensor, RGB LED en buzzer voor intuïtieve gebruikerservaring.

Hardware:
- HC-SR04 ultrasone sensor (TRIGGER: GPIO 23, ECHO: GPIO 24)
- RGB LED (R: GPIO 17, G: GPIO 27, B: GPIO 22)
- Passive buzzer (GPIO 13)
- Weerstanden en voltage divider volgens schema

Functies:
- Afstand meting in real-time
- Kleurgecodeerde feedback (groen -> geel -> rood)
- Audio waarschuwing bij te korte afstand
- LED knippert sneller naarmate object dichterbij komt

Lean & Creatief:
- Modulair design met herbruikbare componenten
- Iteratieve verbetering mogelijk (toevoegen display, etc.)
- Intuïtieve gebruikersinterface
"""

import RPi.GPIO as GPIO
import time

# Pin configuratie
TRIGGER_PIN = 23
ECHO_PIN = 24
RED_PIN = 17
GREEN_PIN = 27
BLUE_PIN = 22
BUZZER_PIN = 13

# Constanten
PWM_FREQ = 1000
SAFE_DISTANCE = 50  # cm
WARNING_DISTANCE = 20  # cm
DANGER_DISTANCE = 10  # cm

class ParkingAssistant:
    """Smart Parking Assistant systeem"""
    
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self._setup_ultrasonic()
        self._setup_rgb_led()
        self._setup_buzzer()
    
    def _setup_ultrasonic(self):
        """Setup ultrasone sensor"""
        GPIO.setup(TRIGGER_PIN, GPIO.OUT)
        GPIO.setup(ECHO_PIN, GPIO.IN)
        GPIO.output(TRIGGER_PIN, GPIO.LOW)
    
    def _setup_rgb_led(self):
        """Setup RGB LED met PWM"""
        GPIO.setup(RED_PIN, GPIO.OUT)
        GPIO.setup(GREEN_PIN, GPIO.OUT)
        GPIO.setup(BLUE_PIN, GPIO.OUT)
        
        self.red_pwm = GPIO.PWM(RED_PIN, PWM_FREQ)
        self.green_pwm = GPIO.PWM(GREEN_PIN, PWM_FREQ)
        self.blue_pwm = GPIO.PWM(BLUE_PIN, PWM_FREQ)
        
        self.red_pwm.start(0)
        self.green_pwm.start(0)
        self.blue_pwm.start(0)
    
    def _setup_buzzer(self):
        """Setup buzzer"""
        GPIO.setup(BUZZER_PIN, GPIO.OUT)
        self.buzzer_pwm = GPIO.PWM(BUZZER_PIN, 2000)  # 2kHz tone
    
    def measure_distance(self):
        """Meet afstand met ultrasone sensor"""
        GPIO.output(TRIGGER_PIN, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(TRIGGER_PIN, GPIO.LOW)
        
        timeout = time.time() + 0.5
        while GPIO.input(ECHO_PIN) == GPIO.LOW:
            pulse_start = time.time()
            if pulse_start > timeout:
                return None
        
        timeout = time.time() + 0.5
        while GPIO.input(ECHO_PIN) == GPIO.HIGH:
            pulse_end = time.time()
            if pulse_end > timeout:
                return None
        
        pulse_duration = pulse_end - pulse_start
        distance = (pulse_duration * 34300) / 2
        return round(distance, 2)
    
    def set_color(self, red, green, blue):
        """Zet RGB LED kleur"""
        self.red_pwm.ChangeDutyCycle(red)
        self.green_pwm.ChangeDutyCycle(green)
        self.blue_pwm.ChangeDutyCycle(blue)
    
    def beep(self, duration=0.1):
        """Maak een beep geluid"""
        self.buzzer_pwm.start(50)  # 50% duty cycle
        time.sleep(duration)
        self.buzzer_pwm.stop()
    
    def get_feedback(self, distance):
        """
        Bepaal feedback gebaseerd op afstand.
        Returns: (color, beep_interval, blink_speed)
        """
        if distance >= SAFE_DISTANCE:
            # Groen - veilig
            return (0, 100, 0), None, None
        elif distance >= WARNING_DISTANCE:
            # Geel - waarschuwing
            return (100, 100, 0), 1.0, 0.5
        elif distance >= DANGER_DISTANCE:
            # Oranje - let op
            return (100, 50, 0), 0.5, 0.25
        else:
            # Rood - gevaar
            return (100, 0, 0), 0.2, 0.15
    
    def display_status(self, distance):
        """Toon status op console"""
        bars = '█' * int((100 - min(distance, 100)) / 2)
        status = "VEILIG"
        
        if distance < WARNING_DISTANCE:
            status = "WAARSCHUWING"
        if distance < DANGER_DISTANCE:
            status = "GEVAAR!"
        
        print(f"Afstand: {distance:5.1f} cm | {bars:50s} | {status}")
    
    def run(self):
        """Hoofd programma loop"""
        print("=" * 60)
        print("Smart Parking Assistant - Gestart")
        print("=" * 60)
        print(f"Veilige afstand: > {SAFE_DISTANCE} cm (Groen)")
        print(f"Waarschuwing:    < {WARNING_DISTANCE} cm (Geel/Oranje)")
        print(f"Gevaar:          < {DANGER_DISTANCE} cm (Rood)")
        print("\nDruk Ctrl+C om te stoppen\n")
        
        try:
            last_beep = 0
            
            while True:
                distance = self.measure_distance()
                
                if distance is not None and distance < 200:  # Filter onrealistische waarden
                    # Bepaal feedback
                    color, beep_interval, blink_speed = self.get_feedback(distance)
                    
                    # Zet LED kleur
                    self.set_color(*color)
                    
                    # Beep indien nodig
                    if beep_interval and (time.time() - last_beep) > beep_interval:
                        self.beep(0.05)
                        last_beep = time.time()
                    
                    # Toon status
                    self.display_status(distance)
                    
                    # Wacht tijd afhankelijk van afstand
                    if blink_speed:
                        time.sleep(blink_speed)
                    else:
                        time.sleep(0.2)
                else:
                    # Geen object gedetecteerd
                    self.set_color(0, 0, 0)  # LED uit
                    print("Geen object gedetecteerd")
                    time.sleep(0.5)
        
        except KeyboardInterrupt:
            print("\n\nProgramma gestopt door gebruiker")
    
    def cleanup(self):
        """Cleanup alle resources"""
        self.set_color(0, 0, 0)
        self.red_pwm.stop()
        self.green_pwm.stop()
        self.blue_pwm.stop()
        self.buzzer_pwm.stop()
        GPIO.cleanup()
        print("GPIO cleanup voltooid")

# Main
if __name__ == "__main__":
    assistant = ParkingAssistant()
    
    try:
        assistant.run()
    finally:
        assistant.cleanup()
