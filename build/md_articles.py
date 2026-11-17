"""Load insight articles written as Markdown files in build/articles/.

Each file starts with a small header between --- lines (slug, title, cat, mins, summary),
followed by the article text. Supported in the text: paragraphs, ### subheadings,
- bullet lists, 1. numbered lists, > quotes, **bold** and [links](page.html).
Files are listed on the Insights page in file-name order, before the older articles.
"""
import glob, html, os, re

E = lambda s: html.escape(s, quote=True)
DIR = os.path.join(os.path.dirname(__file__), "articles")


def inline(text):
    out = E(text)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    def link(m):
        label, href = m.group(1), m.group(2)
        ext = href.startswith("http")
        extra = ' target="_blank" rel="noopener"' if ext else ""
        return f'<a href="{href}"{extra}>{label}</a>'
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, out)


def render(md):
    blocks, out = re.split(r"\n\s*\n", md.strip()), []
    for b in blocks:
        lines = [l.rstrip() for l in b.strip().splitlines()]
        if b.startswith("### "):
            out.append(f"<h2>{inline(b[4:].strip())}</h2>")
        elif all(l.startswith("- ") for l in lines):
            out.append("<ul>" + "".join(f"<li>{inline(l[2:])}</li>" for l in lines) + "</ul>")
        elif all(re.match(r"\d+\. ", l) for l in lines):
            items = [inline(re.sub(r"^\d+\. ", "", l)) for l in lines]
            out.append("<ol>" + "".join("<li>" + i + "</li>" for i in items) + "</ol>")
        elif all(l.startswith(">") for l in lines):
            out.append("<blockquote><p>" + inline(" ".join(l.lstrip("> ") for l in lines)) + "</p></blockquote>")
        else:
            out.append(f"<p>{inline(' '.join(lines))}</p>")
    return "".join(out)


def load():
    arts = []
    for path in sorted(glob.glob(os.path.join(DIR, "*.md"))):
        raw = open(path, encoding="utf-8").read()
        _, head, body = raw.split("---", 2)
        meta = dict(l.split(":", 1) for l in head.strip().splitlines())
        meta = {k.strip(): v.strip() for k, v in meta.items()}
        meta["mins"] = int(meta["mins"])
        meta["html"] = render(body)
        arts.append(meta)
    return arts
