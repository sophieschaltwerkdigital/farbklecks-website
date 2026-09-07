import os, re, io

SP = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SP, "website")

head = open(os.path.join(SP, "parts/head.tpl"), encoding="utf-8").read()
header = open(os.path.join(SP, "parts/header.tpl"), encoding="utf-8").read()
footer = open(os.path.join(SP, "parts/footer.tpl"), encoding="utf-8").read()

JSONLD = """
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Preschool",
    "name": "Kindergarten & Krippe Farbklecks Daxberg",
    "url": "https://www.kindergarten-farbklecks.de/",
    "logo": "https://www.kindergarten-farbklecks.de/assets/img/logo.png",
    "telephone": "+49 6029 5616",
    "email": "info@kindergarten-farbklecks.de",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "Glasbergstra\\u00dfe 14",
      "postalCode": "63776",
      "addressLocality": "M\\u00f6mbris-Daxberg",
      "addressRegion": "Bayern",
      "addressCountry": "DE"
    },
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday"],
        "opens": "07:30", "closes": "15:45" },
      { "@type": "OpeningHoursSpecification",
        "dayOfWeek": "Friday", "opens": "07:30", "closes": "13:30" }
    ]
  }
  </script>
"""

PAGES = [
    ("index",        "index",       "Kindergarten & Krippe Farbklecks Daxberg – Montessori in Mömbris",
     "Katholischer Kindergarten und Kinderkrippe Farbklecks in Mömbris-Daxberg: Betreuung ab 12 Monaten nach Montessori-Pädagogik. Zeiten, Anmeldung und Kontakt.", True),
    ("unser-haus",   "unser-haus",  "Unser Kindergarten – Kindergarten & Krippe Farbklecks Daxberg",
     "Lernen Sie unsere Einrichtung kennen: Gruppenräume, Garten, Krippe in Niedersteinbach, unser Team, Träger und Elternbeirat.", False),
    ("paedagogik",   "paedagogik",  "Pädagogik & Tagesablauf – Farbklecks Daxberg",
     "Wir arbeiten nach Maria Montessori: vorbereitete Umgebung, Freiarbeit, demokratische Erziehung. Dazu der Tagesablauf in Kindergarten und Krippe.", False),
    ("betreuung",    "betreuung",   "Betreuung, Zeiten & Gebühren – Farbklecks Daxberg",
     "Öffnungszeiten, Buchungszeiten, Gebühren, Mittagessen und Ferien im Kindergarten und in der Krippe Farbklecks in Mömbris-Daxberg.", False),
    ("anmeldung",    "anmeldung",   "Anmeldung – Kindergarten & Krippe Farbklecks Daxberg",
     "In vier Schritten zum Betreuungsplatz: Ablauf der Anmeldung, Formulare zum Herunterladen und Antworten auf häufige Fragen.", False),
    ("aktuelles",    "aktuelles",   "Aktuelles & Termine – Farbklecks Daxberg",
     "Neuigkeiten, Feste, Ferienzeiten und Schließtage im Kindergarten und in der Krippe Farbklecks Daxberg.", False),
    ("kontakt",      "kontakt",     "Kontakt & Anfahrt – Farbklecks Daxberg",
     "Kindergarten Farbklecks, Glasbergstraße 14, 63776 Mömbris-Daxberg. Telefon 06029 5616. Kontaktformular und Anfahrt.", True),
    ("impressum",    "",            "Impressum – Kindergarten Farbklecks Daxberg",
     "Impressum und Anbieterkennzeichnung des Kindergartens Farbklecks in Mömbris-Daxberg.", False),
    ("datenschutz",  "",            "Datenschutzerklärung – Kindergarten Farbklecks Daxberg",
     "Informationen zur Verarbeitung personenbezogener Daten auf der Website des Kindergartens Farbklecks Daxberg.", False),
    ("404",          "",            "Seite nicht gefunden – Kindergarten Farbklecks Daxberg",
     "Die aufgerufene Seite existiert nicht.", False),
]

for slug, active, title, desc, jsonld in PAGES:
    body = open(os.path.join(SP, "pages/%s.body.html" % slug), encoding="utf-8").read()

    h = head.replace("{{TITLE}}", title).replace("{{DESC}}", desc)
    h = h.replace("{{FILE}}", "" if slug == "index" else slug + ".html")
    if jsonld:
        h = h.replace("</head>", JSONLD + "</head>")
    if slug == "404":
        h = h.replace('<meta name="robots" content="index, follow">',
                      '<meta name="robots" content="noindex, follow">')
    if slug in ("impressum", "datenschutz"):
        h = h.replace('<meta name="robots" content="index, follow">',
                      '<meta name="robots" content="noindex, follow">')

    hd = header
    if active:
        hd = hd.replace('data-nav="%s" href=' % active,
                        'data-nav="%s" aria-current="page" href=' % active)

    html = h + hd + body + footer
    path = os.path.join(OUT, slug + ".html")
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("geschrieben:", path, len(html), "Zeichen")
