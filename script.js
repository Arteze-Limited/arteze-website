/* Arteze site script: theme, menu, reveal, tabs, calculator, contact form (email), health check. */
(function () {
  "use strict";
  var doc = document, root = doc.documentElement;
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }

  /* theme */
  var tbtn = doc.querySelector("[data-theme-toggle]");
  if (tbtn) tbtn.addEventListener("click", function () {
    var next = root.getAttribute("data-theme") === "light" ? "dark" : "light";
    root.setAttribute("data-theme", next); store("arteze-theme", next);
    tbtn.setAttribute("aria-label", next === "light" ? "Switch to dark theme" : "Switch to light theme");
  });

  /* mobile menu */
  var mbtn = doc.querySelector(".menu"), mnav = doc.getElementById("mnav");
  if (mbtn && mnav) mbtn.addEventListener("click", function () {
    var open = mnav.classList.toggle("open"); mbtn.setAttribute("aria-expanded", open ? "true" : "false");
    doc.body.style.overflow = open ? "hidden" : "";
  });

  /* reveal */
  var rv = doc.querySelectorAll(".rv");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }); }, { rootMargin: "0px 0px -8% 0px" });
    rv.forEach(function (el) { io.observe(el); });
  } else rv.forEach(function (el) { el.classList.add("in"); });

  /* tabs */
  doc.querySelectorAll("[data-tabs]").forEach(function (box) {
    var btns = box.querySelectorAll("[role=tab]"), panels = box.querySelectorAll("[role=tabpanel]");
    function show(i) {
      btns.forEach(function (b, j) { b.setAttribute("aria-selected", i === j ? "true" : "false"); b.tabIndex = i === j ? 0 : -1; });
      panels.forEach(function (p, j) { p.hidden = i !== j; });
    }
    btns.forEach(function (b, i) {
      b.addEventListener("click", function () { show(i); });
      b.addEventListener("keydown", function (e) {
        if (e.key === "ArrowRight" || e.key === "ArrowLeft") { var n = (i + (e.key === "ArrowRight" ? 1 : btns.length - 1)) % btns.length; show(n); btns[n].focus(); }
      });
    });
    show(0);
  });

  /* calculator */
  var range = doc.getElementById("spend");
  if (range) {
    var steps = [1, 2, 3, 5, 7.5, 10, 15, 20, 30, 50, 75, 100, 150, 200];
    var fmt = function (m) { return m >= 1 ? "£" + (Math.round(m * 10) / 10) + "m" : "£" + Math.round(m * 1000) + "k"; };
    var upd = function () {
      var v = steps[+range.value];
      doc.getElementById("spend-val").textContent = fmt(v);
      doc.getElementById("save-val").textContent = fmt(v * 0.05) + " – " + fmt(v * 0.15);
      range.setAttribute("aria-valuetext", fmt(v));
    };
    range.addEventListener("input", upd); upd();
  }

  /* contact form: opens the visitor's email app with the details filled in */
  var form = doc.getElementById("contact-form");
  if (form) {
    var q = new URLSearchParams(location.search), sel = form.elements.topic;
    var map = { vmaas: "VMaaS (Vendor Management as a Service)", jap: "Joint Account Plan" };
    var want = map[q.get("topic")] || q.get("topic");
    if (want) for (var i = 0; i < sel.options.length; i++) if (sel.options[i].text === want) sel.selectedIndex = i;
    if (q.get("message")) form.elements.message.value = q.get("message");
    form.addEventListener("submit", function (e) {
      e.preventDefault(); var ok = true;
      form.querySelectorAll("[required]").forEach(function (el) {
        var f = el.closest(".field"), bad = !el.value.trim() || (el.type === "email" && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(el.value));
        f.classList.toggle("invalid", bad); if (bad && ok) { el.focus(); ok = false; }
      });
      if (!ok) return;
      var v = function (n) { return (form.elements[n].value || "").trim(); };
      var body = "Name: " + v("first") + " " + v("last") + "\nCompany: " + v("company") + "\nEmail: " + v("email") + "\nPhone: " + v("phone") + "\nTopic: " + v("topic") + "\n\n" + v("message");
      location.href = "mailto:hello@arteze.co.uk?subject=" + encodeURIComponent("Enquiry: " + v("topic")) + "&body=" + encodeURIComponent(body);
      var done = doc.getElementById("form-done"); if (done) { done.classList.add("show"); done.focus(); }
    });
  }

  /* health check */
  var hc = doc.getElementById("hc");
  if (hc) {
    var qs = JSON.parse(hc.getAttribute("data-q")), ans = [], idx = 0, busy = false;
    var labels = ["Not at all", "Partly", "Mostly", "Fully"];
    var qbox = doc.getElementById("hc-q"), rbox = doc.getElementById("hc-r"), bar = doc.getElementById("hc-bar"), cnt = doc.getElementById("hc-count");
    var render = function () {
      bar.style.width = (idx / qs.length * 100) + "%"; cnt.textContent = idx + "/" + qs.length;
      qbox.querySelector(".qlabel").textContent = "Question " + (idx + 1) + " of " + qs.length + " · " + qs[idx][0];
      qbox.querySelector(".qtext").textContent = qs[idx][1];
      busy = false;
    };
    qbox.querySelectorAll(".answers button").forEach(function (b, val) {
      b.addEventListener("click", function () {
        if (busy) return; busy = true; ans[idx] = val; idx++;
        if (idx < qs.length) { setTimeout(render, 120); } else { finish(); }
      });
    });
    var finish = function () {
      bar.style.width = "100%"; cnt.textContent = qs.length + "/" + qs.length;
      var sum = ans.reduce(function (a, b) { return a + b; }, 0), score = Math.round(sum / (qs.length * 3) * 100);
      var verdict = score >= 80 ? "Looks strong" : score >= 45 ? "Room to grow" : "Worth a closer look";
      var text = {
        "Looks strong": "Your answers suggest a relationship with good foundations. A confidential maturity assessment could confirm whether your client sees it the same way, and show where it could go further.",
        "Room to grow": "Your answers suggest some solid ground, with a few areas where your view and your client's view may differ. These are often the areas worth understanding before the next renewal.",
        "Worth a closer look": "Your answers suggest several areas where you may not have a clear view of how your client sees you. Hearing directly from your client, in confidence, is usually the best place to start."
      }[verdict];
      var weak = qs.filter(function (q, i) { return ans[i] <= 1; });
      var list = doc.getElementById("hc-areas"); list.innerHTML = "";
      if (weak.length) weak.forEach(function (q) { var li = doc.createElement("li"); li.innerHTML = "<strong></strong> "; li.firstChild.textContent = q[0] + ":"; li.appendChild(doc.createTextNode(q[1])); list.appendChild(li); });
      else {
        var p = doc.createElement("li");
        p.textContent = score < 80 ? "None of your answers stood out as weak, but few were a confident 'Fully'. The gap between 'mostly' and 'fully' is often where a client's view differs most from yours."
          : "You answered \"Mostly\" or \"Fully\" to every statement. The useful question now is whether your client would answer the same way.";
        list.appendChild(p);
      }
      doc.getElementById("hc-score").innerHTML = score + "<small>/100</small>";
      doc.getElementById("hc-verdict").textContent = verdict;
      doc.getElementById("hc-text").textContent = text;
      var msg = "I completed the Supplier Health Check. My indicative score was " + score + "/100 (" + verdict + "). I'd like to talk about a Joint Account Plan.";
      doc.getElementById("hc-book").href = "contact.html?topic=jap&message=" + encodeURIComponent(msg);
      qbox.hidden = true; rbox.hidden = false; rbox.focus();
    };
    doc.getElementById("hc-again").addEventListener("click", function () { ans = []; idx = 0; rbox.hidden = true; qbox.hidden = false; render(); });
    render();
  }

  var y = doc.querySelector("[data-year]"); if (y) y.textContent = new Date().getFullYear();
})();
