# Hardware Componenten Lijst

## Basis Starter Kit

### Essentieel
- **Raspberry Pi** (Model 3B+ of nieuwer)
  - Raspberry Pi 4 (2GB of meer) aanbevolen
- **MicroSD Kaart** (minimaal 16GB, Class 10)
- **Voeding** (5V, 3A USB-C voor Pi 4, of 2.5A micro-USB voor Pi 3)
- **Breadboard** (830 tie-points)
- **Jumper Draden** (male-to-male, male-to-female, female-to-female)

### Basis Componenten
- **LEDs** (5mm, verschillende kleuren)
  - Rood: 10x
  - Geel: 10x
  - Groen: 10x
  - Blauw: 5x
  - Wit: 5x
- **Weerstanden**
  - 220Ω: 20x (voor LEDs)
  - 1kΩ: 10x
  - 10kΩ: 10x
- **Drukknoppen** (tactile push buttons): 5x
- **Buzzer** (passief en actief): 2x

## Sensoren

### Temperatuur & Luchtvochtigheid
- **DHT11** - Goedkoop, basis (temperatuur ±2°C)
- **DHT22/AM2302** - Nauwkeuriger (temperatuur ±0.5°C)
- **DS18B20** - Waterproof, zeer nauwkeurig

### Afstand
- **HC-SR04** - Ultrasone afstandssensor (2-400cm)
- **VL53L0X** - Laser afstand sensor (2-200cm)

### Licht
- **LDR** (Light Dependent Resistor)
- **BH1750** - Digitale licht sensor

### Beweging
- **PIR** - Passive Infrared sensor (bewegingsdetectie)

### Andere
- **MQ-2** - Gas/rook sensor
- **Soil Moisture** - Vochtigheid sensor

## Actuatoren

### Motoren
- **Servo Motor** (SG90 of MG90S)
- **DC Motor** (3-6V) met **L298N Motor Driver**
- **Stepper Motor** (28BYJ-48) met **ULN2003 Driver**

### Displays
- **16x2 LCD** (met I2C module)
- **4-digit 7-segment display** (TM1637)
- **OLED Display** (0.96" SSD1306, I2C)

### Geluid
- **Buzzer** (actief en passief)
- **Small Speaker** (met amplifier module)

## Communicatie Modules

- **HC-05/HC-06** - Bluetooth module
- **NRF24L01** - 2.4GHz draadloze transceiver
- **ESP8266** - WiFi module

## Tools & Accessoires

### Meetapparatuur
- **Multimeter** (voor voltage, stroom, weerstand meten)
- **GPIO Reference Card** (pin layout)

### Bekabeling
- **Breadboard** (meerdere formaten handig)
- **Jumper Wires** (verschillende lengtes)
- **Dupont Connectors**

### Opslag
- **Component Box** (met vakjes voor organisatie)

## Kosten Indicatie

### Budget Starter (~€50-75)
- Raspberry Pi 3B+
- 16GB SD kaart
- Basis componenten (LEDs, weerstanden, knoppen)
- Breadboard en draden
- 1-2 basis sensoren

### Standaard Kit (~€100-150)
- Raspberry Pi 4 (4GB)
- 32GB SD kaart
- Uitgebreide componenten
- 5-10 verschillende sensoren
- Meerdere actuatoren
- Display module

### Professioneel (~€200-300)
- Raspberry Pi 4 (8GB)
- Premium componenten
- Alle genoemde sensoren
- Motor drivers
- Displays
- Communicatie modules
- Meetapparatuur

## Waar te Kopen?

### Nederland
- **Kiwi Electronics** - kiwi-electronics.nl
- **SOS Solutions** - sossolutions.nl
- **Antratek** - antratek.nl

### Internationaal
- **AliExpress** - Goedkoop, langere levertijd
- **Amazon** - Snelle levering, iets duurder
- **Adafruit** - Kwaliteitscomponenten, tutorials
- **SparkFun** - Kwaliteitscomponenten, educatief

## Tips

1. **Start klein**: Begin met basis kit en breid uit
2. **Koop sets**: Component kits zijn vaak voordeliger
3. **Let op kwaliteit**: Goedkope sensoren kunnen onbetrouwbaar zijn
4. **Voorraad**: Heb altijd reserve LEDs en weerstanden
5. **Organisatie**: Label en organiseer componenten direct

## Per Project

### Project 1: Verkeerslicht
- 3x LED (rood, geel, groen)
- 3x 220Ω weerstand
- Breadboard en draden

### Project 2: Temperatuur Monitor
- 1x DHT11 of DHT22
- 1x 10kΩ weerstand (pull-up)
- Draden

### Project 3: Smart Home
- 1x PIR sensor
- 2x Relay module
- 1x DHT22
- 1x OLED display
- Diverse LEDs en weerstanden
