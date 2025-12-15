# GPIO Programmering Basis

## Wat is GPIO?

GPIO staat voor General Purpose Input/Output. Het zijn de pinnen op de Raspberry Pi waarmee je elektronische componenten kunt aansturen (output) of uitlezen (input).

## GPIO Nummering

Er zijn twee manieren om GPIO pinnen te nummeren:
- **BCM (Broadcom)**: Gebruikt de GPIO nummers zoals gedefinieerd door de chip
- **BOARD**: Gebruikt de fysieke pinnummers op de header (1-40)

**We gebruiken BCM nummering in deze cursus.**

## Basis LED Circuit

### Benodigdheden
- 1x LED (elke kleur)
- 1x 220Ω weerstand
- Breadboard
- Jumper draden

### Aansluiting
```
Raspberry Pi GPIO 18 (Pin 12) → 220Ω weerstand → LED (lange poot) → LED (korte poot) → GND
```

## RPi.GPIO Library

### Basis Template

```python
import RPi.GPIO as GPIO
import time

# Setup
GPIO.setmode(GPIO.BCM)  # BCM nummering gebruiken
GPIO.setwarnings(False)  # Waarschuwingen uitschakelen

# Configureer pin als output
LED_PIN = 18
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    # Hoofdcode hier
    GPIO.output(LED_PIN, GPIO.HIGH)  # LED aan
    time.sleep(1)
    GPIO.output(LED_PIN, GPIO.LOW)   # LED uit
    
except KeyboardInterrupt:
    print("\nProgramma gestopt door gebruiker")
    
finally:
    # Altijd opruimen
    GPIO.cleanup()
```

### Output Voorbeeld: LED Knipperen

```python
import RPi.GPIO as GPIO
import time

LED_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)
        print("LED aan")
        time.sleep(1)
        
        GPIO.output(LED_PIN, GPIO.LOW)
        print("LED uit")
        time.sleep(1)
        
except KeyboardInterrupt:
    print("\nGestopt")
    
finally:
    GPIO.cleanup()
```

### Input Voorbeeld: Knop Uitlezen

```python
import RPi.GPIO as GPIO
import time

BUTTON_PIN = 17
LED_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        button_state = GPIO.input(BUTTON_PIN)
        
        if button_state == GPIO.LOW:  # Knop ingedrukt
            GPIO.output(LED_PIN, GPIO.HIGH)
            print("Knop ingedrukt - LED aan")
        else:
            GPIO.output(LED_PIN, GPIO.LOW)
            print("Knop niet ingedrukt - LED uit")
            
        time.sleep(0.1)  # Korte delay
        
except KeyboardInterrupt:
    print("\nGestopt")
    
finally:
    GPIO.cleanup()
```

## GPIO Zero Library

GPIO Zero is een modernere, gebruiksvriendelijkere library.

### LED Knipperen met GPIO Zero

```python
from gpiozero import LED
from time import sleep

led = LED(18)

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
```

Of nog simpeler:
```python
from gpiozero import LED

led = LED(18)
led.blink()  # Knippert automatisch!

# Program draait door
from signal import pause
pause()
```

### Knop met GPIO Zero

```python
from gpiozero import Button, LED
from signal import pause

button = Button(17)
led = LED(18)

button.when_pressed = led.on
button.when_released = led.off

print("Druk op de knop...")
pause()
```

## PWM (Pulse Width Modulation)

PWM laat je de helderheid van een LED of snelheid van een motor regelen.

### PWM met RPi.GPIO

```python
import RPi.GPIO as GPIO
import time

LED_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# PWM met 100Hz frequentie
pwm = GPIO.PWM(LED_PIN, 100)
pwm.start(0)  # Start met 0% duty cycle

try:
    while True:
        # Geleidelijk helderder
        for duty_cycle in range(0, 101, 5):
            pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(0.1)
        
        # Geleidelijk donkerder
        for duty_cycle in range(100, -1, -5):
            pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(0.1)
            
except KeyboardInterrupt:
    pass
    
finally:
    pwm.stop()
    GPIO.cleanup()
```

### PWM met GPIO Zero

```python
from gpiozero import PWMLED
from time import sleep

led = PWMLED(18)

while True:
    # Fade in
    for i in range(100):
        led.value = i / 100
        sleep(0.01)
    
    # Fade out
    for i in range(100, 0, -1):
        led.value = i / 100
        sleep(0.01)
```

Of gebruik de ingebouwde functie:
```python
from gpiozero import PWMLED
from signal import pause

led = PWMLED(18)
led.pulse()  # Automatisch pulseren!

pause()
```

## Best Practices

1. **Altijd GPIO.cleanup() gebruiken**
   - Voorkomt problemen bij het opnieuw starten
   - Gebruik `try-finally` block

2. **Pull-up/Pull-down weerstanden**
   - Voorkomt zwevende inputs
   - Gebruik `GPIO.PUD_UP` of `GPIO.PUD_DOWN`

3. **Stroomlimieten**
   - Gebruik altijd weerstanden met LEDs
   - Maximaal 16mA per pin
   - Maximaal 50mA totaal voor alle pins

4. **Voltage**
   - GPIO pinnen zijn 3.3V
   - NOOIT 5V direct op GPIO aansluiten!

## Opdrachten

1. Maak een verkeerslicht met 3 LEDs
2. Maak een knop die een teller bijhoudt
3. Maak een LED die langzaam in en uit fade
4. Maak een "reactiespel" met knop en LED

## Volgende Stappen

- [03-sensors.md](03-sensors.md) - Werken met sensoren
- [../examples/](../examples/) - Meer voorbeelden
