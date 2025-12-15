# Raspberry Pi Setup

## Stap 1: Raspberry Pi OS Installeren

### Benodigdheden
- MicroSD-kaart (minimaal 8GB, 16GB+ aanbevolen)
- Computer met SD-kaartlezer
- Raspberry Pi Imager (download van raspberrypi.org)

### Installatieprocedure

1. **Download Raspberry Pi Imager**
   - Ga naar https://www.raspberrypi.org/software/
   - Download de versie voor jouw besturingssysteem
   - Installeer de software

2. **OS op SD-kaart schrijven**
   - Open Raspberry Pi Imager
   - Kies "CHOOSE OS" → "Raspberry Pi OS (32-bit)"
   - Kies "CHOOSE STORAGE" → selecteer je SD-kaart
   - Klik op het tandwiel icoon voor geavanceerde opties
   - Configureer:
     - Hostname (bijv. raspberrypi.local)
     - SSH inschakelen
     - Gebruikersnaam en wachtwoord
     - WiFi-instellingen (optioneel)
   - Klik op "WRITE"

3. **Eerste Opstart**
   - Plaats de SD-kaart in de Raspberry Pi
   - Sluit monitor, toetsenbord en muis aan (of gebruik SSH)
   - Sluit de voeding aan
   - Wacht tot het systeem is opgestart

## Stap 2: Eerste Configuratie

### Via Desktop
Als je een monitor hebt aangesloten:
1. Volg de setup wizard
2. Selecteer taal en locatie
3. Wijzig het wachtwoord (indien gevraagd)
4. Configureer WiFi
5. Update het systeem

### Via SSH
Als je SSH hebt ingeschakeld:
```bash
# Verbind vanaf je computer
ssh pi@raspberrypi.local

# Of met IP-adres
ssh pi@<IP_ADRES>

# Default wachtwoord is wat je hebt ingesteld
```

## Stap 3: Systeem Updaten

```bash
# Update pakketlijsten
sudo apt update

# Upgrade geïnstalleerde pakketten
sudo apt upgrade -y

# Optioneel: full upgrade
sudo apt full-upgrade -y

# Herstart indien nodig
sudo reboot
```

## Stap 4: Python en GPIO Libraries Installeren

```bash
# Python3 is meestal al geïnstalleerd, controleer versie
python3 --version

# Installeer pip
sudo apt install python3-pip -y

# Installeer GPIO libraries
sudo apt install python3-rpi.gpio python3-gpiozero -y

# Alternatief via pip
pip3 install RPi.GPIO gpiozero
```

## Stap 5: Test GPIO Functionaliteit

Maak een test bestand:
```bash
nano test_gpio.py
```

Voeg toe:
```python
import RPi.GPIO as GPIO
import time

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Test GPIO 18 (pin 12)
GPIO.setup(18, GPIO.OUT)

print("GPIO test gestart...")
for i in range(5):
    GPIO.output(18, GPIO.HIGH)
    print("LED AAN")
    time.sleep(1)
    GPIO.output(18, GPIO.LOW)
    print("LED UIT")
    time.sleep(1)

GPIO.cleanup()
print("Test voltooid!")
```

Uitvoeren:
```bash
python3 test_gpio.py
```

## Stap 6: Nuttige Tools Installeren

```bash
# Git voor versiebeheer
sudo apt install git -y

# Teksteditors
sudo apt install vim nano -y

# Python development tools
sudo apt install python3-dev python3-venv -y

# GPIO header referentie tool
sudo apt install python3-gpiozero python-gpiozero-doc -y
```

## GPIO Pin Layout

Gebruik het commando `pinout` om de GPIO layout te zien:
```bash
pinout
```

## Troubleshooting

### WiFi verbindt niet
```bash
# Controleer configuratie
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

# Herstart netwerk
sudo systemctl restart dhcpcd
```

### SSH werkt niet
```bash
# Schakel SSH in via raspi-config
sudo raspi-config
# Interface Options → SSH → Enable
```

### GPIO permissions
```bash
# Voeg gebruiker toe aan gpio groep
sudo usermod -a -G gpio $USER
# Log uit en weer in
```

## Volgende Stappen

Nu je Raspberry Pi is ingesteld, ga verder met:
- [02-gpio-basics.md](02-gpio-basics.md) - GPIO programmering basis
- [03-sensors.md](03-sensors.md) - Werken met sensoren
- [../examples/](../examples/) - Voorbeeldprojecten uitproberen
