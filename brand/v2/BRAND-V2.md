# RN INVEST · Brand V2 „Terminus“

Ersetzt die dunkle V1 „Quiet Capital“ als Außenauftritt. V1 bleibt im Repo und in Figma als Archiv.

## Idee

**Terminus**, der römische Gott der Grenzsteine. Als auf dem Kapitol der Jupitertempel gebaut wurde, wichen alle Götter, nur Terminus nicht: Sein Stein wurde in den Tempel hineingebaut (Livius I, Ovid, Fasti II). Für einen Käufer von Grund und Boden ist das die passende Gründungsgeschichte: **Was richtig gesetzt ist, bleibt. Ein gegebenes Wort wird nicht verrückt.**

Gestaltungsgrammatik nach dem Vorbild Gauss Capital, aber mit Münchner Eigenständigkeit:
hell, präzise, Mono-Beschriftungen mit Koordinaten, sichtbares Raster mit Fadenkreuzen, Halbton-Illustrationen statt Fotos, Bento-Raster aus Haarlinien, ein dunkler Mythos-Abschnitt mit drei Zeichen.

## Logo

- **Grenzpunkt-Emblem**: vier Eckwinkel und ein Kreuz. So markiert die Vermessung einen Grenzpunkt, also den Ort, an dem ein Grundstück beginnt.
- Wortmarke **RN INVEST** in Hanken Grotesk Medium, Laufweite +6 %.
- Dateien: `logo/logo-loden.svg`, `logo/logo-cream.svg`, `logo/emblem-grenzpunkt.svg`
- Bewusst verworfen: Stele mit Kreuz (liest sich als Grabstein).

## Drei Zeichen

| Zeichen | Bedeutung | Satz |
|---|---|---|
| Grenzpunkt | Grund und Boden | Wir kaufen, was bleibt. |
| Raute (bayerisch) | München | Wir kaufen nur dort, wo wir uns auskennen. |
| Verbindung | Verbindlichkeit | Ein Handschlag gilt, bis zum Notartermin. |

## Farben

| Token | HEX | Rolle | Kontrast |
|---|---|---|---|
| paper | `#F7F5F0` | Seite, Spalte | |
| paper-2 | `#EEE8DD` | Kalkstein-Flächen | |
| loden | `#24301F` | Primär: Buttons, Hervorhebung, Dunkelsektion, Logo | 12,7 : 1 auf paper |
| loden-2 | `#2E3B28` | Zitatbox auf Dunkel | |
| ink | `#1C2318` | Headlines, starker Text | 14,8 : 1 |
| moss | `#5C6655` | Sekundärtext | 5,5 : 1 auf paper, 4,9 : 1 auf paper-2 |
| cream | `#F2EDE2` | Text auf loden | 11,9 : 1 |
| sage | `#A9B09B` | Sekundärtext auf loden | 6,2 : 1 |
| signal | `#7C9A5E` | nur Statuspunkt „Ankauf aktiv“ | |
| line / line-strong | Loden 14 % / 32 % | Haarlinien, Fadenkreuze | |

## Typografie

- **Hanken Grotesk** 400/500: Headlines (H1 76 px, H2 54 px, −3 % / −2,5 %) und Text.
- **IBM Plex Mono** 400/500: alle Labels, Navigation, Buttons, Koordinaten, Versalien +8 %.
- **Newsreader Italic** 300: genau ein hervorgehobenes Wort pro Headline, im Loden-Block (auf Dunkel invertiert).

## Raster

- Inhaltsspalte 1184 px mit Haarlinien links und rechts über die ganze Seitenhöhe; außerhalb ein Plus-Muster (24 px).
- Fadenkreuze an den Schnittpunkten von Haarlinien.
- Radius 0, keine Schatten.

## Bildsprache

Halbton-Raster in Loden auf transparentem Grund (eigene Rasterung, `images/`):
Frauenkirche vor den Alpen bei Föhn (Hero) · Herme des Terminus (Philosophie) · Siedlungshaus im Garten (Profil A) · Gründerzeit-Eckhaus (Profil B).
Ausgangsmotive sind KI-generiert (Figma AI) und werden als „Illustration“ bezeichnet. Das Porträt von Niko Roncevic wird nach dem Shooting genauso gerastert.

## Ankaufsprofil-Karte

Interaktive SVG-Karte (`design/v2/components/MunichMap.tsx`, Basiskarte `map/map-munich.svg`, 5,7 KB): Stadtgebiet als Punktfeld, Mittlerer Ring gestrichelt, Isar, alle 18 Lagen in echten Koordinaten. Profil A zeigt Stadt und Landkreis, Profil B zoomt in die Innenstadt. Ein Klick auf eine Lage füllt das Formular vor.

## Sprache

Erste Person, wo der Gründer spricht („Ich sage Ihnen ehrlich, ob es passt.“), sonst „wir“. Verkäufer-Hooks: verbindlich, schnell, diskret, ohne Inserat, nichts herrichten müssen. Keine erfundenen Zahlen, keine Zusagen zu Fristen oder Kaufpreisen.

## SEO

Title „Grundstück & Haus verkaufen in München | RN INVEST Ankauf“ · Lagen in Headlines, Ankaufsprofil, FAQ und Footer · JSON-LD `Organization` (Gräfelfing, 18 `areaServed`) + `FAQPage`.
