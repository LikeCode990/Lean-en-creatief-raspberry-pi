# Lean en Creatief Raspberry Pi - Keuzedeel

Een praktische en creatieve module voor het leren werken met Raspberry Pi. Deze repository bevat lesmaterialen, voorbeelden en projecten die lean en creatieve principes combineren met embedded programmering.

## 📋 Overzicht

Deze module richt zich op:
- **Lean principes**: Efficiënt werken, minimale verspilling, iteratieve ontwikkeling
- **Creatief denken**: Innovatieve oplossingen, experimenteren, probleem-oplossend vermogen
- **Praktische vaardigheden**: Hardware interfacing, Python programmering, prototyping

## 🎯 Leerdoelen

Na het voltooien van deze module kun je:
- Raspberry Pi configureren en programmeren voor embedded toepassingen
- GPIO (General Purpose Input/Output) pinnen gebruiken voor sensoren en actuatoren
- Python scripts schrijven voor hardware besturing
- Lean principes toepassen in project development
- Creatieve oplossingen ontwikkelen voor praktische problemen
- Prototypes bouwen en testen volgens iteratieve methoden

## 📚 Structuur

```
.
├── examples/          # Codevoorbeelden
│   ├── basic/        # Basis GPIO voorbeelden
│   ├── intermediate/ # Gevorderde voorbeelden
│   └── projects/     # Volledige projecten
├── docs/             # Documentatie
├── lessons/          # Gestructureerde lessen
└── resources/        # Aanvullende bronnen
```

## 🚀 Aan de slag

### Benodigde Hardware

- Raspberry Pi (3B+, 4, of nieuwer aanbevolen)
- microSD kaart (minimaal 16GB)
- Voeding (5V, minimaal 2.5A)
- LED's (verschillende kleuren)
- Weerstanden (220Ω, 10kΩ)
- Breadboard
- Jumper wires (male-to-female, male-to-male)
- Drukknoppen
- Optioneel: sensoren (temperatuur, afstand, licht)

### Software Setup

1. **Installeer Raspberry Pi OS**
   ```bash
   # Download Raspberry Pi Imager van officiële website
   # Flash Raspberry Pi OS Lite of Desktop op SD kaart
   ```

2. **Eerste configuratie**
   ```bash
   sudo apt update
   sudo apt upgrade -y
   sudo apt install python3-pip python3-rpi.gpio git -y
   ```

3. **Clone deze repository**
   ```bash
   git clone https://github.com/LikeCode990/Lean-en-creatief-raspberry-pi.git
   cd Lean-en-creatief-raspberry-pi
   ```

4. **Installeer Python dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

## 📖 Lessen

1. **Les 1: GPIO Basics** - LED's aansturen, basis elektronica
2. **Les 2: Input verwerking** - Buttons en sensoren lezen
3. **Les 3: PWM en dimmen** - Pulse Width Modulation voor helderheid
4. **Les 4: Sensoren** - Temperatuur, afstand, licht meten
5. **Les 5: Projecten** - Volledige prototypes bouwen

## 💡 Lean & Creatieve Principes

### Lean Aanpak
- **Start klein**: Begin met simpele circuits en bouw stap voor stap op
- **Iteratief ontwikkelen**: Test vaak, leer van fouten, verbeter
- **Minimale verspilling**: Gebruik efficiënte code, herbruikbare componenten
- **Continuous improvement**: Reflecteer en optimaliseer

### Creatieve Mindset
- **Experimenteren**: Probeer verschillende oplossingen
- **Probleem-oplossend denken**: Analyseer, ontwerp, implementeer
- **Innovatie**: Combineer technieken op nieuwe manieren
- **Documenteer je leerproces**: Deel inzichten en bevindingen

## 🤝 Bijdragen

Bijdragen zijn welkom! Zie [CONTRIBUTING.md](CONTRIBUTING.md) voor richtlijnen.

## 📄 Licentie

Dit project is gelicenseerd onder de MIT License - zie [LICENSE](LICENSE) voor details.

## 🔗 Bronnen

- [Raspberry Pi Officiële Documentatie](https://www.raspberrypi.org/documentation/)
- [RPi.GPIO Python Library](https://pypi.org/project/RPi.GPIO/)
- [GPIO Pinout Referentie](https://pinout.xyz/)

## 📧 Contact

Voor vragen of feedback, open een issue in deze repository.

---

**Let op**: Werk altijd veilig met elektronica. Controleer verbindingen voordat je stroom aanzet en gebruik juiste weerstanden om componenten te beschermen.
