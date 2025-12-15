# Lean en Creatief met Raspberry Pi

Een keuzedeel voor het leren werken met Raspberry Pi op een lean en creatieve manier.

## Over dit Keuzedeel

Dit keuzedeel richt zich op het ontwikkelen van praktische vaardigheden met de Raspberry Pi, waarbij de nadruk ligt op:
- **Lean werken**: Efficiënt en doelgericht projecten realiseren
- **Creativiteit**: Innovatieve oplossingen bedenken en implementeren
- **Hands-on ervaring**: Directe praktijkervaring met hardware en software

## Leerdoelen

Na het voltooien van dit keuzedeel kun je:
1. Een Raspberry Pi installeren en configureren
2. Basis GPIO-programmering toepassen
3. Sensoren en actuatoren aansluiten en aansturen
4. Eenvoudige IoT-projecten realiseren
5. Creatieve projecten ontwikkelen met minimale middelen (lean)

## Inhoud

- **[docs/](docs/)** - Documentatie en lesmateriaal
- **[examples/](examples/)** - Voorbeeldcode en projecten
- **[projects/](projects/)** - Grotere projectopdrachten
- **[resources/](resources/)** - Aanvullende bronnen en referenties

## Benodigdheden

### Hardware
- Raspberry Pi (3B+ of nieuwer aanbevolen)
- MicroSD-kaart (minimaal 8GB)
- Voeding (5V, minimaal 2.5A)
- GPIO componenten (LEDs, weerstanden, breadboard, etc.)
- Sensoren (optioneel, afhankelijk van projecten)

### Software
- Raspberry Pi OS (voorheen Raspbian)
- Python 3.x
- GPIO libraries (RPi.GPIO of gpiozero)

## Aan de Slag

1. **Setup je Raspberry Pi**
   ```bash
   # Zie docs/01-setup.md voor gedetailleerde instructies
   ```

2. **Installeer benodigde software**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   pip3 install RPi.GPIO gpiozero
   ```

3. **Test je installatie**
   ```bash
   python3 examples/01-blink/blink.py
   ```

## Projecten

### Basis
- LED knipperen
- Knop inlezen
- PWM voor LED dimmen

### Gemiddeld
- Temperatuur monitoring
- Afstand meten met ultrasone sensor
- Servo motor aansturen
- **Web Dashboard** - Bestuur je Pi via je browser 🌐

### Gevorderd
- Weerstation
- Smart home systeem
- IoT dashboard met real-time data

## Bronnen

- [Officiële Raspberry Pi documentatie](https://www.raspberrypi.org/documentation/)
- [Python GPIO Zero library](https://gpiozero.readthedocs.io/)
- [Raspberry Pi Projects](https://projects.raspberrypi.org/)

## Bijdragen

Bijdragen zijn welkom! Zie [CONTRIBUTING.md](CONTRIBUTING.md) voor meer informatie.

## Licentie

Dit project valt onder de MIT License - zie [LICENSE](LICENSE) voor details.
