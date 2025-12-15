# HC-SR04 Sensor with Web Dashboard

## 🎯 Overzicht

Deze oplossing gebruikt **gescheiden technologieën** voor optimale prestaties:
- **Python** (backend) - Voor sensor data acquisitie via GPIO
- **HTML/CSS/JavaScript** (frontend) - Voor web interface

## 📁 Bestanden

### 1. Python API Server
**Bestand:** `hc_sr04_api_server.py`

Lightweight Python HTTP server zonder externe dependencies (geen Flask!).
- Leest HC-SR04 sensor via GPIO
- Serveert data als JSON via REST API
- Gebruikt alleen Python standard library

### 2. Web Dashboard
**Bestand:** `sensor_dashboard.html`

Pure HTML/CSS/JavaScript interface.
- Moderne, responsive design
- Real-time data updates
- Grafieken en statistieken
- Werkt in elke browser

## 🚀 Gebruik

### Stap 1: Start de Python API Server

```bash
python3 hc_sr04_api_server.py
```

De server start op poort 8080 en begint sensor data te verzamelen.

### Stap 2: Open de Web Dashboard

**Optie A - Direct openen:**
```bash
# Open het HTML bestand in je browser
xdg-open sensor_dashboard.html
# Of dubbelklik op het bestand
```

**Optie B - Via Python webserver (als je CORS issues hebt):**
```bash
# In een nieuwe terminal:
cd examples
python3 -m http.server 8000

# Open in browser:
# http://localhost:8000/sensor_dashboard.html
```

**Optie C - Vanaf andere computer:**
```
http://[raspberry-pi-ip]:8080
```

## 🔌 Hardware Setup

```
HC-SR04 Sensor
├── VCC  → Pin 2  (5V)
├── GND  → Pin 6  (Ground)
├── TRIG → Pin 16 (GPIO 23)
└── ECHO → Voltage Divider → Pin 18 (GPIO 24)

⚠️ Voltage Divider (BELANGRIJK!):
ECHO → 1kΩ → GPIO 24 → 2kΩ → GND
```

## 🌐 API Endpoints

De Python server biedt de volgende endpoints:

### GET /api/sensor
Retourneert sensor data als JSON:

```json
{
  "distance": 42.5,
  "status": "success",
  "timestamp": "2025-12-15 14:30:45",
  "history": [40.2, 41.1, 42.5, ...],
  "stats": {
    "total": 150,
    "success": 148,
    "errors": 2,
    "min": 15.3,
    "max": 150.2,
    "avg": 45.6
  }
}
```

### GET /
Simpele info pagina met live JSON data preview.

## ✨ Dashboard Features

### 📏 Real-time Distance Display
- Grote, duidelijke afstand weergave
- Kleurgecodeerde indicatoren (groen/geel/rood)
- Update elke 500ms

### 📊 Statistieken
- Totaal aantal metingen
- Succes rate
- Min/Max/Gemiddelde afstand
- Error tracking

### 📈 Grafiek
- Visualisatie van laatste 30 metingen
- Hover voor exacte waarden
- Real-time updates

### 🔴 Connection Status
- Live verbindingsindicator
- Automatische reconnect bij uitval

## 🛠️ Voordelen van deze Aanpak

### ✓ Geen Flask Dependencies
Python server gebruikt alleen standard library (`http.server`)

### ✓ Schone Scheiding
- Python = Data acquisitie & GPIO
- JavaScript = UI & Visualisatie

### ✓ Flexibel
- HTML bestand werkt standalone
- Kan gehost worden op elke webserver
- API kan gebruikt worden door andere applicaties

### ✓ CORS Enabled
API heeft CORS headers, werkt vanaf elke origin

### ✓ Debugging Friendly
- Python console toont alle metingen
- Browser console voor frontend debugging
- Losse componenten testbaar

## 🔧 Troubleshooting

### Dashboard toont "Niet verbonden"

**Probleem:** JavaScript kan API niet bereiken

**Oplossing:**
```bash
# Controleer of Python server draait:
ps aux | grep hc_sr04_api_server

# Test API handmatig:
curl http://localhost:8080/api/sensor

# Controleer firewall (if needed):
sudo ufw allow 8080
```

### CORS Errors

**Probleem:** Browser blokkeert cross-origin requests

**Oplossing:**
Open dashboard via HTTP server in plaats van file://
```bash
python3 -m http.server 8000
# Open: http://localhost:8000/sensor_dashboard.html
```

### Sensor timeouts

**Probleem:** Veel timeout errors in Python console

**Checklist:**
- [ ] Voltage divider correct aangesloten?
- [ ] Is er een object binnen bereik (2-400cm)?
- [ ] Sensor krijgt 5V power?
- [ ] GPIO pins correct geconfigureerd?

### Dashboard niet updaten

**Probleem:** Waarden bevriezen

**Check:**
1. Browser console voor JavaScript errors (F12)
2. Python console voor sensor errors
3. Network tab in browser: worden requests verstuurd?

## 📱 Mobile Friendly

Dashboard is responsive en werkt op:
- Desktop browsers
- Tablets
- Smartphones

## 🎨 Customization

### Wijzig update interval
In `sensor_dashboard.html`:
```javascript
const UPDATE_INTERVAL = 500; // Change to desired ms
```

### Wijzig server poort
In `hc_sr04_api_server.py`:
```python
server_address = ('', 8080)  # Change port number
```

In `sensor_dashboard.html`:
```javascript
const API_URL = 'http://localhost:8080/api/sensor';  // Update port
```

## 📚 Gebruik in Andere Projecten

De API kan gebruikt worden door:
- Python scripts
- Node.js applicaties
- Mobile apps
- IoT platforms
- Home automation systemen

Voorbeeld Python client:
```python
import requests

response = requests.get('http://localhost:8080/api/sensor')
data = response.json()
print(f"Distance: {data['distance']} cm")
```

## 💡 Uitbreidingsmogelijkheden

1. **Database logging** - Sla data op in SQLite/MySQL
2. **Multiple sensors** - Breid API uit met meer sensors
3. **WebSocket** - Real-time push in plaats van polling
4. **Authentication** - Beveilig API met tokens
5. **Historical data** - Grafieken over langere periodes
6. **Alerts** - Email/SMS bij specifieke afstanden
7. **Export** - Download data als CSV/JSON

## 📝 Licentie

Onderdeel van "Lean en Creatief met Raspberry Pi" keuzedeel.
