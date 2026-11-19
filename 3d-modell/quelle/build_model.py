# -*- coding: utf-8 -*-
"""
3D-Modell Neubau Doppelhaus Gerlichstrasse 8, 81245 Muenchen
Grundlage: Genehmigungsplan 01/1 (Grundrisse, Ansichten, Schnitte, M 1:100), Juli 2026

Gebaeude-Koordinaten (vor Nordausrichtung):
  +X = Osten (Fassade "Ansicht Ost" bei X=8.00), +Y = Norden (Laengsachse), +Z = oben
  Z=0  = +-0.00 = 518.70 m u. NN (OK FFB EG)
  Haus A (Sued, Nr. 8): Y 0.00 - 7.95 | Mittelbau: Y 7.95 - 12.105 | Haus B (Nord): Y 12.105 - 20.055
Das Gebaeude ist punktsymmetrisch (Haus B = Haus A um 180 Grad gedreht), Ausnahmen: Erker, Mittelbau, Aussenanlagen.
"""
import bpy, bmesh, math, sys, os
from mathutils import Vector, Matrix
from shapely.geometry import Polygon, box as sbox

V = Vector
OUT = os.environ.get("OUTDIR", "/tmp/out")
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

# ------------------------------------------------------------------ Materialien
def s2l(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

MATS = {}
def mat(key, name, hexcol, rough=0.6, metal=0.0, trans=0.0):
    r, g, b = (int(hexcol[i:i + 2], 16) for i in (1, 3, 5))
    col = (s2l(r), s2l(g), s2l(b), 1.0)
    m = bpy.data.materials.new(name)
    try:
        m.use_nodes = True
    except Exception:
        pass
    bsdf = m.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = col
    bsdf.inputs['Roughness'].default_value = rough
    bsdf.inputs['Metallic'].default_value = metal
    if trans:
        bsdf.inputs['Transmission Weight'].default_value = trans
        bsdf.inputs['IOR'].default_value = 1.5
    m.diffuse_color = col
    MATS[key] = m
    return m

mat('putz',     'Putz_weiss_Fassade',         '#F2F1ED', 0.85)
mat('putzw',    'Putz_weiss_Portal_Attika',   '#F4F3EF', 0.85)
mat('putzg',    'Putz_weiss_Erker',           '#F2F1ED', 0.85)
mat('lisene',   'Lisenen_Eckquaderung',       '#EEECE6', 0.75)
mat('stein',    'Kugeln_Abdeckplatten_Stein', '#F1EFEA', 0.5)
mat('holz',     'Fassadenpaneel_anthrazit',   '#303235', 0.45, 0.35)
mat('holzt',    'Terrassenplatten_Feinsteinzeug', '#BEB9B0', 0.6)
mat('tuer',     'Haustuer_anthrazit',         '#2C2E31', 0.4, 0.4)
mat('alu',      'Alu_anthrazit_RAL7016',      '#3A3D41', 0.4, 0.6)
mat('aluh',     'Alu_anthrazit_Abdeckung',    '#33363A', 0.4, 0.6)
mat('stehfalz', 'Metall_Stehfalz_anthrazit',  '#35383C', 0.4, 0.6)
mat('glas',     'Glas',                       '#EEF4F6', 0.02, 0.0, 1.0)
mat('beton',    'Sichtbeton_Carport',         '#A9A8A2', 0.85)
mat('gruen',    'Gruendach_extensiv',         '#6D7E45', 0.95)
mat('kies',     'Kies_Dach',                  '#A29D94', 0.95)
mat('platten',  'Terrassenplatten_Dach',      '#8E8B85', 0.7)
mat('rasen',    'Rasen',                      '#5E893B', 0.95)
mat('pflaster', 'Pflaster_Fahrspur',          '#A19D96', 0.85)
mat('asphalt',  'Asphalt_Strasse',            '#47494C', 0.9)
mat('gehweg',   'Gehweg',                     '#B2B0AB', 0.85)
mat('innen',    'Innen_Wand_Decke',           '#F3F1EC', 0.92)
mat('boden',    'Parkett_Eiche_hell_Landhausdiele', '#C9AE88', 0.55)
mat('pflanze',  'Pflanzen_Platzhalter',       '#4D7834', 0.9)
mat('pv',       'PV_Module_Glas',             '#1B2533', 0.12, 0.3)
mat('innentuer','Innentuer_weiss_lackiert',   '#F2F1EC', 0.4)
mat('treppe',   'Treppe_Trittstufen_Eiche',   '#B8956A', 0.5)
mat('kueche',   'Kueche_Front_Eiche_geraeuchert', '#4E4237', 0.45)
mat('arbeitsplatte','Marmor_Calacatta',      '#EDE9E3', 0.12)
mat('edelstahl','Edelstahl',                  '#B4B6B8', 0.25, 1.0)
mat('hob',      'Kochfeld_Glaskeramik',       '#151515', 0.08)
mat('eiche',    'Holz_Nussbaum',              '#5B4131', 0.4)
mat('stoff',    'Leder_Cognac',               '#8B5A3A', 0.55)
mat('stoff_hell','Boucle_Sand',                '#D9D0C3', 0.97)
mat('bettwaesche','Bettwaesche_weiss',        '#F3F1EC', 0.9)
mat('schrank',  'Schrank_Eiche_geraeuchert',  '#5A4B3E', 0.45)
mat('keramik',  'Keramik_Sanitaer_weiss',     '#F8F8F6', 0.08)
mat('fliesen',  'Fliesen_Bad_grau',           '#C7C4BE', 0.35)
mat('spiegel',  'Spiegel',                    '#E6E8EA', 0.02, 1.0)
mat('travertin','Travertin',                  '#D8CDBB', 0.6)
mat('bronze',   'Bronze_gebuerstet',          '#8E6B44', 0.35, 1.0)
mat('teppich',  'Teppich_Wolle_Greige',       '#B9B0A2', 0.98)
mat('leuchte',  'Leuchte_Schirm_warm',        '#F3E3C4', 0.5)
mat('kunst1',   'Kunst_Leinwand_Terrakotta',  '#B8754E', 0.9)
mat('kunst2',   'Kunst_Leinwand_Sand',        '#CDBFA6', 0.9)
mat('olive',    'Pflanze_Olive',              '#6F7A52', 0.9)
mat('topf',     'Pflanzgefaess_Beton',        '#8D8A84', 0.85)
mat('hecke',    'Hecke_Formschnitt_Platzhalter', '#3F6B2E', 0.95)
mat('erde',     'Erde_Pflanzbeet',            '#4A3B2E', 0.95)
mat('kontext',  'Kontext_Nachbarbebauung',    '#D8D6D1', 0.9)
mat('kontextd', 'Kontext_Dach',               '#8A6E62', 0.9)
M = MATS

# ------------------------------------------------------------------ Geometrie-Sammler
OBJS = {}      # name -> {'bm','mats','coll'}
def O(name, coll):
    if name not in OBJS:
        OBJS[name] = {'bm': bmesh.new(), 'mats': [], 'coll': coll}
    return OBJS[name]

def mi(o, m):
    if m not in o['mats']:
        o['mats'].append(m)
    return o['mats'].index(m)

FACES = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]

def obox(o, m, org, u, v, n, u0, u1, v0, v1, n0, n1):
    if u1 - u0 < 1e-5 or v1 - v0 < 1e-5 or n1 - n0 < 1e-5:
        return
    bm = o['bm']; idx = mi(o, m)
    P = []
    for c in (n0, n1):
        for b in (v0, v1):
            for a in (u0, u1):
                P.append(org + u * a + v * b + n * c)
    vs = [bm.verts.new(p) for p in P]
    rh = u.cross(v).dot(n) > 0          # FACES ist fuer Rechtssystem nach innen orientiert
    for f in FACES:
        fc = bm.faces.new([vs[i] for i in (f[::-1] if rh else f)]); fc.material_index = idx

X_, Y_, Z_ = V((1, 0, 0)), V((0, 1, 0)), V((0, 0, 1))
O0 = V((0, 0, 0))
def abox(o, m, x0, x1, y0, y1, z0, z1):
    obox(o, m, O0, X_, Y_, Z_, x0, x1, y0, y1, z0, z1)

def prism(o, m, pts, f, t0, t1):
    bm = o['bm']; idx = mi(o, m)
    b = [bm.verts.new(f(a, c, t0)) for (a, c) in pts]
    t = [bm.verts.new(f(a, c, t1)) for (a, c) in pts]
    fs = [bm.faces.new(b[::-1]), bm.faces.new(t)]
    for i in range(len(pts)):
        j = (i + 1) % len(pts)
        fs.append(bm.faces.new([b[i], b[j], t[j], t[i]]))
    cen = sum((vv.co for vv in b + t), V((0, 0, 0))) / (2 * len(pts))
    for fc in fs:
        fc.material_index = idx
        fc.normal_update()
        if (fc.calc_center_median() - cen).dot(fc.normal) < 0:
            fc.normal_flip()

def sphere(o, m, c, r):
    bm = o['bm']; idx = mi(o, m)
    res = bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=r, matrix=Matrix.Translation(c))
    fs = set()
    for vv in res['verts']:
        fs.update(vv.link_faces)
    for fc in fs:
        fc.material_index = idx

def icoblob(o, m, c, r, sx=1.0, sy=1.0, sz=0.8):
    bm = o['bm']; idx = mi(o, m)
    mtx = Matrix.Translation(c) @ Matrix.Diagonal((sx, sy, sz, 1.0))
    res = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=r, matrix=mtx)
    fs = set()
    for vv in res['verts']:
        fs.update(vv.link_faces)
    for fc in fs:
        fc.material_index = idx

def beam(o, m, p0, p1, w, h, up=Z_):
    d = p1 - p0; L = d.length; dn = d.normalized()
    side = dn.cross(up)
    if side.length < 1e-6:
        side = dn.cross(X_)
    side.normalize(); up2 = side.cross(dn).normalized()
    obox(o, m, p0, dn, side, up2, 0, L, -w / 2, w / 2, -h / 2, h / 2)

CUTN = {}
def cutbox(coll, m, org, u, v, n, u0, u1, v0, v1, n0, n1):
    k = CUTN.get(coll, 0); CUTN[coll] = k + 1
    obox(O('%s_%03d' % (coll, k), coll), m, org, u, v, n, u0, u1, v0, v1, n0, n1)

def cutprism(coll, m, pts, f, t0, t1):
    k = CUTN.get(coll, 0); CUTN[coll] = k + 1
    prism(O('%s_%03d' % (coll, k), coll), m, pts, f, t0, t1)

def intervals_minus(a, b, holes):
    segs = [(a, b)]
    for (h0, h1) in holes:
        new = []
        for (s0, s1) in segs:
            if h1 <= s0 or h0 >= s1:
                new.append((s0, s1)); continue
            if h0 > s0: new.append((s0, h0))
            if h1 < s1: new.append((h1, s1))
        segs = new
    return [s for s in segs if s[1] - s[0] > 0.03]

def clad(o, m, org, u, v, n, u0, u1, v0, v1, holes=(), n0=0.0, depth=0.022,
         bh=0.125, gap=0.012, ustart=None, uend=None):
    """horizontale Stuelpschalung/Rhombus-Lattung: Bretter entlang u, Reihen entlang v"""
    vb = v0
    while vb < v1 - 0.02:
        vt = min(vb + bh, v1)
        a = u0 if ustart is None else max(u0, ustart(vt))
        b = u1 if uend is None else min(u1, uend(vt))
        hs = [(h[0], h[1]) for h in holes if h[2] < vt and h[3] > vb]
        for (s0, s1) in intervals_minus(a, b, hs):
            obox(o, m, org, u, v, n, s0, s1, vb, vt, n0, n0 + depth)
        vb += bh + gap

def seams(o, m, org, u, v, n, u0, u1, v0, v1, holes=(), pitch=0.45, w=0.025, h=0.035):
    """Stehfalz-Naehte entlang v"""
    k = 1
    while u0 + k * pitch < u1 - 0.1:
        uu = u0 + k * pitch
        hs = [(h_[2], h_[3]) for h_ in holes if h_[0] - 0.03 < uu < h_[1] + 0.03]
        for (s0, s1) in intervals_minus(v0, v1, hs):
            obox(o, m, org, u, v, n, uu - w / 2, uu + w / 2, s0, s1, 0.0, h)
        k += 1

def window(fr, gl, org, u, v, n, u0, u1, v0, v1, rec=0.14, cols=(), rows=(), fw=0.07, fd=0.08,
           sill=False, cutcoll=None, cutmat=None, wall_t=0.365, fm=None):
    fm = fm or M['alu']
    if cutcoll:
        cutbox(cutcoll, cutmat, org, u, v, n, u0, u1, v0, v1, -wall_t - 0.06, 0.06)
    a, b = -rec - fd, -rec
    obox(fr, fm, org, u, v, n, u0, u1, v0, v0 + fw, a, b)
    obox(fr, fm, org, u, v, n, u0, u1, v1 - fw, v1, a, b)
    obox(fr, fm, org, u, v, n, u0, u0 + fw, v0 + fw, v1 - fw, a, b)
    obox(fr, fm, org, u, v, n, u1 - fw, u1, v0 + fw, v1 - fw, a, b)
    for c in cols:
        obox(fr, fm, org, u, v, n, c - fw * 0.45, c + fw * 0.45, v0 + fw, v1 - fw, a, b)
    for r in rows:
        obox(fr, fm, org, u, v, n, u0 + fw, u1 - fw, r - fw * 0.45, r + fw * 0.45, a, b)
    mid = (a + b) / 2
    obox(gl, M['glas'], org, u, v, n, u0 + fw * 0.5, u1 - fw * 0.5, v0 + fw * 0.5, v1 - fw * 0.5, mid - 0.006, mid + 0.006)
    if sill:
        obox(fr, M['aluh'], org, u, v, n, u0 - 0.03, u1 + 0.03, v0 - 0.035, v0, -rec, 0.05)

