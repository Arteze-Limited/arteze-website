"""Build the Arteze static site. Run: python3 build/build.py (from the site root)."""
import html, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import *  # noqa
import art

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE = "https://arteze.co.uk"
E = lambda s: html.escape(s, quote=True)
PAGES = []

ORG = {"@context": "https://schema.org", "@type": "Organization", "name": "Arteze Limited", "alternateName": "Arteze",
       "url": SITE + "/", "logo": SITE + "/assets/logo.png", "email": "hello@arteze.co.uk",
       "address": {"@type": "PostalAddress", "streetAddress": "35 Ruddington Avenue, Broughton", "addressLocality": "Milton Keynes",
                   "postalCode": "MK10 9XA", "addressCountry": "GB"},
       "identifier": {"@type": "PropertyValue", "propertyID": "Companies House company number", "value": "14244761"},
       "sameAs": ["https://www.linkedin.com/company/arteze-limited/"]}

SUN = '<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
MOON = '<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>'


def nav(active):
    svc = "".join(f'<li><a href="{s["file"]}">{E(s["title"])}</a></li>' for s in SERVICES[:2])
    adv = "".join(f'<li><a href="{s["file"]}">{E(s["title"])}</a></li>' for s in ADVISORY)
    ind = "".join(f'<li><a href="{i["file"]}">{E(i["title"])}</a></li>' for i in INDUSTRIES)
    ins = [("insights.html", "Articles"), ("brochures.html", "Brochures"), ("success-stories.html", "Success stories"), ("use-cases.html", "Use cases")]
    insl = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in ins)
    cur = lambda k: ' aria-current="page"' if active == k else ""
    desk = f'''<ul>
<li><a class="top" href="about.html"{cur("about")}>About</a></li>
<li><a class="top caret" href="services.html"{cur("services")}>Services</a><ul class="drop"><li class="lbl">Flagship services</li>{svc}<li class="sep"></li><li class="lbl">Advisory services</li>{adv}<li class="sep"></li><li><a href="health-check.html">Supplier health check</a></li><li><a href="services.html">All services →</a></li></ul></li>
<li><a class="top caret" href="industries.html"{cur("industries")}>Industries</a><ul class="drop">{ind}<li class="sep"></li><li><a href="industries.html">All sectors →</a></li></ul></li>
<li><a class="top caret" href="insights.html"{cur("insights")}>Insights</a><ul class="drop">{insl}</ul></li>
<li><a class="top" href="careers.html"{cur("careers")}>Careers</a></li>
<li><a class="top" href="contact.html"{cur("contact")}>Contact</a></li>
</ul>'''
    mob = f'''<nav class="mnav" id="mnav" aria-label="Mobile">
<a href="index.html">Home</a><a href="about.html">About</a>
<details><summary>Services</summary>{"".join(f'<a href="{s["file"]}">{E(s["title"])}</a>' for s in SERVICES)}<a href="health-check.html">Supplier health check</a></details>
<details><summary>Industries</summary>{"".join(f'<a href="{i["file"]}">{E(i["title"])}</a>' for i in INDUSTRIES)}</details>
<details><summary>Insights</summary>{"".join(f'<a href="{h}">{t}</a>' for h, t in ins)}</details>
<a href="careers.html">Careers</a><a href="contact.html">Contact</a>
<a class="btn" href="contact.html">Book a free conversation</a></nav>'''
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="hdr"><div class="wrap hdr-in">
<a class="brand" href="index.html" aria-label="Arteze home"><img src="assets/logo.png" alt="Arteze" width="361" height="120"></a>
<nav class="nav" aria-label="Main">{desk}
<button class="theme" type="button" data-theme-toggle aria-label="Switch to light theme">{MOON}{SUN}</button>
<a class="btn sm" href="contact.html">Book a free conversation</a></nav>
<button class="menu" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Menu"><span></span><span></span><span></span></button>
</div></header>
{mob}'''


def footer():
    col = lambda t, items: f'<div><h4>{t}</h4><ul>' + "".join(f'<li><a href="{h}">{E(x)}</a></li>' for h, x in items) + '</ul></div>'
    return f'''<footer class="ftr"><div class="wrap">
