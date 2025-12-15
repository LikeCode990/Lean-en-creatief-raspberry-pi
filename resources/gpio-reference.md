# GPIO Pin Referentie

## Raspberry Pi GPIO Layout

```
3.3V    (1) (2)  5V
GPIO 2  (3) (4)  5V
GPIO 3  (5) (6)  GND
GPIO 4  (7) (8)  GPIO 14
GND     (9) (10) GPIO 15
GPIO 17 (11)(12) GPIO 18
GPIO 27 (13)(14) GND
GPIO 22 (15)(16) GPIO 23
3.3V    (17)(18) GPIO 24
GPIO 10 (19)(20) GND
GPIO 9  (21)(22) GPIO 25
GPIO 11 (23)(24) GPIO 8
GND     (25)(26) GPIO 7
GPIO 0  (27)(28) GPIO 1
GPIO 5  (29)(30) GND
GPIO 6  (31)(32) GPIO 12
GPIO 13 (33)(34) GND
GPIO 19 (35)(36) GPIO 16
GPIO 26 (37)(38) GPIO 20
GND     (39)(40) GPIO 21
```

## Pin Categorieën

### Power Pins
- **3.3V**: Pin 1, 17
- **5V**: Pin 2, 4
- **GND**: Pin 6, 9, 14, 20, 25, 30, 34, 39

### GPIO Pins (Algemeen Gebruik)
Vrij te gebruiken voor input/output:
- GPIO 4, 17, 27, 22, 5, 6, 13, 19, 26
- GPIO 23, 24, 25
- GPIO 12, 16, 20, 21

### Speciale Functies

#### I2C
- **GPIO 2 (SDA1)**: Pin 3
- **GPIO 3 (SCL1)**: Pin 5

#### SPI
- **GPIO 10 (MOSI)**: Pin 19
- **GPIO 9 (MISO)**: Pin 21
- **GPIO 11 (SCLK)**: Pin 23
- **GPIO 8 (CE0)**: Pin 24
- **GPIO 7 (CE1)**: Pin 26

#### UART
- **GPIO 14 (TXD)**: Pin 8
- **GPIO 15 (RXD)**: Pin 10

#### PWM
Hardware PWM beschikbaar op:
- **GPIO 12**: Pin 32
- **GPIO 13**: Pin 33
- **GPIO 18**: Pin 12
- **GPIO 19**: Pin 35

## Belangrijke Specificaties

### Voltage Limieten
- **GPIO Pins**: 3.3V (NIET 5V tolerant!)
- **Maximum stroom per pin**: 16mA
- **Maximum totale stroom**: 50mA

⚠️ **WAARSCHUWING**: Aansluiten van 5V op GPIO pins beschadigt je Raspberry Pi!

### Pull-up/Pull-down Weerstanden
Alle GPIO pins hebben configureerbare pull-up en pull-down weerstanden:
- **Pull-up**: ~50kΩ naar 3.3V
- **Pull-down**: ~50kΩ naar GND

## Veelgebruikte Pinnen per Project Type

### LEDs (Output)
Aanbevolen pins:
- GPIO 18, 23, 24, 25 (eerste 4 LEDs)
- GPIO 17, 27, 22 (extra LEDs)

### Knoppen (Input)
Aanbevolen pins:
- GPIO 17, 27, 22, 23

### PWM Toepassingen
Gebruik hardware PWM pins voor:
- Servo motors: GPIO 18
- LED dimmen: GPIO 18 of 12
- Buzzer tonen: GPIO 18

### Sensoren

#### Digitale Sensoren
Elke vrije GPIO pin

#### DHT11/DHT22
Vaak gebruikt: GPIO 4

#### Ultrasone (HC-SR04)
- TRIG: GPIO 23
- ECHO: GPIO 24 (met voltage divider!)

#### PIR Sensor
Vaak gebruikt: GPIO 17

### I2C Devices
Gebruik altijd de dedicated I2C pins:
- SDA: GPIO 2 (Pin 3)
- SCL: GPIO 3 (Pin 5)

Voorbeelden:
- OLED displays
- LCD met I2C backpack
- Diverse sensoren (BMP280, etc.)

## Pin Selectie Tips

1. **Reserveer speciale pins**: Houd I2C, SPI vrij als je die niet gebruikt
2. **Groepeer functionaliteit**: Gebruik naburige pins voor gerelateerde functies
3. **Document altijd**: Noteer welke pin je waarvoor gebruikt
4. **Test individueel**: Test elke pin afzonderlijk voor je alles aansluit

## GPIO Commando's in Python

### BCM vs BOARD
```python
import RPi.GPIO as GPIO

# BCM nummering (aanbevolen)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)  # GPIO 18

# BOARD nummering
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)  # Fysieke pin 12 (= GPIO 18)
```

### Pin Status Controleren
```bash
# In terminal
gpio readall

# Of met Python
pinout
```

## Troubleshooting

### Pin werkt niet
1. Controleer of pin niet in gebruik is door ander proces
2. Controleer GPIO.setmode() matching met pin nummer
3. Test met simpel LED circuit
4. Gebruik multimeter om voltage te meten

### Permission Denied
```bash
# Voeg gebruiker toe aan gpio groep
sudo usermod -a -G gpio $USER
```

### GPIO cleanup
```python
# Altijd aan einde van programma
GPIO.cleanup()

# Of specifieke pin
GPIO.cleanup(18)
```
