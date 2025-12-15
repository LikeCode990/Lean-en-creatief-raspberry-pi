# Les 3: PWM en Dimmen - Analoge Effecten met Digitale Signalen

## Leerdoelen
- Pulse Width Modulation (PWM) begrijpen
- LED's dimmen met verschillende helderheid
- RGB LED aansturen voor kleurenmenging
- Creatief principe: Vloeiende overgangen en visuele effecten

## Tijdsduur
90 minuten

## Benodigde Materialen
- Raspberry Pi (opgezet en werkend)
- 3x LED (of 1x RGB LED)
- 3x 220Ω weerstand
- Breadboard
- Jumper wires
- Optioneel: Potentiometer 10kΩ voor manual brightness control

## Theorie (20 min)

### Wat is PWM?

**PWM = Pulse Width Modulation**

GPIO pins kunnen alleen digitaal: HIGH (3.3V) of LOW (0V).
Maar hoe maak je dan een LED half-helder?

**Oplossing**: Schakel heel snel aan en uit!

```
100% (altijd aan):  ████████████████████
75%  (3/4 aan):     ████████████▁▁▁▁▁▁▁▁
50%  (helft aan):   ████████▁▁▁▁████████
25%  (1/4 aan):     ████▁▁▁▁▁▁▁▁████▁▁▁▁
0%   (altijd uit):  ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁
```

### Belangrijke Begrippen

**Frequency (Frequentie)**:
- Hoe vaak per seconde de cyclus herhaalt
- Gemeten in Hz (Hertz)
- Typisch: 100-1000 Hz voor LED's
- Te laag (<50Hz): Flikkering zichtbaar
- Te hoog (>10kHz): Verspilt energie

**Duty Cycle**:
- Percentage van tijd dat signaal HIGH is
- 0% = altijd uit
- 50% = halve tijd aan
- 100% = altijd aan

**Formule**:
```
Gemiddelde spanning = Duty Cycle × Maximale spanning
50% duty cycle = 0.5 × 3.3V = 1.65V (gemiddeld)
```

### Hardware vs Software PWM

