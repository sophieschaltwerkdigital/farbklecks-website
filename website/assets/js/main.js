/* =========================================================
   Kindergarten & Krippe Farbklecks Daxberg
   main.js – Version 1.0

   Enthält:
   01 Mobile-Navigation
   02 Sticky-Header
   03 Scroll-Animationen (Reveal)
   04 "Nach oben"-Button
   05 Öffnungsstatus (geöffnet / geschlossen)
   06 Tabs (z. B. Kindergarten / Krippe)
   07 Karte mit Einwilligung (DSGVO, 2-Klick-Lösung)
   08 Kontaktformular (Validierung + Versand)
   09 Jahreszahl im Footer

   Es werden keine externen Bibliotheken benötigt.
   ========================================================= */

(function () {
  "use strict";

  var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- 01 Mobile-Navigation ---------------------- */
  function initNav() {
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.getElementById("hauptnavigation");
    if (!toggle || !nav) return;

    var backdrop = document.createElement("div");
    backdrop.className = "nav-backdrop";
    document.body.appendChild(backdrop);

    function open() {
      nav.classList.add("is-open");
      backdrop.classList.add("is-open");
      toggle.setAttribute("aria-expanded", "true");
      document.body.classList.add("is-locked");
      var first = nav.querySelector("a, button");
      if (first) first.focus();
    }

    function close(focusToggle) {
      nav.classList.remove("is-open");
      backdrop.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
      document.body.classList.remove("is-locked");
      if (focusToggle) toggle.focus();
    }

    toggle.addEventListener("click", function () {
      if (toggle.getAttribute("aria-expanded") === "true") close(false);
      else open();
    });

    backdrop.addEventListener("click", function () { close(false); });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) close(true);
    });

    // Beim Klick auf einen Link im Menü schließen
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) close(false);
    });

    // Beim Wechsel auf Desktop-Breite zurücksetzen
    window.addEventListener("resize", function () {
      if (window.innerWidth > 860 && nav.classList.contains("is-open")) close(false);
    });
  }

  /* ---------- 02 Sticky-Header -------------------------- */
  function initStickyHeader() {
    var header = document.querySelector(".header");
    if (!header) return;
    var onScroll = function () {
      header.classList.toggle("is-stuck", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------- 03 Scroll-Animationen --------------------- */
  function initReveal() {
    var items = document.querySelectorAll(".reveal");
    if (!items.length) return;

    if (reducedMotion || !("IntersectionObserver" in window)) {
      items.forEach(function (el) { el.classList.add("is-in"); });
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });

    items.forEach(function (el) { io.observe(el); });
  }

  /* ---------- 04 "Nach oben"-Button --------------------- */
  function initToTop() {
    var btn = document.querySelector(".to-top");
    if (!btn) return;
    var onScroll = function () {
      btn.classList.toggle("is-visible", window.scrollY > 600);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    btn.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: reducedMotion ? "auto" : "smooth" });
    });
  }

  /* ---------- 05 Öffnungsstatus ------------------------- */
  /* Öffnungszeiten zentral pflegen: 0 = Sonntag ... 6 = Samstag
     Format: [Start, Ende] in Minuten seit Mitternacht, null = geschlossen */
  var OPENING_HOURS = {
    1: [450, 945],  // Montag    07:30 - 15:45
    2: [450, 945],  // Dienstag
    3: [450, 945],  // Mittwoch
    4: [450, 945],  // Donnerstag
    5: [450, 810],  // Freitag   07:30 - 13:30
    6: null,        // Samstag
    0: null         // Sonntag
  };

  function initOpeningStatus() {
    var pill = document.querySelector("[data-opening-status]");
    var rows = document.querySelectorAll("[data-weekday]");

    var now = new Date();
    var day = now.getDay();
    var minutes = now.getHours() * 60 + now.getMinutes();

    rows.forEach(function (row) {
      if (parseInt(row.getAttribute("data-weekday"), 10) === day) {
        row.classList.add("is-today");
      }
    });

    if (!pill) return;
    var today = OPENING_HOURS[day];
    var isOpen = !!today && minutes >= today[0] && minutes < today[1];

    pill.classList.add(isOpen ? "status-pill--open" : "status-pill--closed");
    pill.innerHTML =
      '<span class="dot" aria-hidden="true"></span>' +
      (isOpen ? "Jetzt geöffnet" : "Aktuell geschlossen");
  }

  /* ---------- 06 Tabs ----------------------------------- */
  function initTabs() {
    document.querySelectorAll("[data-tabs]").forEach(function (root) {
      var buttons = Array.prototype.slice.call(root.querySelectorAll(".tabs__btn"));
      var panels = Array.prototype.slice.call(root.querySelectorAll(".tabs__panel"));
      if (!buttons.length) return;

      function activate(index, setFocus) {
        buttons.forEach(function (btn, i) {
          btn.setAttribute("aria-selected", i === index ? "true" : "false");
          btn.setAttribute("tabindex", i === index ? "0" : "-1");
        });
        panels.forEach(function (panel, i) { panel.hidden = i !== index; });
        if (setFocus) buttons[index].focus();
      }

      buttons.forEach(function (btn, i) {
        btn.addEventListener("click", function () { activate(i, false); });
        btn.addEventListener("keydown", function (e) {
          var next = null;
          if (e.key === "ArrowRight") next = (i + 1) % buttons.length;
          if (e.key === "ArrowLeft") next = (i - 1 + buttons.length) % buttons.length;
          if (e.key === "Home") next = 0;
          if (e.key === "End") next = buttons.length - 1;
          if (next !== null) { e.preventDefault(); activate(next, true); }
        });
      });

      activate(0, false);
    });
  }

  /* ---------- 07 Karte mit Einwilligung ----------------- */
  /* Die Karte wird erst nach aktivem Klick geladen. Vorher wird
     keine Verbindung zu einem externen Server aufgebaut (DSGVO). */
  function initMapConsent() {
    var box = document.querySelector("[data-map-consent]");
    if (!box) return;
    var btn = box.querySelector("[data-map-load]");
    if (!btn) return;

    btn.addEventListener("click", function () {
      var src = box.getAttribute("data-map-src");
      var iframe = document.createElement("iframe");
      iframe.src = src;
      iframe.title = "Karte mit dem Standort des Kindergartens Farbklecks";
      iframe.loading = "lazy";
      iframe.setAttribute("referrerpolicy", "no-referrer");
      box.innerHTML = "";
      box.classList.add("is-loaded");
      box.appendChild(iframe);
      try { sessionStorage.setItem("fk-map-consent", "1"); } catch (err) { /* egal */ }
    });

    // Innerhalb derselben Sitzung nicht erneut fragen
    try {
      if (sessionStorage.getItem("fk-map-consent") === "1") btn.click();
    } catch (err) { /* egal */ }
  }

  /* ---------- 08 Kontaktformular ------------------------ */
  function initContactForm() {
    var form = document.querySelector("[data-contact-form]");
    if (!form) return;

    var status = form.querySelector(".form__status");

    function setError(field, message) {
      var wrap = field.closest(".field");
      if (!wrap) return;
      wrap.classList.add("field--error");
      var msg = wrap.querySelector(".field__error");
      if (!msg) {
        msg = document.createElement("p");
        msg.className = "field__error";
        wrap.appendChild(msg);
      }
      msg.textContent = message;
      field.setAttribute("aria-invalid", "true");
    }

    function clearError(field) {
      var wrap = field.closest(".field");
      if (!wrap) return;
      wrap.classList.remove("field--error");
      var msg = wrap.querySelector(".field__error");
      if (msg) msg.remove();
      field.removeAttribute("aria-invalid");
    }

    form.querySelectorAll("input, textarea").forEach(function (field) {
      field.addEventListener("input", function () { clearError(field); });
    });

    function showStatus(type, text) {
      if (!status) return;
      status.className = "form__status is-visible form__status--" + type;
      status.textContent = text;
      status.setAttribute("role", "status");
    }

    form.addEventListener("submit", function (e) {
      var valid = true;
      var firstInvalid = null;

      form.querySelectorAll("[required]").forEach(function (field) {
        var value = (field.value || "").trim();
        var ok = field.type === "checkbox" ? field.checked : value !== "";

        if (ok && field.type === "email") {
          ok = /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(value);
        }

        if (!ok) {
          valid = false;
          setError(field, field.type === "checkbox"
            ? "Bitte bestätigen Sie diesen Punkt."
            : "Bitte füllen Sie dieses Feld korrekt aus.");
          if (!firstInvalid) firstInvalid = field;
        } else {
          clearError(field);
        }
      });

      // Spam-Falle: unsichtbares Feld muss leer bleiben
      var honey = form.querySelector(".hp input");
      if (honey && honey.value !== "") {
        e.preventDefault();
        return;
      }

      if (!valid) {
        e.preventDefault();
        showStatus("err", "Bitte prüfen Sie die markierten Felder.");
        if (firstInvalid) firstInvalid.focus();
        return;
      }

      // Solange kein Versand-Skript auf dem Server hinterlegt ist,
      // wird das Formular nicht abgeschickt, sondern ein Hinweis gezeigt.
      if (!form.getAttribute("action")) {
        e.preventDefault();
        showStatus("ok", "Vielen Dank! Ihre Nachricht wurde geprüft. " +
          "Hinweis für die Redaktion: Es ist noch kein Versandziel (action) hinterlegt.");
      }
    });
  }

  /* ---------- 09 Jahreszahl im Footer ------------------- */
  function initYear() {
    document.querySelectorAll("[data-year]").forEach(function (el) {
      el.textContent = new Date().getFullYear();
    });
  }

  /* ---------- Start ------------------------------------- */
  function init() {
    initNav();
    initStickyHeader();
    initReveal();
    initToTop();
    initOpeningStatus();
    initTabs();
    initMapConsent();
    initContactForm();
    initYear();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
