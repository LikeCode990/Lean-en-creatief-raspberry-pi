# Voorbeelden

Deze map bevat verschillende voorbeeldprojecten om je op weg te helpen met Raspberry Pi GPIO programmering.

## Structuur

Elk voorbeeld heeft zijn eigen map met:
- Python script(s)
- README.md met uitleg
- Circuit diagram (waar nodig)

## Volgorde

### Beginners Start Hier 👇

1. **[01-blink](01-blink/)** - LED knipperen
   - Leer: GPIO output, timing
   - Hardware: 1 LED, 1 weerstand
   - Tijd: 15 minuten

2. **[02-button](02-button/)** - Knop uitlezen
   - Leer: GPIO input, event handling
   - Hardware: 1 knop, 1 LED, 1 weerstand
   - Tijd: 20 minuten

3. **[03-pwm-fade](03-pwm-fade/)** - LED dimmen met PWM
   - Leer: PWM, analoge output
   - Hardware: 1 LED, 1 weerstand
   - Tijd: 20 minuten

### Gemiddeld

4. **[04-web-dashboard](04-web-dashboard/)** - Web Dashboard
   - Leer: Flask, REST API, HTML/CSS/JavaScript
   - Hardware: 2 LEDs, 2 weerstanden, DHT22 (optioneel)
   - Tijd: 45 minuten
   - **Nieuw!** Bestuur je Pi via je browser 🌐

5. **[05-sensor-debugger](05-sensor-debugger/)** - Sensor Debugger
   - Leer: Hardware debugging, troubleshooting, systematisch testen
   - Hardware: Afhankelijk van sensor die je wilt testen
   - Tijd: 20 minuten
   - **Nieuw!** Debug tool voor alle sensoren 🔍

6. **RGB LED** (komt binnenkort)
   - Leer: Meerdere PWM kanalen
   - Hardware: 1 RGB LED, 3 weerstanden

7. **Ultrasone Sensor** (komt binnenkort)
   - Leer: Timing, afstand meten
   - Hardware: HC-SR04 sensor

8. **Servo Motor** (komt binnenkort)
   - Leer: PWM voor motoren
   - Hardware: SG90 servo

### Gevorderd

9. **I2C Display** (komt binnenkort)
   - Leer: I2C communicatie
   - Hardware: OLED of LCD display

10. **MQTT Sensor** (komt binnenkort)
   - Leer: IoT, netwerk communicatie
   - Hardware: Sensor naar keuze

## Library Vergelijking

### RPi.GPIO
- **Voordelen**: Laag niveau, veel controle, uitgebreid gebruikt
- **Nadelen**: Meer code nodig, complexer
- **Gebruik voor**: Fijnmazige controle, legacy projecten

Voorbeeld:
```python
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.HIGH)
```

### GPIO Zero
- **Voordelen**: Simpel, intuïtief, objectgeoriënteerd
- **Nadelen**: Minder low-level controle
- **Gebruik voor**: Snelle prototypes, beginners, clean code

Voorbeeld:
```python
from gpiozero import LED
led = LED(18)
led.on()
```

## Beide Libraries Vergelijken

| Taak | RPi.GPIO | GPIO Zero |
|------|----------|-----------|
| LED aan | `GPIO.output(18, HIGH)` | `led.on()` |
| LED knipperen | Loop met sleep | `led.blink()` |
| Knop lezen | `GPIO.input(17)` | `button.is_pressed` |
| PWM | `PWM(18, 100)` | `PWMLED(18)` |

## Tips voor Voorbeelden Gebruiken

1. **Lees de README eerst**: Elke map heeft instructies
2. **Check de hardware**: Zorg dat je alle componenten hebt
3. **Test stap voor stap**: Bouw circuit op, test, dan code
4. **Pas aan en experimenteer**: Verander waarden, zie wat gebeurt
5. **Debuggen**:
   ```bash
   # Check GPIO status
   gpio readall
   
   # Verbose Python output
   python3 -v script.py
   
   # Gebruik de Sensor Debugger tool!
   python3 05-sensor-debugger/sensor_debugger.py
   ```

## Troubleshooting

💡 **Sensor werkt niet?** Gebruik de **[Sensor Debugger](05-sensor-debugger/)** voor systematische diagnose!

### Script loopt niet
```bash
# Check Python versie
python3 --version

# Check libraries
pip3 list | grep -i gpio
```

### Permission errors
```bash
# Voeg gebruiker toe aan gpio groep
sudo usermod -a -G gpio $USER
# Log uit en weer in
```

### LED doet niets
1. Check polariteit LED (lange poot = +)
2. Check weerstand waarde (220Ω)
3. Test LED met batterij
4. Check pin nummer in code

### GPIO in use error
```bash
# Reset GPIO
sudo python3 -c "import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM); GPIO.cleanup()"
```

## Uitbreidingen

Experimenteer met deze uitbreidingen:

1. **Combinaties**: Combineer voorbeelden
   - Button die fade snelheid bepaalt
   - Meerdere LEDs in patronen

2. **Input Variaties**:
   - Command line argumenten
   - Configuratie bestand
   - Webinterface

3. **Output Variaties**:
   - Console logging
   - Bestand schrijven
   - Database opslag

4. **Functionaliteit**:
   - Error handling
   - State machines
   - Threading

## Bijdragen

Heb je een cool voorbeeld gemaakt? Deel het! Zie [CONTRIBUTING.md](../CONTRIBUTING.md).

## Bronnen

- [GPIO Zero Docs](https://gpiozero.readthedocs.io/)
- [RPi.GPIO Wiki](https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/)
- [Raspberry Pi GPIO Pinout](https://pinout.xyz/)
