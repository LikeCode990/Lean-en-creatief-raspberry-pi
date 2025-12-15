# Bijdragen aan Lean en Creatief Raspberry Pi

Bedankt voor je interesse om bij te dragen aan dit project! We waarderen alle bijdragen, of het nu gaat om het melden van bugs, voorstellen van nieuwe features, verbeteren van documentatie, of het toevoegen van voorbeelden.

## 🤝 Hoe kan je bijdragen?

### 1. Issues Melden

Als je een bug vindt of een verbetering wilt voorstellen:

1. Check of het issue al bestaat in [Issues](https://github.com/LikeCode990/Lean-en-creatief-raspberry-pi/issues)
2. Maak een nieuw issue met een duidelijke titel
3. Beschrijf het probleem of voorstel in detail
4. Voeg indien mogelijk toe:
   - Hardware setup die je gebruikt
   - Code die het probleem veroorzaakt
   - Verwachte vs werkelijke resultaat
   - Error messages of screenshots

### 2. Code Bijdragen

#### Voordat je begint:
1. Fork de repository
2. Clone je fork lokaal
3. Maak een nieuwe branch voor je feature/fix

```bash
git checkout -b feature/nieuwe-sensor-voorbeeld
# of
git checkout -b fix/led-blink-bug
```

#### Tijdens ontwikkeling:
- Volg de bestaande code style
- Test je code op een echte Raspberry Pi indien mogelijk
- Voeg comments toe voor complexe logica
- Update documentatie indien nodig

#### Pull Request indienen:
1. Push je branch naar je fork
2. Maak een Pull Request naar de main branch
3. Beschrijf wat je hebt veranderd en waarom
4. Link relevante issues

## 📝 Code Style Guidelines

### Python Code

```python
# Gebruik PEP 8 style guide
# Duidelijke functie/variabele namen (Nederlands of Engels consistent)

# GOED:
LED_PIN = 17
def set_led_state(state):
    """Zet LED aan of uit"""
    GPIO.output(LED_PIN, state)

# VERMIJD:
p = 17
def f(s):
    GPIO.output(p, s)
```

### Docstrings
Voeg docstrings toe aan alle functies en klasses:

```python
def meet_afstand():
    """
    Meet afstand met ultrasone sensor.
    
    Returns:
        float: Afstand in centimeters
        None: Bij timeout of fout
    """
    # implementatie
```

### Comments
- Gebruik Nederlandse comments voor educatieve code
- Leg niet-voor-de-hand-liggende keuzes uit
- Vermeld hardware specifieke requirements

```python
# Voltage divider nodig: HC-SR04 ECHO pin is 5V!
# Pi GPIO pins accepteren max 3.3V
GPIO.setup(ECHO_PIN, GPIO.IN)
```

## 📚 Documentatie

### README Updates
- Houd README.md up-to-date bij nieuwe features
- Voeg voorbeelden toe van nieuwe functionaliteit
- Update hardware requirements lijst

### Lesson Materials
Bij toevoegen van nieuwe lessen:
- Gebruik bestaande les structuur als template
- Bevat: Leerdoelen, Tijdsduur, Materialen, Theorie, Praktijk
- Voeg troubleshooting sectie toe
- Link naar gerelateerde voorbeelden

### Code Examples
Nieuwe voorbeelden moeten bevatten:
- Header comment met uitleg
- Hardware requirements
- Duidelijke variabele namen
- Error handling (try/except/finally)
- GPIO.cleanup() in finally block

## 🧪 Testing

### Minimale Test Checklist
Voor code bijdragen:
- [ ] Code draait zonder errors op Raspberry Pi
- [ ] GPIO.cleanup() wordt altijd uitgevoerd
- [ ] Ctrl+C (KeyboardInterrupt) wordt netjes afgehandeld
- [ ] Hardware requirements zijn duidelijk gedocumenteerd
- [ ] Code bevat geen hardcoded user-specifieke paths

### Hardware Testing
Test bij voorkeur op:
- Raspberry Pi 4 (primaire platform)
- Raspberry Pi 3B+ (legacy support)

## 🎓 Educatieve Focus

Dit is een educatief project, dus:

### ✅ DO:
- Schrijf begrijpelijke, leesbare code
- Voeg uitleg toe voor complexe concepten
- Gebruik voorbeelden die lean & creatieve principes illustreren
- Bouw incrementeel op (van simpel naar complex)

### ❌ DON'T:
- Gebruik geen onnodige complexiteit
- Vermijd obscure shortcuts zonder uitleg
- Skip geen error handling
- Geen productie-only optimalisaties zonder educatieve waarde

## 🔧 Specifieke Bijdrage Types

### Nieuwe Sensoren/Components
Bij toevoegen van nieuwe hardware:
1. Maak voorbeeld script in `examples/intermediate/`
2. Documenteer hardware specificaties
3. Voeg circuit diagram toe (ASCII art of afbeelding)
4. Vermeld veiligheidsoverwegingen (voltage, stroom, etc.)

### Projecten
Voor complete projecten:
1. Plaats in `examples/projects/`
2. Maak aparte README in project directory
3. Lijst alle benodigde componenten
4. Leg lean & creatieve aspecten uit
5. Voeg foto's toe van werkend prototype

### Lessen
Nieuwe les modules:
1. Gebruik `lessons/les-XX-onderwerp.md` format
2. Volg bestaande structuur
3. Voeg oefeningen en uitdagingen toe
4. Include reflectie sectie over lean principes

## 📋 Issue Labels

We gebruiken de volgende labels:
- `bug`: Iets werkt niet zoals verwacht
- `enhancement`: Nieuwe feature of verbetering
- `documentation`: Verbeteringen aan documentatie
- `good first issue`: Goed voor nieuwe contributors
- `help wanted`: Extra aandacht nodig
- `hardware`: Hardware-gerelateerd issue
- `lesson`: Gerelateerd aan les materiaal

## 💬 Communicatie

- **Issues**: Voor bugs en feature requests
- **Pull Requests**: Voor code reviews
- **Discussions**: Voor algemene vragen en ideeën (indien enabled)

## 🌟 Erkenning

Alle contributors worden vermeld in het project. Bedankt voor je bijdrage aan onderwijs en open source!

## ⚖️ Code of Conduct

### Onze Standaarden

- ✅ Respectvol en inclusief taalgebruik
- ✅ Verschillende perspectieven en ervaringen waarderen
- ✅ Constructieve kritiek geven en accepteren
- ✅ Focus op wat het beste is voor de community
- ✅ Empathie tonen naar andere community members

### Niet Acceptabel

- ❌ Intimidatie of discriminatie
- ❌ Beledigend of neerbuigend taalgebruik
- ❌ Persoonlijke of politieke aanvallen
- ❌ Ongewenste aandacht of toenadering

## 📜 Licentie

Door bij te dragen, ga je ermee akkoord dat je bijdragen gelicenseerd worden onder de MIT License van dit project.

---

**Vragen?** Open een issue of neem contact op via de repository!