def ndiv(a, b, k):
    return [a + (b - a) * i / k for i in range(1, k)]

# ------------------------------------------------------------------ Masse
W = 8.00          # Haustiefe Ost-West
L = 7.95          # Hauslaenge Nord-Sued
MID = 4.155       # Mittelbau
YB0 = L + MID     # 12.105
TOT = YB0 + L     # 20.055
T70 = math.tan(math.radians(70)); S70 = math.sin(math.radians(70)); C70 = math.cos(math.radians(70))

ROT_B = (Matrix.Translation((W / 2, TOT / 2, 0)) @ Matrix.Rotation(math.pi, 4, 'Z') @
         Matrix.Translation((-W / 2, -TOT / 2, 0)))

BOOLS = []   # (target, cutter-collection)
ORIGINS = {}  # Objekt -> Drehpunkt (Tueren, Tore)
TOGGLE = {}   # Objekt -> Drehwinkel beim Oeffnen/Schliessen (rad, um Z), wird als Custom Property 'drehwinkel' exportiert

# ------------------------------------------------------------------ Polygon-Extrusion, PV, Treppen
from shapely.geometry import LineString as _LS
from shapely.ops import split as _split
from shapely.geometry.polygon import orient as _orient

def holes_free(g):
    out = []; geoms = list(getattr(g, 'geoms', [g]))
    while geoms:
        p = geoms.pop()
        if p.is_empty or p.area < 1e-4: continue
        if p.geom_type != 'Polygon':
            geoms += list(getattr(p, 'geoms', [])); continue
        if len(p.interiors) == 0:
            out.append(p); continue
        hx = Polygon(p.interiors[0]).centroid.x
        geoms += list(_split(p, _LS([(hx, -100), (hx, 100)])).geoms)
    res = []
    for q in out:
        c = list(_orient(q.simplify(0.002), 1.0).exterior.coords)[:-1]
        cc = [c[0]]
        for pt in c[1:]:
            if abs(pt[0] - cc[-1][0]) > 1e-5 or abs(pt[1] - cc[-1][1]) > 1e-5: cc.append(pt)
        if len(cc) >= 3: res.append(cc)
    return res

def extrude(o, m, pts, z0, z1):
    bm = o['bm']; idx = mi(o, m); n = len(pts)
    b = [bm.verts.new((x, y, z0)) for (x, y) in pts]
    t = [bm.verts.new((x, y, z1)) for (x, y) in pts]
    for vs in (b[::-1], t):
        f = bm.faces.new(vs); f.material_index = idx
    for i in range(n):
        j = (i + 1) % n
        f = bm.faces.new([b[i], b[j], t[j], t[i]]); f.material_index = idx

def slabpoly(o, m, g, z0, z1):
    for pts in holes_free(g):
        extrude(o, m, pts, z0, z1)

def cutpoly(coll, m, g, z0, z1):
    for pts in holes_free(g):
        k = CUTN.get(coll, 0); CUTN[coll] = k + 1
        extrude(O('%s_%03d' % (coll, k), coll), m, pts, z0, z1)

def pv_field(o, org, u, v, n, u0, u1, v0, v1, cols, rows, off=0.04, gap=0.02):
    du, dv = (u1 - u0) / cols, (v1 - v0) / rows
    for i in range(cols):
        for j in range(rows):
            a, b = u0 + i * du + gap / 2, u0 + (i + 1) * du - gap / 2
            c, d = v0 + j * dv + gap / 2, v0 + (j + 1) * dv - gap / 2
            obox(o, M['alu'], org, u, v, n, a, b, c, d, off, off + 0.035)            # Modulrahmen
            obox(o, M['pv'], org, u, v, n, a + 0.025, b - 0.025, c + 0.025, d - 0.025, off + 0.035, off + 0.04)

def flight(o, x0, x1, ys, dirn, z0, r, n, g):
    """gerader Lauf: n Steigungen, Antritt bei ys, Laufrichtung dirn (+1/-1 in Y)"""
    for i in range(n - 1):
        zt = z0 + (i + 1) * r
        ya, yb = ys + dirn * i * g, ys + dirn * (i + 1) * g
        y0, y1 = min(ya, yb), max(ya, yb)
        abox(o, M['beton'], x0, x1, y0, y1, zt - r - 0.17, zt - 0.03)
        abox(o, M['treppe'], x0, x1, y0 - 0.02 if dirn < 0 else y0, y1 + 0.02 if dirn > 0 else y1, zt - 0.03, zt)
    ye = ys + dirn * (n - 1) * g
    beam(o, M['alu'], V((x1 - 0.05, ys + dirn * 0.15, z0 + r + 0.90)), V((x1 - 0.05, ye - dirn * 0.10, z0 + (n - 1) * r + 0.90)), 0.045, 0.045)

def ext_stair(o):
    """halbgewendelte Aussentreppe in der Nische X 1,00-2,78 / Y 5,75-7,78, Antritt Westlauf (Sued) -> Austritt Ostlauf (Sued)"""
    BX0, BX1, BY0, BY1 = 1.00, 2.78, 5.75, 7.78
    CX, CY = 1.815, 6.75; XI_W, XI_E = 1.78, 1.85
    RW = 0.46; L1 = CY - BY0; LA = math.pi * RW; Ltot = L1 + LA + L1
    N = 15; RISE = 2.80 / N; G = Ltot / (N - 1)
    per = [(BX0, BY0), (BX0, BY1), (BX1, BY1), (BX1, BY0)]
    def tpar(pt):
        x, y = pt
        if abs(x - BX0) < 1e-6: return y - BY0
        if abs(y - BY1) < 1e-6: return (BY1 - BY0) + (x - BX0)
        return (BY1 - BY0) + (BX1 - BX0) + (BY1 - y)
    def cut(sv):
        if sv <= L1:
            y = BY0 + sv; return (XI_W, y), (BX0, y), 0.0 + (sv)
        if sv >= L1 + LA:
            y = CY - (sv - L1 - LA); return (XI_E, y), (BX1, y), 10.0 - (CY - y)
        th = math.pi - (sv - L1) / RW
        dx, dy = math.cos(th), math.sin(th)
        ts = []
        if dx < -1e-9: ts.append((BX0 - CX) / dx)
        if dx > 1e-9: ts.append((BX1 - CX) / dx)
        if dy > 1e-9: ts.append((BY1 - CY) / dy)
        tt = min(t for t in ts if t > 0)
        return (CX, CY), (CX + dx * tt, CY + dy * tt), 5.0
    corners = [(BX0, BY1), (BX1, BY1)]
    foot = sbox(BX0, BY0, BX1, BY1)
    for i in range(N - 1):
        A0, B0, ia = cut(i * G); A1, B1, ib = cut((i + 1) * G)
        t0, t1 = tpar(B0), tpar(B1)
        mid = [c for c in corners if t0 < tpar(c) < t1]
        inner = []
        if ia < 5 and ib >= 5: inner = [(XI_W, CY)]
        if ia == 5 and ib > 5: inner = [(XI_E, CY)]
        if ia < 5 and ib > 5: inner = [(XI_E, CY), (XI_W, CY)]
        poly = Polygon([A0, B0] + mid + [B1, A1] + inner).buffer(0).intersection(foot)
        if poly.is_empty or poly.area < 0.01: continue
        zt = 6.0 + (i + 1) * RISE
        poly = poly.buffer(-0.008)
        slabpoly(o, M['alu'], poly, zt - 0.05, zt)
        # Aussenpfosten + Handlauf
        pm = B0 if i == 0 else B1
        inward = V((CX - pm[0], CY - pm[1], 0)).normalized() * 0.04
        beam(o, M['alu'], V((pm[0] + inward.x, pm[1] + inward.y, zt - 0.05)), V((pm[0] + inward.x, pm[1] + inward.y, zt + 0.95)), 0.03, 0.03)
    # Handlauf aussen (Polylinie ueber den Pfosten) und Mittelwange
    pts = []
    for i in range(N):
        A_, B_, _ = cut(min(i * G, Ltot))
        inward = V((CX - B_[0], CY - B_[1], 0)).normalized() * 0.04
        pts.append(V((B_[0] + inward.x, B_[1] + inward.y, 6.0 + max(i, 1) * RISE + 0.95)))
    for a_, b_ in zip(pts, pts[1:]):
        if (b_ - a_).length > 0.01: beam(o, M['alu'], a_, b_, 0.05, 0.04)
    abox(o, M['alu'], XI_W, XI_E, BY0, CY, 6.0, 6.0 + (N - 1) * RISE + 0.95)

