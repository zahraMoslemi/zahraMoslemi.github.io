#!/usr/bin/env python3
"""Original method figures for the research portfolio.

One designed figure per paper, drawn in the same visual language as the MGMT
architecture figure (Helvetica, numbered stages, dashed rule panels, light-blue
operation boxes, stage brackets). Every figure is original artwork that
summarises the paper's method; none reproduces a figure from a journal.

Run:  python3 scripts/paper_figures.py      -> images/figures/*.svg
Then: python3 scripts/build_portfolio.py
"""
from html import escape
from pathlib import Path
import math
import re

OUT = Path(__file__).resolve().parents[1] / 'images' / 'figures'
FONT = "'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "Menlo, Consolas, 'Courier New', monospace"
INK, GRAY, LIGHT, SEP = '#1f1f1f', '#666666', '#c4c4c4', '#dcdcdc'
BOX_FILL, BOX_STROKE = '#dfe9f6', '#3f6aa3'
PANEL_FILL, PANEL_STROKE = '#f4f4f4', '#8a8a8a'
META_FILL, META_STROKE = '#efeaf8', '#8a76c2'
CROSS, ORANGE, GREEN, BLUE = '#c0392b', '#e07b24', '#38761d', '#2e6da4'
SRC = [('#f6b26b', '#b5651d'), ('#93c47d', '#38761d'), ('#f1d56a', '#a3861c'),
       ('#9fc5e8', '#2e6da4'), ('#d5a6bd', '#8e4a6b')]


def markup(s, size):
    """Escape text and turn _{..} / ^{..} into sub/superscript tspans."""
    out, pos = [], 0
    for m in re.finditer(r'([_^])\{([^}]*)\}', s):
        out.append(escape(s[pos:m.start()]))
        d = 0.28 * size if m.group(1) == '_' else -0.42 * size
        out.append(f'<tspan dy="{d:.1f}" font-size="{0.72*size:.1f}">{escape(m.group(2))}</tspan><tspan dy="{-d:.1f}">')
        out.append('</tspan>')  # placeholder closed below
        pos = m.end()
    out.append(escape(s[pos:]))
    # rebuild so trailing text sits inside the restoring tspan
    text = ''.join(part for part in out if part != '</tspan>')
    text += '</tspan>' * out.count('</tspan>')
    return text


class SVG:
    def __init__(self, w, h):
        self.w, self.h, self.parts, self.markers = w, h, [], set()

    def add(self, s):
        self.parts.append(s)

    # ---- primitives -------------------------------------------------------
    def text(self, x, y, s, size=20, color=INK, anchor='start', bold=False, italic=False, mono=False, opacity=None):
        attrs = f'x="{x}" y="{y}" font-family="{MONO if mono else FONT}" font-size="{size}" fill="{color}" text-anchor="{anchor}"'
        if bold: attrs += ' font-weight="700"'
        if italic: attrs += ' font-style="italic"'
        if opacity: attrs += f' opacity="{opacity}"'
        self.add(f'<text {attrs}>{markup(s, size)}</text>')

    def lines(self, x, y, items, size=19, lh=None, **kw):
        for i, s in enumerate(items):
            self.text(x, y + i * (lh or round(size * 1.38)), s, size, **kw)

    def rect(self, x, y, w, h, fill='#fff', stroke=INK, sw=2, rx=0, dash=None, opacity=None):
        a = f'x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"'
        if dash: a += f' stroke-dasharray="{dash}"'
        if opacity: a += f' opacity="{opacity}"'
        self.add(f'<rect {a}/>')

    def circle(self, cx, cy, r, fill, stroke=INK, sw=2, dash=None, opacity=None):
        a = f'cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"'
        if dash: a += f' stroke-dasharray="{dash}"'
        if opacity: a += f' opacity="{opacity}"'
        self.add(f'<circle {a}/>')

    def ellipse(self, cx, cy, rx, ry, angle=0, fill='none', stroke=INK, sw=2, dash=None, opacity=None):
        a = f'cx="0" cy="0" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" transform="translate({cx} {cy}) rotate({angle})"'
        if dash: a += f' stroke-dasharray="{dash}"'
        if opacity: a += f' opacity="{opacity}"'
        self.add(f'<ellipse {a}/>')

    def path(self, d, fill='none', stroke=INK, sw=2, dash=None, opacity=None, cap='round'):
        a = f'd="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}" stroke-linejoin="round"'
        if dash: a += f' stroke-dasharray="{dash}"'
        if opacity: a += f' opacity="{opacity}"'
        self.add(f'<path {a}/>')

    def line(self, x1, y1, x2, y2, color=INK, sw=2.2, dash=None, opacity=None):
        self.path(f'M{x1} {y1}L{x2} {y2}', stroke=color, sw=sw, dash=dash, opacity=opacity)

    def _marker(self, color):
        mid = 'm' + color.strip('#')
        if mid not in self.markers:
            self.markers.add(mid)
            self.add(f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0.5L10 5L0 9.5z" fill="{color}"/></marker></defs>')
        return mid

    def arrow(self, pts, color=INK, sw=2.4, dash=None, both=False):
        mid = self._marker(color)
        d = 'M' + 'L'.join(f'{x} {y}' for x, y in pts)
        a = f'd="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round" marker-end="url(#{mid})"'
        if both: a += f' marker-start="url(#{mid})"'
        if dash: a += f' stroke-dasharray="{dash}"'
        self.add(f'<path {a}/>')

    def box(self, x, y, w, h, label, fill=BOX_FILL, stroke=BOX_STROKE, size=22, bold=True, rx=9, sw=2, color=INK, sub=None, sub_size=None, dash=None):
        """Rounded box with a centred label; `label` may be a list of lines."""
        self.rect(x, y, w, h, fill, stroke, sw, rx, dash=dash)
        items = label if isinstance(label, list) else [label]
        lh = round(size * 1.3)
        total = lh * len(items) + (0 if sub is None else round((sub_size or size * 0.86) * 1.3) * (len(sub) if isinstance(sub, list) else 1))
        y0 = y + h / 2 - total / 2 + size * 0.95
        for i, s in enumerate(items):
            self.text(x + w / 2, round(y0 + i * lh), s, size, color, 'middle', bold)
        if sub is not None:
            subs = sub if isinstance(sub, list) else [sub]
            ss = sub_size or round(size * 0.86)
            yy = y0 + len(items) * lh
            for i, s in enumerate(subs):
                self.text(x + w / 2, round(yy + i * round(ss * 1.3)), s, ss, GRAY, 'middle')

    def panel(self, x, y, w, h, title, items, title_size=22, size=19, fill=PANEL_FILL, stroke=PANEL_STROKE, dashed=True, pad=14):
        self.rect(x, y, w, h, fill, stroke, 1.8, 10, dash='7 5' if dashed else None)
        self.text(x + pad, y + pad + title_size * 0.9, title, title_size, INK, bold=True)
        self.lines(x + pad, y + pad + title_size * 0.9 + round(size * 1.5), items, size)

    def chip(self, x, y, w, h, label, fill, stroke, size=18, color=INK, bold=True):
        self.rect(x, y, w, h, fill, stroke, 1.8, h / 2)
        self.text(x + w / 2, y + h / 2 + size * 0.36, label, size, color, 'middle', bold)

    def stage(self, x, n, title, size=30):
        self.text(x, 48, f'{n}', size, INK, bold=True)
        self.text(x + size * 1.35, 48, title, size, INK, bold=True)

    def vsep(self, x, y1=66, y2=800):
        self.line(x, y1, x, y2, SEP, 1.5)

    def bracket(self, x1, x2, y, label, sub=None):
        self.path(f'M{x1} {y-10}V{y}H{x2}V{y-10}', stroke='#9a9a9a', sw=1.6, cap='butt')
        self.text((x1 + x2) / 2, y + 32, label, 22, INK, 'middle', bold=True)
        if sub:
            self.text((x1 + x2) / 2, y + 58, sub, 18, GRAY, 'middle')

    # ---- compound drawings -----------------------------------------------
    def graph(self, cx, cy, r, nodes, edges, fill, stroke, keep=None, mode='plain', d=16, edge_color=INK, edge_sw=2.2, labels=False):
        pos = {i: (cx + ux * r, cy - uy * r) for i, (ux, uy) in enumerate(nodes)}
        keep = set(keep or [])
        for a, b in edges:
            both = a in keep and b in keep
            if mode == 'plain':
                self.line(*pos[a], *pos[b], edge_color, edge_sw)
            elif mode == 'select':
                if both: self.line(*pos[a], *pos[b], edge_color, edge_sw + 0.3)
                else: self.line(*pos[a], *pos[b], LIGHT, 1.6, dash='5 5')
            elif mode == 'kept' and both:
                self.line(*pos[a], *pos[b], edge_color, edge_sw + 0.3)
        for i, (x, y) in pos.items():
            if mode == 'plain':
                self.circle(x, y, d / 2, fill, stroke, 2)
            elif mode == 'select':
                if i in keep: self.circle(x, y, d / 2, fill, stroke, 2.2)
                else: self.circle(x, y, d / 2 - 1.5, '#fff', LIGHT, 1.6)
            elif mode == 'kept' and i in keep:
                self.circle(x, y, d / 2, fill, stroke, 2.2)
        return pos

    def contours(self, cx, cy, rx, ry, angle, n=4, stroke=BLUE, fill=None):
        for k in range(n, 0, -1):
            f = k / n
            self.ellipse(cx, cy, rx * f, ry * f, angle, fill=(fill if fill else 'none'), stroke=stroke, sw=1.6, opacity=0.35 + 0.55 * (1 - f))

    def curve(self, x0, y0, w, h, f, n=120, stroke=INK, sw=2.4, fill=None, close=False, dash=None, opacity=None):
        pts = []
        for i in range(n + 1):
            t = i / n
            pts.append((x0 + t * w, y0 + h - f(t) * h))
        d = 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
        if close:
            d += f'L{x0+w} {y0+h}L{x0} {y0+h}Z'
        self.path(d, fill=fill or 'none', stroke=stroke, sw=sw, dash=dash, opacity=opacity)

    def axes(self, x0, y0, w, h, xlabel=None, ylabel=None, size=16):
        self.path(f'M{x0} {y0}V{y0+h}H{x0+w}', stroke='#9a9a9a', sw=1.6, cap='butt')
        if xlabel: self.text(x0 + w / 2, y0 + h + 22, xlabel, size, GRAY, 'middle')
        if ylabel: self.text(x0 - 10, y0 - 8, ylabel, size, GRAY, 'end')

    def net(self, x, y, layers, dx, h, fill=BOX_FILL, stroke=BOX_STROKE, d=12):
        """Tiny feed-forward network icon; layers = node counts per column."""
        cols = []
        for j, n in enumerate(layers):
            gap = h / (n + 1)
            cols.append([(x + j * dx, y + gap * (i + 1)) for i in range(n)])
        for a, b in zip(cols, cols[1:]):
            for (x1, y1) in a:
                for (x2, y2) in b:
                    self.line(x1, y1, x2, y2, '#b9c6d6', 1.2)
        for col in cols:
            for (px, py) in col:
                self.circle(px, py, d / 2, fill, stroke, 1.6)
        return cols

    def scan(self, x, y, w, h, variant=0, label=None):
        """OCT B-scan icon: dark background with layered bright bands."""
        self.rect(x, y, w, h, '#1b2430', '#39495c', 1.4, 4)
        for k, (yy, amp, col) in enumerate([(0.35, 0.05, '#c9d6e8'), (0.5, 0.08, '#8fa8c7'), (0.66, 0.05, '#dde7f3')]):
            bump = 0.0 if variant == 0 else (0.16 if k == 1 else 0.07)
            self.curve(x + 6, y + yy * h - 12, w - 12, 24,
                       lambda t, a=amp, b=bump, v=variant: 0.5 + a * math.sin(6.28 * (t + 0.1 * v)) + (b * math.exp(-((t - 0.55) ** 2) / 0.01) if b else 0),
                       n=40, stroke=col, sw=2.2)
        if label:
            self.text(x + w / 2, y + h + 20, label, 16, GRAY, 'middle')

    def dna(self, x, y, h, turns=2.0, w=40, color=BLUE):
        n = 60
        a, b = [], []
        for i in range(n + 1):
            t = i / n
            yy = y + t * h
            a.append((x + w / 2 * math.sin(2 * math.pi * turns * t), yy))
            b.append((x - w / 2 * math.sin(2 * math.pi * turns * t), yy))
        for pts, col in ((a, color), (b, CROSS)):
            self.path('M' + 'L'.join(f'{px:.1f} {py:.1f}' for px, py in pts), stroke=col, sw=3)
        for i in range(0, n + 1, 5):
            (x1, y1), (x2, y2) = a[i], b[i]
            self.line(x1, y1, x2, y2, '#9aa6b2', 1.6)

    def save(self, name):
        body = ''.join(self.parts)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" role="img">'
               f'<rect width="{self.w}" height="{self.h}" fill="#ffffff"/>{body}</svg>\n')
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / f'{name}.svg').write_text(svg)
        print('wrote', name, f'{self.w}x{self.h}')


