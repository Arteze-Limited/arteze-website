/* =========================================================
   ARTEZE — script.js
   1. Settings   2. Cookie banner + analytics loader
   3. Navigation 4. Reveal on scroll   5. Contact form (mailto)
   ========================================================= */

/* 1. SETTINGS -------------------------------------------------
   Analytics stays OFF until one of these is filled in.
   The cookie banner only appears once analytics is configured. */
var ANALYTICS = {
  ga4Id: "",            // e.g. "G-XXXXXXXXXX"
  plausibleDomain: ""   // e.g. "arteze.co.uk"
};
var FORM_EMAIL = "hello@arteze.co.uk";

(function () {
  "use strict";
  var doc = document;
  var KEY = "arteze-cookie-consent";
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* 2. COOKIES ------------------------------------------------ */
  function getConsent() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function setConsent(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
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
    var banner = doc.querySelector(".cookie-banner");
    var consent = getConsent();
    if (consent === "accepted") loadAnalytics();
    if (!banner || (!ANALYTICS.ga4Id && !ANALYTICS.plausibleDomain)) return;
    if (!consent) banner.classList.add("is-visible");
    banner.addEventListener("click", function (e) {
      var choice = e.target.getAttribute("data-consent");
      if (!choice) return;
      setConsent(choice);
      banner.classList.remove("is-visible");
      if (choice === "accepted") loadAnalytics();
    });
    doc.querySelectorAll("[data-cookie-settings]").forEach(function (el) {
      el.addEventListener("click", function () { banner.classList.add("is-visible"); });
    });
  }

  /* 3. NAVIGATION -------------------------------------------- */
  function initNav() {
    var header = doc.querySelector(".site-header");
    var toggle = doc.querySelector(".menu-toggle");
    var mobile = doc.getElementById("mobile-nav");
    if (toggle && mobile) {
      var setOpen = function (open) {
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
        mobile.classList.toggle("is-open", open);
        doc.body.classList.toggle("menu-open", open);
      };
      toggle.addEventListener("click", function () { setOpen(toggle.getAttribute("aria-expanded") !== "true"); });
      doc.addEventListener("keydown", function (e) { if (e.key === "Escape") setOpen(false); });
      mobile.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", function () { setOpen(false); }); });
    }
    if (header) {
      var onScroll = function () { header.classList.toggle("is-scrolled", window.scrollY > 8); };
      onScroll();
      window.addEventListener("scroll", onScroll, { passive: true });
    }
  }

  /* 4. REVEAL ------------------------------------------------- */
  function initReveal() {
    var items = doc.querySelectorAll(".reveal");
    if (reduceMotion || !("IntersectionObserver" in window)) {
      items.forEach(function (el) { el.classList.add("is-in"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add("is-in"); io.unobserve(entry.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  }

  /* 5. CONTACT FORM ------------------------------------------
     No server. Opens the visitor's email app with the details filled in. */
  function initForm() {
    var form = doc.getElementById("contact-form");
    if (!form) return;
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = true;
      form.querySelectorAll("[required]").forEach(function (input) {
        var field = input.closest(".field") || input.closest(".check");
        var valid = input.type === "checkbox" ? input.checked : input.value.trim() !== "" && input.checkValidity();
        if (field) field.classList.toggle("is-invalid", !valid);
        if (!valid && ok) { input.focus(); ok = false; }
      });
      if (!ok) return;
      var v = function (name) { var el = form.elements[name]; return el ? el.value.trim() : ""; };
      var body = [
        "Name: " + v("name"),
        "Email: " + v("email"),
        "Organisation: " + v("company"),
        "Role: " + v("role"),
        "Topic: " + v("topic"),
        "",
        v("message")
      ].join("\n");
      var subject = "Call request: " + (v("company") || v("name"));
      window.location.href = "mailto:" + FORM_EMAIL + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
      var done = doc.getElementById("form-success");
      if (done) { done.classList.add("is-visible"); form.hidden = true; done.focus(); }
    });
  }

  function initMotion() {
    if (!reduceMotion) return;
    doc.querySelectorAll("svg.anim").forEach(function (svg) { if (svg.pauseAnimations) { svg.pauseAnimations(); svg.setCurrentTime && svg.setCurrentTime(parseFloat(svg.getAttribute("data-still") || "1.2")); } });
  }

  doc.addEventListener("DOMContentLoaded", function () {
    initMotion(); initCookies(); initNav(); initReveal(); initForm();
    var y = doc.querySelector("[data-year]");
    if (y) y.textContent = new Date().getFullYear();
  });
})();