<div class="ftr-grid">
<div><a class="brand" href="index.html" aria-label="Arteze home"><img src="assets/logo.png" alt="Arteze" width="361" height="120"></a>
<p class="muted">Commercial contract management and supplier optimisation. Independent, evidence-led and focused on value you can measure.</p>
<p><a href="mailto:hello@arteze.co.uk">hello@arteze.co.uk</a></p>
<p><a href="mailto:hello@arteze.co.uk?subject=Subscribe%20to%20Arteze%20insights">Subscribe to insights by email →</a></p></div>
{col("Services", [(s["file"], s["title"]) for s in SERVICES] + [("health-check.html", "Supplier health check")])}
{col("Industries", [(i["file"], i["title"]) for i in INDUSTRIES])}
{col("Insights", [("insights.html", "Articles"), ("brochures.html", "Brochures"), ("success-stories.html", "Success stories"), ("use-cases.html", "Use cases")])}
{col("Company", [("about.html", "About us"), ("careers.html", "Careers"), ("contact.html", "Contact"), ("https://www.linkedin.com/company/arteze-limited/", "LinkedIn")])}
</div>
<div class="addr"><span>Arteze Limited · 35 Ruddington Avenue, Broughton, Milton Keynes, MK10 9XA, United Kingdom</span>
<span>Arteze GDC India Private Limited · Unit 532, 5th Floor, Jyothi Granules, Kondapur, Gachibowli, Hyderabad, TS 500084</span></div>
<div class="legal"><span>&copy; <span data-year>2026</span> Arteze Limited. Registered in England and Wales, company no. 14244761. Registered office: 35 Ruddington Avenue, Broughton, Milton Keynes, MK10 9XA.</span>
<ul><li><a href="privacy.html">Privacy</a></li><li><a href="cookies.html">Cookies</a></li><li><a href="terms.html">Terms</a></li></ul></div>
</div></footer>
<script src="script.js" defer></script>'''


def page(path, title, desc, body, active=None, noindex=False):
    url = SITE + "/" + ("" if path == "index.html" else path)
    full = title if path == "index.html" else f"{title} | Arteze"
    robots = '\n<meta name="robots" content="noindex">' if noindex else ""
    out = f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(full)}</title>
<meta name="description" content="{E(desc)}">{robots}
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Arteze"><meta property="og:locale" content="en_GB">
<meta property="og:title" content="{E(full)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og-image.jpg"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#17253F">
<link rel="icon" href="assets/favicon-64.png" type="image/png"><link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/outfit-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/manrope-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="style.css">
<script>(function(){{var d=document.documentElement;d.classList.add("js");try{{var t=localStorage.getItem("arteze-theme");if(t)d.setAttribute("data-theme",t)}}catch(e){{}}}})()</script>
<script type="application/ld+json">{json.dumps(ORG, ensure_ascii=False)}</script>
</head>
<body>
{nav(active)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
'''
    write(path, out)
    if not noindex:
        PAGES.append(path)


def write(path, s):
    p = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(s)


def redirect(path, target, label):
    write(path, f'''<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><title>{E(label)} | Arteze</title><meta name="robots" content="noindex">
<link rel="canonical" href="{SITE}/{"" if target == "index.html" else target}"><meta http-equiv="refresh" content="0; url={target}"></head>
<body><p>This page has moved. <a href="{target}">Continue to {E(label)}</a>.</p></body></html>
''')


# ---------- building blocks ----------
def btns(primary="contact.html", ptxt="Book a free conversation", secondary=None, stxt=None):
    s = f'<a class="btn ghost" href="{secondary}">{stxt}</a>' if secondary else ""
    return f'<div class="btns"><a class="btn arrow" href="{primary}">{ptxt} </a>{s}</div>'


def eyebrow(t):
    return f'<p class="eyebrow">{E(t)}</p>'


def cta(title="What could your supplier contracts be giving back?", text=CTA_TEXT, topic=None):
    href = "contact.html" + (f"?topic={topic}" if topic else "")
    return f'''<section class="sec cta"><div class="wrap rv">{eyebrow("Start the conversation")}
<h2>{E(title)}</h2><p class="lead">{E(text)}</p>{btns(href, "Book a free conversation", "mailto:hello@arteze.co.uk?subject=Enquiry", "Or email us directly")}</div></section>'''


def page_hero(eb, h1, lead, extra="", crumb=None, art_key=None):
    c = f'<p class="crumb">{crumb}</p>' if crumb else ""
    if art_key:
        return f'''<section class="page-hero"><div class="wrap hero-grid"><div>{c}{eyebrow(eb)}<h1>{E(h1)}</h1><p class="lead">{E(lead)}</p>{extra}</div>
<div class="hero-art"><img src="assets/art/{art_key}.svg" alt="" width="800" height="500"></div></div></section>'''
    return f'<section class="page-hero"><div class="wrap">{c}{eyebrow(eb)}<h1>{E(h1)}</h1><p class="lead">{E(lead)}</p>{extra}</div></section>'


def svc_card(s, n=None, text=None):
    num = f'<span class="num">{n:02d}</span>' if n else ""
    return f'''<a class="card pic rv" href="{s["file"]}"><div class="img"><img src="assets/art/{s["art"]}.svg" alt="" loading="lazy" width="800" height="500"></div>
<div class="body">{num}<h3>{E(s["title"])}</h3><p class="muted">{E(text or s["q"])}</p><span class="link arrow">Explore </span></div></a>'''


def ind_card(i):
    return f'''<a class="card pic rv" href="{i["file"]}"><div class="img"><img src="assets/art/{i["art"]}.svg" alt="" loading="lazy" width="800" height="500"></div>
<div class="body"><span class="tag">{E(i["tag"])}</span><h3>{E(i["title"])}</h3><p class="muted">{E(i["q"])}</p><span class="link arrow">Explore sector </span></div></a>'''


def uc_card(u):
    return f'''<a class="card rv" href="use-case-{u["id"]}.html"><span class="num">{u["n"]}</span><span class="tag">{E(u["sector"])}</span>
<h3>{E(u["title"])}</h3><p class="muted">{E(u["problem"])}</p><span class="link arrow">Read the full case </span></a>'''


def ul(items, cls="ticks"):
    return f'<ul class="{cls}">' + "".join(f"<li>{E(x)}</li>" for x in items) + "</ul>"


