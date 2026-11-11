"""Arteze card illustrations: light style, no people. Writes assets/art/<key>.svg."""
import os

CSS = """.p{fill:#fff;stroke:#D3DEEA;stroke-width:1.5;filter:url(#sh)}.a{fill:#0098DD}.n{fill:#1F3968}
.l{stroke:#1F3968;stroke-opacity:.22;stroke-width:9;fill:none;stroke-linecap:round}
.w{stroke:#fff;stroke-width:6;stroke-linecap:round;fill:none}
.k{stroke:#1F3968;stroke-width:5;fill:none;stroke-linecap:round;stroke-linejoin:round}
.ka{stroke:#0098DD;stroke-width:6;fill:none;stroke-linecap:round;stroke-linejoin:round}
.cell{fill:#1F3968;fill-opacity:.14}
.tick{fill:none;stroke:#fff;stroke-width:8;stroke-linecap:round;stroke-linejoin:round}
.tick2{fill:none;stroke:#0098DD;stroke-width:12;stroke-linecap:round;stroke-linejoin:round}
.glass{fill:#0098DD;fill-opacity:.1;stroke:#1F3968;stroke-width:8}.handle{stroke:#1F3968;stroke-width:18;stroke-linecap:round}"""

BG = """<defs><filter id="sh" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#1F3968" flood-opacity=".16"/></filter>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F4F8FC"/><stop offset="1" stop-color="#E1ECF6"/></linearGradient></defs>
<rect width="800" height="500" fill="url(#bg)"/><circle cx="420" cy="250" r="215" fill="#fff" fill-opacity=".7"/><circle cx="90" cy="470" r="140" fill="#0098DD" fill-opacity=".07"/><circle cx="740" cy="40" r="90" fill="#1F3968" fill-opacity=".05"/>"""


def lines(x, y, w, n, gap=22, cls="l", short=None):
    out = ""
    for i in range(n):
        ww = w * 0.6 if short is not None and i == short else w
        out += f'<line class="{cls}" x1="{x}" y1="{y+i*gap}" x2="{x+ww:.0f}" y2="{y+i*gap}"/>'
    return out


def doc(x, y, w=190, h=250):
    return f'<rect class="p" x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/>'


def vmaas():
    g = ""
    for i, (dx, dy) in enumerate([(0, 0), (26, 22), (52, 44)]):
        x, y = 230 + dx, 80 + dy
        g += doc(x, y)
        if i == 2:
            g += f'<rect class="a" x="{x+22}" y="{y+24}" width="70" height="14" rx="7"/>' + lines(x + 22, y + 70, 146, 5, 26, short=4)
    g += '<circle class="a" cx="470" cy="350" r="44"/><path class="tick" d="M448 351 l15 15 l28 -30"/>'
    x, y = 500, 110
    g += f'<rect class="p" x="{x}" y="{y}" width="150" height="140" rx="12"/><rect class="a" x="{x}" y="{y}" width="150" height="32" rx="12"/><rect class="a" x="{x}" y="{y+18}" width="150" height="14"/>'
    for r in range(3):
        for c in range(4):
            g += f'<rect class="{"a" if (r, c) == (1, 2) else "cell"}" x="{x+16+c*32}" y="{y+46+r*28}" width="22" height="18" rx="4"/>'
    return g


def building(x, y, w, h, rows, cols=3):
    g = f'<rect class="p" x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>'
    for r in range(rows):
        for c in range(cols):
            g += f'<rect class="cell" x="{x+18+c*36}" y="{y+18+r*36}" width="22" height="20" rx="3"/>'
    return g


def jap():
    g = building(170, 190, 130, 200, 5) + building(520, 150, 130, 240, 6)
    g += '<path class="k" d="M300 260 Q410 150 520 240"/><line class="l" x1="300" y1="300" x2="520" y2="300"/>'
    for t in [0.2, 0.35, 0.5, 0.65, 0.8]:
        x = 300 + 220 * t
        yq = (1 - t) ** 2 * 260 + 2 * (1 - t) * t * 150 + t * t * 240
        g += f'<line class="l" x1="{x:.0f}" y1="{yq:.0f}" x2="{x:.0f}" y2="300"/>'
    g += '<rect class="a" x="340" y="80" width="80" height="46" rx="14"/><path class="a" d="M360 124 l-8 20 l24 -20z"/>'
    g += '<rect class="p" x="430" y="104" width="80" height="46" rx="14"/>'
    g += lines(356, 97, 48, 2, 13, "w") + lines(446, 121, 48, 2, 13, "l")
    return g