# ================================================================== HAUS (lokal wie Haus A)
def build_house(P, coll, bay, openings=()):
    sh = O(P + '_Baukoerper_Putz', coll)
    fr = O(P + '_Fenster_Rahmen', coll)
    gl = O(P + '_Glas', coll)
    ho = O(P + '_Holzfassade', coll)
    li = O(P + '_Lisenen_Kugeln', coll)
    at = O(P + '_Attika_Terrassen', coll)
    dg = O(P + '_Dachgeschoss', coll)
    da = O(P + '_Dach_Dachterrasse', coll)
    er = O(P + '_Erker_Balkon', coll)
    po = O(P + '_Portal_Vordach_Tuer', coll)
    pvo = O(P + '_PV_Module', coll)
    XD0, XW, XD1 = 1.0, 1.55, 7.005      # DG: Suedecke / Westwand (Terrasse unter Ueberstand) / Ostwand
    NX1, NY0, NY1 = 2.76, 5.75, 7.73     # Nische Aussentreppe
    pf = O(P + '_Pflanzen_Platzhalter', coll)
    cM, cE, cD, cX = 'CUT_' + P + '_main', 'CUT_' + P + '_bay', 'CUT_' + P + '_dg', 'CUT_' + P + '_box'
    BOOLS.extend([(sh, cM), (er, cE), (dg, cD)])

    # ---------- Baukoerper EG+OG (Wandstaerke 36,5)
    abox(sh, M['putz'], 0, W, 0, L, 0, 6.0)
    cutbox(cM, M['innen'], O0, X_, Y_, Z_, 0.365, W - 0.365, 0.365, L - 0.365, -0.01, 5.49)

    E = (V((W, 0, 0)), Y_, Z_, X_)          # Ostfassade, u = Y
    Wf = (V((0, 0, 0)), Y_, Z_, -X_)        # Westfassade, u = Y
    S = (V((0, 0, 0)), X_, Z_, -Y_)         # Suedfassade (Erkerseite), u = X

    # Ostfassade: 2 Fensterachsen EG+OG mit Bruestungspaneel, Holzband dazwischen
    for (y0, y1) in [(1.515, 3.215), (4.735, 6.435)]:
        cutbox(cM, M['putz'], *E, y0, y1, 0.0, 5.26, -0.43, 0.06)
        ym = (y0 + y1) / 2
        window(fr, gl, *E, y0, y1, 0.0, 2.33, cols=[ym], rows=[0.98])
        obox(fr, M['alu'], *E, y0, y1, 2.33, 2.96, -0.22, -0.14)       # Bruestungspaneel anthrazit
        window(fr, gl, *E, y0, y1, 2.96, 5.26, cols=[ym], rows=[3.93])
    cutbox(cM, M['putz'], *E, 3.215, 4.735, 0.0, 5.26, -0.06, 0.06)
    clad(ho, M['holz'], *E, 3.215, 4.735, 0.0, 5.26, n0=-0.06, depth=0.03)

    # Westfassade: Eingangsportal + quadratische Fenster
    for (y0, y1) in [(1.32, 1.87), (6.08, 6.63)]:
        for (z0, z1) in [(1.79, 2.32), (4.70, 5.23)]:
            window(fr, gl, *Wf, y0, y1, z0, z1, sill=True, cutcoll=cM, cutmat=M['putz'])
    yo0, yo1 = 2.825, 5.125
    cutbox(cM, M['putz'], *Wf, yo0, yo1, 0.0, 2.45, -0.43, 0.06)
    cutbox(cM, M['putz'], *Wf, yo0, yo1, 3.04, 5.23, -0.43, 0.06)
    window(fr, gl, *Wf, yo0, 3.40, 0.0, 2.45)
    window(fr, gl, *Wf, 4.55, yo1, 0.0, 2.45)
    # Haustuer (Holz, Kassetten)
    obox(fr, M['alu'], *Wf, 3.40, 4.55, 0.0, 2.45, -0.22, -0.14)
    htn = P + '_Haustuer'; ht = O(htn, coll)
    obox(ht, M['tuer'], *Wf, 3.47, 4.48, 0.0, 2.38, -0.20, -0.13)
    pw, ph = (4.48 - 3.47 - 0.24) / 2, (2.38 - 0.30) / 4
    for i in range(2):
        for j in range(4):
            uu = 3.47 + 0.08 + i * (pw + 0.08); vv = 0.12 + j * (ph + 0.03)
            obox(ht, M['tuer'], *Wf, uu, uu + pw, vv, vv + ph - 0.03, -0.13, -0.115)
    obox(ht, M['aluh'], *Wf, 4.30, 4.34, 0.9, 1.5, -0.115, -0.06)   # Stossgriff
    hv = V((0.165, 3.47, 0.0)); hv = (ROT_B @ hv) if P == 'B' else hv
    ORIGINS[htn] = tuple(hv); TOGGLE[htn] = -math.pi / 2
    # OG-Fenster im Portal (3-teilig, Mitte mit Sprossen)
    window(fr, gl, *Wf, yo0, 3.40, 3.04, 5.23)
    window(fr, gl, *Wf, 3.40, 4.55, 3.04, 5.23, rows=ndiv(3.04, 5.23, 4))
    window(fr, gl, *Wf, 4.55, yo1, 3.04, 5.23)
    # Portalrahmen (weiss, 25 cm vorstehend) + Vordach
    obox(po, M['putzw'], *Wf, 2.46, yo0, 0.0, 5.65, 0.0, 0.25)
    obox(po, M['putzw'], *Wf, yo1, 5.49, 0.0, 5.65, 0.0, 0.25)
    obox(po, M['putzw'], *Wf, 2.46, 5.49, 5.23, 5.65, 0.0, 0.25)
    obox(po, M['alu'], *Wf, 2.60, 5.35, 2.70, 2.90, 0.0, 1.0)

    # Suedfassade (Erkerseite): 2 bodentiefe Balkontueren OG
    for (x0, x1) in [(2.35, 3.20), (4.79, 5.65)]:
        window(fr, gl, *S, x0, x1, 2.96, 5.20, cutcoll=cM, cutmat=M['putz'])
    bx0, bx1, bd, d0, d1 = bay
    cutbox(cM, M['innen'], *S, bx0 + 0.3, bx1 - 0.3, 0.0, 2.6, -0.43, 0.06)

    # ---------- Erker EG + Balkon OG
    abox(er, M['putzg'], bx0, bx1, -bd, 0.0, 0.0, 3.11)
    abox(er, M['putzg'], bx0, bx1, -bd, -bd + 0.2, 3.11, 3.62)
    abox(er, M['putzg'], bx0, bx0 + 0.2, -bd + 0.2, 0.0, 3.11, 3.62)
    abox(er, M['putzg'], bx1 - 0.2, bx1, -bd + 0.2, 0.0, 3.11, 3.62)
    cutbox(cE, M['innen'], O0, X_, Y_, Z_, bx0 + 0.3, bx1 - 0.3, -bd + 0.3, 0.05, -0.01, 2.75)
    ac = O(P + '_Erker_Gelaender', coll)
    for (x0, x1, y0, y1) in [(bx0 - 0.02, bx1 + 0.02, -bd - 0.02, -bd + 0.22),
                             (bx0 - 0.02, bx0 + 0.22, -bd + 0.22, 0.0),
                             (bx1 - 0.22, bx1 + 0.02, -bd + 0.22, 0.0)]:
        abox(ac, M['aluh'], x0, x1, y0, y1, 3.62, 3.68)
    abox(gl, M['glas'], bx0 + 0.09, bx1 - 0.09, -bd + 0.09, -bd + 0.11, 3.68, 3.97)
    abox(gl, M['glas'], bx0 + 0.09, bx0 + 0.11, -bd + 0.11, -0.02, 3.68, 3.97)
    abox(gl, M['glas'], bx1 - 0.11, bx1 - 0.09, -bd + 0.11, -0.02, 3.68, 3.97)
    abox(ac, M['aluh'], bx0 + 0.07, bx1 - 0.07, -bd + 0.07, -bd + 0.13, 3.97, 4.01)
    abox(ac, M['aluh'], bx0 + 0.07, bx0 + 0.13, -bd + 0.13, 0.0, 3.97, 4.01)
    abox(ac, M['aluh'], bx1 - 0.13, bx1 - 0.07, -bd + 0.13, 0.0, 3.97, 4.01)
    abox(at, M['platten'], bx0 + 0.2, bx1 - 0.2, -bd + 0.2, 0.0, 3.11, 3.14)   # Balkonbelag
    Sb = (V((0, -bd, 0)), X_, Z_, -Y_)
    window(fr, gl, *Sb, d0, d1, 0.0, 2.45, rec=0.10, cols=[(d0 + d1) / 2], cutcoll=cE, cutmat=M['putzg'], wall_t=0.3)

    # ---------- Attika / DG-Terrassen (OK Bruestung +6,88 / Pflanzkaesten +7,00)
    for (x0, x1) in [(W - 0.30, W), (0.0, 0.30)]:
        abox(at, M['putz'], x0, x1, 0.0, L, 6.0, 6.88)
        abox(at, M['aluh'], x0 - 0.02, x1 + 0.02, -0.02, L + 0.02, 6.88, 6.92)
    abox(at, M['holzt'], 7.005, W - 0.30, 0.75, L, 6.0, 6.035)
    abox(at, M['holzt'], 0.30, XW, 0.75, NY0, 6.0, 6.035)            # Westterrasse unter Dachueberstand
    abox(at, M['holzt'], 0.30, 1.0, NY0, L, 6.0, 6.035)
    abox(at, M['kies'], 0.30, W - 0.30, 0.0, 1.0, 6.0, 6.025)
    abox(at, M['aluh'], 0.0, W, -0.02, 0.02, 5.96, 6.02)                 # Dachrand Sued anthrazit
    for (x0, x1, y0, y1) in [(7.10, 7.68, 0.95, 2.35), (7.10, 7.68, 5.75, 7.15), (0.32, 0.90, 0.95, 2.35)]:
        abox(at, M['alu'], x0, x1, y0, y1, 6.035, 6.95)
        abox(at, M['erde'], x0 + 0.04, x1 - 0.04, y0 + 0.04, y1 - 0.04, 6.95, 6.96)
        for t in (0.2, 0.5, 0.8):
            icoblob(pf, M['pflanze'], V(((x0 + x1) / 2, y0 + (y1 - y0) * t, 7.05)), 0.32, 0.9, 1.0, 0.7)

    # ---------- Dachgeschoss (Mansarde: 70 Grad Stirnseite mit PV, Ost buendig, West zurueckgesetzt mit Dachueberstand)
    prof = [(1.0, 6.0), (1.0 + 2.38 / T70, 8.38), (L, 8.38), (L, 6.0)]
    fYZ = lambda a, c, t: V((t, a, c))
    prism(dg, M['putz'], prof, fYZ, XD0, XD1)
    ext = Polygon([(1.0, 5.0), (1.0, 6.0), (1.0 + 2.38 / T70, 8.38), (L, 8.38), (L, 5.0)])
    inner = ext.buffer(-0.22, join_style='mitre').intersection(sbox(0, 5.99, 20, 20))
    cutprism(cD, M['innen'], list(inner.exterior.coords)[:-1], fYZ, XW + 0.22, XD1 - 0.22)
    cutbox(cD, M['putz'], O0, X_, Y_, Z_, XD0 - 0.05, XW, 1.90, NY1, 5.99, 8.40)          # Westterrasse (Ruecksprung)
    cutbox(cD, M['putz'], O0, X_, Y_, Z_, XD0 - 0.05, NX1, NY0, NY1, 5.99, 8.45)          # Treppennische Aussentreppe
    for (x0, x1, z0, z1) in [o[1:] for o in openings if o[0] == 'D']:
        cutbox(cD, M['innen'], O0, X_, Y_, Z_, x0, x1, L - 0.35, L + 0.05, z0, z1)
    ED = (V((XD1, 0, 0)), Y_, Z_, X_)
    WD = (V((XW, 0, 0)), Y_, Z_, -X_)
    ysl = lambda z: 1.0 + (z - 6.0) / T70
    window(fr, gl, *ED, 3.28, 6.60, 6.0, 8.10, rec=0.09, cols=ndiv(3.28, 6.60, 4), cutcoll=cD, cutmat=M['putz'], wall_t=0.25)
    window(fr, gl, *WD, 2.56, 5.56, 6.0, 8.10, rec=0.09, cols=ndiv(2.56, 5.56, 3), cutcoll=cD, cutmat=M['putz'], wall_t=0.25)
    clad(ho, M['holz'], *ED, 0.0, 7.23, 6.0, 8.38, holes=[(3.28, 6.60, 6.0, 8.10)], ustart=lambda z: ysl(z) + 0.01)
    clad(ho, M['holz'], *WD, 1.90, NY0, 6.0, 8.38, holes=[(2.56, 5.56, 6.0, 8.10)])
    # 70-Grad-Stirnflaeche: Photovoltaik (6 x 2 Module), seitlich Holz
    SL = (V((0, 1.0, 6.0)), X_, V((0, C70, S70)), V((0, -S70, C70)))
    s = lambda z: (z - 6.0) / S70
    smax = s(8.38)
    gx0, gx1, gs0, gs1 = 1.75, 6.23, s(6.12), s(8.06)
    pv_field(pvo, *SL, gx0, gx1, gs0, gs1, 6, 2)
    clad(ho, M['holz'], *SL, XD0, XD1, 0.0, gs1, holes=[(gx0, gx1, gs0, gs1)])
    obox(ho, M['alu'], *SL, XD0, XD1, gs1, smax, 0.0, 0.03)

    # ---------- Dach (+8,38 / +8,62 / Attika +8,85) mit Treppenloch, Dachterrasse
    hole = sbox(XD0 - 0.3, NY0, NX1, L + 0.1)
    slabpoly(da, M['alu'], sbox(0.85, 1.29, 7.10, L).difference(hole), 8.38, 8.62)
    slabpoly(da, M['putzw'], sbox(1.00, 1.34, 6.95, L).difference(hole), 8.62, 8.85)
    slabpoly(da, M['kies'], sbox(1.05, 1.39, 6.90, L - 0.05).difference(hole), 8.85, 8.87)
    RX0, RX1, RY0, RY1 = 1.58, 6.38, 2.48, 7.78
    slabpoly(da, M['platten'], sbox(RX0 + 0.04, RY0 + 0.04, RX1 - 0.04, RY1 - 0.04).difference(hole), 8.87, 8.89)
    dd = lambda z: (z - 8.85) * 0.26
    ge = O(P + '_Dachterrasse_Gelaender', coll)
    for k in range(7):
        zb = 8.92 + k * 0.13; zt = zb + 0.07; d = dd(zb + 0.035); t = 0.035
        abox(ge, M['stehfalz'], RX0 + d, RX1 - d, RY0 + d - t / 2, RY0 + d + t / 2, zb, zt)           # Sued
        abox(ge, M['stehfalz'], RX1 - d - t / 2, RX1 - d + t / 2, RY0 + d, RY1 - d, zb, zt)           # Ost
        abox(ge, M['stehfalz'], 3.86, RX1 - d, RY1 - d - t / 2, RY1 - d + t / 2, zb, zt)              # Nord (bis Kamin)
        abox(ge, M['stehfalz'], RX0 + d - t / 2, RX0 + d + t / 2, RY0 + d, NY0, zb, zt)               # West (bis Treppe)
    d = dd(9.80)
    abox(ge, M['alu'], RX0 + d - 0.03, RX1 - d + 0.03, RY0 + d - 0.03, RY0 + d + 0.03, 9.78, 9.82)
    abox(ge, M['alu'], RX1 - d - 0.03, RX1 - d + 0.03, RY0 + d, RY1 - d + 0.03, 9.78, 9.82)
    abox(ge, M['alu'], 3.86, RX1 - d, RY1 - d - 0.03, RY1 - d + 0.03, 9.78, 9.82)
    abox(ge, M['alu'], RX0 + d - 0.03, RX0 + d + 0.03, RY0 + d, NY0, 9.78, 9.82)
    def posts(p_a, p_b, inward, n):
        for i in range(n + 1):
            p = p_a.lerp(p_b, i / n)
            beam(ge, M['alu'], V((p.x, p.y, 8.87)), V((p.x + inward.x * dd(9.80), p.y + inward.y * dd(9.80), 9.80)), 0.04, 0.04)
    posts(V((RX0, RY0)), V((RX1, RY0)), V((0, 1)), 3)
    posts(V((RX1, RY0)), V((RX1, RY1)), V((-1, 0)), 3)
    posts(V((RX0, RY0)), V((RX0, NY0)), V((1, 0)), 2)
    # Absturzsicherung Glas am Treppenloch (Sued- und Ostkante)
    for (x0, x1, y0, y1) in [(RX0 + 0.25, 1.80, NY0 - 0.03, NY0 - 0.01), (NX1 + 0.01, NX1 + 0.03, NY0, 6.62)]:
        abox(gl, M['glas'], x0, x1, y0, y1, 8.87, 9.85)
        abox(ge, M['alu'], x0 - 0.01, x1 + 0.01, y0 - 0.02, y1 + 0.02, 9.85, 9.90)
    # geneigtes PV-Element an der Dachkante (Plan Dachterrasse: Y 1,62-2,07)
    vv = V((0, 0.45, 0.95)).normalized(); nn = V((0, -0.95, 0.45)).normalized()
    PVR = (V((0, 1.62, 8.87)), X_, vv, nn)
    pv_field(pvo, *PVR, 1.75, 6.23, 0.0, (vv * 1.0).length * 0.98, 6, 1, off=0.0)
    for xp in (1.85, 4.0, 6.13):
        abox(ge, M['alu'], xp - 0.03, xp + 0.03, 2.02, 2.08, 8.85, 9.80)
    # Kamin und Pergola (+11,02)
    abox(da, M['putzw'], 2.82, 3.82, 6.64, 7.94, 8.85, 11.02)
    abox(da, M['alu'], 2.79, 3.85, 6.61, 7.97, 11.02, 11.06)
    pg = O(P + '_Pergola', coll)
    for (px, py) in [(2.86, 5.55), (5.21, 5.55), (5.21, 7.90)]:
        abox(pg, M['alu'], px - 0.04, px + 0.04, py - 0.04, py + 0.04, 8.87, 10.90)
    for (x0, x1, y0, y1) in [(2.82, 5.25, 5.51, 5.59), (2.82, 5.25, 7.86, 7.94), (2.82, 2.90, 5.51, 6.64), (5.17, 5.25, 5.51, 7.94)]:
        abox(pg, M['alu'], x0, x1, y0, y1, 10.90, 11.02)
    yl = 5.66
    while yl < 7.84:
        for (a, b) in intervals_minus(2.90, 5.17, [(2.80, 3.84)] if yl > 6.60 else []):
            abox(pg, M['alu'], a, b, yl, yl + 0.04, 10.92, 11.00)
        yl += 0.15

    # ---------- Aussentreppe DG-Terrasse -> Dachterrasse (15 x 18,7 x 26, halbgewendelt, Stahl anthrazit)
    ext_stair(O(P + '_Aussentreppe', coll))

    # ---------- Innen: Decken mit Treppenaugen, Treppen UG-EG-OG-DG (16 Stg.), DG-Boden
    it = O(P + '_Innen_Decken_Treppen', coll)
    VOID = sbox(2.09, 3.68, 2.98, 7.58)
    inn_rect = sbox(0.365, 0.365, W - 0.365, L - 0.365)
    bay_in = sbox(bx0 + 0.3, -bd + 0.3, bx1 - 0.3, 0.4)
    slabpoly(it, M['beton'], inn_rect.union(bay_in).difference(VOID), -0.35, -0.02)
    slabpoly(it, M['boden'], inn_rect.union(bay_in).difference(VOID), -0.02, 0.0)
    slabpoly(it, M['innen'], inn_rect.difference(VOID), 2.61, 2.94)
    slabpoly(it, M['boden'], inn_rect.difference(VOID), 2.94, 2.96)
    dgfp = sbox(XW + 0.22, 1.30, XD1 - 0.22, L - 0.22).difference(sbox(XD0 - 0.1, NY0 - 0.15, NX1 + 0.24, L))
    dvoid = sbox(2.09, 3.68, 2.98, 6.63)          # Treppenauge OG->DG (Kopfhoehe unter der Nische, Schnitt AA)
    for g_ in getattr(dgfp, 'geoms', [dgfp]):
        cutpoly(cM, M['innen'], g_, 5.84, 6.02)
    cutbox(cM, M['innen'], O0, X_, Y_, Z_, 2.09, 2.98, 3.68, 6.63, 5.45, 6.03)
    abox(gl, M['glas'], 2.09, NX1, NY0, 6.63, 5.97, 6.0)                       # begehbares Glas ueber dem Treppenlauf in der Nische
    slabpoly(it, M['boden'], dgfp.difference(dvoid), 5.84, 5.85)
    for (z0, r) in [(-2.88, 0.18), (0.0, 0.185), (2.96, 0.18)]:
        flight(it, 2.10, 2.97, 7.58, -1, z0, r, 16, 0.26)
    for (x0, x1, z0, z1) in [o[1:] for o in openings if o[0] == 'M']:
        cutbox(cM, M['innen'], O0, X_, Y_, Z_, x0, x1, L - 0.45, L + 0.05, z0, z1)
    return [n for n in OBJS if n.startswith(P + '_')]

