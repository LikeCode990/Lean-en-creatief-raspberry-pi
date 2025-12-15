# Web Dashboard voor Raspberry Pi

## Beschrijving
Een volledige web applicatie om je Raspberry Pi te besturen via je browser. Bekijk sensor data in real-time en bedien GPIO outputs zoals LEDs.

## Leerdoelen
- Flask web framework gebruiken
- REST API's maken
- Real-time data updates implementeren
- HTML/CSS/JavaScript integreren met hardware
- Responsive web design toepassen

## Features

### ✨ Functionaliteit
- **Sensor monitoring**: Bekijk temperatuur en luchtvochtigheid
- **LED besturing**: Bedien meerdere LEDs via knoppen
- **Auto-refresh**: Data wordt elke 5 seconden automatisch bijgewerkt
- **Responsive design**: Werkt op desktop, tablet en mobiel
- **Keyboard shortcuts**: Snelle bediening met toetsenbord
- **Real-time feedback**: Visuele indicatoren voor LED status

### 🎨 User Interface
- Modern en kleurrijk design
- Duidelijke status indicators
- Gebruiksvriendelijke knoppen
- Smooth animaties

## Hardware Benodigdheden

### Minimum (Demo Modus)
- Raspberry Pi met netwerk verbinding
- 2x LED (elke kleur)
- 2x 220Ω weerstand
- Breadboard en jumper draden

### Volledig (Met Sensor)
- Bovenstaande items
- DHT22 temperatuur/luchtvochtigheid sensor
- 10kΩ pull-up weerstand (vaak al op module)

## Aansluiting

```
LED 1:
  GPIO 18 → 220Ω → LED (+) → LED (-) → GND

LED 2:
  GPIO 23 → 220Ω → LED (+) → LED (-) → GND

DHT22 Sensor (optioneel):
  VCC → 3.3V
  GND → GND
  DATA → GPIO 4 (met 10kΩ pull-up naar 3.3V)
```

## Installatie

### 1. Installeer Flask
```bash
pip3 install flask
```

### 2. Installeer DHT Library (optioneel)
Alleen nodig als je een echte DHT sensor gebruikt:
```bash
sudo pip3 install Adafruit-DHT
```

### 3. Download de Code
```bash
cd examples/04-web-dashboard
```

## Gebruik

### Server Starten
```bash
python3 app.py
```

Je ziet output zoals:
```
==================================================
Raspberry Pi Web Dashboard
==================================================
LED 1: GPIO 18
LED 2: GPIO 23
DHT Sensor: GPIO 4
==================================================

Server gestart op http://0.0.0.0:5000
Druk Ctrl+C om te stoppen
```

### Toegang tot Dashboard
Open een browser op je computer of mobiel en ga naar:
- `http://raspberrypi.local:5000` (als mDNS werkt)
- `http://192.168.1.XXX:5000` (vervang XXX met IP van je Pi)

### IP Adres Vinden
```bash
hostname -I
```

## Functionaliteit

### Sensor Data
- Toont huidige temperatuur en luchtvochtigheid
- Update timestamp
- Status indicator (Demo/Actief)
- Auto-refresh elke 5 seconden
- Handmatige refresh knop

### LED Besturing
Elke LED heeft 3 knoppen:
- **Toggle**: Schakel LED om (aan→uit of uit→aan)
- **Aan**: Zet LED aan
- **Uit**: Zet LED uit

Visuele indicator toont LED status:
- Grijs = uit
- Geel gloeiend = aan

### Keyboard Shortcuts
- **Spatiebalk**: Ververs sensor data
- **1**: Toggle LED 1
- **2**: Toggle LED 2

## API Endpoints

De applicatie biedt een REST API:

### GET /api/sensor
Haal sensor data op
```json
{
  "temperature": 21.5,
  "humidity": 45.0,
  "timestamp": "2025-12-15 14:30:00",
  "status": "success"
}
```

### POST /api/led/1/toggle
Toggle LED 1
```json
{
  "led": 1,
  "state": true
}
```

