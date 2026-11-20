# RN INVEST · V5 · Audit, Umsetzung und offene Punkte

Stand: 20.11.2026. Die V5 liegt im Lovable-Editor (unveröffentlicht). Die veröffentlichte Seite zeigt weiterhin V4, bis die Freigabe erteilt ist.

## 1. Audit des Standes vor V5

Vorgefunden wurde ein unveröffentlichter Relaunch eines anderen Agenten (Commits „Relaunch umgesetzt & geprüft“, „Relaunch & MFH 5 Mio. eingefügt“).

**Bereits korrekt**
- Firmendaten zentral: RN Invest UG (haftungsbeschränkt), Lochhamer Schlag 12, 82166 Gräfelfing, Amtsgericht München, HRB 305629, rn@rninvest.de, keine Telefonnummer
- 5-Mio.-Grenze nur für Mehrfamilienhäuser
- Serverseitige Prüfung des Formulars, Honeypot, Zeitprüfung, Same-Origin-Prüfung, Schutz vor Doppelversand
- Schriften lokal statt Google Fonts (im Editor-Stand; live noch Google Fonts)
- robots.txt, Sitemap-Route, Canonical, Einwilligungslogik ohne Banner

**Teilweise**
- Design: Ultramarine vorhanden, aber Standard-Schrift (Manrope) und ein schwaches Monogramm
- Navigation und Sektionen wichen von der Vorgabe ab (kein „Kontakt“, andere Benennung, FAQ zusätzlich)
- Ankaufsprozess mit „Angebot und Notar“ statt „Entscheidung und weitere Abstimmung“
- Impressum nur einzeilig, kein Open-Graph-Bild

**Fehlerhaft**
- Formular speicherte Anfragen in einer Datenbank und zeigte „Danke“, obwohl keine E-Mail an rn@rninvest.de ging
- Datenschutzerklärung enthielt interne Prüfvermerke („noch zu bestätigen“) im öffentlichen Text
- Unnötiges Google-Consent-Skript (gtag) im Seitenkopf, obwohl kein Google-Dienst genutzt wird
- Bei jedem Seitenaufruf eine unnötige Abfrage `/cdn-cgi/trace`
- Supabase-Bibliothek im Browser-Paket, obwohl es keine Anmeldung gibt
- Alte Comic-Assets (Terminus) und Karte noch im Projekt

**Fehlte**
- Eigenständiges Monogramm mit Varianten, Wordmark, Favicon, Apple-Touch-Icon, OG-Grafik
- E-Mail-Versand, Mengenbegrenzung
- Vollständiges Impressum und Datenschutzerklärung als eigene Seiten
- Sechs Grundsätze des Investmentansatzes

## 2. Technischer Datenschutz-Audit (veröffentlichte Seite, 20.11.2026)

Gemessen mit einem frischen Browser ohne Vorbesuch:

| Punkt | Befund live (V4) | V5 (Editor-Stand, lokal gemessen) |
|---|---|---|
| Fremde Hosts | fonts.googleapis.com, fonts.gstatic.com | keine |
| Cookies | `__dpl` (Hosting, Versionszuordnung), `__cf_bm` (Cloudflare, Bot-Schutz) | von der Anwendung keine; die zwei Hosting-Cookies kommen erst auf der veröffentlichten Seite hinzu |
| localStorage | leer | leer |
| sessionStorage | Scrollposition (Router) | Scrollposition (Router) |
| Analyse-Skripte im HTML | keine | keine |
| Lovable-Besucherstatistik | laut vorigem Agenten per Projekteinstellung deaktiviert; im HTML ist kein Zählskript. Über die Schnittstelle nicht unabhängig prüfbar | unverändert |
| „Edit with Lovable“-Plakette | vorhanden (Hinweis-Link, keine Fremdanfrage) | vorhanden, nur in bezahltem Tarif abschaltbar |

Ergebnis: Es gibt keine einwilligungspflichtige Technik. Deshalb kein Cookie-Banner. Stattdessen zeigt der Dialog „Datenschutzeinstellungen“ im Footer den Stand an. Die vorhandene Einwilligungslogik bleibt für künftige Dienste bestehen: Sie werden erst nach Zustimmung geladen, Ablehnen und Akzeptieren sind gleichwertig.

