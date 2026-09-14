# -*- coding: utf-8 -*-
"""Baut aus den einzelnen HTML-Seiten eine klickbare Ein-Datei-Vorschau (v2 Redesign)."""
import re, os, base64, io

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
SRC = _os.path.join(_HERE, "website")
OUT = _os.path.join(_HERE, "farbklecks-vorschau-v2.html")

PAGES = [
    ("index",       "index",       "Kindergarten & Krippe Farbklecks Daxberg – Montessori in Mömbris",
     "Katholischer Kindergarten und Kinderkrippe Farbklecks in Mömbris-Daxberg: Betreuung ab 12 Monaten nach Montessori-Pädagogik. Zeiten, Anmeldung und Kontakt.", True),
    ("ueber-uns",    "ueber-uns",   "Über uns – Kindergarten & Krippe Farbklecks Daxberg",
     "Lernen Sie unsere Einrichtung kennen: Gruppenräume, Garten, unser Team, Träger, Elternbeirat und unsere Montessori-Pädagogik.", False),
    ("krippe",       "krippe",      "Krippe – Kindergarten & Krippe Farbklecks Daxberg",
     "Kinderkrippe für Kinder ab 12 Monaten: Öffnungszeiten, Gebühren, Konzept, Anmeldung und Alltag in der Krippe Farbklecks Daxberg.", False),
    ("kindergarten", "kindergarten","Kindergarten – Kindergarten & Krippe Farbklecks Daxberg",
     "Kindergarten für Kinder ab 3 Jahren: Öffnungszeiten, Gebühren, Wochenprogramm, Anmeldung und Alltag im Kindergarten Farbklecks Daxberg.", False),
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

def read(p):
    return io.open(os.path.join(SRC, p), encoding="utf-8").read()

css = read("assets/css/style.css")
js  = read("assets/js/main.js")

def data_uri(path, mime):
    raw = open(os.path.join(SRC, path), "rb").read()
    return "data:%s;base64,%s" % (mime, base64.b64encode(raw).decode("ascii"))

FONT_MIMES = {
    "assets/fonts/figtree-latin.woff2": "font/woff2",
    "assets/fonts/figtree-latin-ext.woff2": "font/woff2",
    "assets/fonts/pacifico-latin.woff2": "font/woff2",
    "assets/fonts/pacifico-latin-ext.woff2": "font/woff2",
}
IMG_MIMES = {
    "assets/img/logo.png": "image/png",
    "assets/img/blob-1.png": "image/png",
    "assets/img/blob-2.png": "image/png",
    "assets/img/hero-1.webp": "image/webp",
    "assets/img/hero-2.webp": "image/webp",
    "assets/img/hero-3.webp": "image/webp",
}

# Fonts + Bilder als Data-URI einbetten (externe Dateien gibt es im Artifact nicht)
for rel, mime in FONT_MIMES.items():
    uri = data_uri(rel, mime)
    css = css.replace('url("../%s")' % rel.split("assets/")[1], 'url("%s")' % uri)

img_uris = {rel: data_uri(rel, mime) for rel, mime in IMG_MIMES.items()}

full = read("index.html")

def between(text, start, end):
    i = text.index(start) + len(start)
    j = text.index(end, i)
    return text[i:j]

header_html = between(full, '<div class="topbar">', '<main id="inhalt">')
header_html = '<div class="topbar">' + header_html
footer_html = between(full, '</main>', '<script src="assets/js/main.js" defer></script>')

def fix_links(s):
    s = re.sub(r'href="index\.html"', 'href="#index"', s)
    s = re.sub(r'href="([a-z0-9\-]+)\.html(#[a-z0-9\-]+)?"',
                lambda m: 'href="#%s%s"' % (m.group(1), ("~" + m.group(2)[1:]) if m.group(2) else ""), s)
    for rel, uri in img_uris.items():
        s = s.replace('src="%s"' % rel, 'src="%s"' % uri)
    return s

header_html = fix_links(header_html)
footer_html = fix_links(footer_html)

sections = []
for slug, label, title, desc, jsonld in PAGES:
    page = read(slug + ".html")
    body = between(page, '<main id="inhalt">', '</main>')
    body = fix_links(body)
    sections.append(
        '<section class="pv-page" id="page-%s" data-page="%s"%s>\n%s\n</section>'
        % (slug, slug, "" if slug == "index" else " hidden", body)
    )

PREVIEW_CSS = """
/* ---------- Nur für diese Vorschau ---------- */
.pv-bar{
  position:fixed;inset:0 0 auto 0;z-index:200;
  background:#201e1d;color:#fff9f0;
  display:flex;flex-wrap:wrap;align-items:center;gap:.4rem 1rem;
  padding:.55rem clamp(.8rem,3vw,1.6rem);
  font-family:var(--font-body);font-size:.85rem;line-height:1.4;
}
.pv-bar strong{
  font-family:var(--font-body);letter-spacing:.1em;text-transform:uppercase;
  font-size:.72rem;background:#f27c7e;color:#59121a;
  padding:.2rem .6rem;border-radius:999px;font-weight:700;
}
.pv-bar span{opacity:.82}
.pv-bar .pv-hint{margin-left:auto;opacity:.6;font-size:.8rem}
body{padding-top:var(--pv-bar-h,44px)}
.header{top:var(--pv-bar-h,44px)}
.pv-page[hidden]{display:none}
@media (max-width:700px){ .pv-bar .pv-hint{display:none} }
"""

PREVIEW_JS = """
/* ---------- Seitenwechsel nur für diese Vorschau ---------- */
(function () {
  var bar = document.querySelector('.pv-bar');
  function barHeight() {
    document.documentElement.style.setProperty('--pv-bar-h', bar.offsetHeight + 'px');
  }
  barHeight();
  window.addEventListener('resize', barHeight);

  var pages = Array.prototype.slice.call(document.querySelectorAll('.pv-page'));

  function show(slug, anchor, scroll) {
    var found = false;
    pages.forEach(function (p) {
      var match = p.getAttribute('data-page') === slug;
      p.hidden = !match;
      if (match) {
        found = true;
        p.querySelectorAll('.reveal').forEach(function (el) {
          el.classList.remove('is-in');
          requestAnimationFrame(function () { el.classList.add('is-in'); });
        });
      }
    });
    if (!found) { show('404', null, scroll); return; }

    document.querySelectorAll('[data-nav]').forEach(function (a) {
      if (a.getAttribute('data-nav') === slug) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });

    var titles = %TITLES%;
    document.title = (titles[slug] || 'Vorschau') + ' – Farbklecks Daxberg';
    if (scroll) {
      if (anchor) {
        var target = document.getElementById(anchor);
        if (target) { requestAnimationFrame(function () { target.scrollIntoView({ behavior: 'auto', block: 'start' }); }); return; }
      }
      window.scrollTo({ top: 0, behavior: 'auto' });
    }
  }

  function current() {
    var h = (location.hash || '#index').replace('#', '');
    var parts = (h || 'index').split('~');
    return { slug: parts[0] || 'index', anchor: parts[1] || null };
  }

  window.addEventListener('hashchange', function () { var c = current(); show(c.slug, c.anchor, true); });
  (function () { var c = current(); show(c.slug, c.anchor, false); })();
})();
"""

titles = "{" + ", ".join('"%s": "%s"' % (s, l) for s, l, *_ in PAGES) + "}"
PREVIEW_JS = PREVIEW_JS.replace("%TITLES%", titles)

html = []
html.append('<title>Farbklecks Daxberg – Redesign v2</title>')
html.append('<style>\n' + css + PREVIEW_CSS + '\n</style>')
html.append('<div class="pv-bar">')
html.append('  <strong>Entwurf v2</strong>')
html.append('  <span>Redesign mit neuer Optik (warm &amp; organisch) für den Kindergarten Farbklecks Daxberg – '
            'nicht die offizielle Website. Inhalte teils Platzhalter.</span>')
html.append('  <span class="pv-hint">Alle Menüpunkte sind klickbar</span>')
html.append('</div>')
html.append('<a class="skip-link" href="#inhalt">Zum Inhalt springen</a>')
html.append(header_html)
html.append('<main id="inhalt">')
html.extend(sections)
html.append('</main>')
html.append(footer_html)
html.append('<script>\n' + js + '\n</script>')
html.append('<script>\n' + PREVIEW_JS + '\n</script>')

io.open(OUT, "w", encoding="utf-8").write("\n".join(html))
print("geschrieben:", OUT, os.path.getsize(OUT), "Bytes")
