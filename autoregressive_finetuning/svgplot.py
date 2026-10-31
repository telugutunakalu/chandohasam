"""A small line-chart writer in plain Python (standard library only): SVG figures with one or more panels.

matplotlib could not be installed on the GB10 (2026-10-18: PyPI downloads kept dropping), so plot_curves.py draws
with this instead. It covers what those figures need: lines (solid, dashed, dotted; transparency; circle and star
markers), vertical reference lines, text annotations, linear or log x axes, titles, axis labels, legends, grids, a
figure title and a footnote.

    fig, axes = subplots(1, 2, size=(1100, 400))
    axes[0].plot([0, 1, 2], [3.0, 2.5, 2.4], color="#1f77b4", label="120M")
    axes[0].set_title("val loss"); axes[0].legend()
    fig.suptitle("..."); fig.save("plots/fig.svg")
"""
from __future__ import annotations

import math
from html import escape
from pathlib import Path

FONT = "DejaVu Sans, Arial, Helvetica, sans-serif"
DASH = {"-": None, "--": "7,4", ":": "2,3", "-.": "7,3,2,3"}


def _nice_ticks(lo: float, hi: float, n: int = 6) -> list[float]:
    if not math.isfinite(lo) or not math.isfinite(hi):
        return []
    if hi <= lo:
        hi = lo + 1.0
    raw = (hi - lo) / max(1, n - 1)
    mag = 10 ** math.floor(math.log10(raw))
    step = next(m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw)
    start = math.ceil(lo / step - 1e-9) * step
    ticks, t = [], start
    while t <= hi + step * 1e-9:
        ticks.append(round(t, 12))
        t += step
    return ticks


def _fmt(v: float) -> str:
    if v == 0:
        return "0"
    a = abs(v)
    if a >= 1e4 or a < 1e-3:
        return f"{v:.0e}".replace("e-0", "e-").replace("e+0", "e")
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    return s