def vmaas_areas():
    tabs = "".join(f'<button role="tab" id="t{i}" aria-controls="p{i}" type="button"><span>{i+1:02d}</span>{a[0]}</button>' for i, a in enumerate(VMAAS_AREAS))
    panels = "".join(f'''<div class="panel" role="tabpanel" id="p{i}" aria-labelledby="t{i}"><div class="card">
<div><span class="tag">Area {i+1:02d} · {E(a[1])}</span><h3>{E(a[2])}</h3>{btns("contact.html?topic=vmaas", "Book a free conversation", "vmaas.html", "See VMaaS in detail")}</div>
<div>{ul(a[3])}</div></div></div>''' for i, a in enumerate(VMAAS_AREAS))
    return f'''<section class="sec"><div class="wrap"><div class="head rv">{eyebrow("VMaaS delivery framework")}<h2>Four areas of work. You choose the mix.</h2>
<p class="lead">Start with the area that matters most, then add or remove areas as your priorities change. Your team keeps every decision.</p></div>
<div data-tabs class="rv"><div class="tabs" role="tablist" aria-label="VMaaS areas">{tabs}</div>{panels}</div></div></section>'''


def jap_phases(cls="deep"):
    cards = "".join(f'''<div class="card phase{' two' if i else ''} rv"><span class="ph"><i>{i+1}</i>{E(p[0])}</span><h3>{E(p[1])}</h3><p class="muted">{E(p[2])}</p>{ul(p[3], "dashes")}</div>'''
                    for i, p in enumerate(JAP_PHASES))
    return f'''<section class="sec {cls}"><div class="wrap"><div class="head rv">{eyebrow("Joint Account Plan")}<h2>Two phases, one shared plan</h2>
<p class="lead">We begin by establishing where the relationship genuinely stands. Then, if you choose to proceed, we help you and your client act on what we found.</p></div>
<div class="g2">{cards}</div><p class="note center">{E(JAP_NOTE)}</p>
<div class="center">{btns("contact.html?topic=jap", "Book a free account consultation", "joint-account-plan.html", "Explore the Joint Account Plan")}</div></div></section>'''


def health_teaser(cls="raise"):
    return f'''<section class="sec tight {cls}"><div class="wrap"><div class="card band rv"><div>{eyebrow("Supplier health check")}
<h3>How do your clients likely see you?</h3><p class="muted" style="margin:0">Eight quick statements and an instant, indicative score for one client account. No details collected.</p></div>
<a class="btn arrow" href="health-check.html">Take the health check </a></div></div></section>'''


def track_record():
    return f'''<section class="sec raise"><div class="wrap"><div class="head rv">{eyebrow("Track record")}<h2>Numbers a finance director can take to the board</h2></div>
<div class="stats rv"><div class="stat"><b>£10m+</b><span>Savings delivered</span><small>Price reductions and rebates returned to the budget</small></div>
<div class="stat"><b>£6.7m+</b><span>Costs avoided</span><small>True-ups, exit penalties and renewal uplifts stopped</small></div>
<div class="stat"><b>£0.7m+</b><span>Savings identified</span><small>Unused subscriptions and redundant service lines</small></div>
<div class="stat"><b>£650m+</b><span>Contracts governed</span><small>Annualised supplier spend brought under control</small></div></div>
<p class="note">Figures combine Arteze client engagements with roles our founder held before establishing Arteze. The £17m total comprises around £10m in savings delivered, £6.7m in costs avoided and £0.7m in savings identified.</p>
<p><a class="link arrow" href="success-stories.html">Read the success stories </a></p></div></section>'''