# ---------------------------------------------------------------------------
# shared small drawings
GRAPH_O = dict(nodes=[(-0.9, -0.2), (-0.45, 0.6), (0.1, 0.9), (0.3, 0.25), (-0.3, -0.05), (-0.7, -0.75), (0.0, -0.7), (0.75, -0.55), (0.9, 0.3), (0.55, 0.85)],
               edges=[(0, 1), (0, 4), (0, 5), (1, 2), (1, 4), (2, 3), (2, 9), (3, 4), (3, 8), (3, 9), (4, 6), (5, 6), (6, 7), (7, 8), (8, 9), (4, 7)], keep={1, 2, 3, 4, 8, 9})
GRAPH_G = dict(nodes=[(-0.85, 0.5), (-0.2, 0.85), (0.5, 0.7), (0.9, 0.1), (0.3, -0.1), (-0.4, 0.1), (-0.8, -0.5), (-0.1, -0.75), (0.6, -0.7)],
               edges=[(0, 1), (0, 5), (0, 6), (1, 2), (1, 5), (2, 3), (2, 4), (3, 4), (3, 8), (4, 5), (4, 7), (4, 8), (5, 6), (5, 7), (6, 7), (7, 8)], keep={2, 3, 4, 7, 8})
GRAPH_Y = dict(nodes=[(-0.9, 0.1), (-0.5, 0.8), (0.2, 0.6), (0.85, 0.75), (0.1, 0.0), (-0.45, -0.4), (0.7, -0.1), (0.0, -0.85), (0.8, -0.75)],
               edges=[(0, 1), (0, 5), (1, 2), (1, 4), (2, 3), (2, 4), (2, 6), (3, 6), (4, 5), (4, 6), (4, 7), (5, 7), (6, 8), (7, 8), (3, 8)], keep={0, 1, 2, 4, 5})
GRAPH_B = dict(nodes=[(-0.8, 0.6), (0.0, 0.9), (0.8, 0.5), (0.9, -0.4), (0.2, -0.1), (-0.6, -0.2), (-0.3, -0.85), (0.5, -0.8)],
               edges=[(0, 1), (0, 5), (1, 2), (1, 4), (2, 3), (2, 4), (3, 4), (3, 7), (4, 5), (4, 6), (5, 6), (6, 7), (4, 7)], keep={1, 2, 3, 4, 7})
GRAPH_P = dict(nodes=[(-0.7, 0.7), (0.3, 0.8), (0.9, 0.0), (0.2, -0.2), (-0.6, -0.1), (-0.2, -0.8), (0.7, -0.75)],
               edges=[(0, 1), (0, 4), (1, 2), (1, 3), (2, 3), (2, 6), (3, 4), (3, 5), (4, 5), (5, 6), (3, 6)], keep={1, 2, 3, 6})
GRAPHS5 = [GRAPH_O, GRAPH_G, GRAPH_Y, GRAPH_B, GRAPH_P]


def bimodal(t, a=0.34, b=0.70, s=0.075, wa=1.0, wb=0.8):
    return wa * math.exp(-((t - a) ** 2) / (2 * s * s)) + wb * math.exp(-((t - b) ** 2) / (2 * s * s))


def scatter_in_ellipse(svg, cx, cy, rx, ry, angle, pts, fill, stroke, r=4.2):
    ca, sa = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    for (u, v) in pts:
        x = cx + (u * rx) * ca - (v * ry) * sa
        y = cy + (u * rx) * sa + (v * ry) * ca
        svg.circle(round(x, 1), round(y, 1), r, fill, stroke, 1.2)


# deterministic pseudo-random points inside the unit disc
def disc_points(n, seed=7, spread=0.8):
    pts, s = [], seed
    for _ in range(n):
        s = (s * 48271) % 2147483647; u = (s / 2147483647) * 2 - 1
        s = (s * 48271) % 2147483647; v = (s / 2147483647) * 2 - 1
        s = (s * 48271) % 2147483647; rr = (s / 2147483647)
        norm = math.hypot(u, v) or 1
        rad = spread * math.sqrt(rr)
        pts.append((u / norm * rad, v / norm * rad))
    return pts


