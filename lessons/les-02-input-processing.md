# Les 2: Input Verwerking - Buttons en Sensoren

## Leerdoelen
- GPIO pins configureren als input
- Pull-up en pull-down resistors begrijpen
- Button presses detecteren met debouncing
- Interactive systemen bouwen
- Lean principe: Directe feedback loops

## Tijdsduur
90 minuten

## Benodigde Materialen
- Raspberry Pi (opgezet en werkend)
- 1x LED (rood)
- 1x 220Ω weerstand (voor LED)
- 1x Tactile push button
- 1x 10kΩ weerstand (pull-down)
- Breadboard
- Jumper wires

## Theorie (20 min)

### Input vs Output
- **Output**: Pi stuurt signaal NAAR component (LED)
- **Input**: Pi LEEST signaal VAN component (button)

### Pull-up en Pull-down Resistors

Zonder pull resistor heeft een input pin een "floating" state - willekeurige waarden!

#### Pull-down (meest gebruikt)
```
Button tussen GPIO en 3.3V
GPIO -> 10kΩ -> GND
```
- Default: LOW (0V, button niet ingedrukt)
- Ingedrukt: HIGH (3.3V)

#### Pull-up
```
3.3V -> 10kΩ -> GPIO
Button tussen GPIO en GND
```
- Default: HIGH (3.3V)
- Ingedrukt: LOW (0V)

### Software Pull-up/down
Raspberry Pi heeft **interne** pull resistors!
```python
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
```

### Debouncing
Buttons "bouncen" bij indrukken (meerdere signalen in korte tijd).

**Oplossingen**:
1. Hardware: Condensator parallel aan button
2. Software: Delay na detectie (~20-200ms)

```python
if button_pressed:
    time.sleep(0.2)  # Debounce delay
```

## Praktijk: Circuit Bouwen (20 min)

### Basis Button + LED Circuit

```
[Pi]
GPIO 27 -----> Button -----> 3.3V
    |
    +---[10kΩ]---> GND

GPIO 17 -----> [220Ω] -----> LED+ -----> LED- -----> GND
```

### Stap-voor-stap:

1. **LED gedeelte** (van Les 1):
   - GPIO 17 -> 220Ω -> LED anode
   - LED kathode -> GND

2. **Button gedeelte** (nieuw):
   - Button in breadboard (4 poten - 2 aan elke kant)
   - Één kant button -> 3.3V (Physical pin 1)
   - Andere kant button -> GPIO 27 (Physical pin 13)
   - GPIO 27 -> 10kΩ resistor -> GND

3. **Dubbelcheck**:
   - [ ] LED circuit correct (test met Les 1 code)
   - [ ] Button heeft pull-down weerstand
   - [ ] Geen kortsluiting 3.3V naar GND

## Code: Button Input (25 min)

### Methode 1: Polling (Continue Checking)

```bash
cd ~/Lean-en-creatief-raspberry-pi/examples/basic
python3 02_button_input.py
```

**Code analyse**:
```python
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    button_state = GPIO.input(BUTTON_PIN)
    
    if button_state:  # HIGH = button pressed
        print("Button ingedrukt!")
        time.sleep(0.2)  # Debounce
```

### Methode 2: Event Detection (Efficiënter!)

Maak nieuw bestand `button_event.py`:

```python
#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

BUTTON_PIN = 27
LED_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

led_state = False

def button_callback(channel):
    """Wordt aangeroepen bij button press"""
    global led_state
    led_state = not led_state  # Toggle
    GPIO.output(LED_PIN, led_state)
    print(f"LED: {'AAN' if led_state else 'UIT'}")

# Event detectie op rising edge (LOW -> HIGH)
GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, 
                      callback=button_callback, 
                      bouncetime=200)  # 200ms debounce

print("Event-based button control")
print("Druk button om LED te togglen")

try:
    while True:
        time.sleep(0.1)  # Main loop doet bijna niets!
except KeyboardInterrupt:
    print("\nProgramma gestopt")
finally:
    GPIO.cleanup()
```

**Voordelen event detection**:
- ✅ Efficiënter (minder CPU)
- ✅ Mist geen button presses
- ✅ Ingebouwde debounce support

