# Project 2: Temperatuur Monitor

## Doel
Bouw een temperatuur monitoring systeem dat data logt en visualiseert.

## Leerdoelen
- Sensoren uitlezen (DHT11/DHT22 of DS18B20)
- Data opslaan in bestanden
- Data visualiseren
- Alerts implementeren
- IoT concepten toepassen

## Hardware Benodigdheden

### Optie A: DHT11/DHT22 (Temperatuur + Luchtvochtigheid)
- 1x DHT11 of DHT22 sensor
- 1x 10kΩ pull-up weerstand (vaak al op module)
- Jumper draden

### Optie B: DS18B20 (Alleen temperatuur, nauwkeuriger)
- 1x DS18B20 sensor
- 1x 4.7kΩ pull-up weerstand
- Jumper draden

## Aansluiting DHT11/DHT22

```
DHT Sensor
  VCC → 3.3V
  GND → GND
  DATA → GPIO 4 (met 10kΩ pull-up naar 3.3V)
```

## Software Requirements

```bash
# Voor DHT sensor
pip3 install Adafruit-DHT

# Voor DS18B20
# Geen extra library nodig, gebruikt 1-wire interface
```

## Functionele Requirements

### MVP (Minimum Viable Product)
- [x] Temperatuur uitlezen
- [x] Temperatuur tonen op console
- [x] Elke 5 seconden meten

### Iteratie 1
- [x] Data opslaan in CSV bestand
- [x] Timestamp toevoegen

### Iteratie 2
- [x] Grafiek genereren
- [x] Gemiddelden berekenen

### Iteratie 3
- [x] Alert bij te hoge/lage temperatuur
- [x] Email notificatie (optioneel)

## Code Structuur

```python
import time
import csv
from datetime import datetime

class TemperatureMonitor:
    def __init__(self, sensor_pin, log_file='temp_log.csv'):
        self.sensor_pin = sensor_pin
        self.log_file = log_file
        
    def read_temperature(self):
        """Lees temperatuur van sensor"""
        pass
    
    def log_data(self, temp, humidity=None):
        """Sla data op in CSV"""
        pass
    
    def check_alerts(self, temp):
        """Controleer of temperatuur buiten grenzen is"""
        pass
    
    def run(self, interval=5):
        """Hoofdloop"""
        pass
```

## Implementatie Stappen

### Stap 1: Sensor Test
```python
# Test of sensor werkt
# Print waarden naar console
```

### Stap 2: Data Logging
```python
# Implementeer CSV logging
# Voeg timestamp toe
```

### Stap 3: Visualisatie
```python
# Gebruik matplotlib om grafiek te maken
import matplotlib.pyplot as plt
import pandas as pd

# Lees CSV en maak grafiek
```

### Stap 4: Alerts
```python
# Implementeer min/max grenzen
# Print waarschuwingen
```

## Lean Aanpak

### Waarde Stroom
1. **Meten** → 2. **Opslaan** → 3. **Analyseren** → 4. **Actie**

### Verspilling Elimineren
- Niet te vaak meten (energiebesparing)
- Alleen nodige data opslaan
- Efficiënte datastructuur kiezen

### Continue Verbetering
- Week 1: Basis logging
- Week 2: Visualisatie toevoegen
- Week 3: Alerts implementeren
- Week 4: Web interface

## Test Criteria
- [ ] Sensor leest correcte waarden
- [ ] Data wordt opgeslagen met timestamp
- [ ] CSV bestand is correct geformatteerd
- [ ] Grafieken zijn leesbaar
- [ ] Alerts werken bij limietoverschrijding

## Creatieve Uitbreidingen

### Beginner
1. LED indicator (groen=OK, rood=alert)
2. Meerdere sensoren
3. Min/max waarden bijhouden

### Gemiddeld
4. Web dashboard met Flask
5. Real-time grafiek
6. Database ipv CSV (SQLite)

### Gevorderd
7. MQTT voor IoT communicatie
8. Cloud upload (ThingSpeak, AWS)
9. Machine learning voor voorspelling
10. Mobile app notificaties

## Voorbeeld Output

### Console
```
2025-12-15 14:30:00 - Temp: 21.5°C, Humidity: 45%
2025-12-15 14:30:05 - Temp: 21.6°C, Humidity: 45%
2025-12-15 14:30:10 - Temp: 21.5°C, Humidity: 46%
```

### CSV Format
```csv
timestamp,temperature,humidity
2025-12-15 14:30:00,21.5,45
2025-12-15 14:30:05,21.6,45
2025-12-15 14:30:10,21.5,46
```

## Troubleshooting

**DHT sensor geeft geen data:**
```bash
# Check wiring
# Try different GPIO pin
# Ensure pull-up resistor is connected
```

**Permission errors:**
```bash
sudo pip3 install Adafruit-DHT
```

## Bronnen
- [DHT Sensor Tutorial](https://learn.adafruit.com/dht/overview)
- [Matplotlib Tutorials](https://matplotlib.org/stable/tutorials/index.html)
- [CSV in Python](https://docs.python.org/3/library/csv.html)
