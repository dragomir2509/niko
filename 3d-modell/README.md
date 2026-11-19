# 3D-Modell – Neubau Doppelhaus mit Carports, Gerlichstraße 8, 81245 München

Grundlage ist der Genehmigungsplan 01/1 vom Juli 2026 (Grundrisse UG–DT, Ansichten Ost/West/Süd/Nord,
Schnitte AA/BB, Lageplan, alles M 1:100 bzw. 1:500). Das Modell ist für **Exterior-Renderings** gedacht:
Fassaden, Öffnungen, Dachlandschaft, Carports und die Außenanlagen in vereinfachter Form. Innenräume gibt es nur
als Platzhalter (Decken, Böden, Trennwände), damit man durch die Gläser nicht ins Leere schaut.

## Dateien

| Datei | Zweck |
|---|---|
| `Gerlichstr8_Doppelhaus.blend` | Blender-Masterdatei mit Collections, Kameras, Sonne und Himmel |
| `Gerlichstr8_Doppelhaus.fbx` | 3ds Max (Corona/V-Ray), Cinema 4D, Twinmotion, Lumion, D5, Unreal |
| `Gerlichstr8_Doppelhaus.glb` | glTF 2.0 für D5, Enscape-Viewer, Web und schnelle Kontrolle |
| `Gerlichstr8_Doppelhaus.obj` + `.mtl` | universeller Fallback (Rhino, ArchiCAD, Revit-Import usw.) |
| `vorschau/*.png` | Kontroll-Renderings (Cycles) und orthogonale Ansichten zum Abgleich mit dem Plan |
| `quelle/build_model.py` | parametrisches Erzeugungsskript (Blender/bpy), Maße zentral änderbar |

SketchUp liest FBX/OBJ nicht direkt. Für SketchUp die FBX über Twinmotion/Datasmith oder ein OBJ-Import-Plugin einlesen.

## Koordinaten, Einheiten, Nordung

- Einheit Meter, Z = 0,00 entspricht ±0,00 = **518,70 m ü. NN** (OK FFB EG)
- Ursprung in der Gebäudemitte (Mitte des Mittelbaus)
- **Geo-orientiert:** +Y = Norden. Die Gebäudelängsachse weicht um **13,8° nach Westen** von Nord ab
  (Nordpfeil EG, Lageplan). Die Drehung steckt im Eltern-Empty `Gerlichstr8_ROOT_Nordausrichtung`.
  Wer achsparallel modellieren will, setzt dessen Z-Rotation auf 0. Dann zeigt die Ostfassade nach +X.
- Höhen: EG ±0,00 · OG +2,96 · DG +5,84 · Dachkante +8,85 · Brüstung DT +9,80 · Ausstieg +11,02 · First Mittelbau +8,88

## Aufbau (Collections)

- `01_Haus_A` – Südhaus (Gerlichstraße), mit Erker 1,14 m und Balkon
- `02_Haus_B` – Nordhaus, punktsymmetrisch zu A, Erker 2,015 × 6,50 m
- `03_Mittelbau` – Mansarde 70°/45° mit Stehfalz, Dachflächenfenstern, oben im Westen vollverglast, EG-Durchfahrt
- `04_Carports` – Sichtbeton, OK +3,00, extensives Gründach (eigenes Objekt, löschbar)
- `05_Aussenanlagen` – Gelände, Gerlichstraße mit Gehwegen, Fahrspuren, Holzterrassen, Sichtschutz, Müllhaus
- `06_Kontext_Nachbarn` – Platzhalter-Kubaturen der Nachbarhäuser für Schattenwurf (siehe Hinweise)
- `07_Kameras_Licht` – sieben Perspektiven, vier Orthogonalansichten, Sonne
- `08_Einfriedung_Strasse` – durchgehende Einfriedung zur Gerlichstraße: weiß verputzte Pfeiler mit Steinabdeckung,
  je ein zweiflügeliges Drehtor in Anthrazit an der West- und Ostzufahrt (lichte Breite ca. 2,95 m, Höhe 1,45 m),
  dazwischen vor dem Garten von Haus A ein Zaun aus Flachstahlstäben (1,30 m) auf weißem Sockel mit Formschnitthecke
  (1,15 m) zur Straße. Jeder Torflügel ist ein eigenes Objekt mit dem Ursprung im Drehpunkt; zum Öffnen
  einfach um Z drehen (nach innen ca. ±90°).

Pro Haus ist das Modell nach Bauteilen getrennt: Baukörper/Putz, Lisenen und Kugeln, Holzfassade, Fenster-Rahmen,
Glas, Dachgeschoss, Dach/Dachterrasse, Geländer, Erker, Portal/Vordach/Haustür, Innenraum und Pflanzen-Platzhalter.

## Materialien (zum Ersetzen im Renderer)