A_objs = build_house('A', '01_Haus_A', (1.60, 6.40, 1.14, 2.25, 5.74))
B_objs = build_house('B', '02_Haus_B', (0.75, 7.25, 2.015, 1.88, 6.13),
                     openings=[('M', 0.40, 2.98, 2.96, 5.06), ('D', 3.81, 6.46, 5.84, 7.94)])   # Durchgaenge zum Mittelbau (aus OG/DG-Plan)

# ================================================================== MITTELBAU (Mansarde 70/45 Grad, First +8,88)
cm = '03_Mittelbau'
mb = O('Mitte_Durchfahrt_Decke', cm)
md = O('Mitte_Mansarddach_Stehfalz', cm)
mf = O('Mitte_Fenster_Rahmen', cm)
mg = O('Mitte_Glas', cm)
mi_ = O('Mitte_Innenraum', cm)
BOOLS.append((md, 'CUT_M'))
abox(mb, M['putzw'], 0.0, W, L, YB0, 2.45, 3.0)
abox(mb, M['alu'], 0.0, 0.79, L, YB0, 3.0, 3.02)
abox(mb, M['alu'], 7.21, W, L, YB0, 3.0, 3.02)
pm = [(0.79, 3.0), (2.379, 7.2), (4.0, 8.88), (5.621, 7.2), (7.21, 3.0)]
fXZ = lambda a, c, t: V((a, t, c))
prism(md, M['stehfalz'], pm, fXZ, L, YB0)
extm = Polygon([(0.79, 2.0)] + pm + [(7.21, 2.0)])
innm = extm.buffer(-0.3, join_style='mitre').intersection(sbox(-1, 2.99, 10, 20))
cutprism('CUT_M', M['innen'], list(innm.exterior.coords)[:-1], fXZ, L - 0.01, YB0 + 0.01)
gal = innm.intersection(sbox(-1, 5.53, 10, 5.71))
prism(mi_, M['innen'], list(gal.exterior.coords)[:-1], fXZ, L, YB0)
abox(mi_, M['boden'], 1.2, 6.8, L, YB0, 3.0, 3.01)

def face(p0, p1, outward_sign):
    v = V((p1[0] - p0[0], 0, p1[1] - p0[1])); ln = v.length; v.normalize()
    n = V((-v.z, 0, v.x)) * outward_sign
    if n.z < 0: n = -n
    return (V((p0[0], L, p0[1])), Y_, v, n), ln

FW70, lw70 = face(pm[0], pm[1], 1)
FW45, lw45 = face(pm[1], pm[2], 1)
FE45, le45 = face(pm[3], pm[2], 1)
FE70, le70 = face(pm[4], pm[3], 1)
sz70 = lambda z: (z - 3.0) / (4.2 / lw70)
sz45 = lambda z: (z - 7.2) / (1.68 / lw45)
rw = [(0.70, 1.55, sz70(4.0), sz70(5.47)), (2.70, 3.55, sz70(4.0), sz70(5.47))]
for F in (FW70, FE70):
    for (u0, u1, s0, s1) in rw:
        window(mf, mg, *F, u0, u1, s0, s1, rec=-0.07, fd=0.08, cutcoll='CUT_M', cutmat=M['stehfalz'], wall_t=0.35)
    seams(md, M['stehfalz'], *F, 0.0, MID, 0.0, lw70, holes=rw)
ew = [(1.83, 2.60, sz45(7.27), sz45(7.95))]
window(mf, mg, *FE45, *ew[0], rec=-0.07, fd=0.08, cutcoll='CUT_M', cutmat=M['stehfalz'], wall_t=0.35)
seams(md, M['stehfalz'], *FE45, 0.0, MID, 0.0, le45, holes=ew)
# Westliche 45-Grad-Flaeche: Photovoltaik (6 x 2 Module)
pv_field(O('Mitte_PV_Module', cm), *FW45, 0.06, MID - 0.06, 0.06, lw45 - 0.10, 6, 2)
obox(mf, M['alu'], V((4.0, L, 8.88)), Y_, X_, Z_, 0.0, MID, -0.13, 0.13, -0.03, 0.04)   # Firstabdeckung

# ================================================================== CARPORTS (Sichtbeton, OK +3,00)
cc = '04_Carports'
cw = O('Carport_West_Haus_A', cc)
abox(cw, M['beton'], -3.52, 0.0, 5.52, 10.80, 2.75, 3.00)
abox(cw, M['beton'], -3.52, -3.30, 5.52, 5.74, 0.0, 2.75)          # Stuetze SW, Einfahrt von Sueden offen
abox(cw, M['beton'], -3.52, 0.0, 10.60, 10.80, 0.0, 2.75)
co = O('Carport_Ost_Haus_B', cc)
abox(co, M['beton'], 8.52, 11.55, 19.58, 25.96, 2.75, 3.00)
abox(co, M['beton'], 8.52, 11.55, 24.60, 25.96, 0.0, 2.75)          # Abstellraum
abox(co, M['beton'], 8.55, 8.75, 19.62, 19.82, 0.0, 2.75)
abox(co, M['beton'], 11.32, 11.52, 19.62, 19.82, 0.0, 2.75)
ct = O('Carport_Tueren', cc)
abox(ct, M['alu'], 9.6, 10.6, 24.56, 24.62, 0.0, 2.2)
gd = O('Carport_Gruendach', cc)
abox(gd, M['gruen'], -3.42, -0.10, 5.62, 10.70, 3.00, 3.08)
abox(gd, M['gruen'], 8.62, 11.45, 19.68, 25.86, 3.00, 3.08)

# ================================================================== AUSSENANLAGEN (vereinfacht nach EG-Plan)
ca = '05_Aussenanlagen'
ge_ = O('Gelaende_Rasen', ca)
abox(ge_, M['rasen'], -60, 70, -4.95, 80, -0.32, -0.02)
abox(ge_, M['rasen'], -60, 70, -80, -15.4, -0.32, -0.02)
st = O('Strasse_Gerlichstrasse', ca)
abox(st, M['gehweg'], -60, 70, -6.95, -4.95, -0.32, 0.0)
abox(st, M['beton'], -60, 70, -7.10, -6.95, -0.32, 0.0)            # Bordstein
abox(st, M['asphalt'], -60, 70, -13.25, -7.10, -0.32, -0.12)
abox(st, M['beton'], -60, 70, -13.40, -13.25, -0.32, 0.0)
abox(st, M['gehweg'], -60, 70, -15.4, -13.40, -0.32, 0.0)
pa = O('Gelaende_Pflaster_Fahrspuren', ca)
# Westzufahrt zum Carport A (Fahrspuren mit Rasenmittelstreifen)
abox(pa, M['pflaster'], -3.52, 0.0, -4.95, 5.52, -0.02, 0.0)
abox(pa, M['pflaster'], -3.52, 0.0, 5.52, 10.80, -0.02, 0.0)
# Ostzufahrt zum Carport B
abox(pa, M['pflaster'], 8.0, 11.55, -5.10, 25.96, -0.02, 0.0)
# Durchfahrt Mittelbau
abox(pa, M['pflaster'], 0.0, 8.0, L, YB0, -0.02, 0.0)
rs = O('Gelaende_Rasenstreifen_Beete', ca)
abox(rs, M['rasen'], -2.58, -1.63, -3.10, 3.26, 0.0, 0.01)
abox(rs, M['rasen'], 9.57, 10.50, -3.12, 6.40, 0.0, 0.01)
te = O('Gelaende_Holzterrassen', ca)
abox(te, M['holzt'], 1.61, 5.70, -3.43, -1.14, -0.02, 0.03)          # Terrasse Haus A (9,5 m2)
abox(te, M['holzt'], 1.82, 6.22, 22.07, 24.08, -0.02, 0.03)          # Terrasse Haus B
abox(te, M['holzt'], -1.63, 0.0, 16.65, 22.80, -0.02, 0.03)
abox(te, M['holzt'], 0.0, 1.82, 22.07, 22.80, -0.02, 0.03)
hh = O('Gelaende_Hecken_hoch', ca)
abox(hh, M['hecke'], 7.45, 8.00, -3.35, -0.90, 0.0, 2.00)        # hohe Hecke statt Holz-Sichtschutz an Terrasse A
abox(hh, M['hecke'], 11.00, 11.55, -4.25, 19.55, 0.0, 1.80)      # Meterhecke Sichtschutz Ostgrenze entlang Zufahrt
mu = O('Gelaende_Muelltonnenhaus', ca)
abox(mu, M['alu'], 5.90, 7.40, -4.10, -3.40, 0.0, 1.35)