class Axes:
    def __init__(self, x: float, y: float, w: float, h: float):
        self.box = (x, y, w, h)
        self.series: list[dict] = []
        self.vlines: list[dict] = []
        self.notes: list[dict] = []
        self.title = self.xlabel = self.ylabel = ""
        self.xlog = False
        self.show_grid = False
        self.show_legend = False

    # ------------------------------------------------------------- API
    def plot(self, x, y, color: str = "#333333", lw: float = 1.6, ls: str = "-", alpha: float = 1.0,
             marker: str | None = None, ms: float = 3.0, label: str | None = None, line: bool = True) -> None:
        pts = [(float(a), float(b)) for a, b in zip(x, y) if math.isfinite(float(a)) and math.isfinite(float(b))]
        if pts:
            self.series.append(dict(pts=pts, color=color, lw=lw, ls=ls, alpha=alpha, marker=marker, ms=ms,
                                    label=label, line=line))

    def axvline(self, x: float, color: str = "#888888", ls: str = ":", lw: float = 1.0) -> None:
        self.vlines.append(dict(x=float(x), color=color, ls=ls, lw=lw))

    def annotate(self, text: str, xy: tuple[float, float], offset: tuple[float, float] = (4, -8),
                 color: str = "#333333", size: float = 10) -> None:
        self.notes.append(dict(text=text, xy=(float(xy[0]), float(xy[1])), offset=offset, color=color, size=size))

    def set_title(self, s: str) -> None:
        self.title = s

    def set_xlabel(self, s: str) -> None:
        self.xlabel = s

    def set_ylabel(self, s: str) -> None:
        self.ylabel = s

    def set_xscale(self, scale: str) -> None:
        self.xlog = scale == "log"

    def grid(self, on: bool = True) -> None:
        self.show_grid = on

    def legend(self, on: bool = True) -> None:
        self.show_legend = on

    # ------------------------------------------------------------- drawing
    def _tx(self, v: float) -> float:
        return math.log10(v) if self.xlog else v

    def render(self) -> list[str]:
        X, Y, W, H = self.box
        left, right, top, bottom = 62, 12, 26, 44              # room for tick labels, title, axis labels
        px, py, pw, ph = X + left, Y + top, W - left - right, H - top - bottom
        xs = [self._tx(p[0]) for s in self.series for p in s["pts"]] + [self._tx(v["x"]) for v in self.vlines]
        ys = [p[1] for s in self.series for p in s["pts"]]
        out = [f'<rect x="{px:.1f}" y="{py:.1f}" width="{pw:.1f}" height="{ph:.1f}" fill="white" stroke="#444" '
               f'stroke-width="0.8"/>']
        if self.title:
            out.append(_text(px + pw / 2, Y + 16, self.title, size=12, anchor="middle", weight="bold"))
        if not xs or not ys:
            out.append(_text(px + pw / 2, py + ph / 2, "no data", anchor="middle", color="#999"))
            return out
        x0, x1 = min(xs), max(xs)
        y0, y1 = min(ys), max(ys)
        xpad = (x1 - x0) * 0.03 or 0.5
        ypad = (y1 - y0) * 0.08 or abs(y0) * 0.05 or 0.5
        x0, x1, y0, y1 = x0 - xpad, x1 + xpad, y0 - ypad, y1 + ypad
        sx = lambda v: px + (self._tx(v) - x0) / (x1 - x0) * pw
        sy = lambda v: py + ph - (v - y0) / (y1 - y0) * ph
        # ticks and grid
        if self.xlog:
            xt = [10.0 ** e for e in range(math.floor(x0), math.ceil(x1) + 1) if x0 <= e <= x1]
            for e in range(math.floor(x0), math.ceil(x1) + 1):
                for m in (2, 5):
                    v = m * 10.0 ** e
                    if x0 <= math.log10(v) <= x1:
                        out.append(f'<line x1="{sx(v):.1f}" y1="{py + ph:.1f}" x2="{sx(v):.1f}" y2="{py + ph + 3:.1f}" '
                                   f'stroke="#444" stroke-width="0.6"/>')
        else:
            xt = [t for t in _nice_ticks(x0, x1) if x0 <= t <= x1]
        yt = [t for t in _nice_ticks(y0, y1) if y0 <= t <= y1]
        for t in xt:
            X_ = sx(t)
            if self.show_grid:
                out.append(f'<line x1="{X_:.1f}" y1="{py:.1f}" x2="{X_:.1f}" y2="{py + ph:.1f}" stroke="#e3e3e3" '
                           f'stroke-width="0.7"/>')
            out.append(f'<line x1="{X_:.1f}" y1="{py + ph:.1f}" x2="{X_:.1f}" y2="{py + ph + 5:.1f}" stroke="#444" '
                       f'stroke-width="0.8"/>')
            out.append(_text(X_, py + ph + 17, _fmt(t), anchor="middle", size=10))
        for t in yt:
            Y_ = sy(t)
            if self.show_grid:
                out.append(f'<line x1="{px:.1f}" y1="{Y_:.1f}" x2="{px + pw:.1f}" y2="{Y_:.1f}" stroke="#e3e3e3" '
                           f'stroke-width="0.7"/>')
            out.append(f'<line x1="{px - 5:.1f}" y1="{Y_:.1f}" x2="{px:.1f}" y2="{Y_:.1f}" stroke="#444" '
                       f'stroke-width="0.8"/>')
            out.append(_text(px - 8, Y_ + 3.5, _fmt(t), anchor="end", size=10))
        if self.xlabel:
            out.append(_text(px + pw / 2, Y + H - 6, self.xlabel, anchor="middle", size=11))
        if self.ylabel:
            cx, cy = X + 14, py + ph / 2
            out.append(_text(cx, cy, self.ylabel, anchor="middle", size=11, rotate=(-90, cx, cy)))
        # clip to the plotting area
        cid = f"c{abs(hash((X, Y, W, H))) % 10**8}"
        out.append(f'<clipPath id="{cid}"><rect x="{px:.1f}" y="{py:.1f}" width="{pw:.1f}" height="{ph:.1f}"/></clipPath>')
        out.append(f'<g clip-path="url(#{cid})">')
        for v in self.vlines:
            dash = DASH.get(v["ls"])
            out.append(f'<line x1="{sx(v["x"]):.1f}" y1="{py:.1f}" x2="{sx(v["x"]):.1f}" y2="{py + ph:.1f}" '
                       f'stroke="{v["color"]}" stroke-width="{v["lw"]}"' + (f' stroke-dasharray="{dash}"' if dash else "")
                       + "/>")
        for s in self.series:
            pts = " ".join(f"{sx(a):.1f},{sy(b):.1f}" for a, b in s["pts"])
            dash = DASH.get(s["ls"])
            if s["line"] and len(s["pts"]) > 1:
                out.append(f'<polyline points="{pts}" fill="none" stroke="{s["color"]}" stroke-width="{s["lw"]}" '
                           f'stroke-opacity="{s["alpha"]}" stroke-linejoin="round"'
                           + (f' stroke-dasharray="{dash}"' if dash else "") + "/>")
            for a, b in (s["pts"] if s["marker"] else []):
                out.append(_marker(s["marker"], sx(a), sy(b), s["ms"], s["color"], s["alpha"]))
        out.append("</g>")
        for n in self.notes:
            out.append(_text(sx(n["xy"][0]) + n["offset"][0], sy(n["xy"][1]) - n["offset"][1], n["text"],
                             size=n["size"], color=n["color"]))
        if self.show_legend:
            labelled = [s for s in self.series if s["label"]]
            if labelled:
                lw = 26 + 6.2 * max(len(s["label"]) for s in labelled)
                lh = 8 + 15 * len(labelled)
                lx, ly = px + pw - lw - 6, py + 6
                out.append(f'<rect x="{lx:.1f}" y="{ly:.1f}" width="{lw:.1f}" height="{lh:.1f}" fill="white" '
                           f'fill-opacity="0.85" stroke="#bbb" stroke-width="0.6"/>')
                for i, s in enumerate(labelled):
                    yy = ly + 12 + 15 * i
                    dash = DASH.get(s["ls"])
                    if s["line"]:
                        out.append(f'<line x1="{lx + 5:.1f}" y1="{yy - 3:.1f}" x2="{lx + 21:.1f}" y2="{yy - 3:.1f}" '
                                   f'stroke="{s["color"]}" stroke-width="{s["lw"]}" stroke-opacity="{s["alpha"]}"'
                                   + (f' stroke-dasharray="{dash}"' if dash else "") + "/>")
                    if s["marker"]:
                        out.append(_marker(s["marker"], lx + 13, yy - 3, s["ms"], s["color"], s["alpha"]))
                    out.append(_text(lx + 25, yy, s["label"], size=9.5))
        return out


