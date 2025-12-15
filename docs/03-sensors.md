# Werken met Sensoren

## Sensor Types

### Digitale vs Analoge Sensoren

#### Digitale Sensoren
- Output: HIGH (3.3V) of LOW (0V)
- Direct te lezen met GPIO
- Voorbeelden: PIR, knop, sommige afstand sensoren

#### Analoge Sensoren
- Output: Variërend voltage (0-3.3V)
- Raspberry Pi heeft GEEN analoge inputs
- Oplossingen:
  - Gebruik ADC (Analog-Digital Converter) zoals MCP3008
  - Kies digitale alternatief
  - Gebruik Arduino als tussenstuk

### Communicatie Protocols

#### Direct GPIO
- Simpelste vorm
- 1 pin per sensor
- Voorbeelden: DHT11, HC-SR04

#### I2C (Inter-Integrated Circuit)
- 2 draden: SDA (data), SCL (clock)
- Meerdere devices op zelfde bus
- Adressen tot 127 devices
- Voorbeelden: OLED, BMP280, verschillende sensoren

```python
from smbus2 import SMBus

bus = SMBus(1)  # I2C bus 1
address = 0x76  # Device address

# Lees byte
data = bus.read_byte_data(address, register)
```

#### SPI (Serial Peripheral Interface)
- Sneller dan I2C
- 4 draden: MOSI, MISO, SCK, CS
- Voorbeelden: MCP3008 (ADC), sommige displays

#### UART (Serial)
- 2 draden: TX, RX
- Voor serial communicatie
- Voorbeelden: GPS modules, sommige sensoren

## Veelgebruikte Sensoren

### 1. DHT11 / DHT22 - Temperatuur & Luchtvochtigheid

**Specificaties DHT11:**
- Temperatuur: 0-50°C (±2°C)
- Luchtvochtigheid: 20-90% (±5%)
- Sample rate: 1Hz (1x per seconde)

**Specificaties DHT22:**
- Temperatuur: -40 tot 80°C (±0.5°C)
- Luchtvochtigheid: 0-100% (±2-5%)
- Sample rate: 0.5Hz (1x per 2 seconden)

**Aansluiting:**
```
DHT Sensor
  VCC → 3.3V
  GND → GND
  DATA → GPIO 4 (met 10kΩ pull-up)
```

**Code:**
```python
import Adafruit_DHT

sensor = Adafruit_DHT.DHT22
pin = 4

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
    print(f'Temp={temperature:.1f}°C  Humidity={humidity:.1f}%')
```

### 2. HC-SR04 - Ultrasone Afstandssensor

**Specificaties:**
- Bereik: 2cm - 400cm
- Nauwkeurigheid: ±3mm
- Meet hoek: 15°

**⚠️ BELANGRIJK**: Echo pin is 5V output, gebruik voltage divider!

**Aansluiting:**
```
HC-SR04
  VCC → 5V
  GND → GND
  TRIG → GPIO 23
  ECHO → Voltage Divider → GPIO 24
  
Voltage Divider:
  ECHO → 1kΩ → GPIO 24 → 2kΩ → GND
```

**Code:**
```python
import RPi.GPIO as GPIO
import time

TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def measure_distance():
    # Trigger pulse
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    # Wacht op echo
    start_time = time.time()
    while GPIO.input(ECHO) == 0:
        start_time = time.time()
    
    while GPIO.input(ECHO) == 1:
        end_time = time.time()
    
    # Bereken afstand
    duration = end_time - start_time
    distance = (duration * 34300) / 2  # cm
    
    return distance

print(f"Afstand: {measure_distance():.1f} cm")
```

### 3. PIR - Bewegingssensor

**Specificaties:**
- Detectie afstand: tot 7 meter
- Detectie hoek: 110°
- Output: HIGH bij beweging

**Aansluiting:**
```
PIR Sensor
  VCC → 5V
  GND → GND
  OUT → GPIO 17
```

**Code met GPIO Zero:**
```python
from gpiozero import MotionSensor
from signal import pause

pir = MotionSensor(17)

def motion_detected():
    print("Beweging gedetecteerd!")

def no_motion():
    print("Geen beweging meer")

pir.when_motion = motion_detected
pir.when_no_motion = no_motion

print("PIR sensor actief...")
pause()
```

### 4. BMP280/BME280 - Druk & Temperatuur (I2C)

**BME280 heeft ook luchtvochtigheid**

**Specificaties:**
- Luchtdruk: 300-1100 hPa
- Temperatuur: -40 tot 85°C
- Interface: I2C

**Aansluiting:**
```
BMP280
  VCC → 3.3V
  GND → GND
  SCL → GPIO 3 (SCL)
  SDA → GPIO 2 (SDA)
```

**Code:**
```python
from smbus2 import SMBus
from bmp280 import BMP280

bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)

temperature = bmp280.get_temperature()
pressure = bmp280.get_pressure()

print(f'Temperatuur: {temperature:.2f}°C')
print(f'Druk: {pressure:.2f} hPa')
```

### 5. MCP3008 - ADC voor Analoge Sensoren

8-kanaals ADC voor analoge sensoren (LDR, potmeter, etc.)

**Aansluiting via SPI:**
```
MCP3008
  VDD → 3.3V
  VREF → 3.3V
  AGND → GND
  DGND → GND
  CLK → GPIO 11 (SCLK)
  DOUT → GPIO 9 (MISO)
  DIN → GPIO 10 (MOSI)
  CS → GPIO 8 (CE0)
```

## Sensor Best Practices

### 1. Power Management
- Schakel sensoren uit als niet gebruikt
- Gebruik sleep modes
- Meet niet vaker dan nodig

### 2. Data Filtering
```python
# Median filter voor stabielere metingen
import statistics

def read_sensor_filtered(sensor_func, samples=5):
    readings = [sensor_func() for _ in range(samples)]
    return statistics.median(readings)
```

### 3. Error Handling
```python
def safe_read_sensor(sensor_func, retries=3):
    for attempt in range(retries):
        try:
            value = sensor_func()
            if value is not None:
                return value
        except Exception as e:
            print(f"Poging {attempt + 1} mislukt: {e}")
            time.sleep(0.5)
    return None
```

### 4. Calibratie
Sommige sensoren vereisen calibratie:
- LDR: Meet in verschillende lichtcondities
- Soil moisture: Meet in droge en natte grond
- Gas sensors: Warm-up tijd (vaak 24-48 uur)

## Troubleshooting

### Sensor geeft geen data
1. Check voeding (voltage, GND)
2. Check bekabeling
3. Test met simpel voorbeeld
4. Check I2C adres: `i2cdetect -y 1`

### Onstabiele metingen
1. Gebruik kortere kabels
2. Voeg pull-up/pull-down weerstanden toe
3. Filter data (median/average)
4. Check voltage stabiliteit

### I2C werkt niet
```bash
# Schakel I2C in
sudo raspi-config
# Interface Options → I2C → Enable

# Installeer tools
sudo apt install i2c-tools

# Scan voor devices
i2cdetect -y 1
```

## Sensor Projectideeën

1. **Weerstation**: DHT22 + BMP280 + LDR
2. **Security systeem**: PIR + camera
3. **Plant monitor**: Soil moisture + licht + temp
4. **Parkeer sensor**: Ultrasone + LEDs
5. **Luchtkwaliteit**: MQ-135 gas sensor + display

## Volgende Stappen

- Experimenteer met één sensor tegelijk
- Combineer sensoren voor complexe projecten
- Implementeer data logging
- Maak visualisaties van sensor data