# ================================================================== EINFRIEDUNG STRASSE (Pfeiler verputzt, Fluegeltore, Zaun + Hecke)
ce = '08_Einfriedung_Strasse'
YP0, YP1 = -4.90, -4.30          # Pfeiler (Vorderkante = Heckenflucht)
YF = -4.40                        # Achse Zaun / Tore
HP = 1.95                         # Pfeilerhoehe (+ Abdeckplatte)
pfo = O('Einfriedung_Pfeiler_Putz_weiss', ce)
zno = O('Einfriedung_Zaun_anthrazit', ce)
sko = O('Einfriedung_Sockel_Putz_weiss', ce)
hko = O('Einfriedung_Hecke', ce)
PFEILER = [(-3.52, -3.12), (-0.20, 0.20), (2.47, 2.87), (5.13, 5.53), (7.80, 8.20), (11.15, 11.55)]
for (x0, x1) in PFEILER:
    abox(pfo, M['putzw'], x0, x1, YP0, YP1, -0.02, HP)
    abox(pfo, M['stein'], x0 - 0.04, x1 + 0.04, YP0 - 0.04, YP1 + 0.04, HP, HP + 0.08)
def stabfeld(o, x0, x1, z0, z1, pitch=0.11, bw=0.04, bt=0.012):
    n = max(1, int((x1 - x0) / pitch))
    step = (x1 - x0) / n
    for k in range(1, n):
        x = x0 + k * step
        abox(o, M['alu'], x - bw / 2, x + bw / 2, YF - bt / 2, YF + bt / 2, z0, z1)
# Zaunfelder vor dem Garten Haus A: Sockel weiss, Flachstahlstaebe anthrazit, Hecke strassenseitig
for (xa, xb) in [(0.20, 2.47), (2.87, 5.13), (5.53, 7.80)]:
    abox(sko, M['putzw'], xa, xb, YF - 0.12, YF + 0.12, -0.02, 0.30)
    abox(sko, M['stein'], xa, xb, YF - 0.14, YF + 0.14, 0.30, 0.34)
    abox(zno, M['alu'], xa, xb, YF - 0.025, YF + 0.025, 0.34, 0.39)
    abox(zno, M['alu'], xa, xb, YF - 0.025, YF + 0.025, 1.25, 1.30)
    stabfeld(zno, xa, xb, 0.39, 1.25)
    abox(hko, M['hecke'], xa, xb, YP0, YF - 0.14, 0.0, 1.15)
# Zweifluegelige Drehtore anthrazit, je Fluegel eigenes Objekt mit Ursprung im Drehpunkt (zum Oeffnen um Z drehen)
def fluegel(name, xh, xe):
    """blickdichter Torfluegel 1,80 m, Alu anthrazit mit horizontalen Schattenfugen"""
    o = O(name, ce)
    sgn = 1 if xe > xh else -1
    a, b = xh + sgn * 0.02, xe - sgn * 0.01
    x0, x1 = min(a, b), max(a, b)
    abox(o, M['alu'], x0, x1, YF - 0.03, YF + 0.03, 0.06, 1.80)
    for k in range(1, 9):
        zz = 0.06 + k * (1.74 / 9)
        abox(o, M['aluh'], x0 + 0.03, x1 - 0.03, YF - 0.036, YF + 0.036, zz - 0.006, zz + 0.006)
    for zb in (0.25, 1.50):
        abox(o, M['alu'], xh - 0.015, xh + 0.015, YF - 0.045, YF + 0.045, zb, zb + 0.10)
    ORIGINS[name] = (xh, YF, 0.0); TOGGLE[name] = math.pi / 2 if xe > xh else -math.pi / 2
xm_w = (-3.12 + -0.20) / 2
xm_o = (8.20 + 11.15) / 2
fluegel('Tor_West_Fluegel_links', -3.12, xm_w)
fluegel('Tor_West_Fluegel_rechts', -0.20, xm_w)
fluegel('Tor_Ost_Fluegel_links', 8.20, xm_o)
fluegel('Tor_Ost_Fluegel_rechts', 11.15, xm_o)

# ================================================================== INNENAUSBAU 1:1 (aus den Vektor-Grundrissen UG/EG/OG/DG des Genehmigungsplans)
import json
INT = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'innenausbau.json')))
ci = '09_Innenausbau'
HGT = {'UG_all': (-3.18, -0.35, -2.88), 'EG_A': (0.0, 2.61, 0.0), 'EG_B': (0.0, 2.61, 0.0),
       'OG_A': (2.96, 5.49, 2.96), 'OG_B': (2.96, 5.49, 2.96), 'OG_M': (3.0, 5.60, 3.0),
       'DG_A': (5.84, 8.25, 5.84), 'DG_B': (5.84, 8.25, 5.84), 'DG_M': (5.71, 8.70, 5.71)}
OBJN = {'UG_all': 'Innen_UG_Waende', 'EG_A': 'Innen_EG_Waende', 'EG_B': 'Innen_EG_Waende',
        'OG_A': 'Innen_OG_Waende', 'OG_B': 'Innen_OG_Waende', 'OG_M': 'Innen_Mittelbau_Waende',
        'DG_A': 'Innen_DG_Waende_A', 'DG_B': 'Innen_DG_Waende_B', 'DG_M': 'Innen_Mittelbau_Waende'}
igl = O('Innen_UG_Fensterglas', ci)
ndoor = 0
for key, (zb, zt, zf) in HGT.items():
    d = INT[key]; o = O(OBJN[key], ci)
    for pts in d['walls']:
        extrude(o, M['innen'], [tuple(p) for p in pts], zb, zt)
    for pts in d['lintels']:
        extrude(o, M['innen'], [tuple(p) for p in pts], zf + 2.10, zt)
    for pts in d['ugwin']:
        q = Polygon(pts)
        extrude(o, M['innen'], [tuple(p) for p in pts], zb, -1.55)
        extrude(o, M['innen'], [tuple(p) for p in pts], -0.80, zt)
        gq = q.buffer(-0.11, join_style='mitre')
        if not gq.is_empty: slabpoly(igl, M['glas'], gq, -1.55, -0.80)
    for dr in d['doors']:
        hx, hy = dr['h']; ex, ey = dr['open']
        u = V((ex - hx, ey - hy, 0)); ln = u.length; u.normalize()
        nvec = u.cross(Z_).normalized()
        ndoor += 1; nm = 'Tuer_%s_%02d' % (key, ndoor)
        obox(O(nm, ci), M['innentuer'], V((hx, hy, 0)), u, Z_, nvec, 0.03, ln - 0.03, zf + 0.01, zf + 2.02, -0.02, 0.02)
        ORIGINS[nm] = (hx, hy, zf)
        cx_, cy_ = dr['closed'][0] - hx, dr['closed'][1] - hy
        TOGGLE[nm] = math.atan2(u.x * cy_ - u.y * cx_, u.x * cx_ + u.y * cy_)
# DG-/Mittelbau-Waende auf das Innenvolumen begrenzen (Dachschraegen)
extI = Polygon([(1.0, 5.0), (1.0, 6.0), (1.0 + 2.38 / T70, 8.38), (L, 8.38), (L, 5.0)]).buffer(-0.22, join_style='mitre').intersection(sbox(0, 5.80, 20, 20))
fYZ_ = lambda a, c, t: V((t, a, c))
cutprism('CUT_INT_DG_A', M['innen'], list(extI.exterior.coords)[:-1], fYZ_, 1.55 + 0.22, 7.005 - 0.22)
cutprism('CUT_INT_DG_B', M['innen'], list(extI.exterior.coords)[:-1], fYZ_, 1.55 + 0.22, 7.005 - 0.22)
bmB = OBJS['CUT_INT_DG_B_000']['bm']; bmesh.ops.transform(bmB, matrix=ROT_B, verts=bmB.verts)
innM = Polygon([(0.79, 2.0)] + pm + [(7.21, 2.0)]).buffer(-0.3, join_style='mitre').intersection(sbox(-1, 2.95, 10, 20))
cutprism('CUT_INT_M', M['innen'], list(innM.exterior.coords)[:-1], fXZ, L - 0.01, YB0 + 0.01)
BOOLS_I = [('Innen_DG_Waende_A', 'CUT_INT_DG_A'), ('Innen_DG_Waende_B', 'CUT_INT_DG_B'), ('Innen_Mittelbau_Waende', 'CUT_INT_M')]
# UG: Bodenplatte, Decke ausserhalb der Haeuser
ug = O('Innen_UG_Boden_Decke', ci)
for pts in INT['ug_floor']:
    extrude(ug, M['beton'], [tuple(p) for p in pts], -3.18, -2.90)
    extrude(ug, M['boden'], [tuple(p) for p in pts], -2.90, -2.88)
for pts in INT['ug_ceiling_extra']:
    extrude(ug, M['beton'], [tuple(p) for p in pts], -0.35, -0.33)
# Gelaende ueber den Treppenaugen UG->EG oeffnen
for (x0, x1, y0, y1) in [(2.09, 2.98, 3.68, 7.58), (8 - 2.98, 8 - 2.09, TOT - 7.58, TOT - 3.68)]:
    cutbox('CUT_ground', M['rasen'], O0, X_, Y_, Z_, x0, x1, y0, y1, -0.5, 0.1)
BOOLS.append(('Gelaende_Rasen', 'CUT_ground'))

# ================================================================== MOEBLIERUNG nach Plan (Kueche, Bad, Wohnen, Schlafen, Diele)
cf = '10_Moeblierung'
FO = {k: O('Moebel_' + k, cf) for k in ('Kueche', 'Bad', 'Wohnen', 'Schlafen', 'Schraenke')}
def fb(o, m, x0, x1, y0, y1, z0, z1): abox(o, m, min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1), z0, z1)
def counter(x0, x1, y0, y1, z, sink=None, hob=None, upper=None, wall=None, waterfall=False):
    """grifflose Kueche Eiche geraeuchert, Calacatta-Marmor, Spritzschutz und Wasserfallkanten"""
    o = FO['Kueche']
    fb(o, M['alu'], x0 + 0.05, x1 - 0.05, y0 + 0.05, y1 - 0.05, z, z + 0.10)
    fb(o, M['kueche'], x0, x1, y0, y1, z + 0.10, z + 0.86)
    # Grifffugen
    if (x1 - x0) < (y1 - y0):
        for xx in ((x0 - 0.002, x0 + 0.004), (x1 - 0.004, x1 + 0.002)):
            fb(o, M['alu'], xx[0], xx[1], y0 + 0.02, y1 - 0.02, z + 0.80, z + 0.83)
    else:
        for yy in ((y0 - 0.002, y0 + 0.004), (y1 - 0.004, y1 + 0.002)):
            fb(o, M['alu'], x0 + 0.02, x1 - 0.02, yy[0], yy[1], z + 0.80, z + 0.83)
    fb(o, M['arbeitsplatte'], x0 - 0.01, x1 + 0.01, y0 - 0.01, y1 + 0.01, z + 0.86, z + 0.92)
    if waterfall:
        if (x1 - x0) < (y1 - y0):
            fb(o, M['arbeitsplatte'], x0 - 0.01, x1 + 0.01, y0 - 0.01, y0 + 0.05, z, z + 0.86); fb(o, M['arbeitsplatte'], x0 - 0.01, x1 + 0.01, y1 - 0.05, y1 + 0.01, z, z + 0.86)
        else:
            fb(o, M['arbeitsplatte'], x0 - 0.01, x0 + 0.05, y0 - 0.01, y1 + 0.01, z, z + 0.86); fb(o, M['arbeitsplatte'], x1 - 0.05, x1 + 0.01, y0 - 0.01, y1 + 0.01, z, z + 0.86)
    if sink: fb(o, M['edelstahl'], *sink, z + 0.915, z + 0.921); fb(o, M['bronze'], sink[0] + 0.02, sink[0] + 0.05, (sink[2] + sink[3]) / 2 - 0.015, (sink[2] + sink[3]) / 2 + 0.015, z + 0.92, z + 1.22)
    if hob: fb(o, M['hob'], *hob, z + 0.92, z + 0.926)
    if wall:
        w = {'-X': (x0, x0 + 0.02, y0, y1), '+X': (x1 - 0.02, x1, y0, y1)}[wall]
        fb(o, M['arbeitsplatte'], *w, z + 0.92, z + 1.45)
    if upper: fb(o, M['kueche'], *upper, z + 1.45, z + 2.25)
def tall(x0, x1, y0, y1, z, h=2.25, o=None, m=None):
    o = o or FO['Kueche']; m = m or M['kueche']
    fb(o, m, x0, x1, y0, y1, z, z + h)
    n = max(1, int(round(max(x1 - x0, y1 - y0) / 0.6)))
    for k in range(1, n):
        if (x1 - x0) > (y1 - y0): xx = x0 + k * (x1 - x0) / n; fb(o, M['alu'], xx - 0.003, xx + 0.003, y0 - 0.003, y1 + 0.003, z + 0.02, z + h - 0.02)
        else: yy = y0 + k * (y1 - y0) / n; fb(o, M['alu'], x0 - 0.003, x1 + 0.003, yy - 0.003, yy + 0.003, z + 0.02, z + h - 0.02)
def wardrobe(x0, x1, y0, y1, z, h=2.30): tall(x0, x1, y0, y1, z, h, FO['Schraenke'], M['schrank'])
def lowbox(x0, x1, y0, y1, z, h=0.50, m=None, o=None): fb(o or FO['Wohnen'], m or M['eiche'], x0, x1, y0, y1, z, z + h)
def cyl(o, m, cx, cy, z0, z1, r, seg=24):
    bm = o['bm']; idx = mi(o, m)
    res = bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=z1 - z0, matrix=Matrix.Translation((cx, cy, (z0 + z1) / 2)))
    for fc in {f for vv in res['verts'] for f in vv.link_faces}: fc.material_index = idx
