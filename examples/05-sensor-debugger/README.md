# Sensor Debugger - Universele Sensor Debug Tool

## Beschrijving
Een uitgebreide debug tool voor het testen en diagnosticeren van verschillende sensoren op de Raspberry Pi. Perfect voor troubleshooting wanneer sensoren niet werken zoals verwacht.

## Leerdoelen
- Systematisch debuggen van hardware problemen
- GPIO pin functionaliteit testen
- Sensor communicatie verifiëren
- I2C bus scannen
- Error handling en probleem diagnose

## Features

### ✨ Functionaliteit
- **GPIO Pin Test**: Test individuele pins als input/output
- **DHT11/DHT22 Test**: Temperatuur en luchtvochtigheid sensoren
- **HC-SR04 Test**: Ultrasone afstandssensor
- **PIR Test**: Bewegingssensor
- **I2C Scan**: Detecteer aangesloten I2C devices
- **Volledige Scan**: Test alle veelvoorkomende sensoren
- **Custom Tests**: Flexibele test opties
- **Automatische Diagnose**: Suggesties bij problemen

### 📊 Output
- Real-time logging met timestamps
- Duidelijke status indicators (✅❌⚠️)
- Gedetailleerde foutmeldingen
- Test samenvatting aan het einde
- Troubleshooting tips

## Gebruik

### Basis Gebruik
```bash
python3 sensor_debugger.py
```

Je krijgt een interactief menu:
```
============================================================
  🔍 RASPBERRY PI SENSOR DEBUGGER
============================================================

Selecteer een test:

1. Test GPIO pin (output)
2. Test GPIO pin (input)
3. Test DHT22 sensor
4. Test DHT11 sensor
5. Test HC-SR04 ultrasone sensor
6. Test PIR bewegingssensor
7. Scan I2C devices
8. Volledige systeem scan
9. Custom pin test
0. Afsluiten

Keuze (0-9):
```

## Test Types

### 1. GPIO Pin Test (Output)
Test of een GPIO pin correct werkt als output:
- Zet pin naar HIGH
- Zet pin naar LOW
- Controleert op errors

**Voorbeeld:**
```
Keuze: 1
GPIO pin nummer: 18

[14:30:00] 🔍 Test GPIO pin 18 (output)
[14:30:00] ℹ️   Pin 18 gezet naar HIGH
[14:30:01] ℹ️   Pin 18 gezet naar LOW
[14:30:01] ✅ GPIO pin 18 werkt correct (output)
```

### 2. GPIO Pin Test (Input)
Test of een pin leesbaar is als input:
- Configureert pin met pull-up weerstand
- Leest huidige status
- Toont HIGH of LOW

### 3. DHT22/DHT11 Sensor Test
Uitgebreide test voor DHT sensoren:
- Leest temperatuur en luchtvochtigheid
- Valideert waarden (range check)
- Geeft troubleshooting tips bij falen

**Mogelijke output bij succes:**
```
[14:30:05] 🔍 Test DHT22 sensor op GPIO 4
[14:30:05] ℹ️   Poging 1: Sensor uitlezen...
[14:30:06] ℹ️   Temperatuur: 21.5°C
[14:30:06] ℹ️   Luchtvochtigheid: 45.0%
[14:30:06] ✅ DHT22 werkt correct!
```

**Bij problemen:**
```
[14:30:05] ❌ Geen data van sensor ontvangen
[14:30:05] ℹ️  Mogelijke oorzaken:
[14:30:05] ℹ️    - Sensor niet aangesloten
[14:30:05] ℹ️    - Verkeerde pin (check GPIO nummer)
[14:30:05] ℹ️    - Defecte sensor
[14:30:05] ℹ️    - Geen pull-up weerstand (10kΩ nodig)
```

### 4. HC-SR04 Ultrasone Sensor
Test afstandssensor:
- Verstuurt trigger pulse
- Meet echo tijd
- Berekent afstand
- Valideert bereik (2-400cm)

**Troubleshooting tips bij falen:**
- Voltage divider nodig (5V → 3.3V)
- ECHO pin aansluiting controleren
- Sensor oriëntatie

### 5. PIR Bewegingssensor
Monitor bewegingsdetectie:
- Leest sensor voor 5 seconden
- Detecteert beweging
- Geeft feedback

**Tip:** Beweeg voor de sensor tijdens de test!

### 6. I2C Device Scan
Scan I2C bus:
- Detecteert alle aangesloten devices
- Toont adressen in hex
- Controleert SDA/SCL verbinding

**Voorbeeld output:**
```
[14:30:10] 🔍 Scan I2C bus voor aangesloten devices
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- 76 --                         
[14:30:10] ✅ Gevonden devices op adressen: ['0x76']
```

### 7. Volledige Systeem Scan
Automatische test van:
- GPIO pin 18 (output)
- DHT22 op GPIO 4
- I2C bus scan

Perfect voor een snelle health check!

### 8. Custom Pin Test
Flexibele test met eigen configuratie:
- Kies sensor type
- Specificeer pin nummers
- Custom timing

## Veelvoorkomende Problemen & Oplossingen

### "Geen data van sensor ontvangen"
**Oplossingen:**
1. Check fysieke aansluiting
2. Controleer GPIO pin nummer in code
3. Meet voltage met multimeter (moet 3.3V zijn)
4. Probeer andere sensor (mogelijk defect)
5. DHT sensoren: voeg 10kΩ pull-up weerstand toe

### "Timeout: Geen echo ontvangen" (HC-SR04)
**Oplossingen:**
1. Voeg voltage divider toe voor ECHO pin (5V → 3.3V)
   ```
   ECHO → 1kΩ → GPIO 24 → 2kΩ → GND
   ```
