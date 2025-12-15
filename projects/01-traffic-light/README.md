# Project 1: Verkeerslicht

## Doel
Bouw een werkend verkeerslicht met LEDs dat realistische overgangen simuleert.

## Leerdoelen
- Meerdere GPIO outputs aansturen
- State machines implementeren
- Timing sequences programmeren
- Clean code structuur toepassen

## Hardware Benodigdheden
- 1x Rode LED
- 1x Gele LED  
- 1x Groene LED
- 3x 220Ω weerstanden
- Breadboard
- Jumper draden

## Aansluiting Schema

```
GPIO 23 → 220Ω → Rode LED → GND
GPIO 24 → 220Ω → Gele LED → GND
GPIO 25 → 220Ω → Groene LED → GND
```

## Functionele Requirements

### Basis Functionaliteit
1. Rood licht: 5 seconden
2. Rood + Geel licht: 2 seconden
3. Groen licht: 5 seconden
4. Geel licht: 2 seconden
5. Terug naar stap 1

### Uitbreidingen (Lean Denken)
- **Minimum Viable Product (MVP)**: Start met basis cycle
- **Iteratief**: Voeg features toe in kleine stappen
- **User Story 1**: Als bestuurder wil ik een duidelijk verkeerslicht zien
- **User Story 2**: Als voetganger wil ik een voetgangerslicht
- **User Story 3**: Als gebruiker wil ik de tijden kunnen aanpassen

## Implementatie Stappenplan

### Stap 1: Setup (MVP)
```python
# Setup GPIO voor 3 LEDs
# Test elke LED individueel
```

### Stap 2: Basis Cycle
```python
# Implementeer de basis verkeerslicht cyclus
# Gebruik functies voor elke state
```

### Stap 3: State Machine
```python
# Refactor naar een state machine
# Maak code herbruikbaar
```

### Stap 4: Configureerbaar
```python
# Lees timing vanuit configuratie
# Voeg command line argumenten toe
```

## Code Structuur Voorbeeld

```python
class TrafficLight:
    def __init__(self, red_pin, yellow_pin, green_pin):
        # Initialize pins
        pass
    
    def red_only(self, duration):
        # Set red light
        pass
    
    def red_yellow(self, duration):
        # Set red + yellow
        pass
    
    def green_only(self, duration):
        # Set green light
        pass
    
    def yellow_only(self, duration):
        # Set yellow light
        pass
    
    def run_cycle(self):
        # Run complete traffic light cycle
        pass
```

## Test Criteria
- [ ] Alle LEDs werken individueel
- [ ] Correcte volgorde van lichten
- [ ] Juiste timing tussen states
- [ ] Programma stopt netjes met Ctrl+C
- [ ] GPIO wordt correct opgeruimd

## Creatieve Uitbreidingen
1. **Nachtmodus**: Alleen geel knippert
2. **Voetgangerslicht**: Knop om groen aan te vragen
3. **Meerdere richtingen**: 4-weg kruispunt
4. **Display**: Toon countdown op LED display
5. **Logging**: Log alle state changes

## Lean Principes
- **Waarde**: Wat is de minimale functionaliteit voor een werkend verkeerslicht?
- **Verspilling**: Welke code is niet noodzakelijk?
- **Flow**: Hoe maak je de code makkelijk uitbreidbaar?
- **Pull**: Voeg alleen features toe als ze nodig zijn
- **Perfectie**: Iteratief verbeteren

## Reflectie Vragen
1. Wat was de moeilijkste uitdaging?
2. Hoe kun je de code leesbaarder maken?
3. Welke uitbreiding voegt de meeste waarde toe?
4. Wat heb je geleerd over state machines?

## Bronnen
- [State Machine Tutorial](https://realpython.com/python-state-machine/)
- [GPIO Zero Traffic Lights](https://gpiozero.readthedocs.io/en/stable/recipes.html#traffic-lights)