def stool(cx, cy, z, r=0.20):
    o = FO['Kueche']
    cyl(o, M['bronze'], cx, cy, z, z + 0.02, 0.19); cyl(o, M['bronze'], cx, cy, z, z + 0.66, 0.025); cyl(o, M['stoff'], cx, cy, z + 0.66, z + 0.75, r)
def table(x0, x1, y0, y1, z, h=0.75, top=None):
    """Esstisch: Marmorplatte, zwei Travertin-Wangen (bzw. Schreibtisch Nussbaum)"""
    o = FO['Wohnen']
    if top is None and (x1 - x0) * (y1 - y0) > 1.5:
        fb(o, M['arbeitsplatte'], x0, x1, y0, y1, z + h - 0.05, z + h)
        if (y1 - y0) > (x1 - x0):
            for yy in (y0 + 0.35, y1 - 0.55): fb(o, M['travertin'], x0 + 0.18, x1 - 0.18, yy, yy + 0.2, z, z + h - 0.05)
        else:
            for xx in (x0 + 0.35, x1 - 0.55): fb(o, M['travertin'], xx, xx + 0.2, y0 + 0.18, y1 - 0.18, z, z + h - 0.05)
    else:
        fb(o, top or M['eiche'], x0, x1, y0, y1, z + h - 0.035, z + h)
        for (lx, ly) in [(x0 + 0.05, y0 + 0.05), (x1 - 0.05, y0 + 0.05), (x0 + 0.05, y1 - 0.05), (x1 - 0.05, y1 - 0.05)]:
            fb(o, M['bronze'], lx - 0.015, lx + 0.015, ly - 0.015, ly + 0.015, z, z + h - 0.035)
def chair(x0, x1, y0, y1, z, back):
    """Polsterstuhl Leder cognac, schlanke Bronzebeine"""
    o = FO['Wohnen']
    fb(o, M['stoff'], x0 + 0.01, x1 - 0.01, y0 + 0.01, y1 - 0.01, z + 0.40, z + 0.48)
    for (lx, ly) in [(x0 + 0.05, y0 + 0.05), (x1 - 0.05, y0 + 0.05), (x0 + 0.05, y1 - 0.05), (x1 - 0.05, y1 - 0.05)]:
        fb(o, M['bronze'], lx - 0.012, lx + 0.012, ly - 0.012, ly + 0.012, z, z + 0.40)
    bx = {'-X': (x0, x0 + 0.07, y0, y1), '+X': (x1 - 0.07, x1, y0, y1), '-Y': (x0, x1, y0, y0 + 0.07), '+Y': (x0, x1, y1 - 0.07, y1)}[back]
    fb(o, M['stoff'], *bx, z + 0.48, z + 0.84)
def sofa(x0, x1, y0, y1, z, back, m=None):
    """flaches Modulsofa (Minotti-Anmutung): Bouclé, zurueckgesetzter Sockel, Sitz- und Rueckenkissen"""
    o = FO['Wohnen']; m = m or M['stoff_hell']
    fb(o, M['alu'], x0 + 0.08, x1 - 0.08, y0 + 0.08, y1 - 0.08, z, z + 0.06)
    fb(o, m, x0, x1, y0, y1, z + 0.06, z + 0.28)
    along_y = back in ('-X', '+X'); L0, L1 = (y0, y1) if along_y else (x0, x1)
    n = max(1, int(round((L1 - L0) / 0.95))); step = (L1 - L0) / n
    bd = 0.24
    for k in range(n):
        a, b = L0 + k * step + 0.006, L0 + (k + 1) * step - 0.006
        if along_y:
            sx0, sx1 = (x0 + bd, x1) if back == '-X' else (x0, x1 - bd)
            fb(o, m, sx0, sx1, a, b, z + 0.28, z + 0.40)
            bx = (x0, x0 + bd) if back == '-X' else (x1 - bd, x1)
            fb(o, m, bx[0], bx[1], a, b, z + 0.28, z + 0.74)
        else:
            sy0, sy1 = (y0 + bd, y1) if back == '-Y' else (y0, y1 - bd)
            fb(o, m, a, b, sy0, sy1, z + 0.28, z + 0.40)
            by = (y0, y0 + bd) if back == '-Y' else (y1 - bd, y1)
            fb(o, m, a, b, by[0], by[1], z + 0.28, z + 0.74)
    # zwei Zierkissen in Cognac
    for k in (0.2, 0.75):
        c = L0 + (L1 - L0) * k
        if along_y:
            xx = (x0 + bd, x0 + bd + 0.14) if back == '-X' else (x1 - bd - 0.14, x1 - bd)
            fb(o, M['stoff'], xx[0], xx[1], c - 0.22, c + 0.22, z + 0.40, z + 0.80)
        else:
            yy = (y0 + bd, y0 + bd + 0.14) if back == '-Y' else (y1 - bd - 0.14, y1 - bd)
            fb(o, M['stoff'], c - 0.22, c + 0.22, yy[0], yy[1], z + 0.40, z + 0.80)
def bed(x0, x1, y0, y1, z, head):
    """niedriges Polsterbett, breites Kopfteil Bouclé, Plaid Cognac"""
    o = FO['Schlafen']
    fb(o, M['eiche'], x0 - 0.06, x1 + 0.06, y0 - 0.06, y1 + 0.06, z + 0.06, z + 0.24)
    fb(o, M['alu'], x0 + 0.1, x1 - 0.1, y0 + 0.1, y1 - 0.1, z, z + 0.06)
    fb(o, M['bettwaesche'], x0 + 0.02, x1 - 0.02, y0 + 0.02, y1 - 0.02, z + 0.24, z + 0.50)
    ext = 0.25
    hb = {'-X': (x0 - 0.16, x0 - 0.04, y0 - ext, y1 + ext), '+X': (x1 + 0.04, x1 + 0.16, y0 - ext, y1 + ext),
          '-Y': (x0 - ext, x1 + ext, y0 - 0.16, y0 - 0.04), '+Y': (x0 - ext, x1 + ext, y1 + 0.04, y1 + 0.16)}[head]
    fb(o, M['stoff_hell'], *hb, z, z + 1.15)
    w = (y1 - y0) if head in ('-X', '+X') else (x1 - x0)
    n = 2 if w > 1.3 else 1
    for k in range(n):
        if head in ('-X', '+X'):
            a = y0 + (k + 0.5) * w / n; xx = x0 + 0.06 if head == '-X' else x1 - 0.48
            fb(o, M['bettwaesche'], xx, xx + 0.42, a - w / n * 0.4, a + w / n * 0.4, z + 0.50, z + 0.66)
            fb(o, M['stoff_hell'], xx + 0.30 if head == '-X' else xx - 0.12, xx + 0.42 if head == '-X' else xx, a - w / n * 0.3, a + w / n * 0.3, z + 0.50, z + 0.62)
        else:
            a = x0 + (k + 0.5) * w / n; yy = y0 + 0.06 if head == '-Y' else y1 - 0.48
            fb(o, M['bettwaesche'], a - w / n * 0.4, a + w / n * 0.4, yy, yy + 0.42, z + 0.50, z + 0.66)
    if head in ('-X', '+X'):
        f0, f1 = (x1 - 0.65, x1 + 0.02) if head == '-X' else (x0 - 0.02, x0 + 0.65)
        fb(o, M['stoff'], f0, f1, y0 - 0.01, y1 + 0.01, z + 0.44, z + 0.53)
    else:
        f0, f1 = (y1 - 0.65, y1 + 0.02) if head == '-Y' else (y0 - 0.02, y0 + 0.65)
        fb(o, M['stoff'], x0 - 0.01, x1 + 0.01, f0, f1, z + 0.44, z + 0.53)
def basin(x0, x1, y0, y1, z, wall):
    """schwebender Waschtisch Nussbaum, Marmorplatte, Aufsatzbecken, hinterleuchteter Spiegel"""
    o = FO['Bad']
    fb(o, M['eiche'], x0, x1, y0, y1, z + 0.45, z + 0.80)
    fb(o, M['arbeitsplatte'], x0 - 0.01, x1 + 0.01, y0 - 0.01, y1 + 0.01, z + 0.80, z + 0.84)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    cyl(o, M['keramik'], cx, cy, z + 0.84, z + 0.97, min(0.2, (x1 - x0) / 2.6, (y1 - y0) / 2.6) if min(x1 - x0, y1 - y0) < 0.45 else 0.19)
    mx = {'-X': (x0 - 0.04, x0, y0 + 0.05, y1 - 0.05), '+X': (x1, x1 + 0.04, y0 + 0.05, y1 - 0.05), '-Y': (x0 + 0.05, x1 - 0.05, y0 - 0.04, y0), '+Y': (x0 + 0.05, x1 - 0.05, y1, y1 + 0.04)}[wall]
    fb(o, M['leuchte'], *mx, z + 1.10, z + 1.90)
    mm = {'-X': (x0 - 0.045, x0 - 0.04, y0 + 0.08, y1 - 0.08), '+X': (x1 + 0.04, x1 + 0.045, y0 + 0.08, y1 - 0.08), '-Y': (x0 + 0.08, x1 - 0.08, y0 - 0.045, y0 - 0.04), '+Y': (x0 + 0.08, x1 - 0.08, y1 + 0.04, y1 + 0.045)}[wall]
    fb(o, M['spiegel'], *mm, z + 1.13, z + 1.87)
def rug(x0, x1, y0, y1, z): fb(FO['Wohnen'], M['teppich'], x0, x1, y0, y1, z + 0.002, z + 0.014)
def pendant(cx, cy, zc, z, r=0.17):
    o = FO['Wohnen']
    cyl(o, M['alu'], cx, cy, z + 1.75, zc, 0.004, 6)
    cyl(o, M['bronze'], cx, cy, z + 1.62, z + 1.75, r, 32)
    cyl(o, M['leuchte'], cx, cy, z + 1.60, z + 1.62, r - 0.02, 32)
def olive(cx, cy, z):
    o = FO['Wohnen']
    cyl(o, M['topf'], cx, cy, z, z + 0.48, 0.30, 32)
    cyl(o, M['eiche'], cx, cy, z + 0.48, z + 1.35, 0.04, 8)
    for (dx, dy, dz, r) in [(0, 0, 1.75, 0.42), (0.18, 0.1, 1.55, 0.3), (-0.15, -0.12, 1.6, 0.32), (0.05, -0.2, 1.95, 0.26)]:
        icoblob(o, M['olive'], V((cx + dx, cy + dy, z + dz)), r, 1.0, 1.0, 0.8)
def art(wall, a0, a1, z0, z1, wv, m):
    o = FO['Wohnen']
    if wall in ('X+', 'X-'):
        fb(o, m, wv - (0.04 if wall == 'X+' else 0), wv + (0 if wall == 'X+' else 0.04), a0, a1, z0, z1)
    else:
        fb(o, m, a0, a1, wv - (0.04 if wall == 'Y+' else 0), wv + (0 if wall == 'Y+' else 0.04), z0, z1)
def toilet(wx, wy, z, d):
    """wandhaengendes WC: (wx, wy) Mitte Wandseite, d = Blickrichtung '+X','-X','+Y','-Y'"""
    o = FO['Bad']
    ux, uy = {'+X': (1, 0), '-X': (-1, 0), '+Y': (0, 1), '-Y': (0, -1)}[d]; px, py = -uy, ux
    def rb(a0, a1, b0, b1, z0, z1, m):
        xs = [wx + ux * a + px * b for a in (a0, a1) for b in (b0, b1)]; ys = [wy + uy * a + py * b for a in (a0, a1) for b in (b0, b1)]
        fb(o, m, min(xs), max(xs), min(ys), max(ys), z + z0, z + z1)
    rb(0.0, 0.16, -0.25, 0.25, 0.0, 1.10, M['fliesen'])          # Vorwand
    rb(0.0, 0.02, -0.12, 0.12, 0.95, 1.10, M['edelstahl'])      # Druckplatte
    rb(0.16, 0.70, -0.18, 0.18, 0.30, 0.42, M['keramik'])
    rb(0.18, 0.68, -0.17, 0.17, 0.42, 0.44, M['keramik'])
def _basin_alt(x0, x1, y0, y1, z, wall):
    o = FO['Bad']
    fb(o, M['eiche'], x0, x1, y0, y1, z + 0.45, z + 0.82)
    fb(o, M['keramik'], x0 - 0.01, x1 + 0.01, y0 - 0.01, y1 + 0.01, z + 0.82, z + 0.86)
    mx = {'-X': (x0 - 0.005, x0, y0, y1), '+X': (x1, x1 + 0.005, y0, y1), '-Y': (x0, x1, y0 - 0.005, y0), '+Y': (x0, x1, y1, y1 + 0.005)}[wall]
    fb(o, M['spiegel'], *mx, z + 1.05, z + 1.85)
def shower(x0, x1, y0, y1, z, glass):
    o = FO['Bad']
    fb(o, M['fliesen'], x0, x1, y0, y1, z, z + 0.03)
    for side in glass:
        g = {'-X': (x0, x0 + 0.01, y0, y1), '+X': (x1 - 0.01, x1, y0, y1), '-Y': (x0, x1, y0, y0 + 0.01), '+Y': (x0, x1, y1 - 0.01, y1)}[side]
        fb(o, M['glas'], *g, z + 0.03, z + 2.00)
        fb(o, M['edelstahl'], *g, z + 2.00, z + 2.02)
