# 3D-Modell – Neubau Doppelhaus mit Carports, Gerlichstraße 8, 81245 München

Grundlage ist der Genehmigungsplan 01/1 vom Juli 2026 (Grundrisse UG–DT, Ansichten Ost/West/Süd/Nord,
Schnitte AA/BB, Lageplan, alles M 1:100 bzw. 1:500). Das Modell taugt für **Exterior-Renderings** und ist
**innen begehbar**: Alle Innenwände aller Geschosse (UG, EG, OG, DG, Mittelbau) sind direkt aus den Vektordaten des
Plan-PDFs übernommen, also 1:1 und nicht nachgezeichnet. Dazu kommen Decken mit Treppenaugen, alle Treppen, Türen und
Stürze.

## Dateien

| Datei | Zweck |
|---|---|
| `Gerlichstr8_Doppelhaus.blend` | Blender-Masterdatei mit Collections, Kameras, Sonne und Himmel |
| `Gerlichstr8_Doppelhaus.fbx` | 3ds Max (Corona/V-Ray), Cinema 4D, Twinmotion, Lumion, D5, Unreal |
| `Gerlichstr8_Doppelhaus.glb` | glTF 2.0 für D5, Enscape-Viewer, Web und schnelle Kontrolle |
| `Gerlichstr8_Doppelhaus.obj` + `.mtl` | universeller Fallback (Rhino, ArchiCAD, Revit-Import usw.) |
| `vorschau/*.png` | Kontroll-Renderings (Cycles) und orthogonale Ansichten zum Abgleich mit dem Plan |
| `quelle/build_model.py` | parametrisches Erzeugungsskript (Blender/bpy), Maße zentral änderbar |
| `quelle/extract.py`, `doors.py`, `plan_interior.py` | lesen Wände, PV, Glas und Türbögen aus dem Plan-PDF und erzeugen `innenausbau.json` |

SketchUp liest FBX/OBJ nicht direkt. Für SketchUp die FBX über Twinmotion/Datasmith oder ein OBJ-Import-Plugin einlesen.

## Koordinaten, Einheiten, Nordung

- Einheit Meter, Z = 0,00 entspricht ±0,00 = **518,70 m ü. NN** (OK FFB EG)
- Ursprung in der Gebäudemitte (Mitte des Mittelbaus)
- **Geo-orientiert:** +Y = Norden. Die Gebäudelängsachse weicht um **13,8° nach Westen** von Nord ab
  (Nordpfeil EG, Lageplan). Die Drehung steckt im Eltern-Empty `Gerlichstr8_ROOT_Nordausrichtung`.
  Wer achsparallel modellieren will, setzt dessen Z-Rotation auf 0. Dann zeigt die Ostfassade nach +X.
- Höhen (OK FFB): UG −2,88 · EG ±0,00 · OG +2,96 · DG +5,84 · Bad Mittelbau-DG +5,71 · Dachterrasse +8,80/8,85 ·
  Brüstung DT +9,80 · Pergola/Kamin +11,02 · First Mittelbau +8,88
- Lichte Raumhöhen: UG 2,53 · EG 2,61 · OG 2,53 · DG ca. 2,40

## Aufbau (Collections)

- `01_Haus_A` – Südhaus (Gerlichstraße), mit Erker 1,14 m und Balkon
- `02_Haus_B` – Nordhaus, punktsymmetrisch zu A, Erker 2,015 × 6,50 m
- `03_Mittelbau` – Mansarde 70°/45° mit Stehfalz und Dachflächenfenstern, oben im Westen PV-Module, EG-Durchfahrt
- `04_Carports` – Sichtbeton, OK +3,00, extensives Gründach (eigenes Objekt, löschbar)
- `05_Aussenanlagen` – Gelände, Gerlichstraße mit Gehwegen, Fahrspuren, Holzterrassen, Sichtschutz, Müllhaus
- `06_Kontext_Nachbarn` – Platzhalter-Kubaturen der Nachbarhäuser für Schattenwurf (siehe Hinweise)
- `07_Kameras_Licht` – sieben Perspektiven, vier Orthogonalansichten, Sonne
- `08_Einfriedung_Strasse` – durchgehende Einfriedung zur Gerlichstraße: weiß verputzte Pfeiler mit Steinabdeckung,
  je ein zweiflügeliges Drehtor in Anthrazit an der West- und Ostzufahrt (lichte Breite ca. 2,95 m, Höhe 1,45 m),
  dazwischen vor dem Garten von Haus A ein Zaun aus Flachstahlstäben (1,30 m) auf weißem Sockel mit Formschnitthecke
  (1,15 m) zur Straße. Hohe Hecke (2,00 m) statt Holz-Sichtschutz an der Terrasse von Haus A, Meterhecke (1,80 m)
  als Sichtschutz entlang der Ostgrenze neben der Zufahrt (Objekt `Gelaende_Hecken_hoch`). Jeder Torflügel ist ein eigenes Objekt mit dem Ursprung im Drehpunkt; zum Öffnen
  einfach um Z drehen (nach innen ca. ±90°).

