# Kindergarten & Krippe Farbklecks Daxberg – Website

**Kunde:** Kath. Kindergarten „Farbklecks", Glasbergstraße 14, 63776 Mömbris-Daxberg
**Träger:** St.-Johannes-Verein e. V.
**Bisherige Seite:** https://www.kindergarten-farbklecks.de/ (WordPress, wird abgelöst)
**Repo:** `schaltwerkdigital-dev/farbklecks-website`

Dieses Projekt ist **eigenständig**. Es hat nichts mit den Shopify-Themes
(bySchultz B2B/B2C) oder anderen Kundenprojekten zu tun. Niemals Dateien,
Konventionen oder Git-Remotes aus anderen Projektordnern hierher übernehmen.

## Ziel

Umzug der bestehenden WordPress-Seite auf einen eigenen Server, verbunden mit
einem Redesign. Inhalte bleiben inhaltlich erhalten, werden aber neu und
übersichtlicher geordnet und mit echten, aktuellen Daten gepflegt.

## Design-Richtung

Warm, organisch, verspielt – bewusst weg vom klassischen „Kita-Blau".

| Rolle | Farbe | Variable |
|---|---|---|
| Hintergrund | Warmes Creme `#f5ead8` | `--bg` |
| Flächen/Karten | Sand `#ebddc5` | `--surface` |
| Text | Warmes Dunkelbraun `#4a3c36` | `--ink` |
| Akzent 1 | Terracotta `#c67139` | `--accent` |
| Akzent 2 | Olivgrün `#7a8a5e` | `--accent-2` |
| Handlungsfarbe (Buttons) | Koralle `#f27c7e` | `--cta` |

**Schriften** (selbst gehostet, `website/assets/fonts/`, kein Google-Fonts-CDN):
- `Pacifico` – Klasse `.display`, wird laut Kundenwunsch für **alle
  Überschriften (h1–h4)** sowie Zahlen-Fakten und Zitate verwendet.
- `Figtree` – Fließtext, Navigation, Formulare (Standard-`body`-Schrift).

Alle Komponenten (Buttons, Karten, Badges, Formulare …) ziehen ihre Farben
und Radien ausschließlich aus den Variablen in `website/assets/css/style.css`,
Abschnitt „01 Design Tokens". **Nie Farben oder Radien direkt in Komponenten
schreiben.**

Icon-Glyphen in `.card__icon`/`.download__icon` sind handgezeichnete Inline-
SVGs im Linienstil des Logos (dünne einheitliche Outlines in `--ink`, runde
Linienenden, dezente Flächenfarben aus der Palette) – **keine Emoji.**

## Stack

Statische Website – **HTML, CSS und JavaScript strikt getrennt**.
Kein CMS, kein Framework, keine externe Bibliothek, kein Build-Schritt zur
Laufzeit (der Python-Build erzeugt nur statische HTML-Dateien aus Templates).

```
farbklecks-website/
├── CLAUDE.md              Diese Datei
├── build.py               Baut pages/*.body.html + parts/*.tpl → website/*.html
├── make_preview2.py       Bündelt website/ zu einer einzigen Vorschau-HTML-Datei
├── parts/                 head.tpl, header.tpl, footer.tpl (auf allen Seiten identisch)
├── pages/                 *.body.html – der Seiteninhalt je Unterseite
├── source-fotos/          Original-Fotos/Logo/Blobs vor der Optimierung
└── website/               Fertiges, deploybares Ergebnis (das, was live geht)
    ├── index.html
    ├── unser-haus.html       Einrichtung, Räume, Team, Träger, Elternbeirat
    ├── paedagogik.html       Montessori-Konzept, Tagesablauf, Eingewöhnung
    ├── betreuung.html        Gruppen, Öffnungs-/Buchungszeiten, Gebühren, Ferien
    ├── anmeldung.html        Ablauf (zentrale Kitaplatzanmeldung), Downloads, FAQ
    ├── aktuelles.html        Termine und Berichte
    ├── kontakt.html          Kontaktdaten, Formular, Anfahrt
    ├── impressum.html        Vorlage – teils noch zu vervollständigen
    ├── datenschutz.html      Vorlage – teils noch zu vervollständigen
    ├── 404.html
    ├── robots.txt / sitemap.xml / .htaccess
    └── assets/
        ├── css/style.css     ein Stylesheet, nummerierte Abschnitte
        ├── js/main.js        ein Skript
        ├── fonts/            Pacifico + Figtree (woff2, latin + latin-ext)
        ├── img/               Logo, Fotos, Farbklecks-Dekoration
        └── downloads/         PDF-Dateien
```

**Wichtig:** `website/*.html` wird von `build.py` aus `parts/` + `pages/`
generiert – Änderungen an Kopf-/Fußbereich oder Seiteninhalt immer in
`parts/*.tpl` bzw. `pages/*.body.html` vornehmen und danach `python3
build.py` laufen lassen. Nie direkt in den generierten `website/*.html`-
Dateien editieren, die Änderung geht beim nächsten Build verloren.
`website/assets/css/style.css` und `website/assets/js/main.js` sind dagegen
die kanonischen, direkt editierten Quelldateien (kein Build-Schritt dafür).

## Arbeitsweise