## Experimenteer! (20 min)

### Opdracht 1: Telpatroon
Bouw een teller die count op LED's laat zien (binair):
- 2 LED's = 4 states (0-3)
- 3 LED's = 8 states (0-7)

```
LED1 LED0  Waarde
OFF  OFF   0
OFF  ON    1
ON   OFF   2
ON   ON    3
```

### Opdracht 2: Hold Detection
Detecteer hoe lang button wordt ingedrukt:
- Kort (< 1s): Groen LED
- Lang (> 1s): Rood LED

**Hint**:
```python
press_time = time.time()
while GPIO.input(BUTTON_PIN):  # Wacht tot losgelaten
    pass
duration = time.time() - press_time
```

### Opdracht 3: Combination Lock
Maak simpele code lock:
- Juiste reeks button presses = LED aan
- Foute reeks = LED knippert rood

Voorbeeld code: "Kort - Lang - Kort"

## Creatieve Uitdaging (25 min)

### Project: Reactie Spel

**Concept**: Test je reactiesnelheid!

1. LED gaat aan na random delay (2-5 seconden)
2. Gebruiker moet zo snel mogelijk button drukken
3. Meet en toon reactietijd

**Features**:
- Beste tijd opslaan
- Meerdere rondes
- LED kleuren voor score (rood=langzaam, groen=snel)

**Pseudo-code**:
```python
import random

while True:
    print("Wacht op LED...")
    time.sleep(random.uniform(2, 5))
    
    GPIO.output(LED_PIN, HIGH)
    start_time = time.time()
    
    # Wacht op button press
    while not GPIO.input(BUTTON_PIN):
        pass
    
    reaction_time = time.time() - start_time
    print(f"Reactietijd: {reaction_time:.3f}s")
```

## Lean Reflectie (5 min)

### Input -> Process -> Output Loop
Dit is de basis van alle embedded systemen:
1. **Input**: Button press detecteren
2. **Process**: Logica (toggle, timer, etc.)
3. **Output**: LED feedback

### Feedback Loop Principes:
- **Direct**: Instant LED feedback bij button press
- **Duidelijk**: Visuele bevestiging van actie
- **Consistent**: Zelfde input = zelfde output

### Iteratieve Verbetering:
1. Start: Basic button -> LED
2. Verbeter: Debouncing
3. Optimaliseer: Event detection
4. Uitbreiden: Timers, patronen, spellen

## Troubleshooting

### Button werkt niet
```python
# Test button state direct
while True:
    print(GPIO.input(BUTTON_PIN))
    time.sleep(0.1)
```
Verwacht: 0 (niet ingedrukt), 1 (ingedrukt)

### Floating input (random waarden)
- Controleer pull-down configuratie
- Verifieer weerstand (10kΩ)
- Test met software pull-down

### LED reageert niet op button
- Test LED apart (Les 1 code)
- Print button state naar console
- Check pin nummers (BCM vs Physical)

### Te veel false positives
- Verhoog debounce tijd
- Controleer hardware bounce
- Overweeg hardware debounce (condensator)

## Code Best Practices

### ✅ Gebruik pull-down voor buttons
```python
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
```

### ✅ Altijd cleanup
```python
try:
    # main code
finally:
    GPIO.cleanup()
```

### ✅ Event detection voor efficiency
```python
GPIO.add_event_detect(pin, GPIO.RISING, callback=func, bouncetime=200)
```

### ❌ Vermijd polling zonder delay
```python
# SLECHT - 100% CPU gebruik!
while True:
    if GPIO.input(PIN):
        do_something()

# GOED - Kleine delay
while True:
    if GPIO.input(PIN):
        do_something()
    time.sleep(0.01)
```

## Volgende Les

**Les 3: PWM en Dimmen** - Analoge effecten met digitale signalen

In de volgende les leren we:
- Pulse Width Modulation (PWM)
- LED's dimmen met PWM
- RGB LED control
- Servo motor aansturen

## Extra Resources

- [Button Debouncing Explained](https://www.raspberrypi.org/forums/viewtopic.php?t=146906)
- [GPIO Events Documentation](https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/)
- [Interactive Circuit Simulator](https://www.tinkercad.com/circuits)