def _marker(kind: str, x: float, y: float, ms: float, color: str, alpha: float) -> str:
    if kind == "*":
        r, pts = ms * 1.6, []
        for k in range(10):
            rr = r if k % 2 == 0 else r * 0.45
            a = math.pi / 2 + k * math.pi / 5
            pts.append(f"{x + rr * math.cos(a):.1f},{y - rr * math.sin(a):.1f}")
        return f'<polygon points="{" ".join(pts)}" fill="{color}" fill-opacity="{alpha}" stroke="black" stroke-width="0.5"/>'
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{ms:.1f}" fill="{color}" fill-opacity="{alpha}"/>'


def _text(x: float, y: float, s: str, size: float = 10, anchor: str = "start", color: str = "#222",
          weight: str = "normal", rotate: tuple | None = None) -> str:
    rot = f' transform="rotate({rotate[0]} {rotate[1]:.1f} {rotate[2]:.1f})"' if rotate else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" text-anchor="{anchor}" '
            f'fill="{color}" font-weight="{weight}"{rot}>{escape(s)}</text>')


class Figure:
    def __init__(self, nrows: int, ncols: int, size: tuple[int, int]):
        self.w, self.h = size
        self.head, self.foot = 0, 0
        self.title = self.footnote = ""
        self.nrows, self.ncols = nrows, ncols
        self.axes = [Axes(0, 0, 0, 0) for _ in range(nrows * ncols)]

    def suptitle(self, s: str) -> None:
        self.title, self.head = s, 26

    def text(self, s: str) -> None:
        self.footnote, self.foot = s, 22

    def save(self, path: str | Path) -> None:
        H = self.h + self.head + self.foot
        cw, ch = self.w / self.ncols, self.h / self.nrows
        for i, ax in enumerate(self.axes):
            r, c = divmod(i, self.ncols)
            ax.box = (c * cw + 4, self.head + r * ch + 2, cw - 8, ch - 4)
        body = [f'<rect width="{self.w}" height="{H}" fill="white"/>']
        if self.title:
            body.append(_text(self.w / 2, 18, self.title, size=13, anchor="middle", weight="bold"))
        for ax in self.axes:
            body += ax.render()
        if self.footnote:
            body.append(_text(self.w / 2, H - 7, self.footnote, size=9.5, anchor="middle", color="#666"))
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{H}" viewBox="0 0 {self.w} {H}">\n'
               + "\n".join(body) + "\n</svg>\n")
        Path(path).write_text(svg, encoding="utf-8")


def subplots(nrows: int = 1, ncols: int = 1, size: tuple[int, int] = (700, 420)):
    fig = Figure(nrows, ncols, size)
    return fig, (fig.axes if nrows * ncols > 1 else fig.axes[0])
