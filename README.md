# Air Drawing – Software Life Cycle Document (SLDC)

**Naam:** Air Drawing  
**Repository:** [Starley-iggy/air-drawing](https://github.com/Starley-iggy/air-drawing)  
**Taal:** Python  
**Maker:** Starley Igbinomwhaia Briggs

## Doel
Air Drawing is een interactieve applicatie die gebruikers in staat stelt te tekenen in de lucht met hun hand, via een webcam en realtime handtracking. Het systeem detecteert de hand en vertaalt bewegingen van de wijsvinger naar lijnen op een digitaal canvas.

## Scope

**Inclusief:**  
- Realtime tekenen  
- Kleurselectie  
- Canvas wissen  
- Handtracking via Mediapipe  

**Exclusief:**  
- Opslaan van tekeningen  
- Meerdere brush types  
- Multi-hand tracking (voor toekomstige uitbreiding)  

## Doelgroep / Stakeholders

**Primair:** hobbyisten, studenten en makers die experimenteren met computer vision en interactieve projecten.  

**Secundair:** docenten, demonstraties in educatieve context, creatieve prototypes.  

---

## 2. Projectdoelstellingen

| Doelstelling             | Beschrijving                                                        |
|---------------------------|-------------------------------------------------------------------|
| Realtime handtracking     | Detecteer handlandmarks en volg de indexvinger nauwkeurig.        |
| Intuïtief tekenen         | Gebruiker kan eenvoudig tekenen door de lucht te bewegen.         |
| Interactie via UI-zones   | Kleuren en canvas wissen via handbewegingen.                      |
| Responsief en lichtgewicht| Laag latency, minimale vertraging bij tekenbewegingen.            |
| Eenvoudige uitbreidbaarheid | Ondersteuning voor extra features in toekomst (brushes, opslaan). |

---

## 3. Functioneel Ontwerp

### 3.1 Hoofdfunctionaliteiten

| Functionaliteit           | Beschrijving                                                      |
|---------------------------|-------------------------------------------------------------------|
| Handdetectie               | Detecteert handlandmarks via Mediapipe.                           |
| Tekenmodus                 | Teken alleen als indexvinger boven middelvinger is.               |
| Kleurselectie              | Bovenaan scherm: vier zones (Blue, Green, Red, Clear).            |
| Wis canvas                 | Wis het volledige canvas bij aanraking van Clear zone.            |
| Realtime visualisatie      | Canvas en webcamfeed worden samengevoegd en realtime weergegeven.|

### 3.2 Use Case Diagram
```
                       +---------------------+
                       |    User (Actor)     |
                       +---------------------+
                                 |
  +-----------------------------------------------------------+
  |                        Air Drawing App                     |
  |                                                           |
  |   [UC1] Detect Hand          [UC2] Select Color            |
  |        +-----------------------------+                     |
  |        | capture webcam frames       |                     |
  |        | run hand‑tracking module     |                     |
  |        +-----------------------------+                     |
  |                         |                                  |
  |                    detects hand                             |
  |                         |                                  |
  |       +------------------------+   +---------------------+  |
  |       | [UC3] Draw On Canvas   |   | [UC4] Clear Canvas  |  |
  |       | record finger motion   |   | clear canvas buffer |  |
  |       +------------------------+   +---------------------+  |
  +-----------------------------------------------------------+
                                  |
                              Display to Screen
```
*(Prototype)*

**Beschrijving Use Cases**
| Use Case           | Kort overzicht                                              |
| ------------------ | ----------------------------------------------------------- |
| **Detect Hand**    | Detecteert de hand + positie van wijsvinger met Mediapipe.  |
| **Select Color**   | Gebruiker kiest kleur door naar kleurzone te bewegen.       |
| **Draw on Canvas** | Zet beweging van wijsvinger om in lijnen op canvas.         |
| **Clear Canvas**   | Wisst alle getekende lijnen bij aanraking van “Clear” zone. |

**Use Cases:**  
1. **Detect Hand** – Applicatie herkent de hand in beeld.  
2. **Select Color** – Gebruiker beweegt wijsvinger naar gewenste kleurzone.  
3. **Draw on Canvas** – Beweging van de wijsvinger wordt vertaald naar lijnen.  
4. **Clear Canvas** – Wis functie via Clear zone.  

### 3.3 Niet-functionele eisen

| Eisen         | Beschrijving                                                   |
|---------------|---------------------------------------------------------------|
| Performance   | Minimaal 15–30 FPS voor vloeiende realtime ervaring.          |
| Compatibiliteit | Python 3.7+, OpenCV en Mediapipe geïnstalleerd.            |
| Usability     | Eenvoudige interface met duidelijke zones voor kleuren/wissen.|
| Stabiliteit   | Foutafhandeling bij afwezigheid van hand of slechte belichting.|

---

## 4. Technisch Ontwerp

### 4.1 Architectuur
```
+----------------------------------------------------------------------------------+
|                                Air Drawing App                                   |
|                                                                                  |
|  INPUT LAYER                                                                     |
|  +------------------+                                                            |
|  | Camera Service   |                                                            |
|  | (cv2 wrapper)    |                                                            |
|  +--------+---------+                                                            |
|           |                                                                      |
|           v                                                                      |
|  PERCEPTION LAYER                                                                |
|  +------------------------+      +---------------------------+                   |
|  | Hand Tracking Service  | ---> | Gesture Recognition       |                   |
|  | (MediaPipe Adapter)    |      | (Stateful + ML optional)  |                   |
|  +-----------+------------+      +-------------+-------------+                   |
|              |                                 |                                 |
|              v                                 v                                 |
|  INTERACTION LAYER                                                               |
|  +-------------------------------------------------------------+                 |
|  | Interaction Engine (Core Brain)                              |                |
|  | - Gesture → Intent Mapping                                   |                |
|  | - State Machine (DRAW, ERASE, IDLE, UI)                      |                |
|  | - Smoothing / Filtering                                      |                |
|  | - Debounce / Confidence Handling                             |                |
|  +----------------------+--------------------------------------+                 |
|                         |                                                        |
|         +---------------+---------------+                                        |
|         |                               |                                        |
|         v                               v                                        |
|  DRAWING DOMAIN                   UI DOMAIN                                      |
|  +------------------+            +------------------------+                      |
|  | Draw Controller  |            | UI Controller          |                      |
|  | - Stroke logic   |            | - Buttons / Zones      |                      |
|  | - Brush engine   |            | - Tool selection       |                      |
|  +--------+---------+            +-----------+------------+                      |
|           |                                  |                                   |
|           v                                  v                                   |
|  +------------------+            +------------------------+                      |
|  | Canvas Engine    |            | HUD Renderer           |                      |
|  | (Layered buffer) |            | (Overlay system)       |                      |
|  +--------+---------+            +-----------+------------+                      |
|           |                                  |                                   |
|           +---------------+------------------+                                   |
|                           v                                                      |
|                   RENDERING PIPELINE                                             |
|                   +--------------------------+                                   |
|                   | Frame Composer           |                                   |
|                   | - Blend webcam + canvas  |                                   |
|                   | - Z-order layers         |                                   |
|                   +------------+-------------+                                   |
|                                |                                                 |
|                                v                                                 |
|                        Display / Output                                          |
+----------------------------------------------------------------------------------+
```
*(High-level overzicht van modules & datastromen)* 

*(Prototype)*

**Modulebeschrijving**
| Module                | Verantwoordelijkheid                                                          |
| --------------------- | ----------------------------------------------------------------------------- |
| **Webcam Input**      | Captures video frames via OpenCV (`cv2.VideoCapture`).                        |
| **Frame Processor**   | Verwerkt elk frame: flip for mirror, detecteert handlandmarks met Mediapipe.  |
| **Gesture Evaluator** | Analyseert vingers (index boven middelvinger ⇒ tekenen).                      |
| **Draw Controller**   | Beslist wat er getekend wordt en welke kleur gebruikt wordt.                  |
| **Canvas Buffer**     | Behoudt getekende lijnen als een `numpy`‑image array.                         |
| **UI Overlay**        | Detecteert kleurzones & wis‑actie en toont deze zones getekend bovenop beeld. |
| **Renderer**          | Combineert webcambeeld + canvas + UI → output naar scherm.                    |

**Datastromen**


1. ***Webcam → Frame Processor***

-      Frames worden ingelezen → gespiegeld → doorgestuurd naar handtracking.

2. ***Hand Detection → Gesture Evaluator***

  -     Handlandmarks worden geëxtraheerd → positie wijsvinger vergeleken met zones.

3. ***Gesture → Draw Controller***

-     Indien “tekenen”: voeg lijnelement toe aan canvas met huidige kleur.

-      Indien in “Clear”-zone: reset canvas buffer.

4. ***Canvas + Webcam → Renderer***

-      Canvas (met getekende lijnen) wordt over webcamfeed gelegd → weergave.

5. ***UI Zones → Colour State***

-      Detecteren selecties in bovenste balk → update tekenkleur.

### 4.2 Modules & Verantwoordelijkheden

| Module                        | Functie                                        |
|-------------------------------|-----------------------------------------------|
| cv2.VideoCapture              | Leest webcam frames.                           |
| mediapipe.solutions.hands     | Detecteert handlandmarks.                     |
| mp.solutions.drawing_utils    | Teken handlandmarks op frame.                 |
| Canvas (numpy array)          | Slaat lijnen en tekendata op.                 |
| UI zones                       | Detecteert kleur- of wisselecties.            |
| Main loop                      | Verwerkt frames, detecteert hand, tekent, combineert en toont output.|

### 4.3 Pseudocode

```python
start webcam
initialize mediapipe hands
initialize empty canvas

while webcam active:
    read frame
    flip frame for mirror effect
    detect hand landmarks
    if hand detected:
        get index and middle finger positions
        if index above middle:
            draw line from previous position
        else:
            reset previous position
    check color zones (Blue, Green, Red, Clear)
    overlay canvas on frame
    show frame in fullscreen
    if ESC pressed: break
```


## 5. Gebruikersinterface

Canvas & UI Zones:

Horizontale balk bovenaan met zones: Blue | Green | Red | Clear

Gebruiker kiest kleur door wijsvinger in zone te bewegen

Canvas overlay op webcam feed voor realtime feedback

Handlandmarks zichtbaar voor gebruikersfeedback

### Mockup:
```
╔══════════════════════════════════════╗
║ Blue │ Green │ Red │ Clear           ║
╠══════════════════════════════════════╣
║                                      ║
║  ╔══════════════════════════════╗    ║
║  ║      Canvas + Webcam         ║    ║
║  ╚══════════════════════════════╝    ║
║                                      ║
╚══════════════════════════════════════╝
```
### Screenshot van Air Drawing interface 

![Air Drawing](airdrawing1.png)
![Air Drawing](airdrawing.png)


## 6. Teststrategie

| Testtype                       | Beschrijving                                        |
|-------------------------------|-----------------------------------------------|
| **Unit tests**              | Test individuele functies zoals lijntekenen, kleurselectie.|
| **Integratietests**     | Test volledige loop: webcam → handdetectie → canvas overlay. |
| **Performance tests**    | Meet FPS en latency bij verschillende belichting en achtergrond.|
| **User Acceptance**       | 	Feedback van primaire doelgroep over gebruiksgemak en intuïtiviteit.                 |


## 7. Mogelijke uitbreidingen

- Opslaan van tekeningen als .png

- Meerdere brushes en diktes

- GUI knoppen in plaats van zones

- Multi-hand tracking

- Gesture control voor extra functies

## 8. Conclusie

Air Drawing combineert handtracking, realtime beeldverwerking en interactieve UI tot een lichtgewicht Python-app. Het biedt een intuïtieve en creatieve ervaring voor gebruikers die willen tekenen in de lucht en vormt een solide basis voor toekomstige uitbreidingen.