# ---------- pages ----------
def home():
    s1, s2 = SERVICES[0], SERVICES[1]
    adv = "".join(svc_card(s, i + 1, s["q"]) for i, s in enumerate(ADVISORY))
    inds = "".join(ind_card(i) for i in INDUSTRIES)
    body = f'''<section class="hero"><div class="wrap hero-grid"><div>{eyebrow("For clients and suppliers of IT and outsourced services")}
<h1>We help clients get more from their suppliers, and help suppliers keep their clients.</h1>
<p class="lead">Every supplier contract has two sides. We work with both: finance leaders who want every pound of supplier spend to earn its keep, and IT service providers who want to know how their clients really see them.</p>
{btns("contact.html", "Book a free conversation", "services.html", "Explore our services")}</div>
<div class="hero-art"><img src="assets/art/hero.svg" alt="Illustration of two linked contracts" width="800" height="500"></div></div>
<div class="wrap g2" style="margin-top:56px">
<a class="card rv" href="vmaas.html"><span class="tag">For clients · CFOs and finance directors</span><h3>Buying IT and outsourced services?</h3><p class="muted">We check, renegotiate and manage your supplier contracts, so you pay the right price for what you actually use, with a monthly ROI your finance team signs off.</p><span class="link arrow">Explore VMaaS </span></a>
<a class="card rv" href="joint-account-plan.html"><span class="tag">For suppliers · IT service providers</span><h3>Providing IT services to clients?</h3><p class="muted">We find out how your clients really see you, then help you co-create a Joint Account Plan that protects renewals and grows the account.</p><span class="link arrow">Explore Joint Account Plan </span></a>
</div></section>

<section class="sec deep"><div class="wrap rv">{eyebrow("Results for finance leaders")}
<div class="stats two"><div class="stat"><b>£17m+</b><span>Supplier costs saved, avoided or identified</span></div><div class="stat"><b>£650m+</b><span>Annual supplier spend brought under governance</span></div></div>
<ul class="results"><li>£7m software renewal brought down to £4m (infrastructure programme)*</li><li>£6.5m saved in everyday running costs (public sector)*</li>
<li>About £1m saved moving from one supplier to several (insurance)*</li><li>Contract changes agreed in 5 days instead of 25*</li></ul>
<p class="note">*Results from roles our founder held before setting up Arteze. Client details are withheld.</p></div></section>

<section class="sec cmp"><div class="wrap"><div class="head rv">{eyebrow("The commercial reality")}<h2>Same contract, same supplier. A very different number on your P&amp;L.</h2>
<p class="lead">The difference between overspending and saving is rarely the deal itself. It's how the contract is managed once it's signed.</p></div>
<div class="g2"><div class="card rv"><h3>Contracts left to run</h3>{ul(["Invoices paid without being checked against the contract", "Renewals discovered when the supplier calls", "Rebates and service credits left unclaimed", "True-up liabilities quietly building up"], "crosses")}</div>
<div class="card good rv"><h3>Contracts managed with Arteze</h3>{ul(["Invoices checked against the contract before they are paid", "Renewals planned months ahead, with real leverage", "Credits and rebates chased and recovered", "A monthly ROI your finance team agrees with"])}</div></div></div></section>

<section class="sec raise"><div class="wrap"><div class="head rv">{eyebrow("Savings calculator")}<h2>What could your supplier contracts give back to the budget?</h2>
<p class="lead">A quick, illustrative estimate for finance leaders. It takes ten seconds and doesn't ask for any details.</p></div>
<div class="calc rv"><div class="card"><label for="spend" class="tag">Your annual third-party spend</label><div class="val" id="spend-val">£10m</div>
<input class="range" type="range" id="spend" min="0" max="13" step="1" value="5"><div class="ends"><span>£1m</span><span>£200m</span></div>
<p class="muted small" style="margin-top:16px">This is an illustrative range only, based on the kinds of issues we look for: unchecked invoices, late renewals, unused licences and unclaimed credits. Your own figure could be higher or lower, and the only way to know is to look at the contracts.</p></div>
<div class="card out"><span class="tag">Illustrative annual range</span><b id="save-val">£500k – £1.5m</b><a class="btn arrow" href="contact.html?topic=vmaas">Validate this with our team </a></div></div></div></section>

<section class="sec"><div class="wrap"><div class="head rv">{eyebrow("Two flagship models")}<h2>Where is the money leaking from your P&amp;L, and who is plugging it?</h2>
<p class="lead">For finance leaders, the value usually hides in unchecked invoices, late renewals and unclaimed credits. For IT service providers, it hides in what clients won't say out loud. We built a model for each.</p></div>
<div class="g2">
<a class="card pic rv" href="vmaas.html"><div class="img"><img src="assets/art/vmaas.svg" alt="" loading="lazy" width="800" height="500"></div><div class="body"><span class="tag">01 · For buyers of IT &amp; outsourced services</span><h3>VMaaS</h3><p><strong>{E(s1["q"])}</strong></p><p class="muted">{E(s1["desc"])}</p><span class="link arrow">Explore VMaaS </span></div></a>
<a class="card pic rv" href="joint-account-plan.html"><div class="img"><img src="assets/art/joint-account-plan.svg" alt="" loading="lazy" width="800" height="500"></div><div class="body"><span class="tag">02 · For IT service providers</span><h3>Joint Account Plan</h3><p><strong>{E(s2["q"])}</strong></p><p class="muted">{E(s2["desc"])}</p><span class="link arrow">Explore Joint Account Plan </span></div></a>
</div></div></section>
{vmaas_areas()}
{jap_phases()}
{health_teaser()}
{track_record()}
<section class="sec"><div class="wrap"><div class="head rv">{eyebrow("Advisory services")}<h2>Targeted expertise, exactly where you need it</h2>
<p class="lead">Engage us for a single, focused piece of work, or combine services into a wider programme.</p></div><div class="g3">{adv}<div class="card band rv span2"><div><h3>Need an independent view of your contracts?</h3><p class="muted" style="margin:0">Tell us which contracts are on your mind, and we will tell you where we would look first.</p></div><a class="btn arrow" href="contact.html">Request a contract review </a></div></div></div></section>
<section class="sec raise"><div class="wrap"><div class="head rv">{eyebrow("Sectors we support")}<h2>Every sector has its own supplier traps. We know where to look.</h2></div><div class="g3">{inds}<div class="card band rv span2"><div><h3>Don't see your sector?</h3><p class="muted" style="margin:0">Supplier contracts look different in every sector, but the questions worth asking are often the same.</p></div><a class="btn arrow" href="contact.html">Talk to us </a></div></div></div></section>
{cta()}'''
    page("index.html", "Arteze | Commercial Contract Management & Supplier Optimisation",
         "Arteze helps organisations get more from their IT and outsourcing suppliers, and helps IT service providers understand and strengthen their client relationships.", body)