**Hardware PWM**:
- Gebruikt dedicated hardware
- Nauwkeurige timing
- Beperkt aantal pins: GPIO 12, 13, 18, 19
- ✅ Voorkeur voor kritische toepassingen (servo's)

**Software PWM**:
- Geïmplementeerd in software
- Alle GPIO pins kunnen PWM
- Minder nauwkeurig (timing afhankelijk van CPU load)
- ✅ Prima voor LED's, displays

### PWM en Menselijk Oog

Ons oog heeft **persistence of vision**:
- Beelden blijven ~1/25 seconde "hangen"
- PWM >50Hz lijkt continu licht
- Hogere frequencies = gladdere dimming

## Praktijk: PWM LED Circuit (15 min)

### Circuit: Basis LED met PWM

```
Raspberry Pi GPIO 18 --> 220Ω --> LED+ --> LED- --> GND
```

**Waarom GPIO 18?**
- GPIO 18 heeft **hardware PWM** capability
- Beter voor vloeiende dimming
- Kan ook software PWM op andere pins

### Stap-voor-stap:
1. LED + weerstand in breadboard
2. GPIO 18 (Physical pin 12) naar weerstand
3. LED kathode naar GND

## Code: LED Fading (20 min)

### Basis PWM Setup

```bash
cd ~/Lean-en-creatief-raspberry-pi/examples/basic
python3 03_pwm_fade.py
```

**Code analyse**:

```python
import RPi.GPIO as GPIO

LED_PIN = 18  # PWM capable pin
PWM_FREQ = 1000  # 1000 Hz

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Maak PWM object
pwm = GPIO.PWM(LED_PIN, PWM_FREQ)
pwm.start(0)  # Start met 0% duty cycle

# Fade in
for duty_cycle in range(0, 101):  # 0 tot 100%
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.02)  # 20ms per stap

# Fade out
for duty_cycle in range(100, -1, -1):
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.02)

pwm.stop()
GPIO.cleanup()
```

### PWM Methodes

```python
pwm = GPIO.PWM(pin, frequency)  # Maak PWM object
pwm.start(duty_cycle)           # Start PWM
pwm.ChangeDutyCycle(value)      # Wijzig duty cycle (0-100)
pwm.ChangeFrequency(freq)       # Wijzig frequentie
pwm.stop()                      # Stop PWM
```

## RGB LED Control (25 min)

### Circuit: RGB LED

RGB LED heeft 4 poten:
- R (Rood)
- G (Groen)
- B (Blauw)
- Common Cathode (-) -> GND

```
GPIO 17 --> 220Ω --> R pin
GPIO 27 --> 220Ω --> G pin  } RGB LED
GPIO 22 --> 220Ω --> B pin
Common Cathode --> GND
```

### Code: Kleurenmenging

```bash
cd ~/Lean-en-creatief-raspberry-pi/examples/intermediate
python3 01_rgb_led.py
```

**Kleurentheorie**:
```
Rood + Groen = Geel
Rood + Blauw = Magenta
Groen + Blauw = Cyaan
Rood + Groen + Blauw = Wit
```

**Code snippet**:
```python
def set_color(red, green, blue):
    """Zet RGB kleur (0-100%)"""
    red_pwm.ChangeDutyCycle(red)
    green_pwm.ChangeDutyCycle(green)
    blue_pwm.ChangeDutyCycle(blue)

# Voorbeelden
set_color(100, 0, 0)     # Rood
set_color(0, 100, 0)     # Groen
set_color(100, 100, 0)   # Geel
set_color(50, 0, 100)    # Paars
```

## Experimenteer! (20 min)

### Opdracht 1: Breathing Effect
Maak een LED die "ademt" (smooth fade in/out):

```python
import math

def breathing_effect():
    """Simuleer ademhaling patroon"""
    while True:
        for i in range(0, 360, 2):  # 0 tot 360 graden
            # Gebruik sine wave voor natuurlijke curve
            brightness = (math.sin(math.radians(i)) + 1) * 50
            pwm.ChangeDutyCycle(brightness)
            time.sleep(0.01)
```

### Opdracht 2: Traffic Light
Simuleer verkeerslicht met 3 LED's:
- Rood (5s) -> Rood+Geel (2s) -> Groen (5s) -> Geel (2s) -> herhaal
- Gebruik vloeiende overgangen met PWM

### Opdracht 3: Rainbow Cycle
Maak continue regenboog effect met RGB LED:
- Smooth overgang door alle kleuren
- Gebruik HSV naar RGB conversie

**Hint**: Zie `01_rgb_led.py` voor rainbow implementatie

## Creatieve Uitdaging (20 min)

### Project: Mood Light

**Concept**: LED kleur/helderheid control via button of potentiometer

**Features**:
- Button 1: Volgende kleur preset
- Button 2: Helderheid aanpassen
- Of: Potentiometer voor vloeiende brightness control

**Bonus**:
- Save/load favoriete kleuren
- Slow color transitions
- Music reactive (met microfoon module)

**Pseudo-code**:
```python
colors = [
    (100, 0, 0),    # Rood
    (0, 100, 0),    # Groen
    (0, 0, 100),    # Blauw
    (100, 100, 0),  # Geel
    # etc.
]

current_color = 0
brightness = 100

def next_color():
    global current_color
    current_color = (current_color + 1) % len(colors)
    set_color_with_brightness(colors[current_color])

def adjust_brightness(delta):
    global brightness
    brightness = max(0, min(100, brightness + delta))
    set_color_with_brightness(colors[current_color])
```

## PWM Best Practices (5 min)

### ✅ DO:
```python
# Gebruik hogere frequentie voor LED's
pwm = GPIO.PWM(LED_PIN, 1000)  # 1kHz

# Stop PWM voor cleanup
pwm.stop()

# Smooth transitions met kleine stappen
for dc in range(0, 101, 1):  # Stap van 1%
    pwm.ChangeDutyCycle(dc)
    time.sleep(0.01)
```

### ❌ DON'T:
```python
# Te lage frequentie -> flikkering
pwm = GPIO.PWM(LED_PIN, 10)  # SLECHT

# Te grote stappen -> niet smooth
for dc in range(0, 101, 25):  # Stappen van 25%
    pwm.ChangeDutyCycle(dc)
    # Niet smooth!

# Vergeet niet te stoppen
pwm.start(50)
# ... code ...
# pwm.stop() VERGETEN!
```

## Troubleshooting

### LED flikkert zichtbaar
- Verhoog PWM frequentie (>100Hz)
- Test met verschillende frequencies
- Check of andere processen CPU belasten

### Geen vloeiende fade
- Verklein stap grootte in loop
- Verlaag delay tussen stappen
- Gebruik float voor precisie:
  ```python
  for i in range(1000):
      dc = i / 10.0  # 0.0 tot 100.0
      pwm.ChangeDutyCycle(dc)
  ```

### RGB kleuren kloppen niet
- Check LED type (common cathode vs anode)
- Verifieer pin nummers
- Test elke kleur apart:
  ```python
  set_color(100, 0, 0)  # Alleen rood
  time.sleep(2)
  set_color(0, 100, 0)  # Alleen groen
  time.sleep(2)
  set_color(0, 0, 100)  # Alleen blauw
  ```

## Lean Reflectie (5 min)

### PWM als Creative Tool
- **Expressiviteit**: Duizenden kleuren met 3 LED's
- **User Experience**: Vloeiende feedback beter dan aan/uit
- **Iteratie**: Begin simpel (on/off), verbeter naar dimming

### Toepassingen
- **Indicators**: Status feedback met kleur + helderheid
- **Mood/Ambient lighting**: Sfeerverlichting
- **Displays**: 7-segment displays, LED matrices
- **Motor control**: Snelheid regelen (volgende lessen)

## Volgende Les

**Les 4: Sensoren** - Temperatuur, afstand, licht meten

In de volgende les leren we:
- Analoge sensoren lezen
- Digitale sensor protocollen (I2C, SPI)
- Data processing en filtering
- Sensor data visualisatie

## Extra Resources

- [PWM Explained (Video)](https://www.youtube.com/watch?v=GQLED3gmONg)
- [Color Theory for Programmers](https://programmingdesignsystems.com/color/)
- [Hardware PWM Pins](https://pinout.xyz/pinout/pwm)
