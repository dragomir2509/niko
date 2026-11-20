# RN INVEST · Brand V5 „Quiet by default. Radical by intention.“

**Aktuell.** Ersetzt V4 „Quiet Luxury × Pop“. V1–V4 bleiben als Archiv im Repo und in Figma.

## Haltung

RN INVEST ist die private, persönlich geführte Investmentgesellschaft von Niko Roncevic. Die Marke tritt auf wie eine international arbeitende Investmentgesellschaft: ruhig, präzise, selektiv. Sie verkauft nichts und wirbt nicht um Kapital.

**90 / 10.** 90 % der Gestaltung sind Reduktion: Porcelain, Carbon, eine Schriftfamilie, Haarlinien, viel Fläche. 10 % sind bewusst radikal: das angeschnittene Riesen-Monogramm im Hero, die sehr breite, leichte Headline, eine einzige Ultramarine-Sektion.

Keine Bilder, keine Karte, keine Illustrationen, keine Figuren. Die Identität entsteht aus Monogramm, Typografie und Komposition.

## Monogramm

Eine Ligatur aus R und N mit eigener Konstruktion:

- **Drei Stämme, zwei Diagonalen, ein Bogen.** Der Schenkel des R landet exakt am Fuß des ersten N-Stamms. Der Schenkel und die N-Diagonale laufen parallel.
- **Umgekehrter Strichkontrast.** Haarfeine Senkrechte, kräftige Diagonalen. Das macht die Form unverwechselbar und gibt der Marke ihr zweites Zeichen: die **Doppeldiagonale** (zwei parallele Schrägstriche im Winkel des Monogramms), die als Marker vor jeder Sektion steht.
- **Drei optische Größen**, damit die Haarlinien in jeder Größe tragen:

| Variante | Stamm / Diagonale (bei Höhe 100) | Einsatz |
|---|---|---|
| `display` | 4 / 16 | ab etwa 120 px Höhe, Hero, Druck |
| `text` | 6 / 15 | 24 bis 120 px, Navigation, Footer, Briefkopf |
| `micro` | 9 / 17 | Favicon, App-Icon, Stempel |

Bewusst ausgeschlossen: Häuser, Dächer, Schlüssel, Wappen, Kronen, Säulen, Diagramme.

## Wordmark und Logo-Varianten

Wordmark „RN INVEST“: Archivo Expanded Medium, Versalien, Laufweite +14 %, als Pfad gezeichnet (keine Schrift nötig).

| Datei (`brand/v5/logo/`) | Verwendung |
|---|---|
| `logo-horizontal-carbon.svg` | Standard auf hellem Grund |
| `logo-horizontal-porcelain.svg` | auf Carbon oder Ultramarine |
| `logo-horizontal-ultramarine.svg` | einfarbig Ultramarine |
| `logo-horizontal-duo.svg` | Monogramm Ultramarine, Wordmark Carbon |
| `logo-stacked-*.svg` | kompakte Variante: Monogramm über Wordmark |
| `monogram-{display,text,micro}-{carbon,porcelain,ultramarine}.svg` | Monogramm allein, Schwarz-Weiß und Ultramarine |
| `wordmark-*.svg` | Wordmark allein |

Regeln: Wordmark-Höhe = 30 % der Monogramm-Höhe. Schutzraum = Breite eines N-Stamm-Abstands rundum. Mindesthöhe horizontal 20 px. Nicht verzerren, nicht kursiv stellen, keine Verläufe, keine Schatten.

Icons (`brand/v5/icons/`): `favicon.svg`, `favicon-32.png`, `favicon-48.png`, `apple-touch-icon.png` (180 px), `icon-192.png`, `icon-512.png`. Immer Porcelain-Monogramm auf Ultramarine.
Open-Graph-Grafik: `brand/v5/og-image.png` (1200 × 630).
Übersicht aller Varianten: `brand/v5/logo-overview.png`.

Die Identität ist für Briefpapier, Visitenkarte und Dokumente ausgelegt: einfarbig druckbar, ohne Rasterflächen, mit einer Stempelgröße (`micro`).

## Farben

