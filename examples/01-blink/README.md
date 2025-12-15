# LED Knipperen

## Beschrijving
Dit is het "Hello World" van Raspberry Pi GPIO programmering. Een simpele LED die aan en uit gaat.

## Leerdoelen
- GPIO pin configureren als output
- Digitale output aansturen (HIGH/LOW)
- Time delays gebruiken
- GPIO cleanup correct uitvoeren

## Hardware Benodigdheden
- 1x LED (elke kleur)
- 1x 220Ω weerstand
- Breadboard
- 2x jumper draden (male-female)

## Schematische Aansluiting

```
Raspberry Pi                  Breadboard
  GPIO 18 (pin 12) -----> 220Ω weerstand -----> LED (+, lange poot)
                                                   |
  GND (pin 6)      <---------------------------- LED (-, korte poot)
```

## Gebruik

```bash
python3 blink.py
```

Druk op Ctrl+C om te stoppen.

## Uitbreidingen

1. **Verschillende snelheden**: Pas `BLINK_INTERVAL` aan
2. **Morse code**: Implementeer punten en strepen
3. **Meerdere LEDs**: Gebruik meerdere GPIO pinnen
4. **Patronen**: Maak een knipperpatroon (bijv. 2x snel, 1x langzaam)

## Troubleshooting

**LED knippert niet:**
- Controleer of LED correct om aangesloten is (lange poot naar weerstand)
- Controleer GPIO pin nummer (fysiek pin 12 = GPIO 18)
- Test LED met een batterij

**Permission denied error:**
```bash
sudo usermod -a -G gpio $USER
# Log uit en weer in
```

**GPIO already in use:**
```bash
# Reset GPIO
sudo python3 -c "import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM); GPIO.cleanup()"
```