def review():
    g = '<path class="p" d="M260 60 h170 l60 60 v270 a12 12 0 0 1 -12 12 h-218 a12 12 0 0 1 -12 -12 v-318 a12 12 0 0 1 12 -12z"/><path class="l" d="M430 60 v48 a12 12 0 0 0 12 12 h48"/>'
    g += lines(290, 150, 170, 6, 28, short=5) + '<path class="k" d="M292 350 c20 -30 30 10 50 -10 s25 -20 40 5"/>'
    g += '<circle class="glass" cx="530" cy="270" r="78"/><line class="ka" x1="410" y1="262" x2="490" y2="262"/><line class="handle" x1="586" y1="326" x2="650" y2="392"/>'
    return g


def costs():
    g = '<path class="p" d="M240 70 h200 v300 l-25 -16 l-25 16 l-25 -16 l-25 16 l-25 -16 l-25 16 l-25 -16 l-25 16z"/>'
    g += lines(270, 120, 140, 5, 30, short=4) + '<rect class="a" x="270" y="290" width="90" height="16" rx="8"/>'
    g += '<rect class="p" x="470" y="140" width="210" height="190" rx="14"/>'
    for i, h in enumerate([120, 95, 70, 45]):
        g += f'<rect class="{"a" if i == 3 else "cell"}" x="{495+i*45}" y="{310-h}" width="28" height="{h}" rx="5"/>'
    g += '<path class="ka" d="M500 175 L548 205 L592 230 L650 262"/><path class="ka" d="M628 264 L652 263 L646 240"/>'
    return g


def renewals():
    x, y = 250, 90
    g = f'<rect class="p" x="{x}" y="{y}" width="260" height="250" rx="16"/><rect class="a" x="{x}" y="{y}" width="260" height="54" rx="16"/><rect class="a" x="{x}" y="{y+30}" width="260" height="24"/>'
    g += f'<rect class="n" x="{x+50}" y="{y-18}" width="14" height="40" rx="7"/><rect class="n" x="{x+196}" y="{y-18}" width="14" height="40" rx="7"/>'
    for r in range(4):
        for c in range(5):
            g += f'<rect class="{"a" if (r, c) == (2, 3) else "cell"}" x="{x+22+c*46}" y="{y+76+r*40}" width="32" height="26" rx="5"/>'
    g += '<circle class="p" cx="560" cy="330" r="70"/><path class="ka" d="M525 330 a35 35 0 1 1 12 26"/><path class="ka" d="M520 345 L536 357 L548 340"/>'
    return g


def performance():
    g = '<path class="p" d="M200 330 a150 150 0 0 1 300 0 z"/>'
    g += '<path class="cell" d="M232 330 a118 118 0 0 1 59 -102 l16 28 a86 86 0 0 0 -43 74z"/>'
    g += '<path class="a" d="M409 228 a118 118 0 0 1 59 102 h-32 a86 86 0 0 0 -43 -74z"/>'
    g += '<line class="k" x1="350" y1="330" x2="420" y2="250"/><circle class="n" cx="350" cy="330" r="14"/>'
    x, y = 520, 110
    g += f'<rect class="p" x="{x}" y="{y}" width="160" height="230" rx="14"/>'
    for i in range(4):
        g += f'<circle class="{"a" if i < 3 else "cell"}" cx="{x+30}" cy="{y+45+i*48}" r="12"/>' + f'<line class="l" x1="{x+55}" y1="{y+45+i*48}" x2="{x+135}" y2="{y+45+i*48}"/>'
    return g


