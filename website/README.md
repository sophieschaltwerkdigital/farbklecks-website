# Kindergarten & Krippe Farbklecks Daxberg – neue Website

Statische Website (HTML, CSS, JavaScript – sauber getrennt), die die bisherige
WordPress-Seite unter <https://www.kindergarten-farbklecks.de/> ablösen soll.

Keine Datenbank, kein CMS, keine externen Dienste – dadurch schnell, sicher,
günstig im Betrieb und von Haus aus DSGVO-freundlich.

**Design v2:** warme, organische Optik (Creme/Terracotta/Olivgrün/Koralle),
Handschrift „Pacifico" sparsam für Hero-Aussagen und Zahlen, „Figtree" für
den Fließtext – beide selbst gehostet in `assets/fonts/`. Details und
Design-Tokens siehe `CLAUDE.md` im übergeordneten Projektordner.

---

## 1. Aufbau des Projekts

```
farbklecks-website/
├── index.html            Startseite
├── unser-haus.html       Einrichtung, Räume, Team, Träger, Elternbeirat
├── paedagogik.html       Montessori-Konzept, Tagesablauf, Eingewöhnung
├── betreuung.html        Gruppen, Öffnungs-/Buchungszeiten, Gebühren, Ferien
├── anmeldung.html        Ablauf der Anmeldung, Downloads, FAQ
├── aktuelles.html        Termine und Berichte
├── kontakt.html          Kontaktdaten, Formular, Anfahrt (Karte)
├── impressum.html        Pflichtangaben (Vorlage)
├── datenschutz.html      Datenschutzerklärung (Vorlage)
├── 404.html              Fehlerseite
├── robots.txt            Hinweise für Suchmaschinen
├── sitemap.xml           Seitenverzeichnis für Suchmaschinen
├── .htaccess             Server-Einstellungen und Weiterleitungen (nur Apache)
└── assets/
    ├── css/style.css     komplettes Design, in 12 Abschnitte gegliedert
    ├── js/main.js        alle Funktionen, ohne fremde Bibliotheken
    ├── img/              Logo, Favicon, Fotos  (siehe img/README.md)
    └── downloads/        PDF-Dateien           (siehe downloads/README.md)
```

Jede Seite ist eine eigenständige HTML-Datei. Kopf- und Fußbereich sind auf
allen Seiten identisch aufgebaut – wird dort etwas geändert (z. B. ein neuer
Menüpunkt), muss die Änderung in allen HTML-Dateien vorgenommen werden.

---

## 2. Die neue Struktur im Vergleich

Die Inhalte der alten Seite bleiben erhalten, sind aber neu gebündelt:
statt vieler kleiner Einzelseiten gibt es sieben klare Themenbereiche.

| Neue Seite | Enthält bisherige Inhalte zu |
|---|---|
| Start | Begrüßung, Kurzvorstellung, Öffnungszeiten, aktuelle Hinweise |
| Unser Haus | Einrichtung, Räume, Team, Träger, Elternbeirat |
| Pädagogik | Konzept/Montessori, Tagesablauf, Eingewöhnung |
| Betreuung & Zeiten | Öffnungs- und Buchungszeiten, Gebühren, Essen, Ferien |
| Anmeldung | Anmeldeablauf, Formulare, häufige Fragen |
| Aktuelles | Termine, Feste, Berichte |
| Kontakt | Adresse, Telefon, E-Mail, Formular, Anfahrt |

---

## 3. Was noch eingetragen werden muss

Alle offenen Stellen sind im Code sichtbar markiert:

* **Gelb hinterlegte Kästen** auf den Seiten („Hinweis für die Redaktion“) –
  im HTML als `<p class="todo-note">`. Diese Kästen vor dem Livegang löschen.
* **Platzhalter-Bilder** – Blöcke mit `media-frame--placeholder`. Sobald ein
  Foto vorliegt, den Block durch das auskommentierte `<img …>` ersetzen.
* **Eckige Klammern** in Impressum und Datenschutz, z. B. `[PLZ Ort]`.
* **Logo** – `assets/img/logo.png` stammt aus dem Claude-Design-Entwurf.
  Bitte bestätigen, dass es die aktuelle Version ist, im Idealfall als
  Vektordatei (SVG) nachreichen (Dateiname beibehalten, dann ist keine
  Code-Änderung nötig).

Offene Stellen im Projekt finden:

```bash
grep -rn "todo-note\|\[PLZ\|PLATZHALTER" .
```

---

## 4. Inhalte pflegen – die häufigsten Fälle

**Text ändern:** HTML-Datei in einem Editor öffnen, Text zwischen den
spitzen Klammern anpassen, speichern, hochladen.

