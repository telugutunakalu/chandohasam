"""Drop the duplicate <a:pPr> elements pptxgenjs writes for the 2nd+ run of a paragraph."""
import re, sys, zipfile, shutil, os

src = sys.argv[1]
tmp = src + '.tmp'
P_RE = re.compile(r'<a:p>(.*?)</a:p>', re.S)
PPR_RE = re.compile(r'<a:pPr\b[^>]*?(?:/>|>.*?</a:pPr>)', re.S)

def fix_para(m):
    body = m.group(1)
    seen = [0]
    def keep_first(mm):
        seen[0] += 1
        return mm.group(0) if seen[0] == 1 else ''
    return '<a:p>' + PPR_RE.sub(keep_first, body) + '</a:p>'

removed = 0
with zipfile.ZipFile(src) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename.startswith('ppt/slides/slide') and item.filename.endswith('.xml'):
            text = data.decode('utf-8')
            before = len(PPR_RE.findall(text))
            text = P_RE.sub(fix_para, text)
            removed += before - len(PPR_RE.findall(text))
            data = text.encode('utf-8')
        zout.writestr(item, data)
shutil.move(tmp, src)
print(f'fix_ppr: removed {removed} duplicate pPr elements')
