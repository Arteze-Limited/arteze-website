# Arteze website (arteze.co.uk)

A plain static site. No build step, no framework, no server. Edit the files and push to GitHub; GitHub Pages publishes them.

## Files

| File | What it is | How to edit |
|---|---|---|
| `index.html` | Home page | Edit the text between the tags. Sections are marked with comments (`<!-- 1. HERO -->` etc.). |
| `free-check.html` | Free Contract Value Check (main conversion page), including the 12 levers, "How we measure value" (`#how-we-measure`: value types and confidence levels) and the booking form | Each lever is one `<li class="lever">`. The form is identical to the one on `contact.html`; change both if you edit fields. |
| `services.html` | The published catalogue with filters | Each area is a `<div class="svc-group" data-area="...">`. Each service is one `<article class="svc">`. To add an area, add a group with a new `data-area` value and a matching filter button (`data-filter="..."`). |
| `vmaas.html` | Vendor Management as a Service | Plain text sections. |
| `msps.html` | For MSPs | Pain points are `<li class="leak">`; offers are `<article class="info">`. |
| `tokvale.html` | Short Tokvale page linking to tokvale.com | Plain text. |
| `about.html` | About Arteze, including "Before Arteze" (`#before-arteze`): founder track record from roles held before Arteze | Plain text. To add a track record card, copy an `<article class="svc">` block in that section. |
| `contact.html` | Contact page and booking form | See "Booking form" below. |
| `privacy.html`, `cookies.html`, `terms.html` | Legal pages (starting drafts, please have them reviewed) | Plain text. Search for `[Insert` to find gaps. |
| `404.html` | "Page not found" page used by GitHub Pages | Plain text. |
| `style.css` | All styling | Brand colours and fonts are CSS variables at the very top (`:root`). The live look is the "Bold Gradient" theme: its colours, gradient, fonts and images are in the `[data-theme="gradient"]` block further down. Every page has `data-theme="gradient"` on its `<html>` tag. |
| `script.js` | Menu, cookie banner, analytics loader, animations, services filter, booking form | Settings at the very top: `ANALYTICS` and `FORM_EMAIL`. |
| `assets/logo-mark.png` | Logo mark, used in the header only | Replace with a file of the same name. (`logo.png` is used for search engines and schema; `logo-mark-large.webp` is no longer used on pages.) |
| `assets/img/` | Abstract background images (hero, page headers, founder band) | Replace with files of the same name, or change the `--t-hero-img` / `--t-side-img` paths in the theme block. |
| `assets/favicon-64.png`, `assets/apple-touch-icon.png` | Browser and phone icons | Replace with files of the same name. |
| `assets/og-image.jpg` | Image shown when a page is shared on LinkedIn, Teams, etc. (1200 × 630) | Replace with a file of the same name. |
| `assets/icons.svg` | All line icons, one `<symbol>` each | Use an icon with `<svg class="icon" aria-hidden="true"><use href="assets/icons.svg#i-NAME"/></svg>`. |
| `assets/fonts/` | Self-hosted fonts. Live theme uses Bricolage Grotesque (headings) and DM Sans (text). No calls to Google. | Leave as is. Unused font files can be deleted. |
| `assets/js/lenis.min.js` | Small smooth-scrolling library (self-hosted). Turned off automatically for visitors who prefer reduced motion. | Delete the `<script src="assets/js/lenis.min.js">` line on each page to turn it off. |
| `CNAME` | Tells GitHub Pages to serve the site at arteze.co.uk | Leave as is. |
| `robots.txt`, `sitemap.xml` | For search engines | Add a line to `sitemap.xml` when you add a page. |

## Common edits

**Header and footer.** They are repeated on every page (there is no build step). If you change a menu item, change it on every `.html` file. Use find-and-replace across files in your editor. Move `aria-current="page"` to the current page's link.

**Page titles and descriptions (SEO).** In each file's `<head>`: `<title>` and `<meta name="description">`. The `og:` lines control link previews.

**Organisation schema.** The `<script type="application/ld+json">` block in each `<head>`.

**Show the client quote on the home page.** In `index.html`, find `<figure class="quote" hidden data-quote>`, put in the real quote and name, and delete the word `hidden`. Only publish a quote you have written approval for.

**Booking form.** It opens the visitor's email app with the details filled in, addressed to `hello@arteze.co.uk` (set by `FORM_EMAIL` at the top of `script.js`). Nothing is sent to a server. If you rename a field, keep the `name` attribute the same as in `script.js` (`name`, `email`, `company`, `role`, `spend`, `orgType`, `contract`, `renewal`, `message`).

**Analytics (off by default).** Nothing loads until a visitor presses "Accept analytics". To switch on:
- Google Analytics 4: set `ga4Id: "G-XXXXXXXXXX"` at the top of `script.js`.
- Plausible: set `plausibleDomain: "arteze.co.uk"`.
Then list the provider and its cookies in `cookies.html`.

**Placeholders.** Search the files for `placeholder` or `[` to find everything waiting for real content. Do not publish invented case studies, client names, logos, testimonials or figures.

## Publishing on GitHub Pages
1. Put these files at the root of the repository (the same level as `CNAME`).
2. Settings → Pages → Deploy from branch → `main` / root.
3. In your DNS, point `arteze.co.uk` at GitHub Pages (as you did for tokvale.com) and tick "Enforce HTTPS".

## Previewing locally
Open the folder in a terminal and run `python3 -m http.server`, then visit http://localhost:8000. (Opening files directly from disk works, but some browsers block the shared icon file that way.)