- **Immer vollständige Dateien ausgeben**, nie Teil-Schnipsel.
- Kopf- und Fußbereich sind in allen Seiten identisch (`parts/header.tpl`,
  `parts/footer.tpl`). Änderungen dort betreffen automatisch alle Seiten.
- Alle Texte auf Deutsch, Ansprache der Eltern mit „Sie".
- Barrierefreiheit erhalten: Sprunglink, sichtbarer Fokus, sinnvolle
  Überschriftenreihenfolge, ARIA für Menü und Reiter, `prefers-reduced-motion`.
- Bei layoutrelevanten Änderungen (Abstände, Umbrüche, sticky-Verhalten)
  mit Playwright bei mehreren Viewport-Breiten verifizieren, nicht nur
  visuell vermuten.

## Feste Regeln (DSGVO)

Die Seite kommt bewusst ohne Dritt-Dienste aus. Das darf nicht aufgeweicht werden:

- Keine Google Fonts vom CDN – Schriften liegen selbst gehostet in
  `website/assets/fonts/` (siehe `@font-face` am Anfang von `style.css`).
- Keine Analyse- oder Tracking-Dienste, keine Cookies (außer einem
  Session-Storage-Flag für die Kartenanzeige-Einwilligung).
- Die Karte auf der Kontaktseite lädt erst nach aktivem Klick
  (Zwei-Klick-Lösung, OpenStreetMap).
- Fotos, auf denen Kinder erkennbar sind, nur mit schriftlicher Einwilligung
  der Erziehungsberechtigten veröffentlichen.

## Gesicherte Eckdaten

| | |
|---|---|
| Öffnungszeiten Kindergarten | Mo–Do 7:30–15:45 Uhr, Fr 7:30–13:30 Uhr |
| Öffnungszeiten Krippe | weicht ab – siehe `betreuung.html`, Abschnitt „Öffnungszeiten" |
| Kindergarten | eine Gruppe, 25 Plätze, ab 3 Jahren |
| Krippe | ab 12 Monaten, seit September 2022, **mittlerweile im neuen Anbau
  direkt am Standort Daxberg** (nicht mehr Niedersteinbach – dort war die
  Krippe nur zu Beginn untergebracht) |
| Pädagogik | nach Maria Montessori, „Hilf mir, es selbst zu tun" |
| Träger | St.-Johannes-Verein e. V. |
| Telefon | 06029 5616 |
| E-Mail | info@kindergarten-farbklecks.de |

Bei Änderungen an Öffnungszeiten/Kontaktdaten: Topbar (`parts/header.tpl`),
Footer (`parts/footer.tpl`), `index.html`- und `betreuung.html`-Inhalt sowie
`assets/js/main.js` (`OPENING_HOURS`) und das JSON-LD in `build.py`
konsistent halten.

## Offene Punkte

1. **Restliche Platzhalter-Fotos** ersetzen (Team, weitere Räume). Die
   ersten echten Fotos (Außenansicht, Eingang, Gruppenraum, Spielhaus,
   Montessori-Material) liegen als Chat-Anhänge vor und müssen noch nach
   `website/assets/img/` übernommen werden, sobald sie als Datei-Upload
   (z. B. über GitHub) statt als reiner Chat-Anhang verfügbar sind.
2. **Impressum und Datenschutz** vervollständigen (eckige Klammern:
   Registergericht/-nummer, Aufsichtsbehörde, Hosting-Anbieter,
   Bildnachweise) und rechtlich prüfen lassen.
3. **Kontaktformular** an ein Versandskript anbinden (`action`-Attribut in
   `kontakt.html` bzw. `pages/kontakt.body.html`).
4. **Alte URLs** erfassen und ggf. 301-Weiterleitungen in `.htaccess` ergänzen.
5. `paedagogik.html`, Abschnitt „Konzept der Krippe" → Räumlichkeiten:
   Beschreibung ist noch die alte (Niedersteinbach), muss an den neuen
   Anbau angepasst werden (im Code mit `todo-note` markiert).

Alle offenen Stellen sind im Code sichtbar markiert:

```bash
grep -rn "todo-note\|\[PLZ\|PLATZHALTER" website/
```

Vor dem Livegang müssen alle `todo-note`-Kästen entfernt sein.

## Vorschau

```bash
python3 build.py                # baut website/*.html aus pages/ + parts/
cd website && python3 -m http.server 8080   # http://localhost:8080

# Alternativ: eine einzelne, self-contained Vorschau-Datei (für Artifact-Vorschau)
python3 make_preview2.py        # schreibt farbklecks-vorschau-v2.html
```

## Umzug (Reihenfolge)

1. Inhalte und PDFs der alten Seite sichern (`/wp-content/uploads/`)
2. Alte URLs auflisten
3. Testadresse einrichten, dort `robots.txt` auf `Disallow: /`
4. Inhalte einpflegen und Korrektur lesen
5. Impressum/Datenschutz finalisieren
6. Domain umziehen (Auth-Code / DNS)
7. SSL aktivieren, HTTPS erzwingen
8. 301-Weiterleitungen scharf schalten
9. Livegang prüfen, `sitemap.xml` in der Search Console einreichen
10. Alte Seite abschalten, Sicherung aufbewahren
