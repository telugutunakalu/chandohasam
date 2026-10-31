"""A small Markdown → HTML converter for the report (headings, paragraphs, emphasis, code, lists, tables, images, links)."""
import html, re, sys
from pathlib import Path
src = Path(sys.argv[1]).read_text(encoding="utf-8"); out = []
def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)
    t = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1">', t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    return t
lines = src.split("\n"); i = 0; para = []
def flush():
    global para
    if para: out.append("<p>" + inline(" ".join(para)) + "</p>"); para = []
while i < len(lines):
    l = lines[i]
    if l.startswith("```"):
        flush(); j = i + 1; buf = []
        while j < len(lines) and not lines[j].startswith("```"): buf.append(lines[j]); j += 1
        out.append("<pre><code>" + html.escape("\n".join(buf)) + "</code></pre>"); i = j + 1; continue
    m = re.match(r"^(#{1,6})\s+(.*)", l)
    if m: flush(); n = len(m.group(1)); out.append(f"<h{n}>{inline(m.group(2))}</h{n}>"); i += 1; continue
    if l.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|?\s*$", lines[i + 1]):
        flush(); hdr = [c.strip() for c in l.strip().strip("|").split("|")]; rows = []; j = i + 2
        while j < len(lines) and lines[j].startswith("|"): rows.append([c.strip() for c in lines[j].strip().strip("|").split("|")]); j += 1
        out.append("<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in hdr) + "</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table>"); i = j; continue
    m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)", l)
    if m:
        flush(); ordered = m.group(2)[0].isdigit(); items = []; j = i
        while j < len(lines) and (mm := re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)", lines[j])) and (mm.group(2)[0].isdigit() == ordered):
            text = mm.group(3); j += 1
            while j < len(lines) and lines[j].startswith("   ") and not re.match(r"^\s*([-*]|\d+\.)\s", lines[j]): text += " " + lines[j].strip(); j += 1
            items.append(text)
        tag = "ol" if ordered else "ul"; out.append(f"<{tag}>" + "".join(f"<li>{inline(t)}</li>" for t in items) + f"</{tag}>"); i = j; continue
    if l.startswith("!["): flush(); out.append(f'<figure>{inline(l)}</figure>'); i += 1; continue
    if not l.strip(): flush(); i += 1; continue
    para.append(l.strip()); i += 1
flush()
css = """body{font-family:'Noto Sans','DejaVu Sans',sans-serif;font-size:10.5pt;line-height:1.45;color:#0b0b0b;max-width:900px;margin:28px auto;padding:0 24px}
h1{font-size:21pt;margin:0 0 6px}h2{font-size:15pt;margin-top:26px;border-bottom:1px solid #d8d7d2;padding-bottom:3px}h3{font-size:12pt;margin-top:18px}
table{border-collapse:collapse;margin:8px 0;font-size:9pt;width:100%}th,td{border:1px solid #d8d7d2;padding:3px 6px;text-align:left;vertical-align:top}th{background:#f1f0ec}
code{font-family:'DejaVu Sans Mono',monospace;font-size:9pt;background:#f3f2ee;padding:0 3px}pre{background:#f3f2ee;padding:8px;font-size:8.5pt;overflow-x:auto}
img{max-width:100%;height:auto;display:block;margin:10px auto}figure{margin:10px 0}em{color:#52514e}
:lang(te),td,p{font-family:'Noto Sans Telugu','Noto Sans','DejaVu Sans',sans-serif}
@page{size:A4;margin:16mm 14mm}@media print{h2,h3{page-break-after:avoid}figure,img,tr{page-break-inside:avoid}p em{page-break-after:avoid}}"""
Path(sys.argv[2]).write_text(f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>Word resolution for Padyarchana</title><style>{css}</style></head><body>" + "\n".join(out) + "</body></html>", encoding="utf-8")
print("html written", len(out), "blocks")