def about():
    steps = [("Understand", "We get under the skin of the contract, the relationship, the commitments and what you genuinely need.", "Step 1 · Discovery"),
             ("Identify", "We surface cost inefficiency, contractual gaps, risk, duplication and the opportunities worth pursuing.", "Step 2 · Analysis"),
             ("Improve", "We renegotiate terms, restructure pricing, recover rebates and strengthen supplier performance alongside you.", "Step 3 · Improvement"),
             ("Sustain", "We keep the oversight and controls running so improvements keep paying back, year after year.", "Step 4 · Governance")]
    vals = [("Integrity", "Honest, unbiased assessments, including when the answer is that a contract is already working well."),
            ("Independence", "No ties to vendors, cloud providers or resellers. We take no commission from suppliers."),
            ("Transparency", "Evidence-backed advice and clear reporting on every pound saved, avoided or recovered."),
            ("Accountability", "We own outcomes and stand with your team through difficult negotiations."),
            ("Commercial discipline", "Commitments, invoice lines and credits checked against what was agreed."),
            ("Continuous improvement", "Structured review cycles that keep supplier relationships getting better.")]
    body = page_hero("About Arteze", "We ask the questions that help both sides of a contract get more from it.",
                     "Arteze helps organisations take control of their IT and outsourced services contracts. We find out what you're really paying for, where value is leaking, and how to build supplier relationships that deliver on their promises.",
                     btns()) + f'''
<section class="sec deep"><div class="wrap"><div class="head rv">{eyebrow("Our methodology")}<h2>A four-step framework that turns curiosity into commercial results</h2>
<p class="lead">Every engagement follows the same disciplined path across the supplier lifecycle, so improvements are found, delivered and sustained.</p></div>
<div class="g4">{"".join(f'<div class="card rv"><span class="num">{i+1:02d}</span><h3>{a}</h3><p class="muted">{b}</p><span class="tag" style="margin:0">{c}</span></div>' for i, (a, b, c) in enumerate(steps))}</div></div></section>
<section class="sec"><div class="wrap"><div class="head rv">{eyebrow("Guiding principles")}<h2>Independent by design. Accountable by choice.</h2></div>
<div class="g3">{"".join(f'<div class="card rv"><h3>{a}</h3><p class="muted">{b}</p></div>' for a, b in vals)}</div></div></section>
<section class="sec raise"><div class="wrap"><div class="head rv">{eyebrow("Commercial leadership")}<h2>25+ years on the buyer's side of the table</h2>
<p class="lead">Our founder has spent 25+ years managing IT and outsourcing contracts from the buyer's side. Across those roles and Arteze's own work, that experience adds up to more than £17m in supplier costs saved, avoided or identified: around £10m saved, £6.7m avoided and £0.7m identified.</p>
<p class="note">These figures include results from roles our founder held before setting up Arteze. Client details are withheld.</p></div>
<div class="stats rv"><div class="stat"><b>£10m+</b><span>Savings delivered</span></div><div class="stat"><b>£6.7m+</b><span>Costs avoided</span></div><div class="stat"><b>£0.7m+</b><span>Savings identified</span></div><div class="stat"><b>£650m+</b><span>Contracts governed</span></div></div>
{btns("contact.html", "Speak with our founder")}</div></section>
{cta()}'''
    page("about.html", "About Arteze", "Arteze is an independent UK consultancy helping organisations and IT service providers get more from their supplier contracts.", body, "about")


def services():
    fl = "".join(f'''<a class="card pic rv" href="{s["file"]}"><div class="img"><img src="assets/art/{s["art"]}.svg" alt="" loading="lazy" width="800" height="500"></div><div class="body"><span class="tag">{E(s["eyebrow"])}</span><h3>{E(s["title"])}</h3><p class="muted">{E(s["desc"])}</p><span class="link arrow">Explore {E(s["title"])} </span></div></a>''' for s in SERVICES[:2])
    adv = "".join(svc_card(s, i + 1, s["q"] + " " + s["card"]) for i, s in enumerate(ADVISORY))
    body = page_hero("Our services", "Every contract has untapped value. Here's how we unlock it.",
                     "Two flagship models for continuous commercial control, backed by seven focused advisory services you can engage individually or combine.", btns()) + f'''
<section class="sec deep"><div class="wrap"><div class="head rv">{eyebrow("Flagship models")}<h2>Built for ongoing value, not one-off fixes</h2></div><div class="g2">{fl}</div></div></section>
{health_teaser("")}
<section class="sec raise"><div class="wrap"><div class="head rv">{eyebrow("Advisory services")}<h2>Specialist help for specific commercial challenges</h2></div><div class="g3">{adv}<div class="card band rv span2"><div><h3>Not sure which service fits?</h3><p class="muted" style="margin:0">Start with the problem. We will tell you honestly which approach, if any, makes sense.</p></div><a class="btn arrow" href="contact.html">Book a free conversation </a></div></div></div></section>
{cta()}'''
    page("services.html", "Services", "VMaaS, the Joint Account Plan and seven advisory services for IT and outsourced services contracts.", body, "services")


def service_page(s):
    rel = "".join(uc_card(UC[r]) for r in s["related"])
    extra = ""
    if s["slug"] == "vmaas":
        extra = vmaas_areas()
    if s["slug"] == "joint-account-plan":
        extra = jap_phases("") + health_teaser("deep")
    topic = {"vmaas": "vmaas", "joint-account-plan": "jap"}.get(s["slug"])
    href = "contact.html" + (f"?topic={topic}" if topic else "")
    body = page_hero(s["eyebrow"] if s["slug"] in ("vmaas",) else s["title"], s["q"], s["desc"],
                     btns(href, "Book a free conversation", "#how", "See how we help"),
                     f'<a href="services.html">Services</a> / {E(s["title"])}', s["art"]) + f'''
<section class="sec deep"><div class="wrap"><div class="head rv">{eyebrow("Sound familiar?")}<h2>The challenges we hear most often</h2></div>
<ol class="numbered rv">{"".join(f"<li>{E(c)}</li>" for c in s["challenges"])}</ol></div></section>
<section class="sec" id="how"><div class="wrap g2"><div class="rv">{eyebrow("How we help")}<h2>What Arteze does about it</h2></div><div class="rv">{ul(s["helps"])}</div></div></section>
{extra}
<section class="sec raise"><div class="wrap g2"><div class="rv">{eyebrow("Focus areas")}<h3>Where we put our attention</h3><ul class="chips">{"".join(f"<li>{E(f)}</li>" for f in s["focus"])}</ul></div>
<div class="rv">{eyebrow("The outcome")}<h3>What changes for you</h3>{ul(s["outcome"])}</div></div></section>
<section class="sec"><div class="wrap"><div class="head rv">{eyebrow("Related use cases")}<h2>See this service in action</h2></div><div class="g2">{rel}</div></div></section>
{cta(f"Curious what {s['title']} could deliver for you?", topic=topic)}'''
    page(s["file"], s["title"], s["q"] + " " + s["desc"][:110].rsplit(" ", 1)[0] + "…", body, "services")


