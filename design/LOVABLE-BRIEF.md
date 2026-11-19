Build the complete production one-pager for **RN INVEST**, a private investment company (real estate, Munich). Language of the site: **German only**. This brief is the binding spec, derived from a finished Figma design. The attached `ref-*.jpg` images are Figma exports of the desktop design (1440 px) — match them closely. Do NOT improvise a different look, do NOT add sections, do NOT add stock UI patterns (cards with icons, gradients, shadows, rounded corners, emojis, testimonials, stats counters).

## 0. Tech & scope
- Static marketing one-pager. **No backend, no database, no auth, no Supabase, no CMS.** Keep dependencies minimal.
- React + TypeScript + Tailwind. Clean component architecture: `src/components/site/` with `Nav.tsx`, `Hero.tsx`, `Haltung.tsx`, `Interlude.tsx`, `Fokus.tsx`, `CoInvest.tsx`, `Ankaufsprofil.tsx`, `Kontakt.tsx`, `Footer.tsx`, plus `ui/` primitives `SectionLabel.tsx`, `ButtonLine.tsx`, `TextLink.tsx`, `Reveal.tsx`, `Wordmark.tsx`. All copy in `src/content/site.ts` (one typed object) so texts are editable in one place. Contact data in `src/config/site.ts`.
- Semantic HTML: `<header>`, `<nav aria-label="Hauptnavigation">`, `<main>`, one `<section>` per block with `aria-labelledby`, exactly one `<h1>`, then `<h2>` per section, `<h3>` for sub-items, `<footer>`. Skip link „Zum Inhalt springen“.
- Remove any default Lovable/Vite placeholder content, default favicon and default OG tags.

## 1. Design tokens (use exactly; define as CSS variables in `index.css` and map into Tailwind theme)
```
--rn-ink: #11100E;        /* page background */
--rn-espresso: #1B1714;   /* Co-Investments section bg, hover fills, selected option */
--rn-anthracite: #282623;
--rn-slate: #4B4741;      /* secondary text on light */
--rn-taupe: #8C8379;      /* labels/meta on dark only */
--rn-stone: #B9B1A5;      /* body text on dark */
--rn-bone: #E9E4DA;       /* headlines, logo, primary text */
--rn-travertine: #E4DFD5; /* the ONE light section (Ankaufsprofil) */
--rn-line: rgba(233,228,218,.14);       /* hairlines on dark */
--rn-line-strong: rgba(233,228,218,.40);
--rn-line-light: rgba(17,16,14,.16);    /* hairlines on light */
--rn-error: #D2A193;
--rn-ease: cubic-bezier(0.22, 1, 0.36, 1);
```
- Border radius: **0 everywhere**. Box shadows: **none**. Separation only through 1px hairlines and background changes.
- `::selection { background: var(--rn-bone); color: var(--rn-ink); }`

### Fonts (Google Fonts, `display=swap`, preconnect)
- Serif: **Newsreader** variable with optical size: `family=Newsreader:ital,opsz,wght@0,6..72,300..500;1,6..72,300..400`. Use `font-optical-sizing: auto` so large sizes render with the display optical size.
- Sans: **Hanken Grotesk** `wght@400;500`.
- Body: Hanken Grotesk 400, color stone, `-webkit-font-smoothing: antialiased`, `text-rendering: optimizeLegibility`, `font-feature-settings: "kern","liga"`.

### Type scale (fluid; mobile → desktop)
| Token | Font | Size | Line-height | Tracking |
|---|---|---|---|---|
| display-xl (H1) | Newsreader 300 | clamp(2.75rem, 1.2rem + 6.6vw, 8rem) | 0.98 | -0.025em |
| display-l (H2) | Newsreader 300 | clamp(2.25rem, 1.4rem + 3.8vw, 5rem) | 1.04 | -0.02em |
| display-m | Newsreader 300 | clamp(1.875rem, 1.4rem + 1.6vw, 3rem) | 1.1 | -0.015em |
| heading-s | Newsreader 400 | clamp(1.375rem, 1.2rem + .5vw, 1.75rem) | 1.25 | -0.005em |
| figure | Newsreader 300 | clamp(1.875rem, 1.5rem + 1vw, 2.5rem) | 1.1 | -0.01em, `font-variant-numeric: lining-nums tabular-nums` |
| lead | Hanken 400 | clamp(1.125rem, 1.05rem + .3vw, 1.25rem) | 1.6 | 0 |
| body | Hanken 400 | clamp(1rem, .97rem + .12vw, 1.0625rem) | 1.7 | 0 |
| small | Hanken 400 | .875rem | 1.6 | .005em |
| label | Hanken 500 | .75rem | 1.2 | .22em, uppercase |
| nav | Hanken 500 | .75rem | 1.2 | .18em, uppercase |
Italic accents use Newsreader italic 300 in color stone. Never bold. Use `text-wrap: balance` on headings, `text-wrap: pretty` on paragraphs. Use `hyphens: manual` (no auto hyphenation in headlines).