def governance():
    x, y = 230, 70
    g = doc(x, y, 230, 300) + f'<rect class="a" x="{x+80}" y="{y-14}" width="70" height="28" rx="10"/>'
    for i in range(4):
        cy = y + 70 + i * 55
        g += f'<rect class="{"a" if i < 3 else "cell"}" x="{x+28}" y="{cy-14}" width="28" height="28" rx="6"/>'
        if i < 3:
            g += f'<path class="w" d="M{x+34} {cy} l6 6 l11 -12" style="stroke-width:4"/>'
        g += f'<line class="l" x1="{x+76}" y1="{cy}" x2="{x+190}" y2="{cy}"/>'
    g += '<path class="p" d="M560 170 l85 30 v65 c0 60 -40 95 -85 115 c-45 -20 -85 -55 -85 -115 v-65z"/><path class="tick2" d="M527 270 l24 24 l46 -50"/>'
    return g


def licensing():
    g = ""
    for i in range(3):
        x, y = 220 + i * 40, 250 - i * 70
        g += f'<rect class="p" x="{x}" y="{y}" width="280" height="110" rx="16"/><circle class="{"a" if i == 2 else "cell"}" cx="{x+55}" cy="{y+55}" r="26"/>'
        g += f'<line class="l" x1="{x+105}" y1="{y+42}" x2="{x+240}" y2="{y+42}"/><line class="l" x1="{x+105}" y1="{y+72}" x2="{x+190}" y2="{y+72}"/>'
    g += '<circle class="p" cx="580" cy="130" r="40"/><circle class="n" cx="580" cy="130" r="14"/><path class="k" d="M610 155 L670 215 M650 195 l16 -16 M636 181 l12 -12"/>'
    return g


def exit_():
    g = '<rect class="p" x="250" y="70" width="200" height="320" rx="12"/><rect class="cell" x="276" y="96" width="148" height="294" rx="6"/>'
    g += '<path class="p" d="M276 96 L380 120 V390 L276 390z"/><circle class="n" cx="360" cy="260" r="8"/>'
    g += '<path class="ka" d="M470 240 H640" style="stroke-width:12"/><path class="ka" d="M600 200 L645 240 L600 280" style="stroke-width:12"/>'
    return g


def insurance():
    g = '<path class="p" d="M380 70 l130 45 v105 c0 95 -60 150 -130 180 c-70 -30 -130 -85 -130 -180 v-105z"/><path class="tick2" d="M328 236 l36 36 l70 -76"/>'
    g += '<circle class="p" cx="590" cy="150" r="58"/><path class="a" d="M590 150 v-58 a58 58 0 0 1 55 40z"/>'
    for i, h in enumerate([50, 80, 64, 110]):
        g += f'<rect class="{"a" if i == 3 else "cell"}" x="{552+i*26}" y="{390-h}" width="18" height="{h}" rx="4"/>'
    return g + '<line class="l" x1="542" y1="392" x2="658" y2="392"/>'


def banking():
    g = '<path class="p" d="M220 170 L400 80 L580 170z"/><circle class="a" cx="400" cy="138" r="16"/>'
    g += '<rect class="p" x="230" y="175" width="340" height="22" rx="4"/>'
    for i in range(5):
        g += f'<rect class="p" x="{250+i*66}" y="208" width="34" height="140" rx="4"/>'
    g += '<rect class="p" x="210" y="352" width="380" height="28" rx="6"/><rect class="n" x="190" y="384" width="420" height="16" rx="6"/>'
    return g


def government():
    g = '<path class="p" d="M320 150 a80 80 0 0 1 160 0z"/><rect class="a" x="394" y="40" width="12" height="40"/><path class="a" d="M406 42 h40 l-10 12 l10 12 h-40z"/>'
    g += '<rect class="p" x="250" y="150" width="300" height="24" rx="4"/>'
    for i in range(6):
        g += f'<rect class="p" x="{268+i*46}" y="184" width="26" height="150" rx="4"/>'
    g += '<rect class="p" x="230" y="338" width="340" height="26" rx="6"/><rect class="n" x="210" y="368" width="380" height="16" rx="6"/>'
    return g


