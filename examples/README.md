# Sensor Voorbeelden

Deze map bevat praktische Python voorbeelden voor verschillende sensoren op de Raspberry Pi.

## 📁 Beschikbare Scripts

### 1. DHT22 Temperatuur & Luchtvochtigheid
**Bestand:** [dht22_sensor.py](dht22_sensor.py)

Meet temperatuur en luchtvochtigheid met een DHT22 sensor.

```bash
python3 dht22_sensor.py
```

**Hardware nodig:**
- DHT22 sensor
- 10kΩ pull-up resistor

### 2. HC-SR04 Afstandssensor
**Bestand:** [hc_sr04_distance.py](hc_sr04_distance.py)

Meet afstand met een ultrasone sensor.

⚠️ **Let op:** Gebruik een voltage divider voor de ECHO pin!

```bash
python3 hc_sr04_distance.py
```

**Hardware nodig:**
- HC-SR04 ultrasone sensor
- 1kΩ resistor
- 2kΩ resistor

### 3. PIR Bewegingssensor
**Bestand:** [pir_motion_sensor.py](pir_motion_sensor.py)

Detecteer beweging met een PIR sensor.

```bash
python3 pir_motion_sensor.py
```

**Hardware nodig:**
- PIR sensor (bijv. HC-SR501)

### 4. Multi-Sensor Dashboard
**Bestand:** [multi_sensor_dashboard.py](multi_sensor_dashboard.py)

Geavanceerd voorbeeld dat meerdere sensoren combineert met data logging.

```bash
python3 multi_sensor_dashboard.py
```

**Hardware nodig:**
- DHT22 sensor
- HC-SR04 sensor
- PIR sensor

## 📦 Installatie Vereisten

Installeer de benodigde Python libraries:

```bash
# Update package lijst
sudo apt-get update

# Installeer Python dependencies
sudo apt-get install -y python3-pip python3-dev

# DHT22 library
sudo pip3 install Adafruit_DHT

# GPIO Zero (meestal al geïnstalleerd)
sudo pip3 install gpiozero

# RPi.GPIO (meestal al geïnstalleerd)
sudo pip3 install RPi.GPIO
```

## 🔌 GPIO Pin Configuratie

Standaard pin configuratie voor alle scripts:

| Sensor  | Component | GPIO Pin | Physical Pin |
|---------|-----------|----------|--------------|
| DHT22   | DATA      | GPIO 4   | Pin 7        |
| HC-SR04 | TRIG      | GPIO 23  | Pin 16       |
| HC-SR04 | ECHO      | GPIO 24  | Pin 18       |
| PIR     | OUT       | GPIO 17  | Pin 11       |

**Gemeenschappelijke aansluitingen:**
- 3.3V: Pin 1
- 5V: Pin 2
- Ground: Pin 6, 9, 14, 20, etc.

## 🎓 Leerdoelen

Door deze voorbeelden te bestuderen en uit te voeren leer je:

1. **Basis sensor interfacing**
   - Digitale inputs lezen
   - Pulsen genereren en meten
   - Event-driven programmering

2. **Error handling**
   - Timeout afhandeling
   - Sensor validatie
   - Graceful shutdown

3. **Data verwerking**
   - Berekeningen met sensor data
   - Waarschuwingen en thresholds
   - Data logging naar bestanden

4. **Best practices**
   - Code structuur
   - Comments en documentatie
   - GPIO cleanup

## 🔧 Troubleshooting

### "No module named 'Adafruit_DHT'"
```bash
sudo pip3 install Adafruit_DHT
```

### "Permission denied" errors
```bash
sudo python3 script.py
```

Of voeg je gebruiker toe aan de gpio groep:
```bash
sudo usermod -a -G gpio $USER
# Log uit en weer in
```

### Sensor geeft geen data
1. Controleer alle aansluitingen
2. Controleer GPIO pin nummers
3. Wacht tot sensor gestabiliseerd is (vooral PIR)
4. Controleer voltage divider (bij HC-SR04)
5. Test met multimeter of sensor power krijgt

### HC-SR04 timeout errors
- Controleer voltage divider correct is
- Zorg dat niets de sensor blokkeert
- Sensor heeft vrij zicht nodig
- Test binnen bereik (2-400 cm)

## 📚 Meer Informatie

Voor meer details over sensoren, zie:
- [docs/03-sensors.md](../docs/03-sensors.md) - Uitgebreide sensor documentatie
- [docs/02-gpio-basics.md](../docs/02-gpio-basics.md) - GPIO fundamentals

## 💡 Uitbreidingen

Ideeën om deze voorbeelden uit te breiden:

1. **Web interface** - Toon sensor data in browser
2. **Database logging** - Sla data op in SQLite of MySQL
3. **Grafieken** - Visualiseer data met matplotlib
4. **Alerting** - Stuur email/SMS bij events
5. **MQTT** - Publiceer data naar IoT platform
6. **Home automation** - Integreer met Home Assistant

## 📝 Licentie

Deze voorbeelden zijn onderdeel van het "Lean en Creatief met Raspberry Pi" keuzedeel.