def tub(x0, x1, y0, y1, z):
    o = FO['Bad']; t = 0.07
    fb(o, M['keramik'], x0, x1, y0, y1, z, z + 0.10)
    for (a, b, c, d) in [(x0, x0 + t, y0, y1), (x1 - t, x1, y0, y1), (x0, x1, y0, y0 + t), (x0, x1, y1 - t, y1)]:
        fb(o, M['keramik'], a, b, c, d, z + 0.10, z + 0.58)
def shelf(x0, x1, y0, y1, z, h=2.0):
    o = FO['Schraenke']
    for k in range(5):
        zz = z + k * (h - 0.03) / 4
        fb(o, M['eiche'], x0, x1, y0, y1, zz, zz + 0.03)
    for (a, b) in [(x0, x0 + 0.02), (x1 - 0.02, x1)] if (x1 - x0) > (y1 - y0) else [(y0, y0 + 0.02), (y1 - 0.02, y1)]:
        if (x1 - x0) > (y1 - y0): fb(o, M['eiche'], a, b, y0, y1, z, z + h)
        else: fb(o, M['eiche'], x0, x1, a, b, z, z + h)

UG, EG, OG, DG = -2.88, 0.0, 2.96, 5.84
# ---------------- Haus A
# EG: Kueche (Zeile an WC-Wand + Insel mit Kochfeld und Barhockern), Essen, Wohnen, Diele, WC
counter(1.40, 1.99, 0.40, 1.79, EG, sink=(1.55, 1.85, 0.47, 0.85), wall='-X')
tall(1.40, 1.99, 1.79, 2.40, EG)
counter(3.03, 3.96, 0.05, 1.79, EG, hob=(3.17, 3.67, 0.45, 1.20), waterfall=True)
tall(3.03, 3.61, 1.79, 2.40, EG)
for yy in (0.25, 0.86, 1.45): stool(4.27, yy, EG)
table(5.82, 6.77, 0.93, 3.02, EG)
for (a, b) in [(1.16, 1.62), (1.82, 2.24), (2.48, 2.93)]:
    chair(5.25, 5.71, a, b, EG, '-X'); chair(6.90, 7.36, a, b, EG, '+X')
sofa(6.20, 6.90, 4.35, 7.42, EG, '+X'); sofa(4.65, 6.20, 6.74, 7.42, EG, '+Y')
lowbox(5.02, 5.67, 4.81, 6.09, EG, 0.32, M['travertin'])
lowbox(3.89, 4.44, 7.00, 7.50, EG, 0.55)
wardrobe(1.35, 1.94, 4.63, 6.45, EG); lowbox(1.60, 1.94, 3.70, 4.63, EG, 0.45, M['eiche'])
toilet(0.365, 0.90, EG, '+X'); basin(1.00, 1.38, 1.55, 2.00, EG, '+X')
# OG: WC, Bad (Wanne, Waschtisch), Kinderzimmer 1+2, Diele
toilet(0.365, 0.90, OG, '+X'); basin(1.00, 1.38, 1.55, 2.00, OG, '+X')
tub(1.40, 2.24, 0.40, 2.38, OG); basin(3.26, 3.75, 0.40, 1.79, OG, '+X'); tall(3.30, 3.75, 1.79, 2.40, OG, o=FO['Bad'], m=M['schrank'])
wardrobe(3.90, 4.36, 0.40, 2.40, OG)
bed(5.37, 7.19, 3.34, 4.35, OG, '+X'); table(5.86, 7.53, 0.40, 1.21, OG); chair(6.29, 6.77, 1.27, 1.81, OG, '+Y'); shelf(4.36, 5.20, 3.99, 4.35, OG)
bed(5.37, 7.19, 6.57, 7.57, OG, '+X'); table(5.37, 6.77, 4.54, 5.39, OG); chair(5.78, 6.29, 5.43, 5.98, OG, '+Y'); wardrobe(4.17, 5.36, 6.98, 7.57, OG)
wardrobe(1.35, 1.94, 3.65, 6.45, OG)
# DG: Schlafen (Doppelbett, Nachttische, Schrankwand), Bad (Dusche, WC, Waschtisch)
bed(3.64, 5.44, 3.63, 5.60, DG, '+Y'); lowbox(3.24, 3.61, 5.16, 5.54, DG, 0.45, M['eiche'], FO['Schlafen']); lowbox(5.46, 5.84, 5.16, 5.54, DG, 0.45, M['eiche'], FO['Schlafen'])
wardrobe(3.09, 6.45, 2.07, 2.68, DG)
shower(3.15, 4.15, 5.80, 6.74, DG, ['+X']); toilet(4.76, 7.70, DG, '-Y'); basin(5.25, 6.18, 7.25, 7.70, DG, '+Y')
# UG: Bad (Dusche, WC, Waschtisch), Diele
shower(0.95, 1.95, 0.40, 1.25, UG, ['+Y']); toilet(1.95, 1.60, UG, '-X'); basin(1.55, 1.95, 1.92, 2.38, UG, '+X')
wardrobe(1.35, 1.94, 3.65, 6.45, UG)
# ---------------- Haus B
counter(6.01, 6.60, 17.56, 20.05, EG, sink=(6.10, 6.45, 17.80, 18.20), hob=(6.08, 6.55, 18.95, 19.67), wall='+X')
counter(4.38, 6.60, 20.05, 20.90, EG, waterfall=True)
for xx in (5.25, 5.77, 6.35): stool(xx, 21.17, EG)
table(1.84, 2.77, 17.42, 19.52, EG)
for (a, b) in [(17.56, 17.99), (18.21, 18.65), (18.86, 19.31)]:
    chair(1.25, 1.72, a, b, EG, '-X'); chair(2.90, 3.37, a, b, EG, '+X')
sofa(0.97, 1.79, 12.48, 15.71, EG, '-X'); sofa(1.79, 3.36, 12.48, 13.30, EG, '-Y')
lowbox(2.31, 2.98, 13.97, 15.26, EG, 0.32, M['travertin']); lowbox(3.58, 4.08, 12.56, 13.06, EG, 0.50)
lowbox(1.12, 1.48, 20.05, 21.38, EG, 0.80)
wardrobe(6.03, 6.63, 13.64, 15.41, EG); lowbox(6.20, 6.63, 15.41, 16.30, EG, 0.45, M['eiche']); wardrobe(4.37, 4.97, 17.68, 18.86, EG)
toilet(7.17, 19.56, EG, '-Y'); basin(7.25, 7.62, 18.10, 18.55, EG, '+X')
toilet(7.17, 19.56, OG, '-Y'); basin(7.25, 7.62, 18.10, 18.55, OG, '+X')
bed(0.38, 2.62, 12.48, 13.48, OG, '-X'); table(1.21, 2.65, 14.69, 15.54, OG); chair(1.67, 2.22, 14.02, 14.63, OG, '-Y'); wardrobe(2.62, 3.81, 12.48, 13.06, OG)
bed(0.55, 2.62, 15.71, 16.71, OG, '-X'); table(0.70, 2.14, 18.84, 19.69, OG); chair(1.16, 1.72, 18.18, 18.78, OG, '-Y'); shelf(2.79, 3.64, 15.71, 16.07, OG)
tall(3.51, 4.10, 17.66, 19.69, OG, o=FO['Bad'], m=M['schrank']); basin(4.27, 4.70, 18.42, 19.35, OG, '-X'); tub(5.75, 6.60, 17.66, 19.69, OG)
wardrobe(6.03, 6.63, 13.64, 16.35, OG)
bed(2.71, 4.91, 13.99, 15.78, DG, '+X'); lowbox(4.53, 4.88, 13.57, 13.95, DG, 0.45, M['eiche'], FO['Schlafen']); lowbox(4.53, 4.88, 15.80, 16.18, DG, 0.45, M['eiche'], FO['Schlafen'])
sofa(1.70, 2.45, 12.70, 13.45, DG, '-X', M['stoff_hell']); wardrobe(1.55, 4.88, 17.39, 18.00, DG)
toilet(6.35, 18.58, UG, '+X'); basin(6.35, 6.75, 17.70, 18.17, UG, '-X'); shower(6.35, 6.95, 18.93, 19.69, UG, ['+X'])
wardrobe(6.03, 6.63, 13.64, 16.35, UG); shelf(0.40, 3.05, 17.70, 18.10, UG); shelf(0.95, 3.05, 19.30, 19.65, UG)
# Atmosphaere: Teppiche, Pendelleuchten, Oliven, Kunst
rug(4.55, 6.15, 4.15, 7.0, EG); rug(5.45, 7.15, 0.6, 3.35, EG)
rug(1.85, 3.60, 13.25, 15.95, EG); rug(1.45, 3.15, 17.10, 19.85, EG)
for yy in (1.45, 1.98, 2.51): pendant(6.30, yy, 2.61, EG)
for xx in (1.98, 2.31, 2.64) if False else (): pass
for yy in (17.95, 18.47, 18.99): pendant(2.31, yy, 2.61, EG)
for yy in (0.55, 1.25): pendant(3.50, yy, 2.61, EG, 0.13)
for xx in (4.95, 5.85): pendant(xx, 20.48, 2.61, EG, 0.13)
olive(7.15, 3.75, EG); olive(1.05, 16.45, EG)
art('X+', 4.8, 6.7, 1.15, 2.25, 7.635, M['kunst1']); art('X-', 13.0, 15.2, 1.15, 2.25, 0.365, M['kunst2'])
rug(3.2, 5.9, 3.3, 6.0, DG); rug(2.4, 5.2, 13.6, 16.2, DG)
# Mittelbau DG: Bad (+5,71)
shower(3.40, 4.58, 8.10, 9.30, 5.71, ['-X']); basin(4.20, 4.58, 10.83, 11.94, 5.71, '+X'); lowbox(2.68, 2.96, 8.10, 9.28, 5.71, 0.45, M['eiche'], FO['Bad'])

# ================================================================== KONTEXT (Platzhalter aus Lageplan M 1:500, +-1 m)
ck = '06_Kontext_Nachbarn'
P0 = V((585, 1005)); ex = V((0.974, -0.231)); ey = V((-0.231, -0.974)); sc = 15.9
def lp(px, py):
    d = V((px, py)) - P0
    return (d.dot(ex) / sc - 3.525, d.dot(ey) / sc - 4.86)
NB = {
    'Nachbar_Ost_Nr6_6a': [(790, 550), (946, 522), (1000, 752), (840, 788)],
    'Nachbar_Ost_Nr6_Anbau': [(930, 770), (1022, 750), (1037, 835), (950, 855)],
    'Nachbar_Nord_Nr9_9b': [(443, 152), (590, 123), (646, 408), (500, 438)],
    'Nachbar_West_Nr10': [(278, 768), (458, 718), (463, 855), (305, 887)],
    'Nachbar_West_Nr10_Garage': [(490, 765), (535, 755), (562, 960), (520, 968)],
    'Nachbar_West_gross': [(113, 795), (275, 757), (320, 968), (186, 1003)],
}
for nm, pts in NB.items():
    o = O(nm, ck)
    q = [lp(*p) for p in pts]
    hgt = 2.8 if 'Garage' in nm else 6.2
    prism(o, M['kontext'], q, lambda a, c, t: V((a, c, t)), 0.0, hgt)
    if 'Garage' not in nm and 'Anbau' not in nm:
        # Satteldach, First entlang der laengeren Seite
        p = [V(x) for x in q]
        e1, e2 = (p[1] - p[0]).length, (p[2] - p[1]).length
        if e1 >= e2:
            a0, a1 = (p[0] + p[3]) / 2, (p[1] + p[2]) / 2; base = [p[0], p[1], p[2], p[3]]
            tris = [(p[0], p[3], a0), (p[1], p[2], a1)]; slopes = [(p[0], p[1], a1, a0), (p[3], p[2], a1, a0)]
        else:
            a0, a1 = (p[0] + p[1]) / 2, (p[3] + p[2]) / 2
            tris = [(p[0], p[1], a0), (p[3], p[2], a1)]; slopes = [(p[0], p[3], a1, a0), (p[1], p[2], a1, a0)]
        bm = o['bm']; idr = mi(o, M['kontextd']); idw = mi(o, M['kontext'])
        H2 = hgt + 3.0
        def v3(pp, z): return bm.verts.new((pp.x, pp.y, z))
        cen3 = V((sum(x.x for x in p) / 4, sum(x.y for x in p) / 4, hgt))
        newf = []
        for (t0, t1, t2) in tris:
            f = bm.faces.new([v3(t0, hgt), v3(t1, hgt), v3(t2, H2)]); f.material_index = idw; newf.append(f)
        for (s0, s1, s2, s3) in slopes:
            f = bm.faces.new([v3(s0, hgt), v3(s1, hgt), v3(s2, H2), v3(s3, H2)]); f.material_index = idr; newf.append(f)
        for f in newf:
            f.normal_update()
            if (f.calc_center_median() - cen3).dot(f.normal) < 0:
                f.normal_flip()