| Token | HEX | Rolle | Kontrast |
|---|---|---|---|
| Porcelain | `#ECECE9` | primärer Hintergrund | |
| Porcelain 2 | `#E2E2DE` | Ton-in-Ton-Flächen, Hero-Monogramm | |
| Carbon Black | `#171719` | Schrift, dunkle Sektionen | 15,1 : 1 auf Porcelain |
| Carbon 2 | `#222225` | Ton-in-Ton auf Carbon | |
| Signature Ultramarine | `#4535E8` | Akzent, Marker, eine Statement-Sektion | 6,1 : 1 auf Porcelain |
| Silver Grey | `#B9B9B8` | nur Linien und Dekor, nie Text | |
| Graphite | `#5C5C60` | Sekundärtext auf hell | 5,6 : 1 |
| Mist | `#A9A9AB` | Sekundärtext auf Carbon | 7,6 : 1 |

Ultramarine ist Signatur, nicht Fläche: zweite Headline-Zeile, Doppeldiagonale, Ankaufspreis, Fokuszustände, genau eine Sektion (Ankaufsprozess). Kein Gold, kein Grün, keine Creme-Töne, keine Verläufe, keine zweite Akzentfarbe.

Alle Tokens: [`tokens.css`](tokens.css), [`tokens.json`](tokens.json).

## Typografie

Eine Familie in drei Breiten, dazu eine Mono für Daten:

| Rolle | Schrift | Einstellung |
|---|---|---|
| Display, Headlines | Archivo, Breite 125 (Expanded), Light 300 | bis 120 px, −3,5 % Laufweite, Zeilenabstand 0,98 |
| Zwischentitel | Archivo, Breite 112, Regular | 22 bis 30 px |
| Text | Archivo, Breite 100, Regular | 17 px, Zeilenabstand 1,6 |
| Mikrotypografie | Archivo, Breite 125, Medium, Versalien | 11 px, +14 % |
| Daten | IBM Plex Mono | 12 px (Stand, Nummern) |

Lizenz: beide Schriften stehen unter der SIL Open Font License 1.1 (kommerzielle Nutzung, Einbettung und Logo-Nutzung erlaubt). Die Dateien liegen im Projekt (`src/assets/fonts`, mit Lizenztexten) und werden vom eigenen Server geladen. Es gibt keine Anfrage an Google Fonts oder andere Dritte.

Satzregeln: Headlines in zwei kurzen, parallel gebauten Sätzen mit festem Umbruch. Linksbündig, asymmetrisch im 12-Spalten-Raster. Radius 0, keine Schatten.

## Sprache

- Dritte Person: „RN INVEST …“. Kein „wir“, keine Ansprache von Kapitalgebern.
- Kurz, belegbar, ohne Superlative. Keine Renditen, Referenzen oder Fristzusagen.
- Leitsatz: **Unabhängig im Denken. Klar im Handeln.**

## Seitenaufbau

1. **Hero:** Leitsatz, Monogramm angeschnitten im Hintergrund, zwei zurückhaltende Aktionen.
2. **Über RN INVEST:** kurze Vorstellung, Gesellschaftsdaten.
3. **Investmentansatz** (Carbon): sechs Grundsätze als nummerierter Index.
4. **Ankaufsprofil:** zwei Dossiers A und B nebeneinander. Im Profil B hervorgehoben: „Ankaufspreis: bis 5.000.000 €, gilt für Mehrfamilienhäuser“.
5. **Ankaufsprozess** (Ultramarine): drei Schritte.
6. **Kontakt:** Formular mit zwei Anliegen, direkte E-Mail.
7. **Footer** (Carbon): Monogramm, Anschrift, E-Mail, Impressum, Datenschutz, Datenschutzeinstellungen.

Eigene Seiten: `/impressum`, `/datenschutz`.

## Bewegung

Zeilenweises Aufsteigen der Hero-Headline, Enthüllen des Monogramms von oben, dezentes Einblenden der Sektionen, Linien-Wischer bei Links, verschobener Pfeil bei Buttons. Alles einmalig, nichts in Schleife. `prefers-reduced-motion` schaltet jede Bewegung ab.

## Dateien

- Quellcode der Seite (identisch mit Lovable, per Prüfsumme bestätigt): [`design/v5/site/`](../../design/v5/site)
- Prüf-Screenshots: [`design/v5/qa/`](../../design/v5/qa)
- Audit und offene Punkte: [`design/v5/AUDIT-V5.md`](../../design/v5/AUDIT-V5.md)
