Air Drawing – Software Life Cycle Document (SLDC)
1. Projectoverzicht

Naam: Air Drawing
Repository: Starley‑iggy/air-drawing

Taal: Python
Doel:
Air Drawing is een interactieve applicatie die realtime handtracking gebruikt om gebruikers toe te staan tekenen in de lucht met hun wijsvinger. Het systeem herkent de handbewegingen via een webcam en vertaalt deze naar lijnen op het scherm.

Belangrijkste kenmerken:

Realtime handtracking met Mediapipe

Interactieve tekenfunctie via wijsvinger

Dynamische kleurselectie en canvas‑clearing

Volledig Python‑based, geen externe GUI frameworks nodig

2. Functioneel Ontwerp (Wat doet het systeem?)
2.1 Hoofdfunctionaliteiten
Functionaliteit	Beschrijving
Handdetectie	Detecteert handlandmarks (vingertoppen, gewrichten) via webcam.
Tekenmodus	Teken alleen wanneer de indexvinger boven de middelvinger is.
Kleurselectie	Bovenaan scherm: vier zones (Blue, Green, Red, Clear).
Wis canvas	Knop Clear wist het volledige tekenoppervlak.
Realtime visualisatie	Canvas en webcamfeed worden samengevoegd en realtime weergegeven.
2.2 Use Case Diagram
Diagram is not supported.

Beschrijving Use Cases:

Detect Hand: Applicatie herkent hand in beeld.

Select Color: Gebruiker beweegt wijsvinger naar kleurzone.

Draw on Canvas: Bewegingsdata van indexvinger wordt vertaald naar lijnen op canvas.

Clear Canvas: Canvas wordt geleegd bij aanraking van Clear zone.

3. Technisch Ontwerp (Hoe werkt het systeem?)
3.1 Architectuur
Webcam → Beeldverwerking → Handdetectie → Tekenlogica → UI feedback → Output

Modules & verantwoordelijkheden:

Module	Functie
cv2.VideoCapture	Start webcam en leest frames.
mediapipe.solutions.hands.Hands	Detecteert handlandmarks.
mp.solutions.drawing_utils	Teken landmarks voor debug/feedback.
Canvas (numpy array)	Slaat lijnen en tekendata op.
UI zones	Detecteert kleur- of wisselecties.
Main loop	Realtime frameverwerking en rendering.
3.2 Dataflow
3.3 Pseudocode
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
4. Scherm & Gebruikersinterface

Canvas & UI:

Horizontale balk bovenaan met 4 zones: Blue | Green | Red | Clear

Kleur verandert wanneer wijsvinger in een zone komt

Canvas overlay op live webcamfeed

Handlandmarks zichtbaar voor realtime feedback

Voorbeeld Mockup:

+--------------------------------------+
| Blue | Green | Red | Clear           |  <- UI Zones
+--------------------------------------+
|                                      |
|          [Canvas + Webcam]           |
|                                      |
+--------------------------------------+
5. Technische Specificaties
Aspect	Detail
Taal	Python 3.7+
Libraries	OpenCV, Mediapipe, Numpy
Systeemvereisten	Webcam, CPU voor realtime tracking
Optimalisatie	Goed verlichte omgeving voor nauwkeurige handdetectie
6. Mogelijke Verbeteringen

Meerdere brushes & diktes

Opslaan van tekeningen als .png

GUI knoppen in plaats van zones

Gesture controls voor extra functies

Multi-hand tracking voor meerdere gebruikers

7. Conclusie

Air Drawing is een compacte, interactieve Python-app die computer vision gebruikt voor realtime handtracking en tekenen in de lucht. Het project combineert eenvoudige UI‑zones met een responsieve tekenlogica, waardoor het geschikt is voor educatieve projecten, prototypes en creatieve experimenten.