**Neuen Beitrag unter „Aktuelles“ anlegen:** In `aktuelles.html` einen
bestehenden `<article class="card">…</article>`-Block kopieren und den Inhalt
ersetzen. Neueste Beiträge nach oben.

**Neuen Termin anlegen:** In `aktuelles.html` in der Liste `<ul class="dates">`
ein `<li>`-Element kopieren und Datum sowie Titel anpassen.

**Öffnungszeiten ändern:** Die Zeiten stehen an drei Stellen:
`index.html`, `betreuung.html` (Tabellen) und im Kopf-/Fußbereich jeder Seite.
Zusätzlich in `assets/js/main.js` im Abschnitt `OPENING_HOURS` – daraus wird
die Anzeige „Jetzt geöffnet / Aktuell geschlossen“ berechnet.

**Farben ändern:** Ganz oben in `assets/css/style.css` im Abschnitt
„01 Design Tokens“. Eine Farbe dort geändert – die ganze Seite passt sich an.

---

## 5. Vorschau auf dem eigenen Rechner

Die Dateien können per Doppelklick auf `index.html` im Browser geöffnet werden.
Realistischer ist eine kleine lokale Vorschau:

```bash
cd farbklecks-website
python3 -m http.server 8080
# dann im Browser: http://localhost:8080
```

---

## 6. Umzug auf den eigenen Server – Ablauf

1. **Inhalte sichern:** Alle Texte, Bilder und PDFs der alten Seite speichern.
   PDFs liegen dort unter `/wp-content/uploads/`.
2. **Alte Adressen notieren:** Liste aller bisherigen Seiten-URLs anlegen –
   sie wird für die Weiterleitungen gebraucht (Abschnitt 3 der `.htaccess`).
3. **Testadresse einrichten:** Die neue Seite zuerst unter einer Unteradresse
   (z. B. `neu.kindergarten-farbklecks.de`) hochladen und in Ruhe prüfen.
   In `robots.txt` dort vorübergehend `Disallow: /` eintragen, damit die
   Testseite nicht bei Google landet.
4. **Inhalte einpflegen** (Abschnitt 3) und gemeinsam Korrektur lesen.
5. **Impressum und Datenschutz** vervollständigen und rechtlich prüfen lassen.
6. **Domain umziehen:** Beim bisherigen Anbieter den Auth-Code anfordern, die
   Domain zum neuen Anbieter übertragen bzw. die DNS-Einträge (A/AAAA-Record)
   auf den neuen Server umstellen.
7. **SSL-Zertifikat** aktivieren (bei den meisten Hostern kostenlos über
   Let's Encrypt) und HTTPS erzwingen – siehe `.htaccess`.
8. **Weiterleitungen scharf schalten:** Die 301-Weiterleitungen von alten auf
   neue Adressen aktivieren, damit Google-Treffer und Lesezeichen weiter
   funktionieren.
9. **Livegang prüfen:** Alle Seiten aufrufen, Formular testen, Ansicht auf
   dem Handy kontrollieren, `sitemap.xml` in der Google Search Console
   einreichen.
10. **Alte Seite abschalten** – erst dann, wenn alles läuft. Eine Sicherung
    der WordPress-Installation aufbewahren.

---

## 7. Kontaktformular scharf schalten

Das Formular auf `kontakt.html` prüft die Eingaben bereits im Browser,
versendet aber noch nichts. Für den Versand gibt es zwei Wege:

**a) PHP auf dem eigenen Server** (üblich bei Standard-Hosting):
Ein kleines Skript `kontakt.php` anlegen und im Formular ergänzen:

```html
<form class="form" data-contact-form action="kontakt.php" method="post" novalidate>
```

**b) Dienst des Hosters** oder ein Formulardienst – dann dessen Adresse
in `action` eintragen.

Wichtig: Im Skript die Eingaben prüfen (Absender-Adresse nicht ungeprüft in
den Mail-Header übernehmen) und das versteckte Feld `website` auswerten –
ist es ausgefüllt, handelt es sich um Spam.

Solange kein `action` hinterlegt ist, zeigt das Formular nach dem Absenden
einen Hinweis an.

---

## 8. Technische Eckdaten

* Keine externen Schriftarten, keine Tracking-Dienste, keine Cookies.
* Die Karte auf der Kontaktseite wird erst nach aktivem Klick geladen
  (Zwei-Klick-Lösung).
* Barrierefreiheit: Sprunglink, sichtbarer Tastaturfokus, sinnvolle
  Überschriftenstruktur, ARIA-Auszeichnung für Menü und Reiter,
  Rücksicht auf `prefers-reduced-motion`.
* Vollständig responsiv ab ca. 320 px Bildschirmbreite.
* Getestet in aktuellen Versionen von Chrome, Firefox, Safari und Edge.