# ---------------------------------------------------------------------------
def fig_scope():
    f = SVG(1700, 900)
    f.stage(30, 1, 'Find the directions that matter', 28)
    f.stage(660, 2, 'Sample the active subspace', 28)
    f.stage(1140, 3, 'Select and calibrate', 28)
    f.vsep(648); f.vsep(1128)
    f.panel(30, 72, 610, 104, 'Score-guided active subspace (no sampling yet)', [
        'score s(y, x; θ) = −log p̂(y | x, θ) on a held-out guide set D_{guide}',
        'B = top-r eigenvectors of the weighted score-gradient covariance'], size=16)
    f.panel(660, 72, 460, 104, 'Slice MCMC + projected completion', [
        'MALA on θ = θ_{*} + B a,  a ∈ ℝ^{r},  r ≪ d',
        'complement ⟂ B: projected variational Gaussian'], size=16)
    f.panel(1140, 72, 550, 104, 'Conformal level from the same guide set', [
        'anchor ← candidate with the lower guide NLL',
        'q̂ = (1−α)-quantile of guide scores → region {−log p̂(y|x) ≤ q̂}'], size=16)

    # stage 1 ---------------------------------------------------------------
    f.box(40, 222, 120, 50, 'D_{train}', size=21)
    f.box(200, 205, 210, 92, ['candidate anchors'], size=21, sub=['θ_{VI}  (mean-field VI mean)', 'θ_{MAP}  (converged MAP)'], sub_size=17)
    f.arrow([(160, 247), (198, 247)])
    f.box(40, 338, 120, 50, 'D_{guide}', size=21)
    f.box(200, 322, 210, 82, ['score gradients'], size=21, sub=['∇_{θ} s on D_{guide}, weighted', 'toward the target level 1−α'], sub_size=17)
    f.arrow([(160, 363), (198, 363)])
    f.arrow([(410, 251), (436, 251), (436, 330), (446, 330)])
    f.arrow([(410, 363), (436, 363), (436, 330)], sw=2.4)
    cx, cy = 540, 330
    f.contours(cx, cy, 96, 44, -28)
    f.circle(cx, cy, 5, INK, INK)
    f.text(cx + 10, cy + 24, 'θ_{*}', 19, INK)
    # active direction (not the major axis)
    ang = math.radians(-28 + 72)
    dx, dy = math.cos(ang), math.sin(ang)
    f.arrow([(cx - 78 * dx, cy - 78 * dy), (cx + 78 * dx, cy + 78 * dy)], CROSS, 3.2, both=True)
    f.text(cx + 82 * dx + 8, cy + 82 * dy + 8, 'B', 22, CROSS, bold=True)
    am = math.radians(-28)
    f.line(cx - 112 * math.cos(am), cy - 112 * math.sin(am), cx + 112 * math.cos(am), cy + 112 * math.sin(am), GRAY, 1.8, dash='5 5')
    f.line(44, 452, 84, 452, CROSS, 3.2)
    f.text(94, 458, 'active directions B: they move the region boundary', 16, INK)
    f.line(44, 484, 84, 484, GRAY, 1.8, dash='5 5')
    f.text(94, 490, 'largest-variance direction: left to the cheap completion', 16, GRAY)
    f.rect(40, 540, 600, 190, '#fff', SEP, 1.5, 10)
    f.text(60, 575, 'Key observation', 21, INK, bold=True)
    f.lines(60, 608, ['A prediction region depends on the posterior mainly through a few',
                      'parameter directions that move its boundary; these are generally',
                      'not the directions of largest posterior variance. Score gradients',
                      'on the guide set find them; rank r follows a spectral-mass rule.'], 16, lh=26, color=INK)

    # stage 2 ---------------------------------------------------------------
    cx, cy = 820, 330
    f.contours(cx, cy, 96, 44, -28, stroke='#9fb6cf')
    # completion band perpendicular to B (along the major axis)
    f.ellipse(cx, cy, 108, 22, -28, fill=META_FILL, stroke=META_STROKE, sw=1.6, dash='5 4', opacity=0.9)
    f.line(cx - 90 * dx, cy - 90 * dy, cx + 90 * dx, cy + 90 * dy, CROSS, 2.6)
    for t in (-0.82, -0.6, -0.42, -0.28, -0.12, 0.05, 0.2, 0.33, 0.5, 0.7):
        f.circle(round(cx + 90 * t * dx, 1), round(cy + 90 * t * dy, 1), 5, '#fff', CROSS, 2.2)
    f.text(cx, 440, 'slice MCMC along B: samples a_{1} … a_{N} (r-dimensional MALA)', 16, CROSS, 'middle')
    f.text(cx, 464, 'projected VI completion carries the remaining directions', 16, META_STROKE, 'middle')
    f.arrow([(cx, 478), (cx, 506)])
    f.box(680, 508, 300, 60, 'completed predictive p̂(y | x)', size=19, sub='mixture over completed states', sub_size=15)
    f.axes(700, 596, 260, 130, 'y', 'density')
    f.curve(700, 596, 260, 130, lambda t: 0.92 * bimodal(t), fill='#dfe9f6', close=True, stroke=BOX_STROKE, sw=2.4)
    f.text(890, 770, 'r ≪ d directions sampled: 12–15× faster than full HMC', 15, GRAY, 'middle')

    # stage 3 ---------------------------------------------------------------
    f.axes(1170, 215, 240, 150, 'guide score s_{i}', 'count')
    heights = [0.15, 0.35, 0.62, 0.9, 1.0, 0.8, 0.55, 0.36, 0.22, 0.12, 0.07]
    bw = 240 / len(heights)
    for i, hh in enumerate(heights):
        f.rect(1170 + i * bw + 2, 215 + 150 - hh * 140, bw - 4, hh * 140, '#dfe9f6', BOX_STROKE, 1.4)
    qx = 1170 + 8.55 * bw
    f.line(qx, 205, qx, 365, CROSS, 2.4, dash='6 4')
    f.text(qx + 6, 222, 'q̂_{1−α}', 19, CROSS, bold=True)
    f.box(1440, 222, 240, 84, ['choose the anchor'], size=20, sub=['θ_{VI} or θ_{MAP}:', 'lower guide NLL wins'], sub_size=16)
    f.arrow([(1290, 395), (1290, 428)])
    f.axes(1170, 440, 500, 190, 'y', 'p̂(y | x)')
    level = 0.42
    f.curve(1170, 440, 500, 190, lambda t: 0.92 * bimodal(t, 0.3, 0.68, 0.07, 1.0, 0.75), stroke=BOX_STROKE, sw=2.6)
    # shaded regions where density >= level
    def region(lo, hi):
        pts = [(1170 + t * 500, 440 + 190 - 0.92 * bimodal(t, 0.3, 0.68, 0.07, 1.0, 0.75) * 190) for t in [lo + (hi - lo) * k / 40 for k in range(41)]]
        d = f'M{pts[0][0]:.1f} {440+190-level*190:.1f}' + ''.join(f'L{x:.1f} {y:.1f}' for x, y in pts) + f'L{pts[-1][0]:.1f} {440+190-level*190:.1f}Z'
        f.path(d, fill='#f2b8b1', stroke='none', opacity=0.85)
    region(0.21, 0.39); region(0.586, 0.765)
    f.line(1170, 440 + 190 - level * 190, 1670, 440 + 190 - level * 190, CROSS, 2, dash='6 4')
    f.text(1662, 440 + 190 - level * 190 - 8, 'level e^{−q̂}', 17, CROSS, 'end')
    f.text(1400, 475, 'SCOPE region = {y : −log p̂(y | x) ≤ q̂}', 18, INK, 'middle')
    f.text(1400, 500, 'follows every mode, skips low-density gaps', 16, GRAY, 'middle')
    f.box(1170, 680, 240, 70, 'SCOPE', size=20, sub='asymptotic coverage ≥ 1−α', sub_size=16)
    f.box(1440, 680, 240, 70, 'SCOPE/Split', size=20, sub='finite-sample validity', sub_size=16)

    f.bracket(30, 640, 812, 'Stage 1 · guide', 'score gradients pick r directions; no MCMC yet')
    f.bracket(660, 1120, 812, 'Stage 2 · sample', 'MCMC only where it matters; VI elsewhere')
    f.bracket(1140, 1690, 812, 'Stage 3 · calibrate', 'conformal quantile sets the density level')
    f.save('scope-figure')