## 3. Umsetzung V5

- Neue Identität: Monogramm (drei optische Größen), Wordmark, Logo-Varianten, Icons, OG-Grafik
- Schrift: Archivo (variable Breite) und IBM Plex Mono, Dateien im Projekt, OFL-Lizenz liegt bei
- Struktur: Hero · Über RN INVEST · Investmentansatz · Ankaufsprofil · Ankaufsprozess · Kontakt · Footer; dazu `/impressum`, `/datenschutz`
- Entfernt: FAQ, Karte, Comic-Assets, gtag-Skript, `/cdn-cgi/trace`-Abfrage, Supabase im Browser (JavaScript von 180 auf 123 KB gzip)
- Kontaktformular: zwei Anliegen, Felder passen sich an, Pflichtfelder laut Vorgabe, Versand per E-Mail über Resend, keine Speicherung, Mengenbegrenzung, Erfolgsmeldung nur nach Annahme durch den Versanddienst
- SEO: Titel, Description, Canonical, Open Graph, Twitter Card, Organization- und WebSite-Daten, Sitemap mit drei Seiten

## 4. Prüfergebnisse

Lokal am identischen Code (Prüfsummen von Lovable bestätigt: 43 von 43):

- TypeScript strict: fehlerfrei
- ESLint für alle geänderten Dateien: fehlerfrei
- Vitest: 38 von 38 Tests
- Produktions-Build: erfolgreich
- Playwright bei 360, 390, 820, 1280, 1440, 1920 px: keine Konsolenfehler, kein horizontaler Überlauf, keine Fremdanfragen
- axe-core (WCAG 2.0/2.1/2.2 A und AA, Best Practices) auf `/`, `/impressum`, `/datenschutz`, Desktop und Mobil: 0 Verstöße
- Funktionen: Navigation, Mobilmenü (Escape, Fokus zurück, Hintergrund gesperrt), Lagen-Übernahme ins Formular, Profil-Schaltflächen, Pflichtfeldprüfung mit Fokus auf dem ersten Fehler, Datenschutz-Dialog (Fokusfalle, Escape), 404-Seite

In der Lovable-Sandbox bestätigt: Build, Browser-Checks bei 1440 und 390 px, alle Routen, alle Icon-URLs, Formular zeigt ohne Versandschlüssel die Fehlermeldung und keine Erfolgsmeldung.

**Nicht getestet:** die tatsächliche Zustellung einer E-Mail ins Postfach rn@rninvest.de. Dafür fehlt der Versandschlüssel (siehe 5).

## 5. Offene Voraussetzungen

1. **E-Mail-Versand aktivieren.** Kostenloses Resend-Konto mit rn@rninvest.de anlegen, API-Schlüssel erzeugen und in Lovable als Secret `RESEND_API_KEY` hinterlegen. Ohne eigene Absenderdomain kann Resend nur an die Adresse des Kontoinhabers senden; deshalb das Konto mit rn@rninvest.de anlegen. Danach Testanfrage senden und den Eingang prüfen. Optional: Domain rninvest.de bei Resend verifizieren und `CONTACT_FROM` setzen.
2. **Mengenbegrenzung** arbeitet im Arbeitsspeicher der Serverinstanz (5 Anfragen je 10 Minuten und Anschluss, 40 je Stunde gesamt). Sie dämpft Missbrauch, ist aber keine harte Quote über alle Instanzen.
3. **Tabelle `contact_submissions`** wird nicht mehr beschrieben. Löschen erfordert eine Datenbank-Migration mit Freigabe.
4. **Auftragsverarbeitung:** DPA mit Lovable (Lovable Labs Incorporated) und mit Resend prüfen und ablegen. Die Datenschutzerklärung nennt beide.
5. **Umsatzsteuer-ID:** falls vorhanden, im Impressum ergänzen.
6. **Lovable-Statistik:** Abschaltung in den Projekteinstellungen einmal selbst kontrollieren.
7. **Eigene Domain:** nach Aufschaltung von rninvest.de die Adresse in `src/config/site.ts`, `src/lib/site-url.ts`, `src/routes/sitemap[.]xml.ts` und `public/robots.txt` anpassen.
8. **Veröffentlichung:** erst nach Freigabe.