# ================================================================== Objekte erzeugen
colls = {}
def get_coll(name):
    if name not in colls:
        c = bpy.data.collections.new(name); scene.collection.children.link(c); colls[name] = c
    return colls[name]

for name, rec in OBJS.items():
    bm = rec['bm']
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6) if name.startswith('CUT_') else None
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for m_ in rec['mats']:
        me.materials.append(m_)
    ob = bpy.data.objects.new(name, me)
    get_coll(rec['coll']).objects.link(ob)
    rec['obj'] = ob

# ------------------------------------------------------------------ Booleans
dg = bpy.context.evaluated_depsgraph_get()
for (tgt, ccol) in BOOLS:
    tname = tgt if isinstance(tgt, str) else [k for k, v in OBJS.items() if v is tgt][0]
    ob = OBJS[tname]['obj']
    col = colls.get(ccol)
    if col is None:
        continue
    mod = ob.modifiers.new('cut', 'BOOLEAN')
    mod.operation = 'DIFFERENCE'; mod.solver = 'EXACT'
    mod.operand_type = 'COLLECTION'; mod.collection = col
    try:
        mod.material_mode = 'TRANSFER'
    except Exception:
        pass
    dg = bpy.context.evaluated_depsgraph_get(); dg.update()
    ev = ob.evaluated_get(dg)
    newme = bpy.data.meshes.new_from_object(ev)
    old = ob.data; ob.modifiers.remove(mod); ob.data = newme; newme.name = old.name
    bpy.data.meshes.remove(old)
    print('boolean', tname, len(newme.polygons))

for (tname, ccol) in BOOLS_I:
    ob = OBJS[tname]['obj']; col = colls.get(ccol)
    for solver in ('EXACT', 'MANIFOLD', 'FLOAT'):
        mod = ob.modifiers.new('int', 'BOOLEAN')
        mod.operation = 'INTERSECT'; mod.solver = solver
        mod.operand_type = 'OBJECT'; mod.object = list(col.objects)[0]
        dg = bpy.context.evaluated_depsgraph_get(); dg.update()
        newme = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
        ob.modifiers.remove(mod)
        print('intersect', tname, solver, len(newme.polygons))
        if len(newme.polygons) > 0:
            old = ob.data; ob.data = newme; newme.name = old.name; bpy.data.meshes.remove(old); break
        bpy.data.meshes.remove(newme)

for cname in list(colls):
    if cname.startswith('CUT_'):
        c = colls.pop(cname)
        for o in list(c.objects):
            bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(c)

# ------------------------------------------------------------------ Haus B drehen
for n in B_objs:
    if n in OBJS and 'obj' in OBJS[n] and OBJS[n]['obj'].name in bpy.data.objects:
        OBJS[n]['obj'].data.transform(ROT_B)

# ------------------------------------------------------------------ UV (Box-Mapping, 1 UV-Einheit = 1 m)
def box_uv(ob):
    me = ob.data
    bm = bmesh.new(); bm.from_mesh(me)
    uv = bm.loops.layers.uv.verify()
    for f in bm.faces:
        n = f.normal; ax = max(range(3), key=lambda i: abs(n[i]))
        for l in f.loops:
            c = l.vert.co
            if ax == 0: l[uv].uv = (c.y * (1 if n.x > 0 else -1), c.z)
            elif ax == 1: l[uv].uv = (c.x * (-1 if n.y > 0 else 1), c.z)
            else: l[uv].uv = (c.x, c.y)
    bm.to_mesh(me); bm.free()

for ob in bpy.data.objects:
    if ob.type == 'MESH':
        box_uv(ob)
        for p in ob.data.polygons:
            p.use_smooth = False

for nm, h in ORIGINS.items():
    ob = OBJS[nm]['obj']
    if nm in TOGGLE: ob['drehwinkel'] = TOGGLE[nm]
    ob.data.transform(Matrix.Translation((-h[0], -h[1], -h[2])))
    ob.location = h

# ------------------------------------------------------------------ Nordausrichtung (Root-Empty)
NORD = 13.8   # Gebaeudeachse weicht um 13,8 Grad nach Westen von Nord ab (Nordpfeil EG / Lageplan)
root = bpy.data.objects.new('Gerlichstr8_ROOT_Nordausrichtung', None)
scene.collection.objects.link(root)
root.empty_display_type = 'ARROWS'; root.empty_display_size = 3
root.matrix_world = Matrix.Rotation(math.radians(NORD), 4, 'Z') @ Matrix.Translation((-W / 2, -TOT / 2, 0))
for ob in bpy.data.objects:
    if ob is not root:
        ob.parent = root

# ------------------------------------------------------------------ Kameras, Licht, Welt
ccam = get_coll('07_Kameras_Licht')
def cam(name, loc, tgt, lens=24, shift_y=0.0):
    cd = bpy.data.cameras.new(name); cd.lens = lens; cd.shift_y = shift_y; cd.sensor_width = 36
    co_ = bpy.data.objects.new(name, cd); ccam.objects.link(co_)
    co_.parent = root
    d = V(tgt) - V(loc)
    co_.location = loc
    co_.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return co_

CAMS = [
    cam('CAM_01_Strasse_Suedost', (17.0, -13.0, 1.65), (4.0, 7.0, 4.6), 24, 0.08),
    cam('CAM_02_Strasse_Suedwest', (-9.5, -14.0, 1.65), (4.0, 6.0, 4.8), 24, 0.08),
    cam('CAM_03_Ost_Zufahrt', (10.9, -4.0, 1.65), (5.0, 13.0, 4.5), 18, 0.05),
    cam('CAM_04_Garten_Nordwest', (-12.0, 30.0, 1.65), (4.0, 13.0, 4.8), 24, 0.08),
    cam('CAM_05_Vogel_Suedost', (32.0, -24.0, 24.0), (4.0, 10.0, 3.0), 35),
    cam('CAM_06_Vogel_Nordwest', (-24.0, 40.0, 22.0), (4.0, 10.0, 3.0), 35),
    cam('CAM_07_Strasse_Einfriedung', (2.0, -15.5, 1.65), (4.0, 4.0, 3.2), 24, 0.10),
    cam('CAM_08_Dach_Aussentreppe', (-7.0, 1.5, 13.5), (2.6, 6.2, 8.4), 28),
    cam('CAM_09_DG_Terrasse_West_Treppe', (0.75, 2.2, 7.65), (1.9, 7.2, 7.4), 18),
    cam('INNEN_10_EG_A_Wohnen_Essen', (6.9, 7.1, 1.55), (2.6, 1.2, 1.25), 16),
    cam('INNEN_11_EG_A_Treppe', (1.15, 7.35, 1.6), (2.55, 5.6, 2.1), 16),
    cam('INNEN_12_OG_B_Kind', (6.6, 18.9, 4.5), (2.0, 13.5, 4.1), 16),
    cam('INNEN_13_DG_A_Schlafen', (6.3, 7.2, 7.4), (2.4, 2.4, 6.9), 16),
    cam('INNEN_14_UG_A_Hobby', (6.9, 7.0, -1.3), (2.0, 1.0, -1.6), 16),
    cam('INNEN_15_EG_B_Kueche', (3.0, 15.6, 1.6), (6.0, 20.2, 0.8), 18),
    cam('INNEN_16_OG_A_Bad', (2.9, 2.3, 4.55), (1.8, 0.5, 3.6), 14),
]
def ocam(name, loc, tgt, scale):
    c = cam(name, loc, tgt)
    c.data.type = 'ORTHO'; c.data.ortho_scale = scale; c.data.shift_y = 0.0
    return c
CAMS += [
    ocam('ORTHO_Ansicht_Ost', (60.0, TOT / 2, 5.0), (0.0, TOT / 2, 5.0), 34),
    ocam('ORTHO_Ansicht_West', (-60.0, TOT / 2, 5.0), (8.0, TOT / 2, 5.0), 34),
    ocam('ORTHO_Ansicht_Sued', (W / 2, -60.0, 5.0), (W / 2, 0.0, 5.0), 20),
    ocam('ORTHO_Ansicht_Nord', (W / 2, 80.0, 5.0), (W / 2, 0.0, 5.0), 20),
]
for (lx, ly) in [(4.0, 2.2), (4.0, 6.0), (4.0, 14.0), (4.0, 17.8)]:
    for (lz, nm_) in [(-0.7, 'UG'), (2.3, 'EG'), (5.2, 'OG'), (7.8, 'DG')]:
        ld = bpy.data.lights.new('Innen_Licht_%s' % nm_, 'POINT'); ld.energy = 70; ld.shadow_soft_size = 0.4
        lo = bpy.data.objects.new('Innen_Licht_%s_%.0f' % (nm_, ly), ld); ccam.objects.link(lo); lo.parent = root; lo.location = (lx, ly, lz)
for (lz, nm_) in [(4.6, 'Mitte_OG'), (7.4, 'Mitte_DG')]:
    ld = bpy.data.lights.new('Innen_Licht_' + nm_, 'POINT'); ld.energy = 100; ld.shadow_soft_size = 0.4
    lo = bpy.data.objects.new('Innen_Licht_' + nm_, ld); ccam.objects.link(lo); lo.parent = root; lo.location = (4.0, 10.0, lz)
sd = bpy.data.lights.new('SUN', 'SUN'); sd.energy = 4.0; sd.angle = math.radians(0.6)
sun = bpy.data.objects.new('SUN', sd); ccam.objects.link(sun)
sun.rotation_euler = (math.radians(50), 0, math.radians(35))   # Sonne aus Suedsuedwest, ca. 40 Grad hoch

world = bpy.data.worlds.new('Himmel'); scene.world = world
try:
    world.use_nodes = True
except Exception:
    pass
nt = world.node_tree
bg = nt.nodes.get('Background')
try:
    sky = nt.nodes.new('ShaderNodeTexSky')
    for t in ('MULTIPLE_SCATTERING', 'SINGLE_SCATTERING', 'NISHITA', 'HOSEK_WILKIE'):
        try:
            sky.sky_type = t; break
        except Exception:
            pass
    try:
        sky.sun_elevation = math.radians(40); sky.sun_rotation = math.radians(215)
        sky.sun_disc = False
    except Exception:
        pass
    nt.links.new(sky.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = 0.35
except Exception as e:
    print('sky fail', e)
    bg.inputs[0].default_value = (0.55, 0.7, 0.9, 1)

scene.camera = CAMS[0]
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = int(os.environ.get('SAMPLES', '48'))
scene.cycles.use_denoising = True
scene.render.resolution_x = int(os.environ.get('RESX', '1600'))
scene.render.resolution_y = int(os.environ.get('RESY', '900'))
scene.render.resolution_percentage = 100
try:
    scene.view_settings.view_transform = 'AgX'
except Exception:
    pass

# ------------------------------------------------------------------ Statistik
tris = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in bpy.data.objects if o.type == 'MESH')
print('OBJECTS', len([o for o in bpy.data.objects if o.type == 'MESH']), 'TRIS', tris)

# ------------------------------------------------------------------ Speichern / Export
base = os.path.join(OUT, 'Gerlichstr8_Doppelhaus')
bpy.ops.wm.save_as_mainfile(filepath=base + '.blend', compress=True)
if os.environ.get('EXPORT', '1') == '1':
    sel_meshes = [o for o in bpy.data.objects if o.type in ('MESH', 'EMPTY')]
    bpy.ops.object.select_all(action='DESELECT')
    for o in sel_meshes:
        o.select_set(True)
    bpy.ops.export_scene.fbx(filepath=base + '.fbx', use_selection=True, object_types={'MESH', 'EMPTY'},
                             apply_scale_options='FBX_SCALE_UNITS', mesh_smooth_type='FACE', path_mode='COPY')
    bpy.ops.export_scene.gltf(filepath=base + '.glb', export_format='GLB', use_selection=True, export_extras=True)
    bpy.ops.wm.obj_export(filepath=base + '.obj', export_selected_objects=True, export_materials=True,
                          forward_axis='NEGATIVE_Z', up_axis='Y', export_uv=True, export_normals=True)

# ------------------------------------------------------------------ Vorschau-Renderings
if os.environ.get('RENDER', '1') == '1':
    kontext = colls.get('06_Kontext_Nachbarn')
    only = os.environ.get('CAMS', '')
    for c in CAMS:
        if only and not any(k in c.name for k in only.split(',')):
            continue
        aerial = 'Vogel' in c.name or 'Dach' in c.name
        ortho = 'ORTHO' in c.name
        if ortho: scene.render.resolution_x, scene.render.resolution_y = (1600, 800) if ('Ost' in c.name or 'West' in c.name) else (1000, 800)
        else: scene.render.resolution_x, scene.render.resolution_y = int(os.environ.get('RESX', '1600')), int(os.environ.get('RESY', '900'))
        for o in kontext.objects:
            o.hide_render = not aerial
        scene.view_settings.exposure = 0.9 if 'INNEN' in c.name else 0.0
        scene.camera = c
        scene.render.filepath = os.path.join(OUT, 'vorschau', c.name + '.png')
        bpy.ops.render.render(write_still=True)
        print('rendered', c.name)
    for o in kontext.objects:
        o.hide_render = False
    bpy.ops.wm.save_as_mainfile(filepath=base + '.blend', compress=True)
print('DONE')