# ---------------------------------------------------------------------------
def fig_fbnn():
    f = SVG(1700, 900)
    f.stage(30, 1, 'Calibrate: a short exploratory run')
    f.stage(580, 2, 'Emulate the posterior map')
    f.stage(1130, 3, 'Sample with the emulator')
    f.vsep(568); f.vsep(1118)
    f.panel(30, 72, 530, 104, 'Calibration (a few hundred samples)', [
        'SGHMC (mini-batch gradients) explores the weights θ ∈ ℝ^{d}',
        'collect pairs (θ_{j}, log π(θ_{j} | D)) near the posterior mode'], size=16)
    f.panel(580, 72, 530, 104, 'Emulator (a neural network)', [
        'train Ĥ(θ) ≈ log π(θ | D) on the calibration pairs',
        'one forward pass replaces a full pass over the data'], size=16)
    f.panel(1130, 72, 560, 104, 'Sampling (preconditioned Crank–Nicolson)', [
        'dimension-robust proposal θ′ = √(1−β²) θ + β ξ,  ξ ~ N(0, C)',
        'accept or reject with the emulated log-posterior Ĥ'], size=16)

    # stage 1
    f.rect(40, 210, 250, 170, '#fff', SEP, 1.5, 10)
    f.text(60, 240, 'Bayesian neural network', 19, INK, bold=True)
    f.net(80, 250, [3, 4, 4, 1], 60, 110)
    f.text(165, 372, 'weights θ ~ posterior π(θ | D)', 16, GRAY, 'middle')
    f.arrow([(165, 382), (165, 416)])
    f.box(40, 418, 250, 54, 'SGHMC', size=21, sub='stochastic-gradient HMC', sub_size=15)
    f.arrow([(290, 445), (330, 445)])
    f.axes(340, 230, 210, 210)
    f.contours(445, 335, 88, 48, -32)
    scatter_in_ellipse(f, 445, 335, 88, 48, -32, disc_points(26, 11, 0.85), '#9fc5e8', BLUE)
    f.text(445, 470, 'calibration samples θ_{j}', 18, INK, 'middle')
    f.text(445, 494, 'with their log-posterior values', 16, GRAY, 'middle')
    f.rect(40, 540, 510, 150, '#fff', SEP, 1.5, 10)
    f.text(60, 572, 'Why a short run is enough', 20, INK, bold=True)
    f.lines(60, 604, ['The exploratory samples only need to cover the high-density region:',
                      'they are the emulator’s training data and give the sampler a',
                      'well-placed starting point.'], 17, lh=25)

    # stage 2
    f.arrow([(550, 335), (590, 335)])
    f.rect(600, 210, 270, 300, '#fff', SEP, 1.5, 10)
    f.text(735, 240, 'Emulator network', 19, INK, bold=True, anchor='middle')
    f.text(620, 300, 'θ', 22, INK)
    f.net(650, 255, [6, 5, 5, 1], 60, 200, fill=META_FILL, stroke=META_STROKE)
    f.text(848, 360, 'Ĥ(θ)', 20, META_STROKE, bold=True)
    f.text(735, 495, 'trained on the calibration pairs', 16, GRAY, 'middle')
    f.axes(910, 230, 190, 190, 'true log π(θ | D)')
    f.text(1005, 222, 'emulated Ĥ(θ) vs. true', 15, GRAY, 'middle')
    f.line(910, 420, 1100, 230, GRAY, 1.6, dash='5 5')
    for (u, v) in [(0.08, 0.1), (0.18, 0.2), (0.27, 0.25), (0.34, 0.36), (0.42, 0.4), (0.5, 0.52), (0.58, 0.57), (0.66, 0.68), (0.73, 0.71), (0.8, 0.82), (0.9, 0.89), (0.95, 0.96)]:
        f.circle(910 + u * 190, 420 - v * 190, 4.2, '#d5a6bd', '#8e4a6b', 1.2)
    f.text(1005, 470, 'emulated ≈ true', 18, INK, 'middle')
    f.box(600, 560, 500, 66, 'cheap surrogate of the posterior', size=20, sub='one forward pass instead of a pass over the data', sub_size=15)
    f.arrow([(1100, 593), (1140, 593)])

    # stage 3
    f.box(1150, 215, 230, 60, 'pCN proposal θ′', size=20, sub='dimension-robust', sub_size=15)
    f.arrow([(1265, 275), (1265, 312)])
    f.box(1150, 314, 230, 60, 'accept / reject', size=20, sub='with Ĥ(θ′), not the data', sub_size=15)
    f.arrow([(1150, 344), (1130, 344), (1130, 245), (1148, 245)])
    f.axes(1410, 220, 260, 200)
    f.contours(1540, 320, 108, 54, -32)
    scatter_in_ellipse(f, 1540, 320, 108, 54, -32, disc_points(110, 23, 0.72), '#9fc5e8', BLUE, r=3.4)
    f.text(1540, 452, 'posterior samples, fast', 18, INK, 'middle')
    f.axes(1150, 520, 520, 170, 'input (first principal component)', 'output')
    def mean(t): return 0.25 + 0.45 * t + 0.08 * math.sin(9 * t)
    band = 'M' + 'L'.join(f'{1150+t*520:.1f} {520+170-(mean(t)+0.16+0.05*math.sin(5*t))*170:.1f}' for t in [k / 60 for k in range(61)])
    band += 'L' + 'L'.join(f'{1150+t*520:.1f} {520+170-(mean(t)-0.16-0.05*math.cos(4*t))*170:.1f}' for t in [k / 60 for k in range(60, -1, -1)]) + 'Z'
    f.path(band, fill='#dfe9f6', stroke='none', opacity=0.95)
    f.curve(1150, 520, 520, 170, mean, stroke=BOX_STROKE, sw=2.4, dash='7 5')
    f.curve(1150, 520, 520, 170, lambda t: mean(t) + 0.06 * math.sin(23 * t) * math.exp(-((t - 0.5) ** 2) / 0.2), stroke=CROSS, sw=2.2)
    f.line(1175, 545, 1205, 545, CROSS, 2.2); f.text(1212, 550, 'true output', 15, GRAY)
    f.line(1320, 545, 1350, 545, BOX_STROKE, 2.4, dash='7 5'); f.text(1357, 550, 'FBNN mean', 15, GRAY)
    f.rect(1470, 536, 30, 16, '#dfe9f6', 'none'); f.text(1507, 550, '95% credible band', 15, GRAY)
    f.text(1410, 745, 'accuracy and uncertainty match the full BNN at a fraction of the cost', 16, GRAY, 'middle')

    f.bracket(30, 560, 812, 'Calibrate', 'short MCMC run collects training pairs')
    f.bracket(580, 1110, 812, 'Emulate', 'a network learns θ ↦ log-posterior')
    f.bracket(1130, 1690, 812, 'Sample', 'pCN with the emulator in the loop')
    f.save('fbnn-figure')


# ---------------------------------------------------------------------------
def fig_crossgraph():
    f = SVG(1700, 900)
    f.stage(30, 1, 'Record and build graphs')
    f.stage(580, 2, 'Select nodes per animal')
    f.stage(1080, 3, 'Align across animals, decode')
    f.vsep(568); f.vsep(1068)
    f.panel(30, 72, 530, 104, 'Data: CA1 local field potentials, five rats', [
        'odor-sequence task; one trial = one collection of five graphs',
        'nodes = electrodes (vary per animal), edges = connectivity'], size=16)
    f.panel(580, 72, 480, 104, 'Graph transformer per animal', [
        'attention ranks nodes; keep those above τ',
        'with induced edges; no shared node identities needed'], size=16)
    f.panel(1080, 72, 610, 104, 'Meta-graph alignment (parameter-free links)', [
        'similarity links join selected nodes across animals (no correspondences)',
        'shared transformer decodes the odor; selections are inspectable'], size=16)

    # stage 1: task strip
    f.text(40, 226, 'odor sequence', 18, INK, bold=True)
    for i, (ch, col) in enumerate(zip('ABCDE', ['#6fa8dc', '#93c47d', '#f6b26b', '#d5a6bd', '#f1d56a'])):
        f.circle(190 + i * 56, 220, 17, col, INK, 1.6)
        f.text(190 + i * 56, 227, ch, 18, INK, 'middle', bold=True)
    f.text(480, 226, 'per trial', 16, GRAY)
    f.text(40, 258, 'each odor presentation is one recorded trial', 15, GRAY)
    names = ['SuperChris', 'Stella', 'Barat', 'Mitt', 'Buchanan']
    centers = [(120, 400), (300, 400), (480, 400), (210, 610), (390, 610)]
    for (gname, g, (cx, cy), (fill, stroke)) in zip(names, GRAPHS5, centers, SRC):
        f.graph(cx, cy, 66, g['nodes'], g['edges'], fill, stroke, mode='plain', d=14, edge_sw=1.8)
        f.text(cx, cy + 96, gname, 17, INK, 'middle', bold=True)
        f.text(cx, cy + 115, f'{len(g["nodes"])} electrodes', 14, GRAY, 'middle')
    f.text(300, 760, 'five graphs with different node sets, recorded separately', 16, GRAY, 'middle')

    # stage 2
    f.arrow([(560, 400), (600, 400)])
    f.box(600, 215, 210, 96, ['GAT layers × 4'], size=20, sub=['depth-mixed attention', 'per animal, own encoder'], sub_size=15)
    f.arrow([(705, 311), (705, 345)])
    f.box(600, 347, 210, 56, 'node scores s_{u}', size=20, sub='keep u if s̃_{u} ≥ τ', sub_size=15)
    sel = [(690, 520), (870, 520), (780, 690)]
    for (g, (cx, cy), (fill, stroke)) in zip(GRAPHS5[:3], sel, SRC[:3]):
        f.graph(cx, cy, 62, g['nodes'], g['edges'], fill, stroke, keep=g['keep'], mode='select', d=14)
    f.text(960, 470, 'kept node', 15, GRAY); f.circle(945, 465, 6, SRC[0][0], SRC[0][1], 1.8)
    f.text(960, 496, 'dropped node', 15, GRAY); f.circle(945, 491, 5, '#fff', LIGHT, 1.6)
    f.text(960, 522, 'inherited edge', 15, GRAY); f.line(936, 517, 954, 517, INK, 2.2)
    f.text(1010, 600, 'selected', 15, GRAY, 'middle'); f.text(1010, 620, 'supernodes', 15, GRAY, 'middle')
    f.text(1010, 640, 'keep their own', 15, GRAY, 'middle'); f.text(1010, 660, 'edges', 15, GRAY, 'middle')

    # stage 3: meta graph
    f.arrow([(1040, 520), (1090, 520)])
    f.rect(1100, 205, 580, 330, META_FILL, META_STROKE, 2, 12)
    f.text(1120, 236, 'meta-graph  G_{M} = (S_{M}, E_{M})', 20, INK, bold=True)
    mcenters = [(1190, 345), (1330, 300), (1480, 330), (1600, 410), (1290, 450)]
    kept_pos = []
    for (g, (cx, cy), (fill, stroke)) in zip(GRAPHS5, mcenters, SRC):
        pos = f.graph(cx, cy, 48, g['nodes'], g['edges'], fill, stroke, keep=g['keep'], mode='kept', d=13)
        kept_pos.append([pos[i] for i in sorted(g['keep'])])
    links = [(0, 1, 1, 0), (1, 2, 2, 1), (2, 3, 0, 2), (0, 4, 3, 1), (4, 2, 2, 3), (1, 4, 3, 0), (3, 4, 1, 2), (0, 2, 2, 0)]
    for (ga, gb, ia, ib) in links:
        (x1, y1), (x2, y2) = kept_pos[ga][ia % len(kept_pos[ga])], kept_pos[gb][ib % len(kept_pos[gb])]
        f.line(x1, y1, x2, y2, CROSS, 2, dash='6 4')
    f.line(1120, 512, 1150, 512, CROSS, 2, dash='6 4'); f.text(1158, 517, 'cross-animal link (similarity ≥ γ)', 15, GRAY)
    f.line(1430, 512, 1460, 512, INK, 2.4); f.text(1468, 517, 'within-animal edge', 15, GRAY)
    f.arrow([(1390, 535), (1390, 568)])
    f.box(1100, 570, 300, 70, ['meta-graph transformer'], size=20, sub='mean pooling → collection label', sub_size=15)
    f.arrow([(1400, 605), (1430, 605)])
    f.rect(1432, 570, 248, 70, '#fff', BOX_STROKE, 2, 9)
    f.text(1556, 596, 'decoded odor', 17, GRAY, 'middle')
    for i, (ch, col) in enumerate(zip('ABCDE', ['#6fa8dc', '#93c47d', '#f6b26b', '#d5a6bd', '#f1d56a'])):
        x = 1476 + i * 40
        if ch == 'C':
            f.circle(x, 620, 15, col, INK, 2.4)
        else:
            f.circle(x, 620, 12, col, '#fff', 1, opacity=0.35)
        f.text(x, 626, ch, 15, INK, 'middle', bold=True)
    f.rect(1100, 662, 580, 110, '#fff', SEP, 1.5, 10)
    f.text(1120, 690, 'interpretation: how often each electrode is selected', 18, INK, bold=True)
    for i in range(12):
        t = i / 11
        col = f'rgb({int(250-120*t)},{int(240-150*t)},{int(190-120*t)})'
        f.circle(1140 + i * 44, 735, 8 + 6 * t, col, '#5a4a7a', 1.4)
    f.text(1140, 766, 'proximal CA1', 14, GRAY, 'middle'); f.text(1624, 766, 'distal CA1', 14, GRAY, 'middle')
    f.text(1382, 766, 'selection frequency rises toward distal CA1 in every animal', 14, GRAY, 'middle')

    f.bracket(30, 560, 812, 'Record', 'heterogeneous graphs, one per animal')
    f.bracket(580, 1060, 812, 'Select', 'attention keeps informative electrodes')
    f.bracket(1080, 1690, 812, 'Align · Decode · Interpret', 'shared meta-graph, one prediction, inspectable structure')
    f.save('crossgraph-figure')