def infrastructure():
    g = '<path class="p" d="M140 300 Q400 90 660 300 L660 320 L140 320z"/><path class="cell" d="M180 300 Q400 140 620 300z"/>'
    for i in range(1, 8):
        x = 140 + i * 65
        g += f'<line class="l" x1="{x}" y1="{300-0.0}" x2="{x}" y2="{300 - (1-((x-400)/260)**2)*150:.0f}" style="stroke-width:5"/>'
    g += '<rect class="n" x="120" y="320" width="560" height="18" rx="6"/>'
    g += '<line class="k" x1="120" y1="400" x2="680" y2="400"/><line class="k" x1="120" y1="430" x2="680" y2="430"/>'
    for i in range(10):
        g += f'<rect class="cell" x="{135+i*56}" y="394" width="14" height="42" rx="3"/>'
    g += '<rect class="a" x="300" y="352" width="160" height="40" rx="12"/><rect class="p" x="316" y="360" width="40" height="18" rx="4"/><rect class="p" x="366" y="360" width="40" height="18" rx="4"/>'
    return g


def energy():
    g = '<path class="k" d="M330 400 L380 120 L430 400 M345 320 H415 M355 250 H405 M365 180 H395 M330 400 L415 320 M430 400 L345 320 M355 250 L415 320 M405 250 L345 320 M365 180 L405 250 M395 180 L355 250"/>'
    g += '<path class="k" d="M300 150 H460 M320 150 v20 M440 150 v20"/>'
    g += '<circle class="p" cx="560" cy="200" r="78"/><path class="a" d="M572 140 L530 212 H560 L548 262 L594 186 H564z"/>'
    return g


def manufacturing():
    g = '<path class="p" d="M200 380 V220 L280 260 V220 L360 260 V220 L440 260 V160 H500 V380z"/><rect class="n" x="455" y="110" width="30" height="60" rx="4"/>'
    for i in range(3):
        g += f'<rect class="cell" x="{225+i*80}" y="300" width="40" height="40" rx="5"/>'
    teeth = "".join(f'<rect class="a" x="{-9}" y="{-80}" width="18" height="26" rx="4" transform="rotate({a})"/>' for a in range(0, 360, 45))
    g += f'<g transform="translate(590,250)">{teeth}<circle class="a" r="62"/><circle class="p" r="26" style="filter:none;stroke:none"/></g>'
    return g


def itproviders():
    g = ""
    for i in range(2):
        x = 230 + i * 150
        g += f'<rect class="p" x="{x}" y="110" width="130" height="270" rx="12"/>'
        for r in range(5):
            y = 130 + r * 48
            g += f'<rect class="cell" x="{x+14}" y="{y}" width="102" height="34" rx="6"/><circle class="{"a" if (r+i) % 2 == 0 else "n"}" cx="{x+100}" cy="{y+17}" r="6"/>'
    g += '<rect class="a" x="520" y="70" width="150" height="86" rx="20"/><path class="a" d="M560 152 l-14 30 l40 -30z"/>' + lines(546, 100, 98, 2, 26, "w")
    return g


def hero():
    g = doc(180, 100, 210, 280) + lines(210, 160, 150, 6, 30, short=5)
    g += '<rect class="a" x="210" y="125" width="80" height="14" rx="7"/>'
    g += doc(410, 120, 210, 280) + lines(440, 180, 150, 6, 30, short=5)
    g += '<rect class="n" x="440" y="145" width="80" height="14" rx="7"/>'
    g += '<circle cx="400" cy="250" r="34" fill="none" stroke="#0098DD" stroke-width="12"/><circle cx="440" cy="250" r="34" fill="none" stroke="#1F3968" stroke-width="12"/>'
    return g


OBJ = {"vmaas": vmaas, "joint-account-plan": jap, "contract-review": review, "supplier-costs": costs,
       "renewals": renewals, "supplier-performance": performance, "governance": governance,
       "software-licensing": licensing, "contract-exit": exit_, "insurance": insurance, "banking": banking,
       "public-sector": government, "infrastructure": infrastructure, "energy": energy,
       "manufacturing": manufacturing, "it-service-providers": itproviders, "hero": hero}


def svg(key):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" preserveAspectRatio="xMidYMid slice" role="img">'
            f'<style>{CSS}</style>{BG}<g>{OBJ[key]()}</g></svg>')


def write_all(root):
    d = os.path.join(root, "assets", "art")
    os.makedirs(d, exist_ok=True)
    for k in OBJ:
        open(os.path.join(d, k + ".svg"), "w", encoding="utf-8").write(svg(k))


if __name__ == "__main__":
    write_all(os.path.join(os.path.dirname(__file__), ".."))
