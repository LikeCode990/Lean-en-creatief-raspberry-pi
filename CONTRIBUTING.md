# Bijdragen aan Lean-en-creatief-raspberry-pi

Bedankt voor je interesse om bij te dragen! We waarderen alle bijdragen, groot of klein.

## Hoe kun je bijdragen?

### 1. Issues Melden
- Bug gevonden? Maak een issue aan
- Feature idee? Deel het via een issue
- Vraag over de code? Stel deze in een issue

### 2. Code Bijdragen

#### Stappen
1. Fork het project
2. Maak een feature branch (`git checkout -b feature/nieuw-voorbeeld`)
3. Commit je wijzigingen (`git commit -m 'Voeg nieuw voorbeeld toe'`)
4. Push naar de branch (`git push origin feature/nieuw-voorbeeld`)
5. Open een Pull Request

### 3. Documentatie Verbeteren
- Typ fouten corrigeren
- Voorbeelden verduidelijken
- Nieuwe tutorials toevoegen
- Vertalingen verbeteren

### 4. Voorbeelden Toevoegen
- Nieuwe GPIO voorbeelden
- Sensor integraties
- Creatieve projecten
- Lean workflow voorbeelden

## Code Richtlijnen

### Python Style
- Volg PEP 8
- Gebruik duidelijke functie/variabele namen
- Voeg docstrings toe
- Commentaar in het Nederlands (voor deze module)

### Voorbeeld Template
```python
#!/usr/bin/env python3
"""
Korte beschrijving
==================
Langere beschrijving van wat het script doet.

Hardware:
- Component 1
- Component 2

Aansluiting:
GPIO X → Component → GND
"""

import RPi.GPIO as GPIO

def setup():
    """Initialiseer GPIO"""
    pass

def main():
    """Hoofdfunctie"""
    pass

if __name__ == "__main__":
    main()
```

### Project Template
Elk project moet bevatten:
- README.md met doel en requirements
- Code met comments
- Circuit diagram (tekst of afbeelding)
- Test criteria

## Lean Principes

Bij het bijdragen, denk aan deze lean principes:

1. **Waarde**: Voegt het waarde toe voor de gebruiker?
2. **Eenvoud**: Kan het simpeler?
3. **Volledigheid**: Is het compleet genoeg om te gebruiken?
4. **Leesbaarheid**: Is het makkelijk te begrijpen?

## Vragen?

Twijfel je of iets een goede bijdrage is? Maak gerust een issue aan om het te bespreken!

## Code of Conduct

- Wees respectvol
- Geef constructieve feedback
- Help anderen leren
- Deel kennis

## Licentie

Door bij te dragen stem je ermee in dat je bijdragen onder de MIT License vallen.