Alle Flächen haben eine Box-UV im Maßstab **1 UV-Einheit = 1 m**, damit Texturen in Realgröße sitzen.
Die Holzfassade ist als echte Brettgeometrie modelliert (12,5 cm Bretter, 1,2 cm Fuge), die Stehfalze als Geometrie
im Raster von 45 cm.

`Putz_hellgrau_Fassade` · `Putz_weiss_Portal_Attika` · `Putz_grau_Erker` · `Lisenen_Eckquaderung` ·
`Kugeln_Abdeckplatten_Stein` · `Holz_Fassade_Laerche_horizontal` · `Holz_Terrassendielen` · `Holz_Haustuer_Eiche` ·
`Alu_anthrazit_RAL7016` (Fenster, Dachrand, Paneele) · `Alu_hellgrau_Blechabdeckung` · `Metall_Stehfalz_hellgrau` ·
`Glas` · `Sichtbeton_Carport` · `Gruendach_extensiv` · `Kies_Dach` · `Terrassenplatten_Dach` · `Rasen` ·
`Pflaster_Fahrspur` · `Asphalt_Strasse` · `Gehweg` · `Innen_Wand_Decke` · `Innen_Boden` · `Pflanzen_Platzhalter` ·
`Erde_Pflanzbeet` · `Kontext_Nachbarbebauung` · `Kontext_Dach`

## Was aus dem Plan interpretiert wurde

Maße kommen aus den Bemaßungsketten. Wo keine Kette existiert, sind sie aus den Ansichten abgegriffen
(Genauigkeit etwa ±5 cm). Folgende Punkte sind Interpretationen und vor dem finalen Rendering mit dem Planer
abzustimmen:

1. **Punktsymmetrie:** Haus B ist Haus A um 180° gedreht. Das ist in allen vier Ansichten und den Grundrissen
   so gezeichnet. Abweichungen gibt es nur bei Erker, Terrassen und Carports, und die sind getrennt modelliert.
2. **DG-Stirnseiten** (Süd bei A, Nord bei B): 70°-Mansardfläche mit Schrägverglasung (6 Felder) und Holz an den
   Seiten. Ost und West sind senkrecht und um 0,92 bzw. 1,00 m zurückgesetzt, davor schmale Terrassen mit
   Pflanzkästen.
3. **Treppenausstieg:** Lage nach dem Grundriss Dachterrasse und Schnitt AA (Nordwest- bzw. Südost-Ecke).
   Die Süd- und die Nordansicht zeigen den Aufbau dagegen mittig. Hier widerspricht sich der Plan.
   Ausgeführt ist ein weiß verputzter Kubus mit Glastür und Glasfeld zur Terrasse, daneben der Kaminkopf.
4. **Brüstung Dachterrasse:** geneigte, horizontale Lamellen in Hellgrau (so in den Ansichten gezeichnet).
   Material und Ausführung sind nicht beschrieben.
5. **Mittelbau:** Mansarde nach Schnitt BB (70° bis +7,20, dann 45° bis First +8,88), Fuß auf der
   Durchfahrtsdecke +3,00. Oben im Westen vollverglast (Ansicht West), oben im Osten Stehfalz mit einem Fenster.
6. **Carports:** Sichtbeton mit Gründach. Das Gründach ist eine Annahme und kann als eigenes Objekt
   gelöscht werden. Das Carport West (Haus A) ist zur Zufahrt nach Süden offen und wird an der Ecke von einer
   Stütze getragen, hinten (Norden) schließt eine Wand ab.
7. **Außenanlagen:** Fahrspuren mit Rasenmittelstreifen, Terrassen und Müllhaus sind nach dem EG-Plan vereinfacht.
   Bäume, Hecken und Möblierung fehlen bewusst, weil sie im Renderer mit dessen Assets besser aussehen.
8. **Nachbarbebauung:** grobe Kubaturen aus dem Lageplan 1:500 (Lage ±1–2 m). Traufe 6,2 m und Satteldach
   sind geschätzt. Diese Objekte dienen nur dem Schattenwurf, für die Bildwirkung bitte nicht darauf verlassen.
9. **UG** ist nicht modelliert, weil es von außen nicht sichtbar ist.

## Tipps für die Renderings

- Sonne für München setzen (ca. 48,1° N / 11,4° E), Nordung ist bereits korrekt im Modell
- Glas als Thin-Glass oder Architekturglas mit leichter Reflexion. Hinter den Fenstern bei Bedarf Vorhänge
  oder Interior-Cards einsetzen.
- Holz: Lärche, sägerau bis gehobelt, Brettlänge entlang der Fassade (die UVs sind darauf ausgerichtet)
- Kameras `CAM_01` bis `CAM_06` sind klassische Exposé-Standpunkte (Augenhöhe 1,65 m, 18–24 mm, Shift für
  stürzende Linien). `ORTHO_*` sind die Planansichten zum Abgleich.
