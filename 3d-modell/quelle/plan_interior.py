"""Erzeugt aus den Vektor-Polygonen des Genehmigungsplans die Innenausbau-Daten (Gebaeudekoordinaten X=Ost, Y=Nord)."""
import json, math
from shapely.geometry import Polygon, box, Point, LineString, MultiPolygon
from shapely.ops import unary_union, split
from shapely.geometry.polygon import orient
P = json.load(open('polys.json')); D = json.load(open('door_arcs.json'))
OFF = {'EG':(48.906,29.729),'OG':(9.536,7.308),'DG':(48.907,7.31),'UG':(9.536,29.73)}
L, TOT = 7.95, 20.055
def tf(fl, q):
    ox, oy = OFF[fl]; return Polygon([(py-oy, px-ox) for (px, py) in q]).buffer(0)
def walls(fl, cols):
    return unary_union([tf(fl, q) for c in cols for q in P[fl][c]]).buffer(0)
rotB = lambda g: __import__('shapely.affinity', fromlist=['x']).affine_transform(g, [-1, 0, 0, -1, 8.0, TOT])
innerA = box(0.365, 0.365, 7.635, 7.585); innerB = box(0.365, 12.47, 7.635, 19.69)
bayA = box(1.9, -0.84, 6.1, 0.4); bayB = box(1.05, 19.65, 6.95, 21.77)
mid = box(0.6, 7.95, 7.4, 12.105)
dgA = box(1.14, 1.0, 6.785, 7.73); dgB = rotB(dgA)
REG = {
 'UG': {'all': None},
 'EG': {'A': innerA.union(bayA), 'B': innerB.union(bayB)},
 'OG': {'A': innerA, 'B': innerB, 'M': mid},
 'DG': {'A': dgA, 'B': dgB, 'M': mid},
}
def holes_free(g):
    out = []
    geoms = list(getattr(g, 'geoms', [g]))
    while geoms:
        p = geoms.pop()
        if p.is_empty or p.area < 1e-4: continue
        if p.geom_type != 'Polygon':
            geoms += list(getattr(p, 'geoms', [])); continue
        if len(p.interiors) == 0:
            out.append(p); continue
        hx = Polygon(p.interiors[0]).centroid.x
        parts = split(p, LineString([(hx, -100), (hx, 100)]))
        geoms += list(parts.geoms)
    return [list(orient(q.simplify(0.003), 1.0).exterior.coords)[:-1] for q in out]
