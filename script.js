/* =========================================================
   ARTEZE — script.js
   1. Analytics settings (edit here)
   2. Cookie consent
   3. Navigation
   4. Motion (smooth scroll, reveals, hero tilt, counters)
   5. Services filter
   6. Booking form (mailto)
   ========================================================= */

/* ---------- 1. Analytics settings ----------
   Nothing loads until a visitor accepts cookies.
   Leave both blank to run with essential cookies only. */
var ANALYTICS = {
  ga4Id: "",            // e.g. "G-XXXXXXXXXX"
  plausibleDomain: ""   // e.g. "arteze.co.uk"
};
var FORM_EMAIL = "hello@arteze.co.uk";
var CONSENT_KEY = "arteze-cookie-consent";

(function () {
  "use strict";
  var doc = document;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- 2. Cookie consent ---------- */
  function getConsent() {
    try { return localStorage.getItem(CONSENT_KEY); } catch (e) { return null; }
  }
  function setConsent(value) {
    try { localStorage.setItem(CONSENT_KEY, value); } catch (e) {}
  }
  function loadAnalytics() {
    if (ANALYTICS.ga4Id && !window.__gaLoaded) {
      window.__gaLoaded = true;
      var s = doc.createElement("script");
      s.async = true;
      s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(ANALYTICS.ga4Id);
      doc.head.appendChild(s);
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () { window.dataLayer.push(arguments); };
      window.gtag("js", new Date());
      window.gtag("config", ANALYTICS.ga4Id, { anonymize_ip: true });
    }
    if (ANALYTICS.plausibleDomain && !window.__plLoaded) {
      window.__plLoaded = true;
      var p = doc.createElement("script");
      p.defer = true;
      p.setAttribute("data-domain", ANALYTICS.plausibleDomain);
      p.src = "https://plausible.io/js/script.js";
      doc.head.appendChild(p);
    }
  }
  function initCookies() {
    var banner = doc.getElementById("cookie-banner");
    var consent = getConsent();
    if (consent === "accepted") loadAnalytics();
    if (!banner) return;
    if (!ANALYTICS.ga4Id && !ANALYTICS.plausibleDomain) return;
    if (!consent) banner.hidden = false;
    banner.addEventListener("click", function (e) {
      var btn = e.target.closest("[data-consent]");
      if (!btn) return;
      var choice = btn.getAttribute("data-consent");
      setConsent(choice);
      banner.hidden = true;
      if (choice === "accepted") loadAnalytics();
      else if (window.__gaLoaded || window.__plLoaded) window.location.reload();
    });
    doc.querySelectorAll("[data-cookie-settings]").forEach(function (el) {
      el.addEventListener("click", function () {
        banner.hidden = false;
        var first = banner.querySelector("button");
        if (first) first.focus();
      });
    });
  }

  /* ---------- 3. Navigation ---------- */
  function initNav() {
    var header = doc.querySelector(".site-header");
    var toggle = doc.querySelector(".menu-toggle");
    var mobile = doc.getElementById("mobile-nav");
    if (toggle && mobile) {
      var setOpen = function (open) {
        doc.body.classList.toggle("menu-open", open);
        toggle.setAttribute("aria-expanded", String(open));
        toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      };
      toggle.addEventListener("click", function () {
        setOpen(toggle.getAttribute("aria-expanded") !== "true");
      });
      doc.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && doc.body.classList.contains("menu-open")) { setOpen(false); toggle.focus(); }
      });
      mobile.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", function () { setOpen(false); }); });
    }
    if (header) {
      var onScroll = function () { header.classList.toggle("is-scrolled", window.scrollY > 8); };
      onScroll();
      window.addEventListener("scroll", onScroll, { passive: true });
    }
  }

  /* ---------- 4. Motion ---------- */
  function initSmoothScroll() {
    if (reduceMotion || typeof window.Lenis !== "function") return;
    var lenis = new window.Lenis({ duration: 1.15, easing: function (t) { return Math.min(1, 1.001 - Math.pow(2, -10 * t)); } });
    function raf(time) { lenis.raf(time); requestAnimationFrame(raf); }
    requestAnimationFrame(raf);
    doc.querySelectorAll('a[href^="#"]').forEach(function (a) {
      a.addEventListener("click", function (e) {
        var id = a.getAttribute("href");
        if (id.length < 2) return;
        var target = doc.querySelector(id);
        if (!target) return;
        e.preventDefault();
        lenis.scrollTo(target, { offset: -90 });
        target.setAttribute("tabindex", "-1");
        target.focus({ preventScroll: true });
      });
    });
  }

  function countUp(el) {
    var end = parseFloat(el.getAttribute("data-count"));
    if (isNaN(end) || reduceMotion) return;
    var start = null, dur = 1600;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(step);
    }
    el.textContent = "0";
    requestAnimationFrame(step);
  }

  function initReveal() {
    var items = doc.querySelectorAll("[data-reveal], [data-count], .steps, .ladder, .leak-chart");
    if (!("IntersectionObserver" in window) || reduceMotion) {
      items.forEach(function (el) { el.classList.add("is-in"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        el.classList.add("is-in");
        if (el.hasAttribute("data-count")) countUp(el);
        io.unobserve(el);
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
    items.forEach(function (el) { io.observe(el); });
  }

  function initHeroTilt() {
    var visual = doc.querySelector(".hero-visual");
    var stage = doc.querySelector(".hero-stage");
    if (!visual || !stage || reduceMotion) return;
    var scrollY = 0, rx = 0, ry = 0;
    function apply() {
      stage.style.transform = "translate3d(0," + (scrollY * 0.12).toFixed(1) + "px,0) rotateX(" + rx.toFixed(2) + "deg) rotateY(" + ry.toFixed(2) + "deg)";
    }
    if (window.matchMedia("(hover: hover)").matches) {
      window.addEventListener("pointermove", function (e) {
        var r = visual.getBoundingClientRect();
        var x = (e.clientX - (r.left + r.width / 2)) / window.innerWidth;
        var y = (e.clientY - (r.top + r.height / 2)) / window.innerHeight;
        ry = x * 18; rx = -y * 14;
        apply();
      }, { passive: true });
    }
    window.addEventListener("scroll", function () {
      if (window.scrollY > window.innerHeight * 1.2) return;
      scrollY = window.scrollY;
      apply();
    }, { passive: true });
  }

  /* ---------- 5. Services filter ---------- */
  function initFilters() {
    var bar = doc.querySelector("[data-filters]");
    if (!bar) return;
    var groups = doc.querySelectorAll("[data-area]");
    var status = doc.getElementById("filter-status");
    bar.hidden = false;
    bar.addEventListener("click", function (e) {
      var btn = e.target.closest("button[data-filter]");
      if (!btn) return;
      var area = btn.getAttribute("data-filter");
      bar.querySelectorAll("button").forEach(function (b) { b.setAttribute("aria-pressed", String(b === btn)); });
      var shown = 0;
      groups.forEach(function (g) {
        var match = area === "all" || g.getAttribute("data-area") === area;
        g.hidden = !match;
        if (match) {
          shown += g.querySelectorAll(".svc").length;
          g.querySelectorAll("[data-reveal]").forEach(function (el) { el.classList.add("is-in"); });
        }
      });
      if (status) status.textContent = "Showing " + shown + (shown === 1 ? " service" : " services") + (area === "all" ? "" : " in " + btn.textContent.trim());
    });
  }

  /* ---------- 6. Booking form ---------- */
  function initForms() {
    doc.querySelectorAll("form[data-booking]").forEach(function (form) {
      form.setAttribute("novalidate", "");
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        if (!validate(form)) return;
        var v = function (name) {
          var el = form.elements[name];
          if (!el) return "";
          return (el.value || "").trim();
        };
        var subject = "Free Contract Value Check request: " + v("company");
        var lines = [
          "Name: " + v("name"),
          "Work email: " + v("email"),
          "Company: " + v("company"),
          "Role: " + v("role"),
          "Annual IT and services spend: " + v("spend"),
          "Organisation type: " + v("orgType"),
          "Contract to check: " + (v("contract") || "Not specified"),
          "Renewal or notice date: " + (v("renewal") || "Not specified"),
          "",
          "Message:",
          v("message"),
          "",
          "GDPR consent: Given (" + new Date().toLocaleDateString("en-GB") + ")",
          "Sent from: " + window.location.href
        ];
        var href = "mailto:" + FORM_EMAIL + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(lines.join("\r\n"));
        window.location.href = href;
        var success = form.parentNode.querySelector(".form-success");
        if (success) {
          form.hidden = true;
          success.hidden = false;
          success.setAttribute("tabindex", "-1");
          success.focus();
        }
      });
    });
  }

  function validate(form) {
    var firstBad = null;
    form.querySelectorAll("[data-required]").forEach(function (el) {
      var msg = "";
      var name = el.getAttribute("name");
      var err = doc.getElementById(name + "-error");
      if (el.type === "checkbox") {
        if (!el.checked) msg = "Please tick to confirm you agree.";
      } else if (el.type === "radio") {
        if (!form.querySelector('input[name="' + name + '"]:checked')) msg = "Please choose an option.";
      } else if (!el.value.trim()) {
        msg = "Please complete this field.";
      } else if (el.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(el.value.trim())) {
        msg = "Please enter a valid email address, like name@company.co.uk.";
      }
      if (el.type === "radio") {
        form.querySelectorAll('input[name="' + name + '"]').forEach(function (r) { r.setAttribute("aria-invalid", msg ? "true" : "false"); });
      } else {
        el.setAttribute("aria-invalid", msg ? "true" : "false");
      }
      if (err) err.textContent = msg;
      if (msg && !firstBad) firstBad = el;
    });
    if (firstBad) firstBad.focus();
    return !firstBad;
  }

  /* ---------- Init ---------- */
  function init() {
    initCookies();
    initNav();
    initSmoothScroll();
    initReveal();
    initHeroTilt();
    initFilters();
    initForms();
    var y = doc.querySelectorAll("[data-year]");
    y.forEach(function (el) { el.textContent = new Date().getFullYear(); });
  }
  if (doc.readyState === "loading") doc.addEventListener("DOMContentLoaded", init);
  else init();
})();