# ---------------------------------------------------------------------------
def fig_polaris():
    f = SVG(1700, 900)
    f.stage(30, 1, 'Normalize', 28)
    f.stage(390, 2, 'Plan (typed)', 28)
    f.stage(900, 3, 'Execute (governed)', 28)
    f.stage(1410, 4, 'Reconcile', 28)
    f.vsep(378); f.vsep(888); f.vsep(1398)
    f.panel(30, 72, 340, 104, 'Input normalizer agent', [
        'prompt, trigger or document →', 'one canonical typed record'], size=16)
    f.panel(390, 72, 490, 104, 'Typed plan synthesis', [
        'planner proposes several type-checked DAGs',
        'rubric-guided reasoning selects one compliant plan'], size=16)
    f.panel(900, 72, 490, 104, 'Validated execution', [
        'validator gates, bounded repair, compiled guardrails',
        'only the agents the plan requires are invoked'], size=16)
    f.panel(1410, 72, 280, 104, 'Decision-grade outputs', [
        'decision + rationale, report,', 'and full execution trace'], size=16)

    # stage 1
    for i, lab in enumerate(['prompt', 'trigger', 'PDF invoice']):
        f.chip(40, 230 + i * 62, 130, 42, lab, '#fff', PANEL_STROKE, 17, bold=False)
        f.arrow([(170, 251 + i * 62), (205, 251 + i * 62), (205, 313), (214, 313)] if i != 1 else [(170, 313), (214, 313)])
    f.box(216, 280, 150, 66, 'Input', size=19, sub='Normalizer', sub_size=17)
    f.arrow([(291, 346), (291, 400)])
    f.rect(40, 402, 326, 200, '#fff', BOX_STROKE, 1.8, 9)
    f.text(56, 430, 'typed record', 17, INK, bold=True)
    f.lines(56, 460, ['{ vendor: "ACME Supplies",', '  invoice_date: 2025-03-31,', '  total: 1240.00, currency: USD,',
                      '  line_items: [7], due_in_days: 30 }'], 15, lh=24, mono=True, color='#2f3a44')
    f.text(56, 582, 'schema-checked before planning', 15, GRAY)

    # stage 2
    f.box(400, 218, 170, 60, 'CoA Planner', size=19, sub='proposes K plans', sub_size=15)
    f.arrow([(570, 248), (598, 248)])
    plans = [('Plan 1', ['Parse', 'Validate', 'Policy', 'Approve'], False),
             ('Plan 2', ['Parse', 'Validate', 'Anomaly', 'Approve'], True),
             ('Plan 3', ['Parse', 'Match', 'Validate', 'Approve'], False)]
    for i, (pn, chain, chosen) in enumerate(plans):
        y = 205 + i * 86
        f.rect(600, y, 280, 70, '#fff', BOX_STROKE if chosen else PANEL_STROKE, 2.6 if chosen else 1.6, 8)
        f.text(614, y + 24, pn, 15, INK, bold=True)
        for k, step in enumerate(chain):
            x = 614 + k * 64
            f.rect(x, y + 36, 54, 22, BOX_FILL, BOX_STROKE, 1.3, 4)
            f.text(x + 27, y + 51, step, 10.5, INK, 'middle')
            if k < 3: f.arrow([(x + 54, y + 47), (x + 63, y + 47)], INK, 1.4)
        if chosen:
            f.circle(862, y + 18, 12, GREEN, GREEN); f.path(f'M{855} {y+18}l5 5l10 -11', stroke='#fff', sw=2.6)
        if i == 0: f.text(740, y - 6, 'type-checked DAGs', 12, GRAY, 'middle')
    f.arrow([(740, 463), (740, 498)])
    f.box(400, 500, 480, 62, 'Reasoning agent', size=19, sub='rubric: completeness · policy fit · cost → one compliant plan', sub_size=15)
    f.rect(400, 590, 480, 46, '#fff', SEP, 1.5, 8)
    f.text(640, 619, 'each edge: output schema of one node matches the input of the next', 14, GRAY, 'middle')
    f.arrow([(880, 531), (912, 531)])

    # stage 3
    f.box(920, 215, 190, 56, 'Document Parser', size=18)
    f.box(1190, 215, 190, 56, 'Data Validator', size=18)
    f.arrow([(1110, 232), (1188, 232)])
    f.arrow([(1188, 254), (1110, 254)], ORANGE, 2.4)
    f.text(1150, 300, 'bounded repair loop', 15, ORANGE, 'middle', bold=True)
    f.text(1150, 320, '≤ k attempts, targeted feedback', 14, GRAY, 'middle')
    f.arrow([(1285, 271), (1285, 345)])
    f.text(1296, 318, 'validated', 14, GRAY)
    procs = ['Policy Retrieval', 'Anomaly Detection', 'Record Matching', 'Risk Control']
    for i, p in enumerate(procs):
        x = 920 + (i % 2) * 235; y = 348 + (i // 2) * 62
        f.box(x, y, 220, 48, p, size=17, bold=False)
    f.text(1150, 478, 'only the processors the plan requires run, in parallel where the DAG allows', 13.5, GRAY, 'middle')
    f.rect(920, 500, 455, 48, '#fbe9e5', CROSS, 1.8, 8)
    f.text(1147, 523, 'compiled policy guardrails', 16, CROSS, 'middle', bold=True)
    f.text(1147, 541, 'block or route side effects before they occur', 13.5, '#7a3b33', 'middle')
    f.arrow([(1147, 548), (1147, 578)])
    f.box(920, 580, 455, 52, 'Approval agent', size=18, sub='decision with rationale', sub_size=14)
    f.arrow([(1375, 606), (1412, 606)])

    # stage 4
    for i, (lab, sub) in enumerate([('Decision + rationale', 'approve, hold or route'), ('Structured report', 'decision-grade artifact'), ('Execution trace', 'every step, prompt and check')]):
        f.box(1420, 215 + i * 84, 260, 66, lab, size=18, sub=sub, sub_size=14)
    f.rect(1420, 480, 260, 150, '#fff', SEP, 1.5, 10)
    f.text(1436, 508, 'Initial benchmark', 17, INK, bold=True)
    f.lines(1436, 538, ['micro-F1 0.81 on SROIE', 'anomaly routing precision', '0.95–1.00 (synthetic suite)', 'with preserved audit trails'], 15, lh=23, color='#2f3a44')

    f.bracket(30, 370, 812, 'Normalize', 'one typed record')
    f.bracket(390, 880, 812, 'Typed planning', 'K candidate DAGs → one compliant plan')
    f.bracket(900, 1390, 812, 'Governed execution', 'validation, bounded repair, guardrails')
    f.bracket(1410, 1690, 812, 'Reconcile', 'auditable outputs')
    f.save('polaris-figure')


# ---------------------------------------------------------------------------
def fig_aema():
    f = SVG(1700, 900)
    f.stage(270, 1, 'Plan', 28)
    f.stage(640, 2, 'Refine', 28)
    f.stage(960, 3, 'Evaluate each step', 28)
    f.stage(1410, 4, 'Report', 28)
    f.vsep(258); f.vsep(628); f.vsep(948); f.vsep(1398)
    f.panel(270, 72, 350, 104, 'Planning agent', [
        'turns the specification into an executable', 'evaluation plan: steps, metrics, rubrics'], size=16)
    f.panel(640, 72, 300, 104, 'Prompt-refinement agent', [
        'retrieves exemplars, sets parameters', 'and few-shot prompts per step'], size=16)
    f.panel(960, 72, 430, 104, 'Evaluation agents (process-aware)', [
        'score the intermediate actions of the workflow', 'under test, not only its final response'], size=16)
    f.panel(1410, 72, 280, 104, 'Final report agent', [
        'aggregates scores and evidence', 'auditable, reproducible report'], size=16)

    # human input column
    f.rect(30, 72, 220, 104, '#fff', SEP, 1.5, 10)
    f.text(44, 104, 'Human evaluator', 20, INK, bold=True)
    f.lines(44, 134, ['business context', 'evaluation specification'], 17)
    f.box(40, 300, 200, 110, ['evaluation', 'request'], size=20, sub='context + spec', sub_size=15)
    f.arrow([(240, 355), (288, 355)])

    # stage 1
    f.box(290, 320, 320, 70, 'Planning Agent', size=20, sub='plans the evaluation', sub_size=15)
    f.arrow([(450, 390), (450, 422)])
    f.rect(290, 424, 320, 176, '#fff', BOX_STROKE, 1.8, 9)
    f.text(306, 452, 'evaluation plan', 17, INK, bold=True)
    f.lines(306, 482, ['step 1 · intent parsing — rubric R1', 'step 2 · tool call — schema check', 'step 3 · retrieval — grounding', 'step 4 · final answer — accuracy, policy'], 15, lh=26, color='#2f3a44')
    f.arrow([(610, 512), (658, 512)])

    # stage 2
    f.box(660, 320, 270, 70, 'Prompt-Refinement', size=20, sub='Agent', sub_size=17)
    f.arrow([(795, 390), (795, 422)])
    f.rect(660, 424, 270, 176, '#fff', BOX_STROKE, 1.8, 9)
    f.text(676, 452, 'per-step evaluation setup', 17, INK, bold=True)
    f.lines(676, 482, ['retrieved exemplars', 'parameters and thresholds', 'few-shot judge prompts', 'seeds for reproducibility'], 15, lh=26, color='#2f3a44')
    f.arrow([(930, 512), (978, 512)])

    # stage 3: workflow under test with score badges
    f.text(980, 232, 'workflow under test', 16, GRAY)
    steps = [('Agent A', 0.9), ('Agent B', 0.6), ('Agent C', 1.0), ('output', 0.8)]
    for i, (name, score) in enumerate(steps):
        x = 980 + i * 104
        f.box(x, 250, 90, 48, name, fill='#fff', stroke=PANEL_STROKE, size=15, bold=False)
        if i < 3: f.arrow([(x + 90, 274), (x + 102, 274)], sw=2)
        col = GREEN if score >= 0.8 else ORANGE
        f.circle(x + 45, 330, 17, '#fff', col, 2.4)
        f.text(x + 45, 336, f'{score:.1f}', 14, col, 'middle', bold=True)
        f.arrow([(x + 45, 368), (x + 45, 349)], col, 1.8)
    f.box(980, 370, 400, 62, 'Evaluation Agents', size=19, sub='one judge per step, rubric-driven', sub_size=15)
    f.arrow([(1180, 432), (1180, 462)])
    f.rect(980, 464, 400, 136, '#fff', BOX_STROKE, 1.8, 9)
    f.text(996, 492, 'step-level scores and feedback', 17, INK, bold=True)
    f.lines(996, 522, ['step 2 → 0.6: required field missing in tool call', 'step 3 → 1.0: answer grounded in retrieved record', 'every score carries evidence and a rationale'], 14.5, lh=25, color='#2f3a44')
    f.arrow([(1380, 532), (1418, 532)])

    # stage 4
    f.box(1420, 320, 260, 70, 'Final Report Agent', size=19, sub='aggregates and signs off', sub_size=15)
    f.arrow([(1550, 390), (1550, 422)])
    f.rect(1420, 424, 260, 176, '#fff', BOX_STROKE, 1.8, 9)
    f.text(1436, 452, 'auditable report', 17, INK, bold=True)
    f.lines(1436, 482, ['aggregate score 0.83', 'per-step evidence and feedback', 'prompts, parameters, seeds', 'reproducible run record'], 15, lh=26, color='#2f3a44')
    # stability chart
    f.rect(1420, 625, 260, 150, '#fff', SEP, 1.5, 10)
    f.text(1436, 652, 'final score over repeated runs', 15, INK, bold=True)
    f.axes(1440, 665, 220, 90)
    f.rect(1470, 680, 60, 12, BOX_STROKE, BOX_STROKE, 1, 2); f.line(1460, 686, 1540, 686, BOX_STROKE, 1.4)
    f.rect(1580, 672, 60, 44, '#f6c9a8', ORANGE, 1.4, 2); f.line(1565, 694, 1655, 694, ORANGE, 1.4)
    f.text(1500, 740, 'AEMA', 14, BOX_STROKE, 'middle', bold=True); f.text(1610, 740, 'single judge', 14, ORANGE, 'middle', bold=True)
    f.text(1550, 768, 'lower dispersion, closer to human judgment', 13, GRAY, 'middle')

    # oversight loop
    f.arrow([(1550, 600), (1550, 612)], sw=0.1)
    f.path('M1680 512H1690V790H140V415', stroke=GRAY, sw=2, dash='8 6')
    f.arrow([(140, 416), (140, 412)], GRAY, 2)
    f.text(900, 782, 'human oversight: review, override, re-plan', 16, GRAY, 'middle')

    f.bracket(30, 250, 812, 'Request', 'context and spec')
    f.bracket(270, 620, 812, 'Plan', 'executable evaluation plan')
    f.bracket(640, 940, 812, 'Refine', 'exemplars and settings')
    f.bracket(960, 1390, 812, 'Evaluate', 'scores for every intermediate action')
    f.bracket(1410, 1690, 812, 'Report', 'auditable, reproducible')
    f.save('aema-figure')


# ---------------------------------------------------------------------------
def fig_strong():
    f = SVG(1700, 900)
    f.stage(30, 1, 'Enroll and follow for one year')
    f.stage(580, 2, 'Genotype and measure outcomes')
    f.stage(1140, 3, 'Model and findings')
    f.vsep(568); f.vsep(1128)
    f.panel(30, 72, 530, 104, 'STRONG: Stroke, Stress, Rehabilitation and Genetics', [
        'prospective 1-year cohort at 28 U.S. stroke centers, 763 adults',
        'covariates: stroke severity, age, sex, ancestry'], title_size=20, size=16)
    f.panel(580, 72, 540, 104, 'Candidate variants and outcomes', [
        'motor/functional: ApoE ε4, BDNF, dopamine polygenic score',
        'stress-related: 7 variants, examined against post-stroke stress'], size=16)
    f.panel(1140, 72, 550, 104, 'Association models', [
        'linear, negative-binomial or Poisson regression per outcome',
        'Holm–Bonferroni correction; replication of GISCOME rs1842681'], size=16)

    # stage 1
    f.rect(40, 215, 250, 170, '#fff', SEP, 1.5, 10)
    f.text(165, 244, '28 U.S. stroke centers', 18, INK, 'middle', bold=True)
    for i in range(28):
        f.circle(70 + (i % 7) * 32, 272 + (i // 7) * 28, 7, '#dfe9f6', BOX_STROKE, 1.6)
    f.arrow([(290, 300), (328, 300)])
    f.box(330, 250, 220, 100, ['763 enrollees'], size=21, sub=['age 63 ± 15 years', 'median NIHSS 4 (IQR 2–9)'], sub_size=15)
    # timeline
    f.line(70, 500, 530, 500, '#9a9a9a', 2.4)
    for i, (lab, n) in enumerate([('baseline', None), ('3 months', 515), ('6 months', 500), ('12 months', 489)]):
        x = 70 + i * 153
        f.circle(x, 500, 9, BOX_FILL, BOX_STROKE, 2)
        f.text(x, 533, lab, 16, INK, 'middle', bold=True)
        if n: f.text(x, 556, f'n = {n}', 15, GRAY, 'middle')
    f.text(300, 455, 'follow-up assessments', 16, GRAY, 'middle')
    f.rect(40, 600, 510, 110, '#fff', SEP, 1.5, 10)
    f.text(60, 630, 'Adjusted for in every model', 18, INK, bold=True)
    f.text(60, 660, 'stroke severity (NIHSS), age, sex, ancestry', 17, '#2f3a44')
    f.text(60, 688, 'stroke subtype explored secondarily', 15, GRAY)

    # stage 2
    f.dna(622, 225, 220, 2.2, 44)
    f.text(622, 475, 'genotyping', 17, INK, 'middle', bold=True)
    f.text(622, 497, 'candidate variants', 14, GRAY, 'middle')
    f.arrow([(660, 300), (688, 300)]); f.arrow([(660, 520), (688, 520)])
    f.rect(692, 215, 420, 180, '#fff', BOX_STROKE, 1.8, 9)
    f.text(708, 243, 'Motor and functional recovery', 17, INK, bold=True)
    f.lines(708, 272, ['ApoE ε4 · BDNF rs6265 · dopamine polygenic score', 'grip-strength change, SIS-ADL, PHQ-8 at 3 months', 't-MoCA cognition at 12 months'], 14.5, lh=24, color='#2f3a44')
    f.text(708, 370, 'plus 3-month mRS for the GISCOME replication', 13.5, GRAY)
    f.rect(692, 430, 420, 200, '#fff', BOX_STROKE, 1.8, 9)
    f.text(708, 458, 'Stress-related outcomes', 17, INK, bold=True)
    f.lines(708, 487, ['5-HTTLPR · ACE · OXTR · FKBP5 · FAAH · BDNF · COMT', 'PTSD (PC-PTSD) and depression (PHQ-8)', 'at 6 and 12 months', 'examined as a function of post-stroke stress'], 14.5, lh=24, color='#2f3a44')
    f.arrow([(1112, 420), (1150, 420)])

    # stage 3: findings
    f.rect(1160, 215, 520, 420, '#fff', SEP, 1.5, 10)
    f.text(1180, 244, 'Findings after correction', 18, INK, bold=True)
    rows = [('BDNF rs6265', 'poorer 12-month cognition: −0.9 t-MoCA, P = 1×10^{−5}', CROSS, -1),
            ('ACE rs4291, FAAH rs324420', 'stress → more 1-year depression and PTSD', CROSS, -1),
            ('COMT rs4680', 'stress → less 1-year depression and PTSD', GREEN, 1),
            ('rs1842681 (GISCOME)', 'replicated: lower 3-month mRS, P = 3.2×10^{−5}', GREEN, 1)]
    for i, (gene, txt, col, sign) in enumerate(rows):
        y = 290 + i * 84
        f.line(1180, y, 1180, y + 50, col, 4)
        f.text(1198, y + 14, gene, 16, INK, bold=True)
        f.text(1198, y + 40, txt, 14.5, '#2f3a44')
        # direction glyph
        f.line(1612, y + 24, 1668, y + 24, '#c9ced3', 1.6)
        f.circle(1640 + 20 * sign, y + 24, 6, col, col)
    f.text(1640, 624, 'direction', 12, GRAY, 'middle')
    f.rect(1160, 655, 520, 110, '#f4f4f4', PANEL_STROKE, 1.8, 10)
    f.text(1180, 684, 'Conclusion', 17, INK, bold=True)
    f.lines(1180, 710, ['genetic susceptibility to PTSD and depression varied with', 'the amount of post-stroke stress, underscoring the role of', 'lived experience in recovery'], 14.5, lh=22, color='#2f3a44')

    f.bracket(30, 560, 812, 'Enroll', 'multicenter 1-year cohort')
    f.bracket(580, 1120, 812, 'Genotype and measure', 'candidate variants, longitudinal outcomes')
    f.bracket(1140, 1690, 812, 'Associate', 'regression with correction and replication')
    f.save('strong-figure')


# ---------------------------------------------------------------------------
OCT_CLASSES = ['normal', 'drusen', 'CNV', 'DME']


def fig_oct():
    f = SVG(1700, 900)
    f.stage(30, 1, 'Few labeled OCT scans')
    f.stage(560, 2, 'Deep triplet network')
    f.stage(1200, 3, 'Detect abnormalities')
    f.vsep(548); f.vsep(1188)
    f.panel(30, 72, 510, 104, 'Limited-data regime', [
        'open-access retinal OCT datasets, few samples per class',
        'standard deep classifiers overfit'], size=16)
    f.panel(560, 72, 620, 104, 'Metric learning with a conditional triplet loss', [
        'a shared VGG16-based encoder embeds anchor, positive, negative',
        'small-sample loss: pull same class together, push others apart'], size=16)
    f.panel(1200, 72, 490, 104, 'Classification in embedding space', [
        'a query scan is embedded and assigned by proximity',
        'higher accuracy than state-of-the-art baselines'], size=16)

    # stage 1: a few scans per class
    for r, cls in enumerate(OCT_CLASSES):
        y = 212 + r * 114
        f.text(40, y + 46, cls, 17, INK, bold=True)
        for c in range(3):
            f.scan(150 + c * 122, y, 108, 82, variant=min(r, 2))
        f.text(508, y + 46, '…', 20, GRAY, 'middle')
    f.text(290, 690, 'few labeled scans per class, not thousands', 16, GRAY, 'middle')

    # stage 2: triplet
    for i, (lab, col, v) in enumerate([('anchor', BLUE, 1), ('positive', GREEN, 1), ('negative', CROSS, 2)]):
        y = 215 + i * 118
        f.scan(580, y, 108, 86, variant=v)
        f.text(634, y + 104, lab, 15, col, 'middle', bold=True)
        f.arrow([(690, y + 43), (740, y + 43), (740, 400), (758, 400)], col, 2)
    f.rect(760, 230, 150, 340, BOX_FILL, BOX_STROKE, 2, 10)
    f.text(835, 262, 'shared', 18, INK, 'middle', bold=True)
    f.text(835, 286, 'encoder', 18, INK, 'middle', bold=True)
    f.net(790, 300, [4, 5, 5, 3], 30, 220, d=9)
    f.text(835, 552, 'VGG16 backbone', 14, GRAY, 'middle')
    f.arrow([(910, 400), (958, 400)])
    f.axes(960, 215, 210, 355, 'embedding space')
    clusters = [((1010, 300), BLUE, 3), ((1120, 280), '#f1d56a', 3), ((1090, 480), CROSS, 3)]
    for (cx, cy), col, n in clusters:
        for k, (dx, dy) in enumerate([(-14, 6), (12, -10), (4, 16)]):
            f.circle(cx + dx, cy + dy, 7, col, col, 1, opacity=0.55)
    ax, ay, px_, py_, nx, ny = 1050, 360, 1010, 300, 1090, 480
    f.circle(ax, ay, 9, '#fff', BLUE, 2.6); f.text(ax + 14, ay + 5, 'a', 15, BLUE, bold=True)
    f.circle(px_, py_ + 22, 9, '#fff', GREEN, 2.6); f.text(px_ - 26, py_ + 28, 'p', 15, GREEN, bold=True)
    f.circle(nx, ny - 30, 9, '#fff', CROSS, 2.6); f.text(nx + 14, ny - 24, 'n', 15, CROSS, bold=True)
    f.arrow([(ax - 8, ay - 8), (px_ + 10, py_ + 30)], GREEN, 2.4)
    f.arrow([(nx - 6, ny - 36), (nx - 28, ny - 56)], CROSS, 2.4)
    f.text(1065, 548, 'pull', 14, GREEN, 'middle', bold=True); f.text(1130, 548, 'push', 14, CROSS, 'middle', bold=True)
    f.box(580, 630, 590, 60, 'conditional triplet loss', size=19, sub='margin between d(a, p) and d(a, n), weighted for the few-sample setting', sub_size=14)

    # stage 3
    f.scan(1220, 230, 120, 94, variant=1, label='query scan')
    f.arrow([(1340, 277), (1380, 277)])
    f.box(1382, 250, 120, 54, 'encoder', size=17, bold=False)
    f.arrow([(1502, 277), (1540, 277)])
    f.axes(1545, 215, 130, 150)
    for (cx, cy), col in [((1575, 250), BLUE), ((1640, 245), '#f1d56a'), ((1620, 330), CROSS)]:
        for (dx, dy) in [(-9, 4), (8, -7), (3, 10)]:
            f.circle(cx + dx, cy + dy, 5, col, col, 1, opacity=0.55)
    f.path('M1615 270l6 10 10 -16 -6 -10z', fill='#fff', stroke=INK, sw=2)
    f.text(1610, 390, 'nearest class wins', 14, GRAY, 'middle')
    f.arrow([(1610, 400), (1610, 436)])
    f.box(1220, 440, 460, 70, ['abnormality label'], size=20, sub='with distances to each class as a confidence cue', sub_size=14)
    f.rect(1220, 560, 460, 130, '#fff', SEP, 1.5, 10)
    f.text(1240, 590, 'Result', 17, INK, bold=True)
    f.lines(1240, 620, ['92.81% accuracy, above published DenseNet, ResNet and', 'Inception baselines (90.4–92.6%); learning distances instead of', 'a direct classifier reduces overfitting on scarce samples'], 14.5, lh=23, color='#2f3a44')

    f.bracket(30, 540, 812, 'Few labels', 'scarce medical images')
    f.bracket(560, 1180, 812, 'Triplet metric learning', 'shared encoder, conditional loss')
    f.bracket(1200, 1690, 812, 'Detect', 'nearest class in embedding space')
    f.save('oct-figure')


# ---------------------------------------------------------------------------
# research-direction illustrations (16:9)
def theme_uncertainty():
    f = SVG(1200, 675)
    f.text(60, 70, 'Bayesian inference, calibrated', 30, INK, bold=True)
    cx, cy = 300, 340
    f.contours(cx, cy, 190, 90, -28)
    f.ellipse(cx, cy, 205, 40, -28, fill=META_FILL, stroke=META_STROKE, sw=1.6, dash='6 4', opacity=0.9)
    ang = math.radians(44); dx, dy = math.cos(ang), math.sin(ang)
    f.line(cx - 150 * dx, cy - 150 * dy, cx + 150 * dx, cy + 150 * dy, CROSS, 3.2)
    for t in (-0.85, -0.62, -0.45, -0.3, -0.15, 0.03, 0.18, 0.32, 0.5, 0.72):
        f.circle(round(cx + 150 * t * dx, 1), round(cy + 150 * t * dy, 1), 8, '#fff', CROSS, 2.6)
    f.text(cx, 560, 'sample only the directions that move the boundary', 19, INK, 'middle')
    f.text(cx, 590, 'projected variational completion elsewhere', 17, GRAY, 'middle')
    f.arrow([(560, 340), (640, 340)], INK, 3.2)
    f.axes(680, 200, 460, 300, 'y', 'p̂(y | x)')
    level = 0.42
    def dens(t): return 0.92 * bimodal(t, 0.3, 0.68, 0.07, 1.0, 0.75)
    def region(lo, hi):
        pts = [(680 + t * 460, 200 + 300 - dens(t) * 300) for t in [lo + (hi - lo) * k / 40 for k in range(41)]]
        d = f'M{pts[0][0]:.1f} {200+300-level*300:.1f}' + ''.join(f'L{x:.1f} {y:.1f}' for x, y in pts) + f'L{pts[-1][0]:.1f} {200+300-level*300:.1f}Z'
        f.path(d, fill='#f2b8b1', stroke='none', opacity=0.85)
    region(0.21, 0.39); region(0.586, 0.765)
    f.curve(680, 200, 460, 300, dens, stroke=BOX_STROKE, sw=3.2)
    f.line(680, 200 + 300 - level * 300, 1140, 200 + 300 - level * 300, CROSS, 2.4, dash='8 5')
    f.text(1132, 200 + 300 - level * 300 - 10, 'conformal level', 17, CROSS, 'end')
    f.text(910, 560, 'prediction region with guaranteed coverage', 19, INK, 'middle')
    f.text(910, 590, 'follows every mode, skips low-density gaps', 17, GRAY, 'middle')
    f.save('theme-uncertainty')


def theme_science():
    f = SVG(1200, 675)
    f.text(60, 70, 'Heterogeneous graphs, one shared structure', 30, INK, bold=True)
    for i, (g, (fill, stroke)) in enumerate(zip(GRAPHS5[:3], SRC[:3])):
        cy = 190 + i * 160
        f.graph(150, cy, 62, g['nodes'], g['edges'], fill, stroke, keep=g['keep'], mode='select', d=15)
        f.arrow([(230, cy), (300, cy), (300, 350), (330, 350)] if i != 1 else [(230, cy), (330, cy)], INK, 2.4)
    f.text(192, 600, 'no shared nodes, no correspondences', 17, GRAY, 'middle')
    f.rect(335, 150, 520, 400, META_FILL, META_STROKE, 2.2, 14)
    f.text(355, 186, 'meta-graph', 22, INK, bold=True)
    mcenters = [(460, 300), (650, 260), (720, 440), (500, 470)]
    kept = []
    for (g, (cx, cy), (fill, stroke)) in zip(GRAPHS5[:4], mcenters, SRC[:4]):
        pos = f.graph(cx, cy, 58, g['nodes'], g['edges'], fill, stroke, keep=g['keep'], mode='kept', d=16)
        kept.append([pos[i] for i in sorted(g['keep'])])
    for (ga, gb, ia, ib) in [(0, 1, 1, 0), (1, 2, 2, 1), (2, 3, 0, 2), (0, 3, 3, 1), (0, 2, 2, 3), (1, 3, 3, 0)]:
        (x1, y1), (x2, y2) = kept[ga][ia % len(kept[ga])], kept[gb][ib % len(kept[gb])]
        f.line(x1, y1, x2, y2, CROSS, 2.4, dash='7 5')
    f.text(595, 600, 'attention selects nodes; similarity links join sources', 17, GRAY, 'middle')
    f.arrow([(860, 350), (930, 350)], INK, 3.2)
    f.box(945, 260, 200, 70, 'prediction', size=22)
    f.box(945, 370, 200, 70, 'interpretation', size=22)
    f.text(1045, 600, 'which nodes and links mattered', 17, GRAY, 'middle')
    f.save('theme-science')


def theme_agents():
    f = SVG(1200, 675)
    f.text(60, 70, 'Plan, govern, verify', 30, INK, bold=True)
    for i, chosen in enumerate([False, True, False]):
        y = 150 + i * 110
        f.rect(60, y, 280, 80, '#fff', BOX_STROKE if chosen else PANEL_STROKE, 3 if chosen else 1.8, 10)
        f.text(80, y + 32, f'typed plan {i+1}', 18, INK, bold=True)
        for k in range(4):
            f.rect(80 + k * 60, y + 46, 44, 18, BOX_FILL, BOX_STROKE, 1.4, 4)
            if k < 3: f.arrow([(124 + k * 60, y + 55), (138 + k * 60, y + 55)], INK, 1.6)
        if chosen:
            f.circle(316, y + 24, 14, GREEN, GREEN); f.path(f'M308 {y+24}l6 6l12 -13', stroke='#fff', sw=3)
    f.text(200, 530, 'type-checked candidate plans, one selected', 17, GRAY, 'middle')
    f.arrow([(345, 300), (410, 300)], INK, 3.2)
    f.box(430, 200, 150, 60, 'parse', size=20)
    f.box(640, 200, 150, 60, 'validate', size=20)
    f.arrow([(580, 220), (638, 220)], INK, 2.4); f.arrow([(638, 242), (580, 242)], ORANGE, 2.4)
    f.text(610, 290, 'bounded repair', 16, ORANGE, 'middle', bold=True)
    f.arrow([(715, 260), (715, 330)], INK, 2.4)
    f.box(430, 332, 150, 54, 'policy', size=18, bold=False); f.box(640, 332, 150, 54, 'anomaly', size=18, bold=False)
    f.rect(430, 410, 360, 44, '#fbe9e5', CROSS, 1.8, 8)
    f.text(610, 438, 'policy guardrails before side effects', 16, CROSS, 'middle', bold=True)
    f.text(610, 530, 'governed execution with a full trace', 17, GRAY, 'middle')
    f.arrow([(800, 300), (860, 300)], INK, 3.2)
    for i, (lab, s) in enumerate([('step 1', 0.9), ('step 2', 0.6), ('step 3', 1.0)]):
        y = 180 + i * 90
        f.box(880, y, 120, 50, lab, fill='#fff', stroke=PANEL_STROKE, size=16, bold=False)
        col = GREEN if s >= 0.8 else ORANGE
        f.circle(1060, y + 25, 20, '#fff', col, 2.8); f.text(1060, y + 31, f'{s:.1f}', 15, col, 'middle', bold=True)
        f.arrow([(1030, y + 25), (1004, y + 25)], col, 1.8)
    f.box(880, 455, 260, 54, 'auditable report', size=18)
    f.text(1010, 530, 'every step scored, every score traceable', 17, GRAY, 'middle')
    f.path('M1140 482H1170V600H36V300', stroke=GRAY, sw=2, dash='8 6')
    f.arrow([(36, 302), (36, 296)], GRAY, 2)
    f.text(640, 630, 'human oversight: review, override, re-plan', 16, GRAY, 'middle')
    f.save('theme-agents')


if __name__ == '__main__':
    fig_scope(); fig_fbnn(); fig_crossgraph(); fig_polaris(); fig_aema(); fig_strong(); fig_oct()
    theme_uncertainty(); theme_science(); theme_agents()
