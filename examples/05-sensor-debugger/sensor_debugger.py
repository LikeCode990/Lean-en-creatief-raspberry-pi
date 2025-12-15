#!/usr/bin/env python3
"""
Sensor Debugger - Universele Sensor Debug Tool
==============================================
Debug tool voor het testen en diagnosticeren van verschillende sensoren.

Features:
- Test DHT11/DHT22 sensoren
- Test HC-SR04 ultrasone sensor
- Test PIR bewegingssensor
- Test I2C devices
- GPIO pin test
- Automatische probleem detectie
- Gedetailleerde output voor troubleshooting

Gebruik:
    python3 sensor_debugger.py
"""

import RPi.GPIO as GPIO
import time
import sys
from datetime import datetime

class SensorDebugger:
    """Universele sensor debugger"""
    
    def __init__(self):
        self.test_results = []
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
    def log(self, message, level="INFO"):
        """Log bericht met timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {
            "INFO": "ℹ️ ",
            "SUCCESS": "✅",
            "ERROR": "❌",
            "WARNING": "⚠️ ",
            "TEST": "🔍"
        }.get(level, "  ")
        
        print(f"[{timestamp}] {prefix} {message}")
        self.test_results.append((timestamp, level, message))
    
    def test_gpio_pin(self, pin, mode="output"):
        """Test individuele GPIO pin"""
        self.log(f"Test GPIO pin {pin} ({mode})", "TEST")
        
        try:
            if mode == "output":
                GPIO.setup(pin, GPIO.OUT)
                
                # Test HIGH
                GPIO.output(pin, GPIO.HIGH)
                self.log(f"  Pin {pin} gezet naar HIGH", "INFO")
                time.sleep(0.5)
                
                # Test LOW
                GPIO.output(pin, GPIO.LOW)
                self.log(f"  Pin {pin} gezet naar LOW", "INFO")
                time.sleep(0.5)
                
                self.log(f"GPIO pin {pin} werkt correct (output)", "SUCCESS")
                return True
                
            elif mode == "input":
                GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                state = GPIO.input(pin)
                self.log(f"  Pin {pin} status: {'HIGH' if state else 'LOW'}", "INFO")
                self.log(f"GPIO pin {pin} leesbaar (input)", "SUCCESS")
                return True
                
        except Exception as e:
            self.log(f"GPIO pin {pin} test MISLUKT: {e}", "ERROR")
            return False
    
    def test_dht_sensor(self, pin=4, sensor_type="DHT22"):
        """Test DHT11/DHT22 sensor"""
        self.log(f"Test {sensor_type} sensor op GPIO {pin}", "TEST")
        
        try:
            import Adafruit_DHT
            
            sensor_map = {
                "DHT11": Adafruit_DHT.DHT11,
                "DHT22": Adafruit_DHT.DHT22,
                "AM2302": Adafruit_DHT.AM2302
            }
            
            sensor = sensor_map.get(sensor_type, Adafruit_DHT.DHT22)
            
            self.log("  Poging 1: Sensor uitlezen...", "INFO")
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin, retries=3)
            
            if humidity is not None and temperature is not None:
                self.log(f"  Temperatuur: {temperature:.1f}°C", "INFO")
                self.log(f"  Luchtvochtigheid: {humidity:.1f}%", "INFO")
                
                # Validatie ranges
                if -40 <= temperature <= 80 and 0 <= humidity <= 100:
                    self.log(f"{sensor_type} werkt correct!", "SUCCESS")
                    return True
                else:
                    self.log(f"Waarden buiten normale range - check sensor", "WARNING")
                    return False
            else:
                self.log("Geen data van sensor ontvangen", "ERROR")
                self.log("Mogelijke oorzaken:", "INFO")
                self.log("  - Sensor niet aangesloten", "INFO")
                self.log("  - Verkeerde pin (check GPIO nummer)", "INFO")
                self.log("  - Defecte sensor", "INFO")
                self.log("  - Geen pull-up weerstand (10kΩ nodig)", "INFO")
                return False
                
        except ImportError:
            self.log("Adafruit_DHT library niet geïnstalleerd", "ERROR")
            self.log("Installeer met: sudo pip3 install Adafruit-DHT", "INFO")
            return False
        except Exception as e:
            self.log(f"DHT sensor test MISLUKT: {e}", "ERROR")
            return False
    
    def test_ultrasonic_sensor(self, trig_pin=23, echo_pin=24):
        """Test HC-SR04 ultrasone sensor"""
        self.log(f"Test HC-SR04 sensor (TRIG={trig_pin}, ECHO={echo_pin})", "TEST")
        
        try:
            GPIO.setup(trig_pin, GPIO.OUT)
            GPIO.setup(echo_pin, GPIO.IN)
            
            # Zorg dat trigger LOW is
            GPIO.output(trig_pin, GPIO.LOW)
            time.sleep(0.1)
            
            # Verstuur 10us pulse
            GPIO.output(trig_pin, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(trig_pin, GPIO.LOW)
            
            # Meet echo tijd
            timeout = time.time() + 1  # 1 seconde timeout
            
            # Initialiseer variabelen
            pulse_start = time.time()
            pulse_end = time.time()
            
            # Wacht op echo HIGH
            while GPIO.input(echo_pin) == 0:
                pulse_start = time.time()
                if time.time() > timeout:
                    self.log("Timeout: Geen echo ontvangen", "ERROR")
                    self.log("Mogelijke oorzaken:", "INFO")
                    self.log("  - ECHO pin niet aangesloten", "INFO")
                    self.log("  - Voltage divider nodig (5V → 3.3V)", "INFO")
                    self.log("  - Sensor defect", "INFO")
                    return False
            
            # Wacht op echo LOW
            while GPIO.input(echo_pin) == 1:
                pulse_end = time.time()
                if time.time() > timeout:
                    break
            
            # Bereken afstand
            pulse_duration = pulse_end - pulse_start
            distance = (pulse_duration * 34300) / 2
            
            self.log(f"  Afstand gemeten: {distance:.1f} cm", "INFO")
            
            if 2 <= distance <= 400:
                self.log("HC-SR04 sensor werkt correct!", "SUCCESS")
                return True
            else:
                self.log("Afstand buiten bereik (2-400cm)", "WARNING")
                return False
                
        except Exception as e:
            self.log(f"Ultrasone sensor test MISLUKT: {e}", "ERROR")
            return False
    
    def test_pir_sensor(self, pin=17, duration=5):
        """Test PIR bewegingssensor"""
        self.log(f"Test PIR sensor op GPIO {pin}", "TEST")
        self.log(f"  Monitor beweging voor {duration} seconden...", "INFO")
        
        try:
            GPIO.setup(pin, GPIO.IN)
            
            motion_detected = False
            start_time = time.time()
            
            while time.time() - start_time < duration:
                if GPIO.input(pin):
                    if not motion_detected:
                        self.log("  Beweging gedetecteerd!", "INFO")
                        motion_detected = True
                time.sleep(0.1)
            
            if motion_detected:
                self.log("PIR sensor werkt correct!", "SUCCESS")
                return True
            else:
                self.log("Geen beweging gedetecteerd", "WARNING")
                self.log("Dit kan normaal zijn als er geen beweging was", "INFO")
                self.log("Test met beweging voor de sensor", "INFO")
                return True  # Niet per se een fout
                
        except Exception as e:
            self.log(f"PIR sensor test MISLUKT: {e}", "ERROR")
            return False
    
    def test_i2c_devices(self):
        """Scan I2C bus voor devices"""
        self.log("Scan I2C bus voor aangesloten devices", "TEST")
        
        try:
            import subprocess
            result = subprocess.run(['i2cdetect', '-y', '1'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log("I2C scan resultaat:", "INFO")
                print(result.stdout)
                
                # Check voor veelvoorkomende adressen
                addresses = []
                for line in result.stdout.split('\n'):
                    for part in line.split():
                        if len(part) == 2 and part != '--':
                            try:
                                addresses.append(int(part, 16))
                            except ValueError:
                                # Niet een geldig hex getal, overslaan
                                pass
                
                if addresses:
                    self.log(f"Gevonden devices op adressen: {[hex(a) for a in addresses]}", "SUCCESS")
                    return True
                else:
                    self.log("Geen I2C devices gevonden", "WARNING")
                    self.log("Controleer SDA/SCL aansluitingen", "INFO")
                    return False
            else:
                self.log("i2cdetect commando mislukt", "ERROR")
                return False
                
        except FileNotFoundError:
            self.log("i2c-tools niet geïnstalleerd", "ERROR")
            self.log("Installeer met: sudo apt install i2c-tools", "INFO")
            return False
        except Exception as e:
            self.log(f"I2C scan MISLUKT: {e}", "ERROR")
            return False
    
    def interactive_menu(self):
        """Interactief menu voor sensor selectie"""
        print("\n" + "="*60)
        print("  🔍 RASPBERRY PI SENSOR DEBUGGER")
        print("="*60)
        print("\nSelecteer een test:")
        print()
        print("1. Test GPIO pin (output)")
        print("2. Test GPIO pin (input)")
        print("3. Test DHT22 sensor")
        print("4. Test DHT11 sensor")
        print("5. Test HC-SR04 ultrasone sensor")
        print("6. Test PIR bewegingssensor")
        print("7. Scan I2C devices")
        print("8. Volledige systeem scan")
        print("9. Custom pin test")
        print("0. Afsluiten")
        print()
        
        choice = input("Keuze (0-9): ").strip()
        
        if choice == "1":
            pin = int(input("GPIO pin nummer: "))
            self.test_gpio_pin(pin, "output")
            
        elif choice == "2":
            pin = int(input("GPIO pin nummer: "))
            self.test_gpio_pin(pin, "input")
            
        elif choice == "3":
            pin = int(input("GPIO pin nummer (standaard 4): ") or "4")
            self.test_dht_sensor(pin, "DHT22")
            
        elif choice == "4":
            pin = int(input("GPIO pin nummer (standaard 4): ") or "4")
            self.test_dht_sensor(pin, "DHT11")
            
        elif choice == "5":
            trig = int(input("TRIG pin (standaard 23): ") or "23")
            echo = int(input("ECHO pin (standaard 24): ") or "24")
            self.test_ultrasonic_sensor(trig, echo)
            
        elif choice == "6":
            pin = int(input("PIR pin (standaard 17): ") or "17")
            self.test_pir_sensor(pin)
            
        elif choice == "7":
            self.test_i2c_devices()
            
        elif choice == "8":
            self.full_system_scan()
            
        elif choice == "9":
            self.custom_test()
            
        elif choice == "0":
            self.log("Debugger afgesloten", "INFO")
            sys.exit(0)
            
        else:
            print("Ongeldige keuze")
    
    def full_system_scan(self):
        """Volledige systeem scan van alle veelvoorkomende sensoren"""
        self.log("Start volledige systeem scan", "TEST")
        print("\n" + "-"*60)
        
        # Test GPIO
        self.log("\n--- GPIO Test ---", "INFO")
        self.test_gpio_pin(18, "output")
        
        # Test DHT22
        self.log("\n--- DHT22 Sensor Test ---", "INFO")
        self.test_dht_sensor(4, "DHT22")
        
        # Test I2C
        self.log("\n--- I2C Bus Scan ---", "INFO")
        self.test_i2c_devices()
        
        print("\n" + "-"*60)
        self.log("Systeem scan voltooid", "SUCCESS")
        
    def custom_test(self):
        """Custom test opties"""
        print("\nCustom Test:")
        print("Welke sensor wil je testen?")
        sensor_type = input("Type (dht/ultrasonic/pir/gpio): ").lower()
        
        if sensor_type == "dht":
            pin = int(input("Pin: "))
            variant = input("Variant (DHT11/DHT22): ").upper()
            self.test_dht_sensor(pin, variant)
        elif sensor_type == "ultrasonic":
            trig = int(input("TRIG pin: "))
            echo = int(input("ECHO pin: "))
            self.test_ultrasonic_sensor(trig, echo)
        elif sensor_type == "pir":
            pin = int(input("Pin: "))
            self.test_pir_sensor(pin)
        elif sensor_type == "gpio":
            pin = int(input("Pin: "))
            mode = input("Mode (input/output): ").lower()
            self.test_gpio_pin(pin, mode)
    
    def print_summary(self):
        """Print samenvatting van test resultaten"""
        print("\n" + "="*60)
        print("  📋 TEST SAMENVATTING")
        print("="*60)
        
        success_count = sum(1 for _, level, _ in self.test_results if level == "SUCCESS")
        error_count = sum(1 for _, level, _ in self.test_results if level == "ERROR")
        warning_count = sum(1 for _, level, _ in self.test_results if level == "WARNING")
        
        print(f"\n✅ Geslaagd: {success_count}")
        print(f"❌ Mislukt: {error_count}")
        print(f"⚠️  Waarschuwingen: {warning_count}")
        print()
    
    def cleanup(self):
        """Cleanup GPIO"""
        GPIO.cleanup()

def main():
    """Hoofdfunctie"""
    debugger = SensorDebugger()
    
    try:
        while True:
            debugger.interactive_menu()
            
            print("\n" + "-"*60)
            input("Druk op Enter voor een nieuwe test...")
            print()
            
    except KeyboardInterrupt:
        print("\n\nDebugger gestopt door gebruiker")
    finally:
        debugger.print_summary()
        debugger.cleanup()

if __name__ == "__main__":
    main()