def industries():
    body = page_hero("Industry expertise", "Different sectors. Different suppliers. The same opportunity to do better.",
                     "Each sector has its own regulation, licensing quirks and supplier dynamics. We bring commercial insight shaped by all of them.", btns()) + f'''
<section class="sec deep"><div class="wrap"><div class="g3">{"".join(ind_card(i) for i in INDUSTRIES)}<div class="card band rv span2"><div><h3>Don't see your sector?</h3><p class="muted" style="margin:0">Supplier contracts look different in every sector, but the questions worth asking are often the same.</p></div><a class="btn arrow" href="contact.html">Talk to us </a></div></div></div></section>{cta()}'''
    page("industries.html", "Industries", "How Arteze helps insurance, financial services, public sector, infrastructure, energy, manufacturing and IT service providers.", body, "industries")


def industry_page(i):
    u = UC[i["related"]]
    founder = f'''<div class="card good-box rv" style="margin-top:28px"><b>From our founder's earlier work</b><p style="margin:0">{E(i["founder"])}</p><p class="small muted" style="margin:6px 0 0">Client details are withheld.</p></div>''' if i["founder"] else ""
    body = page_hero(i["tag"], i["q"], i["desc"], btns("contact.html", "Book a free conversation", "industries.html", "All sectors"),
                     f'<a href="industries.html">Industries</a> / {E(i["title"])}', i["art"]) + f'''
<section class="sec deep"><div class="wrap g2"><div class="rv">{eyebrow("Sector pressures")}<h2>What we see across {E(i["title"])}</h2><ol class="numbered" style="grid-template-columns:1fr">{"".join(f"<li>{E(p)}</li>" for p in i["pressures"])}</ol></div>
<div class="rv">{eyebrow("Our response")}<h2>How Arteze helps</h2>{ul(i["helps"])}{founder}</div></div></section>
{health_teaser("") if i.get("health") else ""}
<section class="sec raise"><div class="wrap"><div class="head rv">{eyebrow("Related use case")}</div><div class="g2">{uc_card(u)}</div></div></section>
{cta(i.get("cta", f"Let's talk about your {i['title']} suppliers"))}'''
    page(i["file"], i["title"], i["q"] + " " + i["desc"][:100].rsplit(" ", 1)[0] + "…", body, "industries")


def insights_hero(cur):
    tabs = [("insights.html", "Articles"), ("brochures.html", "Brochures"), ("success-stories.html", "Success stories"), ("use-cases.html", "Use cases")]
    sub = '<div class="subnav">' + "".join(f'<a href="{h}"{" aria-current=page" if h == cur else ""}>{t}</a>' for h, t in tabs) + "</div>"
    return page_hero("Arteze insights", "Sharper questions lead to better contracts.",
                     "Perspectives from the negotiating table, practical playbooks, examples of results and the nine supplier problems we're asked to solve most.", sub)


def insights():
    cards = "".join(f'''<a class="card rv" href="{a["slug"]}.html"><span class="tag">{E(a["cat"])} · {a["mins"]} min read</span><h3>{E(a["title"])}</h3><p class="muted">{E(a["summary"])}</p><span class="link arrow">Read article </span></a>''' for a in ARTICLES)
    page("insights.html", "Insights", "Articles on supplier contracts, renewals, licensing and governance from Arteze.",
         insights_hero("insights.html") + f'<section class="sec deep"><div class="wrap g2">{cards}</div></section>{cta()}', "insights")
    for a in ARTICLES:
        b = "".join(f"<h2>{E(t)}</h2>" if k == "h" else f"<p>{E(t)}</p>" for k, t in a["body"])
        body = page_hero(f'{a["cat"]} · {a["mins"]} min read', a["title"], a["summary"], crumb='<a href="insights.html">Insights</a> / Article') + \
            f'<section class="sec deep"><div class="wrap prose rv">{b}</div></section>{cta("Want to know whether this applies to your contracts?")}'
        page(a["slug"] + ".html", a["title"], a["summary"], body, "insights")


def brochures():
    cards = "".join(f'''<div class="card rv"><span class="tag">{E(c)} · Available on request</span><h3>{E(t)}</h3><p class="muted">{E(d)}</p>
<a class="link arrow" href="mailto:hello@arteze.co.uk?subject={E(t.replace(' ', '%20'))}%20-%20copy%20request">Request a copy by email </a></div>''' for c, t, d in BROCHURES)
    page("brochures.html", "Brochures", "Arteze guides and overviews, available by email on request.",
         insights_hero("brochures.html") + f'<section class="sec deep"><div class="wrap g2">{cards}</div></section>{cta()}', "insights")


def stories():
    cards = "".join(f'''<div class="card story rv"><span class="tag">{E(sec)}</span><div class="fig">{E(fig)}</div><h3>{E(t)}</h3>
<dl><dt>The challenge</dt><dd>{E(c)}</dd><dt>The approach</dt><dd>{E(a)}</dd><dt>The outcome</dt><dd>{E(o)}</dd></dl><p class="fn">{E(STORY_NOTE)}</p></div>''' for sec, fig, t, c, a, o in STORIES)
    page("success-stories.html", "Success stories", "Examples of supplier contract results from our founder's earlier roles.",
         insights_hero("success-stories.html") + f'<section class="sec deep"><div class="wrap g2">{cards}</div></section>{cta()}', "insights")