- `09_Innenausbau` – Innenwände je Geschoss, Türblätter, UG-Bodenplatte und UG-Fenster zu den Lichtschächten

Pro Haus ist das Modell nach Bauteilen getrennt: Baukörper/Putz, Lisenen und Kugeln, Holzfassade, Fenster-Rahmen,
Glas, Dachgeschoss, Dach/Dachterrasse, Geländer, PV-Module, Außentreppe, Pergola, Erker, Portal/Vordach/Haustür,
Decken/Treppen innen und Pflanzen-Platzhalter.

## Innenausbau (begehbar)

- **Wände:** Die rot (Mauerwerk) bzw. grün (Beton) gefüllten Wandflächen der vier Grundrisse sind aus dem PDF
  ausgelesen (Maßstab 1:100, Kontrolle: EG-Gesamtlänge exakt 23,21 m) und auf Geschosshöhe extrudiert. Die
  Außenwände von EG bis DG kommen aus dem Fassadenmodell, das mit den Ansichten abgeglichen ist. Im DG und im Mittelbau
  sind die Wände an den Dachschrägen beschnitten.
- **Türen:** Die Türblätter sind aus den Türbögen im Plan erkannt und stehen offen wie im Plan gezeichnet. Jede Tür
  ist ein eigenes Objekt mit dem Ursprung im Band, sie lässt sich also durch Drehen um Z schließen. Die Stürze sitzen
  auf 2,10 m.
- **Treppen:** Pro Haus drei gerade Läufe UG→EG (16 × 18/26), EG→OG (16 × 18,5/26) und OG→DG (16 × 18/26), übereinander
  gestapelt wie im Schnitt AA, mit Eiche-Trittstufen und Handlauf. Die Treppenaugen sind in allen Decken ausgespart.
- **Durchgänge** von Haus B in den Mittelbau (OG Flur/Arbeiten, DG Bad) sind nach den Lücken in den Planwänden geöffnet.
- **Licht:** In der Blender-Datei hängen Punktleuchten pro Geschoss, damit man innen sofort etwas sieht. Sie werden
  nicht mit exportiert.
- **Nicht enthalten:** Möblierung, Küchen- und Sanitärobjekte (im Plan nur als Symbol gezeichnet) und die 4 Stufen
  (4 × 18/26) im Mittelbau-Flur. Möbel setzt man am besten aus der Asset-Bibliothek des Renderers.

## Materialien (zum Ersetzen im Renderer)

Alle Flächen haben eine Box-UV im Maßstab **1 UV-Einheit = 1 m**, damit Texturen in Realgröße sitzen.
Die Holzfassade ist als echte Brettgeometrie modelliert (12,5 cm Bretter, 1,2 cm Fuge), die Stehfalze als Geometrie
im Raster von 45 cm.

`Putz_hellgrau_Fassade` · `Putz_weiss_Portal_Attika` · `Putz_grau_Erker` · `Lisenen_Eckquaderung` ·
`Kugeln_Abdeckplatten_Stein` · `Holz_Fassade_Laerche_horizontal` · `Holz_Terrassendielen` · `Holz_Haustuer_Eiche` ·
`Alu_anthrazit_RAL7016` (Fenster, Dachrand, Paneele) · `Alu_hellgrau_Blechabdeckung` · `Metall_Stehfalz_hellgrau` ·
`Glas` · `Sichtbeton_Carport` · `Gruendach_extensiv` · `Kies_Dach` · `Terrassenplatten_Dach` · `Rasen` ·
`Pflaster_Fahrspur` · `Asphalt_Strasse` · `Gehweg` · `Innen_Wand_Decke` · `Innen_Boden` · `Pflanzen_Platzhalter` ·
`Erde_Pflanzbeet` · `Kontext_Nachbarbebauung` · `Kontext_Dach` · `PV_Module_Glas` · `Innentuer_weiss_lackiert` ·
`Treppe_Trittstufen_Eiche` · `Hecke_Formschnitt_Platzhalter`

## Was aus dem Plan interpretiert wurde

