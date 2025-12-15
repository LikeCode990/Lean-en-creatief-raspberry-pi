# Software Setup Guide

## Raspberry Pi OS Installatie

### 1. Download Raspberry Pi Imager

Download van [officiële website](https://www.raspberrypi.org/software/):
- **Windows**: .exe installer
- **macOS**: .dmg installer
- **Linux**: AppImage of via package manager

### 2. Flash OS naar microSD

1. Start Raspberry Pi Imager
2. Klik "CHOOSE OS"
3. Selecteer "Raspberry Pi OS (64-bit)" (aanbevolen) of "Raspberry Pi OS Lite" (zonder desktop)
4. Klik "CHOOSE STORAGE"
5. Selecteer je microSD kaart
6. Klik tandwiel icoon (⚙️) voor geavanceerde opties:
   - **Enable SSH**: Aanvinken
   - **Set username and password**: Configureer
   - **Configure WiFi**: Vul SSID en wachtwoord in (optioneel)
   - **Set locale settings**: Kies tijdzone en keyboard layout
7. Klik "WRITE" en wacht tot klaar

### 3. Eerste Boot

1. Plaats microSD in Raspberry Pi
2. Sluit power supply aan
3. Wacht ~2 minuten voor eerste boot
4. SSH of direct via monitor inloggen

## SSH Verbinding

### Via Terminal (Linux/macOS)
```bash
ssh username@raspberrypi.local
# Of met IP adres:
ssh username@192.168.1.XXX
```

### Via PuTTY (Windows)
1. Download PuTTY
2. Host Name: `raspberrypi.local` of IP adres
3. Port: 22
4. Connection type: SSH
5. Klik "Open"

### IP Adres vinden
```bash
# Op de Pi zelf:
hostname -I

# Op je netwerk (Linux/macOS):
arp -a | grep raspberry

# Op Windows:
arp -a
```

## Systeem Update

### Eerste configuratie
```bash
# Update package lists
sudo apt update

# Upgrade alle packages
sudo apt upgrade -y

# Configuratie tool
sudo raspi-config
```

### Belangrijke raspi-config opties:
- **Interface Options** -> **I2C**: Enable (voor I2C sensoren)
- **Interface Options** -> **SPI**: Enable (voor SPI devices)
- **Performance Options**: GPU memory aanpassen indien nodig
- **Localisation Options**: Keyboard/timezone instellen

## Python Setup

### Python versie check
```bash
python3 --version
# Verwacht: Python 3.9 of nieuwer
```

### Installeer benodigde packages
```bash
# Systeem packages
sudo apt install -y python3-pip python3-dev python3-venv git

# RPi.GPIO library (meestal al geïnstalleerd)
sudo apt install -y python3-rpi.gpio

# Optioneel: andere handige tools
sudo apt install -y python3-pigpio python3-gpiozero
```

## Virtual Environment (Aanbevolen)

Een virtual environment houdt project dependencies gescheiden.

```bash
# Maak virtual environment
python3 -m venv ~/lean-pi-env

# Activeer environment
source ~/lean-pi-env/bin/activate

# Deactiveer (later)
deactivate
```

### Auto-activatie bij login (optioneel)
```bash
echo "source ~/lean-pi-env/bin/activate" >> ~/.bashrc
```

## Repository Setup

### Clone de repository
```bash
cd ~
git clone https://github.com/LikeCode990/Lean-en-creatief-raspberry-pi.git
cd Lean-en-creatief-raspberry-pi
```

### Installeer Python dependencies
```bash
# Als requirements.txt bestaat:
pip3 install -r requirements.txt

# Of handmatig:
pip3 install RPi.GPIO
```

### Test installatie
```bash
python3 examples/basic/01_led_blink.py
# Let op: Sluit eerst LED aan op GPIO 17!
```

## Permissies

### GPIO Toegang zonder sudo

Voeg gebruiker toe aan gpio groep:
```bash
sudo usermod -a -G gpio $USER
```

Log uit en weer in voor effect.

## Handige Tools

### 1. GPIO Command Line Tool
```bash
# Installeer
sudo apt install -y wiringpi

# GPIO pin status bekijken
gpio readall
```

### 2. Python REPL voor GPIO Testen
```bash
python3
>>> import RPi.GPIO as GPIO
>>> GPIO.setmode(GPIO.BCM)
>>> GPIO.setup(17, GPIO.OUT)
>>> GPIO.output(17, GPIO.HIGH)
>>> GPIO.cleanup()
>>> exit()
```

### 3. VS Code Remote SSH (Voor ontwikkeling)

1. Installeer VS Code op je computer
2. Installeer "Remote - SSH" extensie
3. Voeg SSH host toe: `username@raspberrypi.local`
4. Connect en ontwikkel remote!

### 4. File Transfer

**SCP (Secure Copy)**:
```bash
# Van computer naar Pi:
scp file.py username@raspberrypi.local:~/

# Van Pi naar computer:
scp username@raspberrypi.local:~/file.py ./
```

**SFTP**:
```bash
sftp username@raspberrypi.local
# Gebruik put/get commando's
```

## Autostart Scripts (Optioneel)

### Systemd Service

Maak service file: `/etc/systemd/system/my-project.service`
```ini
[Unit]
Description=My Raspberry Pi Project
After=multi-user.target

[Service]
Type=idle
User=username
ExecStart=/usr/bin/python3 /home/username/project/main.py

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
sudo systemctl enable my-project.service
sudo systemctl start my-project.service
```

### rc.local (Simpeler, niet aanbevolen voor productie)

Edit `/etc/rc.local`:
```bash
sudo nano /etc/rc.local

# Voeg toe voor "exit 0":
python3 /home/username/project/main.py &

# Save en exit (Ctrl+X, Y, Enter)
```

## Troubleshooting

### Permission Denied bij GPIO
```bash
# Voeg gebruiker toe aan gpio groep
sudo usermod -a -G gpio $USER
# Log uit en weer in
```

### Module niet gevonden
```bash
# Zorg dat je in juiste environment bent
source ~/lean-pi-env/bin/activate

# Herinstalleer package
pip3 install --upgrade RPi.GPIO
```

### SSH Verbinding lukt niet
```bash
# Check of SSH enabled is
sudo systemctl status ssh

# Enable SSH
sudo systemctl enable ssh
sudo systemctl start ssh
```

### WiFi verbinding problemen
```bash
# Check netwerk status
ifconfig wlan0

# Reconfigure WiFi
sudo raspi-config
# -> System Options -> Wireless LAN
```

## Updates en Onderhoud

### Reguliere updates
```bash
# Eens per week:
sudo apt update && sudo apt upgrade -y

# Python packages:
pip3 list --outdated
pip3 install --upgrade package-name
```

### Disk Space Check
```bash
df -h
# Let op: Minimaal 1GB vrije ruimte houden
```

### Backup maken
```bash
# Backup belangrijke files
tar -czf backup.tar.gz ~/Lean-en-creatief-raspberry-pi
scp backup.tar.gz user@computer:~/backups/
```

## Volgende Stappen

Na succesvolle setup:
1. Test basis voorbeelden in `examples/basic/`
2. Doorloop lessen in `lessons/` directory
3. Bouw eerste project!

Zie [Hardware Setup Guide](hardware-setup.md) voor circuit schema's.
