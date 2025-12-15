# Hardware Setup Guide

## Benodigde Componenten

### Basis Kit
- **Raspberry Pi**: Model 3B+, 4, of nieuwer
  - Aanbevolen: Raspberry Pi 4 (2GB RAM of meer)
- **microSD kaart**: Minimaal 16GB, Class 10
  - Aanbevolen: 32GB voor meer ruimte
- **Voeding**: 5V USB-C (Pi 4) of micro-USB (Pi 3)
  - Minimaal 2.5A, aanbevolen 3A
- **Breadboard**: 830 punten (standaard formaat)
- **Jumper wires**:
  - 20x Male-to-Female (Pi naar breadboard)
  - 20x Male-to-Male (breadboard verbindingen)

### Elektronische Componenten

#### LED's
- 5x Rood (5mm)
- 5x Groen (5mm)
- 5x Geel (5mm)
- 2x RGB LED (common cathode)
- 1x Blauw (5mm)

#### Weerstanden
- 10x 220Ω (voor LED's)
- 5x 10kΩ (pull-up/pull-down)
- 5x 1kΩ (algemeen gebruik)
- 2x 2kΩ (voltage dividers)

#### Input Componenten
- 5x Tactile push buttons
- 1x Potentiometer 10kΩ

#### Sensoren (Optioneel voor gevorderde lessen)
- 1x HC-SR04 Ultrasonic sensor
- 1x DHT11 of DHT22 Temperatuur/Vochtigheid sensor
- 1x LDR (Light Dependent Resistor)
- 1x PIR Motion sensor

#### Audio
- 1x Passive buzzer
- 1x Active buzzer (optioneel)

## GPIO Pinout Referentie

### Raspberry Pi GPIO Layout

```
3V3  (1)  (2)  5V
GPIO2  (3)  (4)  5V
GPIO3  (5)  (6)  GND
GPIO4  (7)  (8)  GPIO14
GND    (9)  (10) GPIO15
GPIO17 (11) (12) GPIO18
GPIO27 (13) (14) GND
GPIO22 (15) (16) GPIO23
3V3    (17) (18) GPIO24
GPIO10 (19) (20) GND
GPIO9  (21) (22) GPIO25
GPIO11 (23) (24) GPIO8
GND    (25) (26) GPIO7
...
```

### Pin Aanbevelingen

#### Output Pins (LED's, etc.)
- GPIO 17, 18, 27, 22, 23, 24, 25

#### PWM Capable Pins
- GPIO 12, 13, 18, 19 (Hardware PWM)
- Alle GPIO pins (Software PWM)

#### Input Pins (Buttons, Sensors)
- GPIO 2, 3, 4, 14, 15

## Basis Circuits

### 1. LED Circuit

```
Raspberry Pi GPIO -> 220Ω Resistor -> LED Anode (+)
                     LED Cathode (-) -> GND
```

**Belangrijk**: Altijd een weerstand gebruiken (220Ω voor standaard LED's)!

### 2. Button Circuit (Pull-down)

```
3.3V -> Button -> GPIO Pin
GPIO Pin -> 10kΩ Resistor -> GND
```

### 3. RGB LED Circuit

```
GPIO 17 (Rood)   -> 220Ω -> RGB LED R pin
GPIO 27 (Groen)  -> 220Ω -> RGB LED G pin
GPIO 22 (Blauw)  -> 220Ω -> RGB LED B pin
RGB LED Common Cathode -> GND
```

### 4. Ultrasonic Sensor (HC-SR04)

**Let op**: HC-SR04 ECHO pin geeft 5V uit, maar Raspberry Pi GPIO accepteert max 3.3V!

```
Sensor VCC    -> 5V
Sensor GND    -> GND
Sensor TRIG   -> GPIO 23
Sensor ECHO   -> Voltage Divider -> GPIO 24
```

**Voltage Divider voor ECHO pin**:
```
ECHO -> 1kΩ -> GPIO 24
GPIO 24 -> 2kΩ -> GND
```
Dit reduceert 5V naar ~3.3V.

## Veiligheidsrichtlijnen

### ⚠️ BELANGRIJK

1. **Spanning Check**
   - Raspberry Pi GPIO pins zijn 3.3V
   - Sluit NOOIT 5V direct aan op GPIO pins
   - Gebruik voltage dividers voor 5V signalen

2. **Stroomlimieten**
   - Maximale stroom per GPIO pin: 16mA
   - Totale stroom alle pins: 50mA
   - Gebruik altijd weerstanden bij LED's

3. **Kortsluiting Preventie**
   - Controleer alle verbindingen voordat je de Pi aanzet
   - Let op polariteit van LED's en sensoren
   - Gebruik multimeter om verbindingen te testen

4. **Statische Elektriciteit**
   - Raak grond aan voor je componenten aanraakt
   - Werk op antistatisch oppervlak indien mogelijk

5. **Debugging**
   - Test circuits stap voor stap
   - Begin met eenvoudige LED test
   - Gebruik multimeter voor voltage/continuity checks

## Breadboard Layout Voorbeeld

### Basis Setup
```
                 Raspberry Pi
                     |
         +-----------+-----------+
         |                       |
    [Breadboard]            [Breadboard]
    Power Rails             Components
    - 3.3V Bus              - LED's
    - GND Bus               - Buttons
    - 5V Bus                - Sensors
```

### Best Practices
1. Gebruik rode draad voor power (3.3V/5V)
2. Gebruik zwarte draad voor GND
3. Gebruik andere kleuren voor signalen
4. Houd power rails links, componenten rechts
5. Organiseer draden netjes (geen "spaghetti")

## Software Setup

Zie de hoofdpagina README.md voor gedetailleerde software installatie instructies.

## Troubleshooting

### LED gaat niet aan
- Check polariteit (lange poot = anode = +)
- Controleer weerstand waarde
- Test met multimeter
- Verifieer GPIO pin nummer in code

### Button werkt niet
- Check pull-up/pull-down configuratie
- Test button met multimeter
- Voeg debounce delay toe

### Sensor geeft rare waarden
- Controleer voltage levels
- Verifieer timing in code
- Test met voorbeeld code eerst

## Aanvullende Resources

- [Raspberry Pi GPIO Pinout](https://pinout.xyz/)
- [Resistor Color Code Calculator](https://www.digikey.com/en/resources/conversion-calculators/conversion-calculator-resistor-color-code)
- [LED Calculator](https://www.ledcalculator.net/)
