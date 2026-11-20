# RN INVEST · Brand V4 „Quiet Luxury × Pop“

**Aktuell.** Ersetzt V3 „Pop-Terminus“ (monochrom, Wir-Form). V1–V3 bleiben als Archiv im Repo und in Figma.

## Haltung

Ein Family Office, das nicht so tut, als wäre es eines. Ruhig, präzise, diskret und dabei nahbar, weil ein Mensch spricht: **Niko Roncevic, in der Ich-Form**.
Vorbild für die Anmutung: Loro Piana, Brunello Cucinelli, Zegna. Kaschmir statt Weiß, Espresso statt Schwarz, Serife statt Grotesk-Headline, viel Luft.
Dazu **ein** Pop-Art-Zitat: der Terminus-Comic mit Ben-Day-Punkten, harter Versatzschatten und Sprechblase. Er wirkt wie ein Augenzwinkern im Maßanzug. Er ist selbstbewusst, aber nie laut. Pop kommt nur an zwei Stellen vor: im Hero-Panel und im Terminus-Band. Sonst gibt es nur die gepunktete Unterstreichung einzelner Wörter.

## Positionierung gegenüber Bauträgern

| Bauträger | RN INVEST |
|---|---|
| rechnet in Quadratmetern | denkt in Häusern und Straßen |
| Gremien, Freigaben | eine Person entscheidet |
| taktische Nachverhandlung | ein Angebot, zu dem ich stehe |
| Inserat, Bieterrunde | diskret, ohne Öffentlichkeit |
| maximale Fläche, Standard | Architektur, die in die Straße passt |

Kernsatz: **„Bauträger rechnen in Quadratmetern. Ich denke in Häusern.“**

## Logo

- Grenzpunkt-Emblem (vier Eckwinkel + Kreuz = Vermessungspunkt, an dem ein Grundstück beginnt) und Wortmarke RN INVEST in Newsreader (als Pfad, keine Schrift nötig).
- `logo/logo-espresso.svg` (auf hell), `logo/logo-cashmere.svg` (auf Espresso), `logo/logo-current.svg` (currentColor, für Code).
- Mindesthöhe 14 px digital. Schutzraum = Emblemhöhe rundum.
- Favicon: Espresso-Quadrat mit Emblem in Kaschmir (`icons/`).

## Farben

| Token | HEX | Rolle | Kontrast |
|---|---|---|---|
| cash | `#F3EEE6` | Seite | |
| sand | `#E8E0D3` | Wechselsektionen (Unterschied, Kontakt) | |
| esp | `#2B2420` | Primär: Headlines, Buttons, dunkles Band, Logo | 13,2 : 1 auf cash |
| ink | `#1E1A17` | Fließtext | 15,0 : 1 |
| mute | `#6A6158` | Sekundärtext | 5,25 : 1 auf cash, 4,6 : 1 auf sand |
| soft | `#B8AC9C` | Sekundärtext auf Espresso | 6,85 : 1 |
| bubble | `#FFFDF9` | nur Sprechblase | |
| line / line-strong | Espresso 14 % / 34 % | Haarlinien | |

Keine weiteren Farben. Kein Gold, kein Grün, kein Akzentrot.

## Typografie

- **Newsreader Light 300** für Headlines (H1 78 px / H2 60 px, −2,2 %), **Light Italic** für hervorgehobene Wörter, Unterschrift und Ziffern.
- **Hanken Grotesk** 400/500 für Text (17 px / 1,65), 700 nur in der Sprechblase (Versalien).
- **IBM Plex Mono** 500 für Labels, Navigation und Buttons (11,5 px, +12 %, Versalien).
- Pro Headline höchstens ein kursives Wort mit gepunkteter Ben-Day-Unterstreichung (`.dotline`).

## Pop-Elemente

- **Comic-Panel:** 1,5 px Espresso-Rahmen, Ben-Day-Punkte (9 px Raster, 13 % Deckkraft), harter Schatten 7/7 px Espresso, Bildunterschrift als Espresso-Reiter.
- **Sprechblase:** Ellipse #FFFDF9, 1,5 px Rahmen, Schatten 4/4 px, −4° gedreht, Hanken Grotesk 700 Versalien. Texte: „Das steht.“, „Keinen Zentimeter!“
- **Illustrationen:** Comic-Tusche in Espresso auf transparentem Grund (`images/`): Terminus-Büste, Götter-Panel, Siedlungshaus, Altbau. Ausgangsmotive sind KI-generiert (Figma AI) und eigens umgefärbt.
- **Kein Foto von Niko.** Persönlichkeit entsteht über Sprache und Unterschrift.

## Sprache

- Durchgehend **ich**. Die Firma heißt „RN INVEST“, nie „wir“.
- Kurze Sätze. Kein Superlativ, keine Zahlen ohne Beleg, keine Fristzusagen.
- Ein Versprechen, das gelebt werden muss: **„Ein Angebot, zu dem ich stehe. Bis zum Notartermin.“**
- Makler und Tippgeber werden nicht direkt angesprochen. Sie erkennen sich wieder: an der Rolle im Formular, am Exposé-Link-Feld, an der NDA-Option, an der direkten E-Mail und an der Zusage, nicht nachzuverhandeln.
- Psychologische Hooks und alle Texte stehen in [`COPY-V4.md`](COPY-V4.md).

## Seitenaufbau (One-Pager, 7 Bereiche)

1. Hero, Ich-Vorstellung, Terminus-Panel, Leiste mit drei Hooks
2. Persönlich: Brief und Unterschrift
3. Der Unterschied: Gegenüberstellung mit Bauträgern
4. Ankaufsprofil: interaktive Karte, Profil A/B
5. Warum Terminus: dunkles Band, Mythos
6. So kaufe ich: drei Schritte, FAQ (4)
7. Objekt anbieten: Formular mit Rollen, direkter Mailkontakt, Adresse

## Dateien

- Prototyp (HTML): `design/v4/prototype.html`, Ansicht `design/v4/prototype-sheet.jpg`
- Figma: Seite „V4 · Quiet Luxury × Pop (aktuell)“
- Assets: `brand/v4/images`, `brand/v4/logo`, `brand/v4/icons`, `brand/v4/og-image.png`