Maße kommen aus den Bemaßungsketten. Wo keine Kette existiert, sind sie aus den Ansichten abgegriffen
(Genauigkeit etwa ±5 cm). Folgende Punkte sind Interpretationen und vor dem finalen Rendering mit dem Planer
abzustimmen:

1. **Punktsymmetrie:** Haus B ist Haus A um 180° gedreht. Das ist in allen vier Ansichten und den Grundrissen
   so gezeichnet. Abweichungen gibt es nur bei Erker, Terrassen und Carports, und die sind getrennt modelliert.
2. **DG-Stirnseiten** (Süd bei A, Nord bei B): 70°-Mansardfläche mit **Photovoltaik** (6 × 2 Module, im Plan dunkelblau),
   seitlich Holz. Die Ostseite liegt 1,00 m zurück, davor eine schmale Terrasse mit Pflanzkästen. Die Westwand liegt
   laut Wandpolygonen 1,55 m zurück: Dort ist eine Terrasse von 1,25 m Tiefe (5,2 m²) unter dem Dachüberstand.
3. **Dach / Dachterrasse:**
   - Zugang über eine **offene, halbgewendelte Außentreppe** (15 × 18,7/26, Stahl anthrazit) aus einer Nische an der
     DG-Westterrasse (bei B gedreht an der Ostterrasse), Austritt auf die Dachterrasse.
   - Auf dem Dach stehen eine **Pergola** mit Lamellendach (OK +11,02) über dem Kaminkopf und ein **geneigtes
     PV-Element** an der Dachkante (Plan Dachterrasse, dunkelblau). Einen geschlossenen Ausstiegsbau gibt es nicht.
   - Die Süd- und die Nordansicht zeichnen die Pergola mittig, Grundriss und Schnitt AA an der Nordwest-Ecke.
     Modelliert ist sie nach dem Grundriss.
4. **Brüstung Dachterrasse:** geneigte, horizontale Lamellen in Hellgrau (so in den Ansichten gezeichnet), am
   Treppenloch eine Glasbrüstung. Material und Ausführung sind nicht beschrieben.
5. **Mittelbau:** Mansarde nach Schnitt BB (70° bis +7,20, dann 45° bis First +8,88), Fuß auf der
   Durchfahrtsdecke +3,00. Oben im Westen **PV-Module** (im Plan dunkelblau), sonst Stehfalz mit Dachflächenfenstern.
6. **Carports:** Sichtbeton mit Gründach. Das Gründach ist eine Annahme und kann als eigenes Objekt
   gelöscht werden. Das Carport West (Haus A) ist zur Zufahrt nach Süden offen und wird an der Ecke von einer
   Stütze getragen, hinten (Norden) schließt eine Wand ab.
7. **Außenanlagen:** Fahrspuren mit Rasenmittelstreifen, Terrassen und Müllhaus sind nach dem EG-Plan vereinfacht.
   Bäume, Hecken und Möblierung fehlen bewusst, weil sie im Renderer mit dessen Assets besser aussehen.
8. **Nachbarbebauung:** grobe Kubaturen aus dem Lageplan 1:500 (Lage ±1–2 m). Traufe 6,2 m und Satteldach
   sind geschätzt. Diese Objekte dienen nur dem Schattenwurf, für die Bildwirkung bitte nicht darauf verlassen.
9. **UG:** komplett nach Grundriss, mit Bodenplatte und Fenstern zu den Lichtschächten (Brüstung 1,33 m, Sturz).
   Die Lichtschächte selbst sind nur als Wände angedeutet.

## Tipps für die Renderings

- Sonne für München setzen (ca. 48,1° N / 11,4° E), Nordung ist bereits korrekt im Modell
- Glas als Thin-Glass oder Architekturglas mit leichter Reflexion. Hinter den Fenstern bei Bedarf Vorhänge
  oder Interior-Cards einsetzen.
- Holz: Lärche, sägerau bis gehobelt, Brettlänge entlang der Fassade (die UVs sind darauf ausgerichtet)
- Kameras `CAM_01` bis `CAM_09` sind Exposé-Standpunkte außen und auf dem Dach (Augenhöhe 1,65 m, 18–28 mm, Shift
  für stürzende Linien). `INNEN_*` sind Standpunkte im Gebäude, `ORTHO_*` die Planansichten zum Abgleich.
- Für Walkthroughs (Twinmotion, D5, Unreal) die FBX laden, Kollision auf die Collections `09_Innenausbau`,
  `*_Innen_Decken_Treppen` und die Baukörper legen.