2. Check TRIG/ECHO aansluitingen
3. Sensor moet vrij zicht hebben (niet te dichtbij muur)
4. VCC moet 5V zijn (niet 3.3V)

### "Adafruit_DHT library niet geïnstalleerd"
```bash
sudo pip3 install Adafruit-DHT
```

### "i2c-tools niet geïnstalleerd"
```bash
sudo apt install i2c-tools
```

### "I2C niet ingeschakeld"
```bash
sudo raspi-config
# Interface Options → I2C → Enable
sudo reboot
```

### "Permission denied"
```bash
# Voeg gebruiker toe aan gpio groep
sudo usermod -a -G gpio $USER
# Log uit en weer in
```

## Hardware Requirements

### Minimaal (voor basis tests)
- Raspberry Pi
- Breadboard
- Jumper draden
- 1x LED + 220Ω weerstand (voor GPIO test)

### Voor Sensor Tests
Afhankelijk van welke sensor je wilt testen:
- **DHT22**: Sensor + 10kΩ weerstand
- **HC-SR04**: Sensor + 1kΩ + 2kΩ weerstanden (voltage divider)
- **PIR**: Sensor (meestal al 3-pin module)
- **I2C devices**: Sensor met SDA/SCL aansluitingen

## Voorbeeld Sessie

```bash
$ python3 sensor_debugger.py

============================================================
  🔍 RASPBERRY PI SENSOR DEBUGGER
============================================================

Selecteer een test:
...
Keuze (0-9): 3
GPIO pin nummer (standaard 4): 4

[14:35:00] 🔍 Test DHT22 sensor op GPIO 4
[14:35:00] ℹ️   Poging 1: Sensor uitlezen...
[14:35:01] ℹ️   Temperatuur: 22.1°C
[14:35:01] ℹ️   Luchtvochtigheid: 48.5%
[14:35:01] ✅ DHT22 werkt correct!

------------------------------------------------------------
Druk op Enter voor een nieuwe test...

Keuze (0-9): 0
[14:35:30] ℹ️  Debugger afgesloten

============================================================
  📋 TEST SAMENVATTING
============================================================

✅ Geslaagd: 1
❌ Mislukt: 0
⚠️  Waarschuwingen: 0
```

## Best Practices

### Systematisch Debuggen
1. **Start simpel**: Test eerst GPIO pin zonder sensor
2. **Isoleer**: Test één component tegelijk
3. **Document**: Noteer welke tests werken/falen
4. **Verifieer**: Meet voltages met multimeter
5. **Vergelijk**: Test bekende werkende sensor eerst

### Safety First
- Controleer altijd voltage voordat je aansluit
- 3.3V GPIO pins kunnen beschadigen bij 5V
- Gebruik voltage dividers waar nodig
- Disconnect power bij het wijzigen van bedrading

### Debug Workflow
```
1. Volledige systeem scan
   ↓
2. Identificeer falende sensor
   ↓
3. Test specifieke sensor
   ↓
4. Volg troubleshooting tips
   ↓
5. Verifieer fix met nieuwe test
```

## Integratie met Projecten

Gebruik in eigen scripts:
```python
from sensor_debugger import SensorDebugger

debugger = SensorDebugger()

# Test sensor voordat je app start
if debugger.test_dht_sensor(4, "DHT22"):
    print("Sensor OK - start applicatie")
    # ... je code hier
else:
    print("Sensor probleem - check hardware")
```

## Uitbreidingen

Voeg je eigen sensor tests toe:
```python
def test_custom_sensor(self, pin):
    """Test voor custom sensor"""
    self.log(f"Test custom sensor op GPIO {pin}", "TEST")
    
    try:
        # Jouw test code hier
        GPIO.setup(pin, GPIO.IN)
        value = GPIO.input(pin)
        
        self.log(f"Sensor waarde: {value}", "INFO")
        self.log("Custom sensor werkt!", "SUCCESS")
        return True
        
    except Exception as e:
        self.log(f"Custom sensor test MISLUKT: {e}", "ERROR")
        return False
```

## Tips & Tricks

### Quick Tests via Command Line
Maak alias voor snelle tests:
```bash
# Voeg toe aan ~/.bashrc
alias debug-dht='python3 ~/sensor_debugger.py'
```

### Log Output Opslaan
```bash
python3 sensor_debugger.py 2>&1 | tee sensor_test.log
```

### Automatische Tests in Script
```bash
#!/bin/bash
# Pre-deployment sensor check
python3 sensor_debugger.py << EOF
8
0
EOF
```

## Troubleshooting Guide

| Symptoom | Mogelijke Oorzaak | Oplossing |
|----------|-------------------|-----------|
| Geen output | Script loopt niet | Check Python versie, permissions |
| Import error | Library ontbreekt | Installeer Adafruit_DHT |
| GPIO warning | Pins niet cleaned up | Run GPIO.cleanup() |
| Timeout | Sensor niet aangesloten | Check bedrading |
| Verkeerde waarden | Noise, EMI | Kortere kabels, pull-up weerstanden |

## Bronnen

- [GPIO Troubleshooting](https://www.raspberrypi.org/documentation/usage/gpio/)
- [DHT Sensor Guide](https://learn.adafruit.com/dht)
- [I2C Debugging](https://www.raspberrypi.org/documentation/hardware/raspberrypi/i2c/)

## Volgende Stappen

Na het debuggen van je sensoren:
1. Gebruik sensor in voorbeeldprojecten
2. Bouw je eigen monitoring systeem
3. Integreer met web dashboard
4. Implementeer data logging