res = {}
for fl, regs in REG.items():
    cols = ['gruen', 'rot'] if fl == 'UG' else ['rot']
    W = walls(fl, cols)
    closed = W.buffer(0.55, join_style='mitre').buffer(-0.55, join_style='mitre')
    patches = closed.difference(W).buffer(-0.005).buffer(0.005)
    pl = list(getattr(patches, 'geoms', [patches]))
    for key, reg in regs.items():
        Wr = W if reg is None else W.intersection(reg)
        Wr = Wr.difference(unary_union([box(2.10, 3.70, 2.97, 7.56), box(8 - 2.97, TOT - 7.56, 8 - 2.10, TOT - 3.70)]))
        doors, lintels = [], []
        for a in D[fl]:
            C = Point(a['c'])
            if reg is not None and not reg.buffer(0.05).contains(C): continue
            Wb = W.buffer(0.02)
            pick = None
            for E, Eo in ((a['e1'], a['e2']), (a['e2'], a['e1'])):
                ux, uy = E[0]-a['c'][0], E[1]-a['c'][1]; ln = math.hypot(ux, uy); ux, uy = ux/ln, uy/ln
                beyond = Point(E[0]+ux*0.12, E[1]+uy*0.12)
                mid_ = Point(a['c'][0]+ux*ln/2, a['c'][1]+uy*ln/2)
                if Wb.contains(beyond) and not W.contains(mid_):
                    pick = (E, Eo, ux, uy, ln); break
            if not pick: continue
            E, Eo, ux, uy, ln = pick
            nx, ny = -uy, ux
            near = W.intersection(C.buffer(0.35))
            pts = []
            for gg in getattr(near, 'geoms', [near]):
                if gg.geom_type == 'Polygon': pts += list(gg.exterior.coords)
            if not pts: continue
            tv = [ (q[0]-a['c'][0])*nx + (q[1]-a['c'][1])*ny for q in pts ]
            ta, tb = max(min(tv), -0.4), min(max(tv), 0.4)
            if tb - ta < 0.08: continue
            cx, cy = a['c']
            lq = Polygon([(cx+nx*ta, cy+ny*ta), (cx+ux*(ln+0.02)+nx*ta, cy+uy*(ln+0.02)+ny*ta),
                          (cx+ux*(ln+0.02)+nx*tb, cy+uy*(ln+0.02)+ny*tb), (cx+nx*tb, cy+ny*tb)]).difference(W)
            if reg is not None: lq = lq.intersection(reg)
            if lq.is_empty or lq.area < 0.02: continue
            lintels += holes_free(lq)
            doors.append(dict(h=a['c'], open=Eo, closed=E, r=a['r'], t=[ta, tb]))
        ug_win = []
        if fl == 'UG':
            G = walls('UG', ['gruen'])
            gc = G.buffer(0.6, join_style='mitre').buffer(-0.6, join_style='mitre')
            gp = gc.difference(G).buffer(-0.005).buffer(0.005)
            used = [Polygon(l) for l in lintels]
            for q in getattr(gp, 'geoms', [gp]):
                if q.area < 0.05 or q.area > 1.2: continue
                if any(q.intersects(u) for u in used): continue
                ug_win += holes_free(q)
        res['%s_%s' % (fl, key)] = dict(walls=holes_free(Wr), lintels=lintels, doors=doors, ugwin=ug_win)
        print(fl, key, 'Wandstuecke', len(res['%s_%s' % (fl, key)]['walls']), 'Tueren', len(doors), 'UG-Fenster', len(ug_win))
# Oeffnungen in den Haus-Innenwaenden zum Mittelbau (OG/DG)
op = []
for fl, z0 in (('EG', 0.0), ('OG', 2.96), ('DG', 5.84)):
    W = walls(fl, ['rot'])
    for nm, band in (('A_Nordwand', box(0.4, 7.55, 7.6, 7.95)), ('B_Suedwand', box(0.4, 12.105, 7.6, 12.5))):
        g = band.difference(W)
        for q in getattr(g, 'geoms', [g]):
            if q.is_empty: continue
            x0, y0, x1, y1 = q.bounds
            if x1 - x0 > 0.6 and y1 - y0 > 0.3:
                op.append(dict(fl=fl, wall=nm, x0=round(x0, 3), x1=round(x1, 3), z0=z0))
                print('Oeffnung', fl, nm, round(x0, 2), round(x1, 2), round(y0, 2), round(y1, 2))
res['openings'] = op
G = walls('UG', ['gruen'])
fp = Polygon(G.buffer(0.6, join_style='mitre').buffer(-0.6, join_style='mitre').geoms[0].exterior if hasattr(G.buffer(0.6, join_style='mitre').buffer(-0.6, join_style='mitre'),'geoms') else G.buffer(0.6, join_style='mitre').buffer(-0.6, join_style='mitre').exterior)
parts = [Polygon(g.exterior) for g in getattr(G.buffer(0.6, join_style='mitre').buffer(-0.6, join_style='mitre'), 'geoms', [G.buffer(0.6, join_style='mitre').buffer(-0.6, join_style='mitre')])]
ugfp = unary_union([q for q in parts if q.area > 20])
houses = unary_union([box(0, 0, 8, L), box(1.6, -1.14, 6.4, 0), box(0, 12.105, 8, TOT), box(0.75, TOT, 7.25, TOT + 2.015)])
res['ug_floor'] = holes_free(ugfp)
res['ug_ceiling_extra'] = holes_free(ugfp.difference(houses))
print('UG Grundflaeche m2', round(ugfp.area, 1), 'ausserhalb Haus', round(ugfp.difference(houses).area, 2))
json.dump(res, open('interior.json', 'w'))
