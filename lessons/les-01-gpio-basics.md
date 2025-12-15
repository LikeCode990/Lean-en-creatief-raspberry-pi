# Les 1: GPIO Basics - LED's Aansturen

## Leerdoelen
- Begrijpen wat GPIO pinnen zijn
- LED circuits bouwen op breadboard
- Eerste Python programma schrijven voor hardware control
- Lean principe: Start simpel, test snel

## Tijdsduur
90 minuten

## Benodigde Materialen
- Raspberry Pi (opgezet en werkend)
- 1x LED (rood)
- 1x 220Ω weerstand
- Breadboard
- 2x Jumper wires (male-to-female)

## Theorie (15 min)

### Wat is GPIO?
GPIO staat voor **General Purpose Input/Output**. Dit zijn programmeerbare pinnen op de Raspberry Pi die je kunt gebruiken om:
- **Output**: Signalen sturen naar componenten (LED's aan/uit, motoren besturen)
- **Input**: Signalen lezen van sensoren (button presses, temperatuur)

### GPIO Voltage Levels
- HIGH (1): 3.3V
- LOW (0): 0V

⚠️ **Belangrijk**: Raspberry Pi GPIO pinnen zijn 3.3V! Niet 5V zoals Arduino.

### Wat is een LED?
LED = Light Emitting Diode
- **Anode** (+, lange poot): Verbind met positieve spanning via weerstand
- **Kathode** (-, korte poot): Verbind met GND
- **Polariteit belangrijk**: LED werkt maar in één richting!

### Waarom een weerstand?
LED's hebben stroombegrenzing nodig:
- Zonder weerstand: Te veel stroom -> LED kapot
- Met 220Ω weerstand: ~10mA (perfect voor standaard LED)

**Ohm's Law**: V = I × R
- V = 3.3V - 2V (LED voltage drop) = 1.3V
- R = 220Ω
- I = 1.3V / 220Ω ≈ 6mA ✓

## Praktijk: Circuit Bouwen (20 min)

### Stap 1: Identificeer componenten
1. LED: Zoek lange poot (anode/+) en korte poot (kathode/-)
2. Weerstand: 220Ω (kleurcode: rood-rood-bruin)

### Stap 2: Bouw circuit op breadboard

```
Raspberry Pi GPIO 17 --> 220Ω Weerstand --> LED Anode (+)
                         LED Kathode (-) --> GND Pin
```

**Breadboard layout**:
1. Steek weerstand in breadboard (rij A)
2. Verbind weerstand andere kant met LED anode (rij E)
3. Steek LED kathode in GND rail (blauw/-)
4. Jumper wire: GPIO 17 (Pi Pin 11) naar weerstand start
5. Jumper wire: GND (Pi Pin 6) naar GND rail

### Stap 3: Dubbelcheck!
- [ ] LED polariteit correct?
- [ ] Weerstand aanwezig?
- [ ] Geen kortsluiting?
- [ ] GPIO 17 en GND juist aangesloten?

## Code: LED Blink (30 min)

### Stap 1: Navigeer naar voorbeelden
```bash
cd ~/Lean-en-creatief-raspberry-pi/examples/basic
```

### Stap 2: Bekijk de code
```bash
cat 01_led_blink.py
```

### Stap 3: Run het programma!
```bash
python3 01_led_blink.py
```

**Verwacht resultaat**: LED knippert elke seconde aan/uit.

### Code Uitleg

```python
import RPi.GPIO as GPIO  # Importeer GPIO library
import time              # Voor delays

LED_PIN = 17  # Gebruik GPIO 17 (BCM nummering)

# Setup
GPIO.setmode(GPIO.BCM)      # Gebruik BCM pin nummering
GPIO.setup(LED_PIN, GPIO.OUT)  # Configureer pin als output

try:
    while True:  # Oneindige loop
        GPIO.output(LED_PIN, GPIO.HIGH)  # Zet pin hoog (3.3V)
        print("LED AAN")
        time.sleep(1)  # Wacht 1 seconde
        
        GPIO.output(LED_PIN, GPIO.LOW)   # Zet pin laag (0V)
        print("LED UIT")
        time.sleep(1)

except KeyboardInterrupt:  # Wanneer Ctrl+C ingedrukt
    print("\nProgramma gestopt")

finally:
    GPIO.cleanup()  # Reset GPIO pinnen
```

## Experimenteer! (20 min)

### Opdracht 1: Verander snelheid
Pas `time.sleep()` aan om sneller/langzamer te knipperen:
- Sneller: `time.sleep(0.5)`  # 0.5 seconden
- Langzamer: `time.sleep(2)`  # 2 seconden

### Opdracht 2: Morse code
Maak een functie die je naam in morse code knippert!
- Kort = 0.2s aan
- Lang = 0.6s aan
- Pauze tussen letters = 0.6s

**Voorbeeld**:
```python
def morse_s():
    """S = · · · (drie korte)"""
    for i in range(3):
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.2)
```

### Opdracht 3: Meerdere LED's
Voeg nog een LED toe op GPIO 27:
1. Bouw tweede circuit
2. Configureer tweede pin in code
3. Laat LED's afwisselend knipperen

## Lean Reflectie (5 min)

### Wat heb je geleerd?
- ✅ Eerste working circuit gebouwd
- ✅ Eerste hardware control code geschreven
- ✅ Iteratief getest en verbeterd

### Lean Principes toegepast:
1. **Start simpel**: Één LED, basic blink
2. **Test snel**: Direct feedback (LED gaat aan/uit)
3. **Itereer**: Experimenteer met timing, morse code, meerdere LED's

## Troubleshooting

### LED gaat niet aan
- Check polariteit (lange poot naar weerstand)
- Verifieer pin nummer: GPIO 17 = Physical pin 11
- Test met multimeter: Meet voltage op LED anode

### "Permission denied" error
```bash
sudo usermod -a -G gpio $USER
# Log uit en weer in
```

### LED blijft heel zwak branden
- Mogelijk verkeerde GPIO pin
- Check of andere programma nog draait
- Run `GPIO.cleanup()` handmatig

## Volgende Les

**Les 2: Input Verwerking** - Buttons en sensoren lezen

In de volgende les leren we:
- Button input lezen
- Pull-up/pull-down resistors
- Event-driven programming
- LED besturen met button

## Extra Resources

- [GPIO Pinout Diagram](https://pinout.xyz/pinout/pin11_gpio17)
- [LED Calculator](https://www.digikey.com/en/resources/conversion-calculators/conversion-calculator-led-series-resistor)
- [RPi.GPIO Documentation](https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/)
