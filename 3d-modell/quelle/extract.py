import pymupdf, json, sys
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
S = 72/25.4*10   # pt per m at 1:100 = 28.3465
d = pymupdf.open(sys.argv[1]); p = d[0]
REG = {'OG': (0, 72, 1116, 630), 'DG': (1188, 72, 2268, 594), 'UG': (54, 666, 1116, 1260),
       'EG': (1250, 700, 2268, 1250), 'DT': (2304, 720, 3240, 1080)}
COL = {(1.0, 0.0, 0.0): 'rot', (0.45, 0.66, 0.45): 'gruen', (0.0, 0.25, 0.49): 'pv', (0.31, 0.55, 0.75): 'glas'}
out = {k: {c: [] for c in COL.values()} for k in REG}
def subpaths(items):
    cur = []; last = None; res = []
    for it in items:
        if it[0] == 're':
            r = it[1]; res.append([(r.x0, r.y0), (r.x1, r.y0), (r.x1, r.y1), (r.x0, r.y1)]); continue
        if it[0] == 'qu':
            q = it[1]; res.append([(t.x, t.y) for t in (q.ul, q.ur, q.lr, q.ll)]); continue
        a = it[1]; b = it[-1]
        if last is None or abs(a.x - last[0]) > 0.01 or abs(a.y - last[1]) > 0.01:
            if len(cur) >= 3: res.append(cur)
            cur = [(a.x, a.y)]
        cur.append((b.x, b.y)); last = (b.x, b.y)
    if len(cur) >= 3: res.append(cur)
    return res
for x in p.get_drawings():
    f = x.get('fill')
    if not f: continue
    k = tuple(round(v, 2) for v in f)
    if k not in COL: continue
    r = x['rect']
    for reg, (x0, y0, x1, y1) in REG.items():
        if r.x0 >= x0 and r.x1 <= x1 and r.y0 >= y0 and r.y1 <= y1:
            for sp in subpaths(x['items']):
                pg = Polygon(sp).buffer(0)
                if pg.area > 0:
                    out[reg][COL[k]].append([(px / S, py / S) for (px, py) in pg.exterior.coords])
for reg in out:
    for c in out[reg]:
        if out[reg][c]:
            u = unary_union([Polygon(q) for q in out[reg][c]])
            print(reg, c, len(out[reg][c]), 'bbox m:', [round(v, 3) for v in u.bounds])
json.dump(out, open('polys.json', 'w'))