### Grid & spacing
- Container: max-width 1440px, horizontal padding `clamp(20px, 4.4vw, 64px)`. 12-column CSS grid, column-gap 24px (16px on mobile).
- Section vertical padding: `clamp(96px, 6rem + 4vw, 160px)`.
- Breakpoints: mobile < 768, tablet 768–1279, desktop ≥ 1280. Below 1024 everything stacks to one column.

## 2. Brand assets
- **Wordmark**: create `Wordmark.tsx` that inlines this exact SVG (fill = currentColor, `role="img" aria-label="RN INVEST"`). Never replace it with live text.
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="68 -1503 14217 1557" role="img" aria-label="RN INVEST"><path fill="currentColor" d="M626 -768Q778 -768 864.5 -847.5Q951 -927 951 -1081Q951 -1173 913.0 -1239.5Q875 -1306 789.0 -1342.0Q703 -1378 559 -1378H295V-1430H628Q828 -1430 944.5 -1385.0Q1061 -1340 1111.0 -1262.0Q1161 -1184 1161 -1083Q1161 -995 1112.0 -919.0Q1063 -843 966.0 -794.0Q869 -745 725 -737V-740Q817 -739 875.0 -719.0Q933 -699 972.5 -655.5Q1012 -612 1048 -538L1205 -218Q1247 -133 1277.5 -94.0Q1308 -55 1343.5 -45.0Q1379 -35 1435 -35V0Q1331 8 1262.5 7.0Q1194 6 1149.0 -11.0Q1104 -28 1072.0 -66.0Q1040 -104 1008 -168L830 -532Q794 -607 765.0 -646.5Q736 -686 705.0 -701.0Q674 -716 629 -716H295V-768ZM453 -1430V-71L632 -29V0H68V-29L247 -71V-1360L68 -1401V-1430ZM2046.0 -71V-1344L1847.0 -1401V-1430H2253.0L3102.0 -276L3049.0 -70V-1359L2850.0 -1401V-1430H3294.0V-1401L3115.0 -1359V20H3077.0L2084.0 -1322L2112.0 -1360V-71L2311.0 -29V0H1867.0V-29ZM5383.0 -29V0H4819.0V-29L4998.0 -71V-1360L4819.0 -1401V-1430H5383.0V-1401L5204.0 -1360V-71ZM6104.0 -71V-1344L5905.0 -1401V-1430H6311.0L7160.0 -276L7107.0 -70V-1359L6908.0 -1401V-1430H7352.0V-1401L7173.0 -1359V20H7135.0L6142.0 -1322L6170.0 -1360V-71L6369.0 -29V0H5925.0V-29ZM7922.0 -1358 7766.0 -1401V-1430H8321.0V-1401L8139.0 -1360L8633.0 -228H8608.0L9019.0 -1353L8829.0 -1401V-1430H9238.0V-1401L9085.0 -1350L8571.0 20H8533.0ZM10548.0 -1039 10514.0 -746 10548.0 -455H10526.0L10415.0 -711L9936.0 -735V-758L10415.0 -786L10526.0 -1039ZM10858.0 -1036 10833.0 -1028 10632.0 -1394 10785.0 -1370H9930.0V-1430H10650.0L10783.0 -1484H10791.0ZM10650.0 -35 10889.0 -402 10914.0 -395 10808.0 54H10800.0L10672.0 0H9930.0V-60H10804.0ZM9690.0 0V-29L9869.0 -71V-1360L9690.0 -1401V-1430H10075.0V0ZM12282.0 -1363 12155.0 -1392 12261.0 -1484H12278.0L12337.0 -1022L12313.0 -1018L12133.0 -1343L12187.0 -1274Q12126.0 -1328 12047.0 -1363.5Q11968.0 -1399 11881.0 -1399Q11750.0 -1399 11688.0 -1336.5Q11626.0 -1274 11626.0 -1171Q11626.0 -1101 11656.0 -1053.5Q11686.0 -1006 11737.5 -974.0Q11789.0 -942 11854.5 -918.0Q11920.0 -894 11991.0 -869Q12062.0 -844 12132.0 -812.0Q12202.0 -780 12259.5 -731.0Q12317.0 -682 12351.5 -608.0Q12386.0 -534 12386.0 -424Q12386.0 -293 12316.5 -192.5Q12247.0 -92 12131.0 -35.5Q12015.0 21 11874.0 21Q11772.0 21 11693.0 6.5Q11614.0 -8 11530.0 -43L11444.0 -423H11473.0L11727.0 -20L11574.0 -124Q11657.0 -75 11723.5 -47.5Q11790.0 -20 11865.0 -20Q11984.0 -20 12068.5 -57.0Q12153.0 -94 12198.0 -164.0Q12243.0 -234 12243.0 -334Q12243.0 -423 12206.5 -481.5Q12170.0 -540 12110.5 -578.5Q12051.0 -617 11980.0 -644.5Q11909.0 -672 11839.0 -699Q11769.0 -726 11707.0 -756.0Q11645.0 -786 11597.0 -827.0Q11549.0 -868 11521.5 -926.0Q11494.0 -984 11494.0 -1066Q11494.0 -1185 11549.5 -1271.0Q11605.0 -1357 11706.5 -1404.0Q11808.0 -1451 11946.0 -1451Q12041.0 -1451 12120.5 -1430.0Q12200.0 -1409 12282.0 -1363ZM13503.0 -1400H13709.0V-71L13888.0 -29V0H13324.0V-29L13503.0 -71ZM14171.0 -1370H13041.0L13154.0 -1389L12956.0 -988L12927.0 -995L12990.0 -1503H13008.0L13155.0 -1414L13065.0 -1430H14147.0L14057.0 -1414L14204.0 -1503H14222.0L14285.0 -995L14256.0 -988L14058.0 -1389Z"/></svg>
```
- Uploaded files → copy into `public/`: `favicon.svg`, `apple-touch-icon.png`, `og-image.png`. Copy photos into `src/assets/`: `travertine.webp` (hero plate, portrait 3:4), `oak.webp` (Haltung, 3:2), `stair.webp` (Interlude, full-bleed 3:2), `facade.webp` (Co-Investments, portrait 3:4). Use `<img>` with explicit `width`/`height`, `loading="lazy"` + `decoding="async"` for all except the hero image (`fetchpriority="high"`). Meaningful German `alt` texts (e.g. „Travertinfassade mit Streiflicht, Referenzmotiv“). Images get `object-fit: cover`, no rounded corners, no filters.
- Every image has a caption below in label style, taupe: „Abb. 01 · Referenzmotiv“ (02 oak, 03 stair (inside interlude, bottom-left), 04 facade). These photos are art-direction reference motifs, not own projects — the caption must stay.

## 3. Global components
- **SectionLabel**: inline-flex row, gap 16px: number (label style, taupe) · 40px × 1px line (line-strong) · term (label, taupe). On the light section use slate + line-light.
- **ButtonLine** (primary): inline-flex, height 56px, padding 0 28px, gap 20px, 1px border line-strong, transparent bg, label style text bone + a thin 20×10 arrow SVG (stroke 1px, currentColor). Hover/focus-visible: a bone fill slides up from the bottom (pseudo-element `transform: scaleY(0→1)`, origin bottom, 320ms var(--rn-ease)); text and arrow turn ink; arrow shifts 4px right. Full width on mobile with arrow pushed to the right (`justify-content: space-between`). Variant `onLight`: ink background, bone text, hover espresso.
- **TextLink**: label-style text + arrow, underline is a 1px line under the text, 40px wide at rest, grows to 100% on hover (240ms).
- **Focus**: `:focus-visible { outline: 1px solid var(--rn-bone); outline-offset: 4px; }` (ink on the light section). Never remove focus styles.
- **Reveal**: IntersectionObserver (threshold .15, once). Initial `opacity:0; transform: translateY(16px)`, to visible in 900ms var(--rn-ease); support `delay` prop for 80ms staggering. Headline lines (H1 and H2) reveal line by line from a mask (each line wrapped in overflow-hidden span, inner span translateY(105%) → 0, 1100ms).
- **prefers-reduced-motion: reduce** → no transforms, no transitions, content visible immediately, smooth scrolling off.

## 4. Sections (in this order)

### 4.0 Navigation (`<header>`, fixed top)
- Height 96px at top → 72px after 24px scroll. At top: transparent. Scrolled: `background: rgba(17,16,14,.85)`, `backdrop-filter: blur(12px)`, 1px bottom border line. Transition 400ms.
- Left: Wordmark, 132px wide desktop / 112px mobile, links to `#top`.
- Right (≥1024px): links Philosophie (#philosophie) · Investments (#investments) · Ankaufsprofil (#ankaufsprofil) · Kontakt (#kontakt), nav style, gap 40px, color stone; active section (IntersectionObserver) and hover = bone. Use `aria-current="true"` on the active link.
- Mobile: text button „Menü“ (nav style, bone, min 48×48 tap area, `aria-expanded`, `aria-controls`). Opens a full-screen ink overlay: top row wordmark + „Schließen“; then 4 links as large Newsreader 300 (display-l) rows with hairline above and a small number (01–04, label taupe) before each; bottom: label „Private Investmentgesellschaft · München“. Esc closes, focus is trapped inside, body scroll locked, links close the menu.
- Smooth anchor scrolling with `scroll-margin-top: 88px` on sections.

### 4.1 Hero (`id="top"`, ink)
- `min-height: 100svh`, content padding-top ~ 180px desktop / 120px mobile, bottom strip at the bottom.
- Desktop grid: left 9 columns text, right 3 columns image plate (aligned ~72px below top of the H1 block). Tablet/mobile: text first, image below (full width, aspect 4:5 on mobile).
- Kicker (label, taupe): „Private Investmentgesellschaft · München“, 40px above H1.
- H1 (display-xl, bone) in two lines: „Erst das Urteil.“ / „Dann das Kapital.“ — second line Newsreader italic 300 in stone. Line-by-line mask reveal on load (second line +120ms).
- Lead (lead style, stone, max-width 6 columns ≈ 640px), 48px below H1: „RN INVEST ist eine unabhängige, inhabergeführte Investmentgesellschaft für Immobilien in München. Wir investieren selektiv in Grundstücke und Wohnimmobilien, deren Wert sich durch Planung, Baurecht und Umsetzung nachvollziehbar heben lässt. Mit eigenem Kapital und gemeinsam mit ausgewählten Co-Investoren.“
- CTAs 56px below: ButtonLine „Investmentkontakt“ → #kontakt, TextLink „Ankaufsprofil“ → #ankaufsprofil, gap 40px.
- Image plate: travertine.webp, aspect 4:5, slow scale 1.06 → 1 over 2.4s on load; plus a very subtle light sweep: an overlay linear-gradient (transparent → rgba(233,228,218,.06) → transparent) translating across over 12s, infinite, ease-in-out (disabled for reduced motion). Caption „Abb. 01 · Referenzmotiv“ 16px below.
- Bottom strip: 1px line, then grid: col 1–4 „Fokus“ (label taupe) + „Wohnimmobilien und Grundstücke in München“ (small, stone); col 5–8 „Strategien“ + „Development, Value-Add, Co-Investments“; right aligned „Scrollen“ (label taupe) next to a 1×32px line-strong vertical line (subtle 2s scaleY loop, off in reduced motion). Hide the strip's third item on mobile.

### 4.2 Haltung (`id="philosophie"`, ink)
- SectionLabel „01 · Haltung“; 48px; H2 (display-l, bone, max 9 columns): „Eine gute Adresse ist noch kein gutes Investment.“
- 96px; grid: cols 1–5 image oak.webp (aspect 4:3) + caption „Abb. 02 · Referenzmotiv“; cols 7–11 text column, gap 28px:
  - lead, bone: „Investmentqualität entsteht nicht aus Lage, Bekanntheit oder einem überzeugenden Exposé allein. Sie entsteht aus dem Verhältnis von Einstiegspreis, realisierbarem Potenzial, Zeit, Risiko, Kapitalbindung und Exit.“
  - body, stone: „Wir beurteilen Immobilien deshalb nicht nur nach ihrem heutigen Zustand, sondern nach den wirtschaftlichen Möglichkeiten, die unter realistischen Annahmen bestehen, und danach, was es kostet, sie zu realisieren.“
  - body, stone: „Ein Kern unseres Ansatzes: architektonische Qualität, die oft Spitzenlagen vorbehalten ist, auf gute bis sehr gute Münchner Lagen zu übertragen. Mit disziplinierter Kostenstruktur, marktgängigen Grundrissen und einem Exit, der vom ersten Tag an mitgedacht ist.“
- 144px; label „Die sechs Variablen einer Investmententscheidung“; 24px; a band with top+bottom hairline, 6 equal cells separated by vertical hairlines (first cell no left border/padding). Each cell: number „01“…„06“ (label taupe) then 40px gap then term (heading-s, bone): Einstiegspreis · Potenzial · Zeit · Risiko · Kapitalbindung · Exit. Mobile: 2 columns × 3 rows. Cells reveal staggered 80ms.
- 160px; header row: „Grundsätze“ (display-m, bone) left, „I – VI“ (label taupe) right, 40px bottom padding.
- 6 rows, each with top hairline, padding 36px 0 40px, grid: col 1 roman numeral (heading-s, taupe), cols 2–6 title (heading-s, bone), cols 8–12 text (body, stone). Mobile: numeral + title in one row, text below.
  - I · Selektivität statt Volumen · „Nicht jede Gelegenheit ist ein Investment. Bewusstes Nichtinvestieren ist eine Entscheidung, getroffen mit derselben Sorgfalt wie ein Ankauf.“
  - II · Substanz vor Inszenierung · „Eine Transaktion muss in ihrem wirtschaftlichen Kern überzeugen. Die Verpackung ist zweitrangig.“
  - III · Wertschöpfung statt Hoffnung · „Potenzial zählt, wenn es durch konkrete Maßnahmen realisierbar ist: Ankauf, Planung, Baurecht, bauliche Optimierung, Repositionierung, Vermietung oder Verkauf.“
  - IV · Kapitaldisziplin · „Kapitalbindung, Finanzierungsstruktur, Liquidität, Kostenreserven und Risikotragfähigkeit sind Teil jeder Entscheidung, nicht ihre Fußnote.“
  - V · Interessengleichheit · „Co-Investments beruhen auf nachvollziehbaren Strukturen. Eine Partnerschaft soll über ein einzelnes Projekt hinaus tragen.“
  - VI · Diskretion, kurze Wege · „Keine unnötige Öffentlichkeit, keine institutionelle Fassade. Entschieden wird dort, wo die Verantwortung liegt.“

### 4.3 Interlude (full-bleed, no container padding)
- Height `clamp(560px, 54vw, 780px)`; background stair.webp cover, overlay `linear-gradient(180deg, rgba(17,16,14,.55) 0%, rgba(17,16,14,.15) 50%, rgba(17,16,14,.7) 100%)`. Very gentle parallax on the image (max 8% translate, disabled for reduced motion and on mobile).
- Centered: blockquote in Newsreader italic 300, display-l size, bone, max-width ~ 1000px: „Auch bewusstes Nichtinvestieren ist eine Entscheidung.“; below 32px label „Grundsatz I“ (stone). Caption „Abb. 03 · Referenzmotiv“ bottom-left (label, stone), 56px from bottom.

### 4.4 Investmentfokus (`id="investments"`, ink)
- SectionLabel „02 · Investmentfokus“; 48px; grid: cols 1–6 H2 (display-l) „Ein Markt.“ / „Drei Strategien.“ (forced line break), cols 8–12 body stone aligned to bottom: „RN INVEST konzentriert sich auf München. Die Beschränkung auf einen Markt erlaubt es, Mikrolagen, Planungsrecht, Kostenstrukturen und Käufergruppen präzise zu beurteilen. Das ist die Voraussetzung, um Potenzial realistisch zu bewerten.“
- 112px; three strategy rows (`<article>`), each with top border line-strong, padding 48px 0 56px; last row followed by a bottom line-strong. Grid: col 1 index letter (display-m, taupe), cols 2–6 title (display-m, bone, h3, break after first word on desktop), cols 8–12: definition (lead, bone), then 28px, label „Ansatzpunkte“ (taupe), 12px, list of 4 items (small, stone), each item with a top hairline and 12px vertical padding.
- Hover (desktop pointer only): row background fades to espresso (400ms) and the index letter shifts 8px right. Rows extend the background to the full container width with 0 horizontal padding change (use negative margin + padding of 24px, or an inset pseudo-element) — keep text alignment unchanged.
  - A · Development Investments · „Grundstücke und Immobilien mit baulichem oder planungsrechtlichem Entwicklungspotenzial.“ · Baurecht nach § 34 BauGB oder Bebauungsplan / Planung und Genehmigung / Neubau und Ersatzneubau / Nachverdichtung
  - B · Value-Add Investments · „Bestandsimmobilien mit nachvollziehbaren Optimierungs-, Sanierungs-, Repositionierungs- oder Entwicklungsmöglichkeiten.“ · Sanierung und Modernisierung / Grundrissoptimierung / Aufstockung und Erweiterung / Repositionierung und Vermietung
  - C · Selective Co-Investments · „Gemeinsame, individuell strukturierte Investitionen mit ausgewählten privaten und professionellen Kapitalpartnern.“ · Projektbezogene Beteiligungsstruktur / Gemeinsame Investitionsentscheidung / Transparente Berichterstattung / Gleichgerichtete Interessen
- Use non-breaking space in „§ 34 BauGB“ („§&nbsp;34&nbsp;BauGB“).

### 4.5 Co-Investments (`id="co-investments"`, background espresso)
- SectionLabel „03 · Co-Investments“; 48px; H2 (display-l, bone, max 9 columns): „Für Kapital, das unternehmerisch denkt.“; 72px.
- Grid: cols 1–5 (sticky on desktop, top 120px): body stone „RN INVEST beteiligt ausgewählte Privatpersonen, Unternehmer, Immobilieninvestoren und Family Offices an einzelnen Münchner Immobilienprojekten. Für Partner, die an der Substanz einer Investition interessiert sind, ohne jede Phase von Ankauf und Entwicklung selbst operativ begleiten zu wollen.“; 48px; ButtonLine „Vertrauliches Investmentgespräch“ → #kontakt and preselects topic „Kapitalpartnerschaft“; 40px; note block with top hairline, padding-top 24px: label „Selektiv“ + small stone „Wir arbeiten bewusst mit wenigen Kapitalpartnern. Ein erstes Gespräch klärt, ob Investmentprofil, Zeithorizont und Erwartungen zusammenpassen, auf beiden Seiten.“
- Cols 7–12: facade.webp (height ~520px desktop, aspect 4:5 mobile) + caption „Abb. 04 · Referenzmotiv“; 48px; two sub-columns (each 3 cols):
  - label „Was RN INVEST einbringt“ + numbered list (01–04 small taupe, text small stone, each row top hairline, 16px padding): „Identifikation und Vorprüfung von Investmentgelegenheiten, auch außerhalb des öffentlichen Marktes.“ / „Beurteilung von Chancen und Risiken: wirtschaftlich, planungsrechtlich und baulich.“ / „Entwicklung des Transaktions- und Finanzierungskonzepts.“ / „Koordination geeigneter Partner- und Umsetzungsgesellschaften für Planung, Bau und Verwertung.“
  - label „Wie Beteiligungen entstehen“ + list: „Beteiligungsmodelle werden projektbezogen und individuell vereinbart.“ / „Vor jeder Entscheidung: vollständige Informationsgrundlage mit Annahmen, Kalkulation, Risiken und Exit-Szenarien.“ / „Struktur und Rolle von RN INVEST werden je Projekt offengelegt.“ / „Keine öffentlichen Angebote, keine Renditeversprechen.“
- 144px; label „Ablauf“; 24px; `<ol>` of 4 steps in 4 columns (mobile: vertical list with number left): top border line-strong, padding-top 28px, number (figure, taupe), title (heading-s, bone), text (small, stone):
  01 Kennenlernen · „Ein vertrauliches Gespräch über Investmentprofil, Kapitalhorizont und Erwartungen.“ / 02 Projektvorstellung · „Bei passender Gelegenheit: Unterlagen, Annahmen und Risiken, vollständig und ungeschönt.“ / 03 Strukturierung · „Eine individuelle, projektbezogene Beteiligungsvereinbarung.“ / 04 Umsetzung · „Regelmäßige Information über den Projektverlauf bis zum Exit.“
- 96px; small taupe, max 7 columns: „Die Inhalte dieser Website stellen weder ein öffentliches Angebot noch eine Anlageberatung dar. Beteiligungen werden ausschließlich individuell und projektbezogen vereinbart.“

### 4.6 Ankaufsprofil (`id="ankaufsprofil"`, background travertine, text ink — the only light section; styled like a mandate document)
- Top row: SectionLabel „04 · Ankaufsprofil“ (slate) left, label „Für Eigentümer, Makler und Berater“ (slate) right; then a 1px **ink** line full width; padding-top of section 120px.
- 72px; grid: cols 1–6 H2 (display-l, ink) „Wonach wir suchen.“; cols 8–12 lead slate bottom-aligned: „Ein Ankaufsprofil für professionelle Marktteilnehmer. Wir prüfen Angebote vertraulich und geben eine klare Rückmeldung.“
- 96px; a definition list (`<dl>`), each row top hairline line-light, padding 32px 0 36px, grid: cols 1–3 `<dt>` (label, slate), cols 4–12 `<dd>`:
  - Standort → (heading-s, ink, max 8 cols) „München. Etablierte und nachgefragte Wohnlagen mit nachvollziehbarer Mikrolage, Substanz und wirtschaftlichem Potenzial.“
  - Assetklassen → numbered list 01–05 (small slate number, lead ink text), rows separated by line-light: Baugrundstücke für hochwertige Wohnbebauung / Einfamilien-, Doppel- und Reihenhäuser mit Entwicklungspotenzial / Kleinere Mehrfamilienhäuser / Sanierungsbedürftige Wohnimmobilien / Immobilien mit Nachverdichtungs-, Erweiterungs- oder Repositionierungspotenzial
  - Planungsrecht → (heading-s, ink) „Insbesondere Grundstücke mit Entwicklungsoptionen nach § 34 BauGB sowie geeignete Grundstücke mit Bebauungsplan.“
  - Mehrfamilienhäuser · Suchprofil → 4 equal columns separated by vertical line-light (mobile: stacked rows with label left, figure right): label / figure (figure style, ink) / small slate note:
    Lage / „Mittlerer Ring“ / „München, bevorzugt innerhalb“ · Wohnfläche / „250–500 m²“ / „ca., je nach Objekt“ · Kaufpreis / „bis 4 Mio. €“ / „ca., als Orientierung“ · Vermietung / „Leerstand“ / „vorzugsweise leerstehend oder teilweise leerstehend“
  - Weitere Investments → (heading-s, ink) „Individuelle Bewertung nach Standort, Baurecht, Grundstücksgröße, Zustand, Ankaufspreis und Exit-Potenzial.“
- Closing line-light, then (cols 4–9) small slate: „Die Angaben beschreiben Suchschwerpunkte, keine starren Ausschlusskriterien. Außergewöhnliche Gelegenheiten prüfen wir auch außerhalb dieses Rahmens.“
- 96px; **Off-Market box**: ink background, padding 64px (24px mobile), grid: left cols 1–4 label „Diskret“ (taupe) + title „Off-Market-Angebote“ (display-m, bone, h3); right cols 6–11: body stone „Diskrete Angebote nehmen wir direkt entgegen. Für eine erste Einschätzung hilfreich: Lage oder Adresse, Grundstücks- und Wohnfläche, Baurechtssituation, Vermietungsstand, Kaufpreisvorstellung und vorhandene Unterlagen.“ + small taupe „Makler und Berater: Bitte nennen Sie Ihr Mandatsverhältnis und Ihre Provisionsvorstellung.“ + ButtonLine „Investmentangebot einreichen“ → #kontakt and preselects topic „Immobilienangebot“.

### 4.7 Kontakt (`id="kontakt"`, ink)
- SectionLabel „05 · Kontakt“; 48px; H2 (display-l) „Sprechen wir über Substanz.“; 96px.
- Grid: cols 1–4 left: lead stone „Ob Kapitalpartnerschaft oder Immobilienangebot: Anfragen werden persönlich gelesen und vertraulich behandelt.“; 56px; block with top line-strong, padding-top 24px: label „Direkt“, then rows (label 88px wide small taupe + value body bone): E-Mail → `SITE.email` (mailto link with TextLink-like underline hover), Telefon → `SITE.phone`, Anschrift → `SITE.address`; small taupe „Jede Anfrage wird vertraulich behandelt.“ Hide a row if its value is empty.
- Cols 6–12: the form (`<form noValidate>`), vertical gap 40px:
  - label „Ihr Anliegen“ + radiogroup of two option tiles side by side (stacked on mobile): each tile 1px border line, padding 28px; top row: number („01“/„02“, label taupe) and an 8×8 square indicator (1px bone border; filled bone when selected); title (heading-s, bone): „Kapitalpartnerschaft“ / „Immobilienangebot“; text small stone: „Für Privatinvestoren, Unternehmer und Family Offices mit Interesse an gemeinsamen Investments.“ / „Für Eigentümer, Makler und Berater mit Grundstücken oder Immobilien, die dem Ankaufsprofil entsprechen.“ Selected tile: border bone, background espresso. Implement as real radio inputs (visually hidden) with labels; arrow keys work. Default: Kapitalpartnerschaft. Support URL hash/query or a shared state so the CTAs above preselect the topic.
  - Fields (2-column grid on desktop, gap 24px): Name* · E-Mail* · Telefon · Unternehmen. Conditional: if Kapitalpartnerschaft → select „Investorentyp“ (Privatinvestor, Unternehmer, Family Office, Institutioneller Investor, Sonstiges). If Immobilienangebot → select „Ihre Rolle“ (Eigentümer, Makler, Berater, Sonstiges), input „Lage oder Adresse“, select „Objektart“ (Grundstück, Ein-, Zwei- oder Reihenhaus, Mehrfamilienhaus, Sonstiges). Then textarea „Nachricht *“ full width (4 rows, auto-grow).
  - Field style: label above (label style, taupe, associated `<label for>`), input transparent, no border except 1px bottom line-strong, text body bone, padding 12px 0, font-size ≥16px; focus: bottom line bone; placeholder taupe. Selects styled the same with a thin chevron. Errors: bottom line + message in `--rn-error`, small, `aria-invalid`, `aria-describedby`.
  - Consent checkbox* (custom 18px square, 1px line-strong; checked: bone fill with ink check): „Ich bin einverstanden, dass meine Angaben zur Bearbeitung meiner Anfrage verarbeitet werden. Hinweise in der Datenschutzerklärung.“ („Datenschutzerklärung“ links to `#datenschutz`).
  - Honeypot field (hidden „website“) for spam.
  - Submit: ButtonLine „Anfrage vertraulich senden“ (loading state: „Wird gesendet …“, disabled).
  - Validation (zod or hand-written) with these messages: „Bitte geben Sie Ihren Namen an.“ · „Bitte geben Sie eine gültige E-Mail-Adresse an.“ · „Bitte beschreiben Sie Ihr Anliegen kurz.“ · „Bitte bestätigen Sie die Einwilligung.“
  - **Submission (prepared, no backend)**: in `src/config/site.ts` export `FORM_ENDPOINT = import.meta.env.VITE_FORM_ENDPOINT ?? ""`. If set: `POST` JSON `{topic, name, email, phone, company, investorType, role, location, propertyType, message}` with `Accept: application/json` (compatible with Formspree/Basin/Make webhooks). If empty: build a `mailto:` link to `SITE.email` with subject „Anfrage über rninvest: <Anliegen>“ and a plain-text body of all fields, and open it. Success state replaces the form with heading-s bone „Vielen Dank.“ + body stone „Ihre Anfrage ist eingegangen. Wir melden uns persönlich.“ Error state (small, error color, `role="alert"`): „Die Anfrage konnte nicht übermittelt werden. Bitte schreiben Sie uns direkt an <email>.“ Comment the integration options in code.

### 4.8 Footer (ink)
- Padding-top 96px, bottom 40px. The Wordmark spans the **full container width** (it's the closing composition of the page), reveal on scroll.
- 56px; 1px line; row (wrap on mobile, stacked): label taupe „Private Investmentgesellschaft · München“ · small taupe „© 2026 RN INVEST · [Rechtsform, Sitz, Registergericht]“ · links (label, stone, hover bone): „Impressum“ (#impressum) „Datenschutz“ (#datenschutz) „Nach oben ↑“ (#top).
- Add two minimal anchored blocks under the footer row, collapsed by default as `<details>` with summary in label style: `id="impressum"` and `id="datenschutz"`, each containing only a clearly marked placeholder paragraph: „[Impressum: Angaben gemäß § 5 DDG werden vor Veröffentlichung ergänzt.]“ / „[Datenschutzerklärung wird vor Veröffentlichung ergänzt.]“. Opening via the footer links.

## 5. Config (`src/config/site.ts`)
```ts
export const SITE = {
  name: "RN INVEST",
  url: "https://[domain]",          // PLATZHALTER
  email: "[E-Mail-Adresse]",        // PLATZHALTER
  phone: "[Telefonnummer]",         // PLATZHALTER
  address: "[Anschrift, München]",  // PLATZHALTER
  legal: "[Rechtsform, Sitz, Registergericht]", // PLATZHALTER
};
```
Show placeholders exactly as written (in brackets). Do not invent any contact details, people names, numbers, track records or legal data.

## 6. SEO & meta (index.html)
- `<html lang="de">`, `<meta name="theme-color" content="#11100E">`, viewport incl. `viewport-fit=cover`.
- Title: „RN INVEST · Private Investmentgesellschaft für Immobilien in München“
- Description: „Unabhängige, inhabergeführte Investmentgesellschaft für selektive Immobilieninvestments in München: Development, Value-Add und Co-Investments mit ausgewählten Kapitalpartnern.“
- Open Graph + Twitter: `og:type=website`, `og:locale=de_DE`, `og:title` „RN INVEST · Erst das Urteil. Dann das Kapital.“, `og:description` = description, `og:image=/og-image.png` (1200×630), `twitter:card=summary_large_image`.
- Icons: `<link rel="icon" href="/favicon.svg" type="image/svg+xml">`, `<link rel="apple-touch-icon" href="/apple-touch-icon.png">`. Remove other default icons.
- JSON-LD `Organization` with name, `areaServed: "München"`, description; url from SITE (placeholder), no invented fields.
- `public/robots.txt` allowing all. Preload the hero image.

## 7. Quality bar
- Must look exactly like the attached Figma exports on desktop: generous negative space, hairlines, no boxes, no shadows, no radius, no extra colors.
- Mobile (375px) must be equally composed: 20px side padding, H1 on two lines („Erst das Urteil.“ / „Dann das Kapital.“), no horizontal scroll anywhere, touch targets ≥48px, form inputs 16px.
- Lighthouse-minded: no layout shift (explicit image dimensions, font `size-adjust` fallback if possible), lazy images, no heavy libraries (no framer-motion needed — use CSS + IntersectionObserver).
- Contrast: taupe text is only allowed on ink/espresso; on travertine use slate.
