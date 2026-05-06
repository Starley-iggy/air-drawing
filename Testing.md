# Test Rapport & Testplan  Air Drawing
 ## 📌 Project Overzicht

**Project:** Air Drawing

**Type:** Computer Vision / Gesture-based drawing

**Technologie:** Python, OpenCV en MediaPipe


**Doel:**
Valideren dat handtracking en drawing functionaliteit correct, stabiel en performant werken onder verschillende omstandigheden.

## 🎯 Teststrategie
### Scope

✔ Hand detectie

✔ Gesture herkenning

✔ Drawing functionaliteit

✔ UI interactie

✔ Performance

### Out of scope

❌ Hardware defects (webcam zelf)

❌ OS-level camera drivers

## 🧪 Testaanpak

- Type test	Methode

- Functioneel	Manual + scripted tests

- Performance	Monitoring tools

- Unit tests	pytest

- Integratie tests	Mock camera input

- Exploratory testing	Hand gestures live

## 📋 Testcases 
### 💻 Basis functionaliteit (core features)

***TC-01:*** Start applicatie
--------
Stap: run script (python main.py)

Expected:
Camera opent
UI zichtbaar

Edge case: geen webcam → foutmelding


***TC-02:*** Hand detectie
--------
Stap: steek hand voor camera

Expected: 

Hand landmarks worden herkend
Cursor volgt vinger

Variatie:

Slechte lighting → nog steeds detectie?


 ***TC-03:*** Tekenen (draw mode)
  --------
Stap: gebruik juiste gesture (bijv. index finger omhoog)

Expected:
Lijnen verschijnen op canvas

Check:
Continu vs stotterend tekenen


***TC-04:*** Stoppen met tekenen
--------
Stap: andere gesture (bijv. hand open)

Expected:
Tekenen stopt direct

### ✏️ Drawing behaviour


***TC-05:*** Lijn continuïteit
--------
Stap: trek lange lijn

Expected:
Geen gaten in lijn

Edge case:
Snelle beweging → nog steeds vloeiend


***TC-06:*** Jitter filtering
 --------
Stap: hand stil houden

Expected:
Geen kleine “trillende” lijnen
Dit test smoothing logic (zoals distance threshold)


***TC-07:*** Meerdere kleuren (indien aanwezig)
--------
Stap: verander kleur

Expected:
Nieuwe lijnen hebben juiste kleur


### 🧽 Erase / Move functies

***TC-08:*** Eraser mode
--------
Stap: activeer erase

Expected:
Lijnen verdwijnen waar je tekent


***TC-09:*** Move canvas
--------
Stap: move gesture (bijv. andere pinch)

Expected:
Hele tekening verschuift


***TC-10:*** Undo / Clear
--------
Stap: klik undo

Expected:
Laatste actie teruggedraaid
Stap: clear

Expected:
Canvas leeg


### 🖐️ Multi-hand & gestures
***TC-11:*** Twee handen tegelijk
--------
Stap: gebruik beide handen

Expected:
Beide worden herkend
Geen conflict


***TC-12:*** Verkeerde gesture
--------
Stap: random hand pose

Expected:
Geen actie (geen false positives)


### ⚡ Performance & robustness
***TC-13:*** FPS / latency
--------
Stap: meet response tijd

Expected:
< ~100ms vertraging


***TC-14:*** CPU gebruik
--------
Stap: monitor CPU

Expected:
Niet extreem hoog (>90%)


***TC-15:*** Lange sessie
--------
Stap: 30 min draaien

Expected:
Geen crash / memory leak


### 💾 Opslaan & output

***TC-16:*** Save drawing
--------
Stap: klik save

Expected:
PNG bestand opgeslagen


***TC-17:*** Bestand inhoud
--------
Expected:
Tekening zichtbaar
Geen corrupte image

### 🚨 Edge cases
***TC-18:*** Geen hand zichtbaar
--------
Expected:
Geen drawing events


***TC-19:*** Meerdere objecten in beeld
--------
Stap: extra object (bijv. pen)

Expected:
Geen false hand detectie


***TC-20:*** Licht / donkere omgeving
--------
Expected:
Detectie degradeert maar crasht niet


## 📊 Test Resultaat Rapport (voorbeeld)
Test Run Summary

Metric	Resultaat

Totaal tests	20

Geslaagd	17

Gefaald	3

Success rate	85%