### POST /api/led/1/state
Zet LED naar specifieke state
```bash
curl -X POST http://raspberrypi.local:5000/api/led/1/state \
  -H "Content-Type: application/json" \
  -d '{"state": true}'
```

### GET /api/status
Haal status van alle componenten op
```json
{
  "led1": true,
  "led2": false,
  "uptime": 1234567.89
}
```

## Project Structuur

```
04-web-dashboard/
├── app.py                 # Flask applicatie (backend)
├── templates/
│   └── index.html        # HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── app.js        # Frontend JavaScript
└── README.md             # Deze documentatie
```

## Uitbreidingen

### Beginner
1. Voeg meer LEDs toe
2. Verander kleuren in CSS
3. Pas refresh interval aan
4. Voeg een titel/naam toe

### Gemiddeld
5. Voeg meer sensoren toe (afstand, licht)
6. Implementeer data logging naar CSV
7. Maak grafieken met Chart.js
8. Voeg PWM slider toe voor LED dimmen

### Gevorderd
9. Voeg authenticatie toe (login)
10. Implementeer WebSocket voor real-time updates
11. Maak database voor historische data
12. Voeg camera stream toe
13. Implementeer MQTT voor IoT

## Demo Modus

Als je geen DHT sensor hebt, werkt de applicatie in demo modus:
- Toont dummy sensor data
- Alle LED functies werken normaal
- Waarschuwing in UI dat het demo data is

## Troubleshooting

### Server start niet
```bash
# Check of Flask geïnstalleerd is
pip3 list | grep -i flask

# Check of poort 5000 vrij is
sudo netstat -tulpn | grep 5000

# Gebruik andere poort in app.py:
# app.run(host='0.0.0.0', port=8080)
```

### Kan niet verbinden via browser
```bash
# Check firewall
sudo ufw allow 5000

# Check IP adres
hostname -I

# Test lokaal
curl http://localhost:5000
```

### LEDs reageren niet
- Controleer GPIO pinnen in circuit
- Controleer LED polariteit
- Test LEDs met basis voorbeeld
- Check `app.py` voor correcte pin nummers

### Sensor geeft geen data
- DHT22 library niet geïnstalleerd → Werkt in demo modus
- Verkeerde pin → Pas `DHT_PIN` aan in `app.py`
- Sensor kapot → Test met apart script

## Beveiliging

⚠️ **Waarschuwing**: Deze applicatie heeft GEEN authenticatie!

Deze applicatie is bedoeld voor educatief gebruik in een vertrouwd netwerk (bijv. thuis). Voor productie of onveilige netwerken:

### Debug Mode
Debug mode is uitgeschakeld in de code voor veiligheid. Debug mode kan code execution mogelijk maken.

```python
# Alleen voor development op localhost
app.run(host='127.0.0.1', port=5000, debug=True)

# Voor productie (standaard in dit voorbeeld)
app.run(host='0.0.0.0', port=5000, debug=False)
```

### Authenticatie Toevoegen
Voor productie gebruik:
```python
# Voeg login toe
from flask_login import LoginManager

# Of beperk toegang tot lokaal netwerk
app.run(host='127.0.0.1', port=5000)
```

## Prestaties

- Lichtgewicht Flask applicatie
- Minimaal CPU gebruik
- Werkt goed op Pi Zero W en hoger
- Auto-refresh kan CPU belasten bij veel clients

## Lean Principes Toegepast

1. **MVP eerst**: Basis LED + dummy data werkt zonder hardware
2. **Iteratief**: Voeg sensor toe als je die hebt
3. **User Value**: Direct bruikbaar via browser
4. **Eenvoud**: Geen complexe setup nodig
5. **Uitbreidbaar**: Makkelijk features toe te voegen

## Bronnen

- [Flask Documentatie](https://flask.palletsprojects.com/)
- [JavaScript Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [Responsive Design](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design)
- [REST API Best Practices](https://restfulapi.net/)

## Volgende Stappen

1. Start de server en test alle functies
2. Probeer de keyboard shortcuts
3. Open dashboard op je mobiel
4. Experimenteer met API endpoints
5. Voeg je eigen uitbreidingen toe!