def use_cases():
    page("use-cases.html", "Use cases", "The nine supplier contract problems Arteze is asked to solve most often.",
         insights_hero("use-cases.html") + f'<section class="sec deep"><div class="wrap g3">{"".join(uc_card(u) for u in USE_CASES)}</div></section>{cta()}', "insights")
    for u in USE_CASES:
        body = page_hero(f'Use case {u["n"]} · {u["sector"]}', u["title"], u["sub"], crumb='<a href="use-cases.html">Use cases</a> / ' + u["n"]) + f'''
<section class="sec deep"><div class="wrap prose rv"><dl class="uc"><dt>The problem</dt><dd>{E(u["problem"])}</dd><dt>Why it happens</dt><dd>{E(u["why"])}</dd>
<dt>The commercial impact</dt><dd>{E(u["impact"])}</dd><dt>How Arteze helps</dt><dd>{E(u["how"])}</dd></dl>
<div class="good-box"><b>What good looks like</b>{E(u["good"])}</div>
<h2>What you gain</h2><ul class="chips">{"".join(f"<li>{E(g)}</li>" for g in u["gain"])}</ul>{btns()}</div></section>
{cta("Facing something similar?")}'''
        page(f'use-case-{u["id"]}.html', u["title"], u["problem"], body, "insights")


def careers():
    roles = "".join(f'<div class="card rv"><h3>{E(t)}</h3><p class="muted">{E(d)}</p><span class="tag" style="margin:0">{E(l)}</span></div>' for t, d, l in ROLES)
    body = page_hero("Careers at Arteze", "For people who read the small print, and enjoy it.",
                     "Work alongside experienced commercial people on real supplier contracts, from renewals and negotiations to everyday governance.",
                     btns("mailto:hello@arteze.co.uk?subject=Talent%20network", "Join our talent network")) + f'''
<section class="sec deep"><div class="wrap"><div class="head rv">{eyebrow("Roles we hire for")}<h2>Where you could make your mark</h2>
<p class="lead">Send your CV and a short introduction to <a href="mailto:hello@arteze.co.uk?subject=Talent%20network">hello@arteze.co.uk</a>. Tell us which supplier problem you most enjoy solving.</p></div>
<div class="g3">{roles}</div><p class="note">We keep what you send us confidential and use it only to consider you for current and future roles.</p></div></section>'''
    page("careers.html", "Careers", "Commercial contract, sourcing and licensing roles at Arteze in Milton Keynes, London and Hyderabad.", body, "careers")


def contact():
    opts = ["VMaaS (Vendor Management as a Service)", "Joint Account Plan", "Contract review and optimisation", "Supplier cost reduction and invoice recovery",
            "An upcoming renewal or negotiation", "Software licensing or audit support", "Something else"]
    f = lambda n, l, t="text", req=True, ac="": f'<div class="field"><label for="f-{n}">{l}{" *" if req else ""}</label><input id="f-{n}" name="{n}" type="{t}"{" required" if req else ""}{f" autocomplete={ac}" if ac else ""}><p class="err">Please complete this field.</p></div>'
    body = page_hero("Get in touch", "Start with one question. We'll take it from there.",
                     "Tell us about a contract, a supplier or a renewal on the horizon. The first conversation is free, and we'll be honest about whether we can help.") + f'''
<section class="sec deep"><div class="wrap g2" style="grid-template-columns:1.3fr .9fr">
<div class="card rv"><form class="form" id="contact-form" novalidate>
<div class="row2">{f("first", "First name", ac="given-name")}{f("last", "Last name", ac="family-name")}</div>
{f("company", "Company", ac="organization")}
<div class="row2">{f("email", "Business email", "email", ac="email")}{f("phone", "Phone", "tel", False, "tel")}</div>
<div class="field"><label for="f-topic">I'd like to discuss *</label><select id="f-topic" name="topic" required><option value="">Please choose</option>{"".join(f"<option>{E(o)}</option>" for o in opts)}</select><p class="err">Please choose a topic.</p></div>
<div class="field"><label for="f-message">What's on your mind? (optional)</label><textarea id="f-message" name="message"></textarea></div>
<button class="btn arrow" type="submit">Send enquiry </button>
<p class="small muted" style="margin:0">When you press the button, your email app opens with these details filled in, addressed to hello@arteze.co.uk. Nothing is sent until you press send. We keep what you tell us confidential and use your details only to reply to you.</p>
</form><div class="done" id="form-done" tabindex="-1"><h3>Your email is ready to send</h3><p class="muted">If your email app didn't open, write to us at <a href="mailto:hello@arteze.co.uk">hello@arteze.co.uk</a>. We reply within one business day.</p></div></div>
<div class="rv" style="display:grid;gap:18px;align-content:start">
<div class="card"><span class="tag">Email us directly</span><p style="margin:0"><a href="mailto:hello@arteze.co.uk">hello@arteze.co.uk</a></p></div>
<div class="card"><span class="tag">United Kingdom · HQ</span><h3>Arteze Limited</h3><p class="muted">35 Ruddington Avenue, Broughton<br>Milton Keynes, MK10 9XA<br>United Kingdom</p><a class="link" href="https://www.google.com/maps/search/?api=1&amp;query=35+Ruddington+Avenue+Broughton+Milton+Keynes+MK10+9XA" target="_blank" rel="noopener">View map</a></div>
<div class="card"><span class="tag">India · Delivery centre</span><h3>Arteze GDC India Private Limited</h3><p class="muted">Unit 532, 5th Floor, Jyothi Granules<br>Kondapur, Gachibowli<br>Hyderabad, TS 500084</p><a class="link" href="https://www.google.com/maps/search/?api=1&amp;query=Jyothi+Granules+Kondapur+Hyderabad+500084" target="_blank" rel="noopener">View map</a></div>
</div></div></section>'''
    page("contact.html", "Contact", "Book a free first conversation with Arteze about a supplier contract, renewal or client relationship.", body, "contact")


def health():
    q = E(json.dumps(HEALTH, ensure_ascii=False))
    body = page_hero("Supplier health check · For IT service providers", "How do your clients likely see you?",
                     "Eight quick statements, about two minutes. Answer honestly for one client account and you'll get an instant, indicative score, with the areas that may be worth a closer look. No details are collected.",
                     '<p><a class="link arrow" href="joint-account-plan.html">About the Joint Account Plan </a></p>') + f'''
<section class="sec deep"><div class="wrap"><div class="card hc" id="hc" data-q="{q}">
<div style="display:flex;justify-content:space-between" class="small muted"><span>Progress</span><span id="hc-count">0/8</span></div><div class="bar"><i id="hc-bar"></i></div>
<div id="hc-q"><p class="qlabel"></p><p class="qtext" aria-live="polite"></p>
<div class="answers"><button type="button">Not at all</button><button type="button">Partly</button><button type="button">Mostly</button><button type="button">Fully</button></div></div>
<div id="hc-r" hidden tabindex="-1"><p class="qlabel">Your indicative score</p><div class="score" id="hc-score"></div><span class="verdict" id="hc-verdict"></span>
<p class="muted" id="hc-text"></p><h3>Areas worth exploring</h3><ul class="dashes" id="hc-areas"></ul>
<p class="note">This is an indicative self-assessment based only on your own answers. It is not a measure of how your client actually sees you; the only way to know that is to ask them, in confidence.</p>
<div class="btns"><a class="btn arrow" id="hc-book" href="contact.html?topic=jap">Book a free conversation </a><button class="btn ghost" type="button" id="hc-again">Start again</button></div></div>
<noscript><p>This health check needs JavaScript. You can <a href="contact.html?topic=jap">talk to us directly</a> instead.</p></noscript>
</div></div></section>'''
    page("health-check.html", "Supplier health check", "A two-minute self-assessment for IT service providers: how do your clients likely see you?", body, "services")


def legal():
    src = os.path.join(os.path.dirname(__file__), "legal")
    titles = {"privacy.html": ("Privacy notice", "How Arteze Limited handles personal information."),
              "terms.html": ("Website terms", "Terms of use for the Arteze website.")}
    for fn, (t, d) in titles.items():
        b = open(os.path.join(src, fn), encoding="utf-8").read()
        page(fn, t, d, page_hero("Legal", t, d) + f'<section class="sec deep"><div class="wrap prose">{b}</div></section>')
    ck = '''<h2>The short version</h2><p>This website sets no cookies and loads no analytics, tracking or third-party fonts.</p>
<h2>Essential storage</h2><ul><li><strong>arteze-theme</strong> (stored in your browser's local storage). Remembers whether you chose the light or dark theme. It stays until you clear your browser storage, and it never leaves your device.</li></ul>
<h2>Third-party links</h2><p>Links to LinkedIn and Google Maps take you to sites with their own cookie policies.</p>
<h2>Questions</h2><p>Email <a href="mailto:hello@arteze.co.uk">hello@arteze.co.uk</a>. See also our <a href="privacy.html">privacy notice</a>.</p>'''
    page("cookies.html", "Cookie policy", "Cookies and browser storage on the Arteze website.", page_hero("Legal", "Cookie policy", "What this website stores in your browser.") + f'<section class="sec deep"><div class="wrap prose">{ck}</div></section>')


def misc():
    page("404.html", "Page not found", "This page could not be found.",
         page_hero("Page not found", "We couldn't find that page.", "It may have moved when we updated the site.", btns("index.html", "Go to the home page", "contact.html", "Contact us")), noindex=True)
    R = {"evidence.html": ("success-stories.html", "Success stories"), "problems.html": ("use-cases.html", "Use cases"),
         "experience.html": ("about.html", "About"), "msps.html": ("joint-account-plan.html", "Joint Account Plan"),
         "free-check.html": ("contact.html", "Contact"), "tokvale.html": ("index.html", "the home page"),
         "insight-exit-terms.html": ("use-case-leaving-a-supplier-with-weak-exit-terms.html", "Leaving a supplier with weak exit terms"),
         "insight-pricing-model.html": ("use-case-pricing-model-no-longer-fits.html", "The pricing model no longer fits"),
         "insight-renewal-checks.html": ("use-case-major-renewal-approaching.html", "A major renewal is approaching")}
    for a, (b, l) in R.items():
        redirect(a, b, l)
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    urls = "".join(f"<url><loc>{SITE}/{'' if p == 'index.html' else p}</loc></url>" for p in PAGES)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    write("CNAME", "arteze.co.uk\n")


if __name__ == "__main__":
    art.write_all(ROOT)
    home(); about(); services()
    for s in SERVICES: service_page(s)
    industries()
    for i in INDUSTRIES: industry_page(i)
    insights(); brochures(); stories(); use_cases(); careers(); contact(); health(); legal(); misc()
    print(len(PAGES), "pages")
