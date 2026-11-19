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

mat('putz',     'Putz_hellgrau_Fassade',      '#E3E2DD', 0.85)
mat('putzw',    'Putz_weiss_Portal_Attika',   '#F3F2EE', 0.85)
mat('putzg',    'Putz_grau_Erker',            '#B4B3AF', 0.85)
mat('lisene',   'Lisenen_Eckquaderung',       '#EEECE6', 0.75)
mat('stein',    'Kugeln_Abdeckplatten_Stein', '#F1EFEA', 0.5)
mat('holz',     'Holz_Fassade_Laerche_horizontal', '#C6AC7C', 0.7)
mat('holzt',    'Holz_Terrassendielen',       '#99744F', 0.75)
mat('tuer',     'Holz_Haustuer_Eiche',        '#C4A267', 0.5)
mat('alu',      'Alu_anthrazit_RAL7016',      '#3A3D41', 0.4, 0.6)
mat('aluh',     'Alu_hellgrau_Blechabdeckung','#C8C9CA', 0.4, 0.6)
mat('stehfalz', 'Metall_Stehfalz_hellgrau',   '#BDC0C2', 0.35, 0.7)
mat('glas',     'Glas',                       '#EEF4F6', 0.02, 0.0, 1.0)
mat('beton',    'Sichtbeton_Carport',         '#A9A8A2', 0.85)
mat('gruen',    'Gruendach_extensiv',         '#6D7E45', 0.95)
mat('kies',     'Kies_Dach',                  '#A29D94', 0.95)
mat('platten',  'Terrassenplatten_Dach',      '#8E8B85', 0.7)
mat('rasen',    'Rasen',                      '#5E893B', 0.95)
mat('pflaster', 'Pflaster_Fahrspur',          '#A19D96', 0.85)
mat('asphalt',  'Asphalt_Strasse',            '#47494C', 0.9)
mat('gehweg',   'Gehweg',                     '#B2B0AB', 0.85)
mat('innen',    'Innen_Wand_Decke',           '#EDEAE5', 0.9)
mat('boden',    'Innen_Boden',                '#A58866', 0.6)
mat('pflanze',  'Pflanzen_Platzhalter',       '#4D7834', 0.9)
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

# ================================================================== HAUS (lokal wie Haus A)
def build_house(P, coll, bay):
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
    inn = O(P + '_Innenraum', coll)
    pf = O(P + '_Pflanzen_Platzhalter', coll)
    cM, cE, cD, cX = 'CUT_' + P + '_main', 'CUT_' + P + '_bay', 'CUT_' + P + '_dg', 'CUT_' + P + '_box'
    BOOLS.extend([(sh, cM), (er, cE), (dg, cD), (P + '_Ausstieg', cX)])

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
    obox(po, M['tuer'], *Wf, 3.47, 4.48, 0.0, 2.38, -0.20, -0.13)
    pw, ph = (4.48 - 3.47 - 0.24) / 2, (2.38 - 0.30) / 4
    for i in range(2):
        for j in range(4):
            uu = 3.47 + 0.08 + i * (pw + 0.08); vv = 0.12 + j * (ph + 0.03)
            obox(po, M['tuer'], *Wf, uu, uu + pw, vv, vv + ph - 0.03, -0.13, -0.115)
    obox(po, M['aluh'], *Wf, 4.30, 4.34, 0.9, 1.5, -0.115, -0.06)   # Stossgriff
    # OG-Fenster im Portal (3-teilig, Mitte mit Sprossen)
    window(fr, gl, *Wf, yo0, 3.40, 3.04, 5.23)
    window(fr, gl, *Wf, 3.40, 4.55, 3.04, 5.23, rows=ndiv(3.04, 5.23, 4))
    window(fr, gl, *Wf, 4.55, yo1, 3.04, 5.23)
    # Portalrahmen (weiss, 25 cm vorstehend) + Vordach
    obox(po, M['putzw'], *Wf, 2.46, yo0, 0.0, 5.65, 0.0, 0.25)
    obox(po, M['putzw'], *Wf, yo1, 5.49, 0.0, 5.65, 0.0, 0.25)
    obox(po, M['putzw'], *Wf, 2.46, 5.49, 5.23, 5.65, 0.0, 0.25)
    obox(po, M['putzw'], *Wf, 2.60, 5.35, 2.55, 2.98, 0.0, 1.0)

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

    # ---------- Lisenen (Eckquaderung), Abdeckplatten, Kugeln
    h = 5.88 / 16
    corners = [(-0.03, 0.75, -0.03, 0.75), (W - 0.75, W + 0.03, -0.03, 0.75),
               (-0.03, 0.75, L - 0.75, L + 0.03), (W - 0.75, W + 0.03, L - 0.75, L + 0.03)]
    for (x0, x1, y0, y1) in corners:
        for k in range(16):
            abox(li, M['lisene'], x0, x1, y0, y1, k * h, (k + 1) * h - 0.02)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        abox(li, M['stein'], cx - 0.48, cx + 0.48, cy - 0.48, cy + 0.48, 5.88, 6.04)
        sphere(li, M['stein'], V((cx, cy, 6.04 + 0.275)), 0.275)

    # ---------- Attika / DG-Terrassen (OK Bruestung +6,88 / Pflanzkaesten +7,00)
    for (x0, x1) in [(W - 0.30, W), (0.0, 0.30)]:
        abox(at, M['putz'], x0, x1, 0.75, L - 0.75, 6.0, 6.88)
        abox(at, M['aluh'], x0 - 0.02, x1 + 0.02, 0.73, L - 0.73, 6.88, 6.92)
    abox(at, M['holzt'], 7.005, W - 0.30, 0.75, L, 6.0, 6.035)
    abox(at, M['holzt'], 0.30, 0.92, 0.75, L, 6.0, 6.035)
    abox(at, M['kies'], 0.75, W - 0.75, 0.0, 1.0, 6.0, 6.025)
    for (x0, x1) in [(7.10, 7.68), (0.32, 0.90)]:
        for (y0, y1) in [(0.95, 2.35), (5.75, 7.15)]:
            abox(at, M['alu'], x0, x1, y0, y1, 6.035, 6.95)
            abox(at, M['erde'], x0 + 0.04, x1 - 0.04, y0 + 0.04, y1 - 0.04, 6.95, 6.96)
            for t in (0.2, 0.5, 0.8):
                icoblob(pf, M['pflanze'], V(((x0 + x1) / 2, y0 + (y1 - y0) * t, 7.05)), 0.32, 0.9, 1.0, 0.7)

    # ---------- Dachgeschoss (Mansarde: 70 Grad Sued-/Stirnseite, Ost/West zurueckgesetzt)
    XD0, XD1 = 0.92, 7.005
    prof = [(1.0, 6.0), (1.0 + 2.38 / T70, 8.38), (L, 8.38), (L, 6.0)]
    fYZ = lambda a, c, t: V((t, a, c))
    prism(dg, M['putz'], prof, fYZ, XD0, XD1)
    ext = Polygon([(1.0, 5.0), (1.0, 6.0), (1.0 + 2.38 / T70, 8.38), (L, 8.38), (L, 5.0)])
    inner = ext.buffer(-0.22, join_style='mitre').intersection(sbox(0, 5.99, 20, 20))
    cutprism(cD, M['innen'], list(inner.exterior.coords)[:-1], fYZ, XD0 + 0.22, XD1 - 0.22)
    ED = (V((XD1, 0, 0)), Y_, Z_, X_)
    WD = (V((XD0, 0, 0)), Y_, Z_, -X_)
    ysl = lambda z: 1.0 + (z - 6.0) / T70
    # DG-Fenster Ost (4-teilig) / West (3-teilig)
    window(fr, gl, *ED, 3.28, 6.60, 6.0, 8.10, rec=0.09, cols=ndiv(3.28, 6.60, 4), cutcoll=cD, cutmat=M['putz'], wall_t=0.25)
    window(fr, gl, *WD, 2.56, 5.56, 6.0, 8.10, rec=0.09, cols=ndiv(2.56, 5.56, 3), cutcoll=cD, cutmat=M['putz'], wall_t=0.25)
    clad(ho, M['holz'], *ED, 0.0, 7.23, 6.0, 8.38, holes=[(3.28, 6.60, 6.0, 8.10)], ustart=lambda z: ysl(z) + 0.01)
    clad(ho, M['holz'], *WD, 0.0, L, 6.0, 8.38, holes=[(2.56, 5.56, 6.0, 8.10)], ustart=lambda z: ysl(z) + 0.01)
    # 70-Grad-Flaeche mit Verglasung
    SL = (V((0, 1.0, 6.0)), X_, V((0, C70, S70)), V((0, -S70, C70)))
    s = lambda z: (z - 6.0) / S70
    smax = s(8.38)
    gx0, gx1, gs0, gs1 = 1.93, 6.10, s(6.15), s(8.06)
    window(fr, gl, *SL, gx0, gx1, gs0, gs1, rec=0.06, cols=ndiv(gx0, gx1, 6), rows=[s(7.12)],
           cutcoll=cD, cutmat=M['putz'], wall_t=0.25)
    clad(ho, M['holz'], *SL, XD0, XD1, 0.0, gs1, holes=[(gx0, gx1, gs0, gs1)])
    obox(ho, M['alu'], *SL, XD0, XD1, gs1, smax, 0.0, 0.03)

    # ---------- Dach (+8,38 / +8,62 / Attika +8,85) und Dachterrasse
    abox(da, M['alu'], 0.85, 7.10, 1.29, L, 8.38, 8.62)
    abox(da, M['putzw'], 1.00, 6.95, 1.34, L, 8.62, 8.85)
    abox(da, M['kies'], 1.05, 6.90, 1.39, L - 0.05, 8.85, 8.87)
    RX0, RX1, RY0, RY1 = 1.74, 6.31, 2.55, 7.85
    abox(da, M['platten'], RX0 + 0.04, RX1 - 0.04, RY0 + 0.04, RY1 - 0.04, 8.87, 8.89)
    dd = lambda z: (z - 8.85) * 0.26
    ge = O(P + '_Dachterrasse_Gelaender', coll)
    for k in range(7):
        zb = 8.92 + k * 0.13; zt = zb + 0.07; d = dd(zb + 0.035); t = 0.035
        abox(ge, M['stehfalz'], RX0 + d, RX1 - d, RY0 + d - t / 2, RY0 + d + t / 2, zb, zt)           # Sued
        abox(ge, M['stehfalz'], RX1 - d - t / 2, RX1 - d + t / 2, RY0 + d, RY1 - d, zb, zt)           # Ost
        abox(ge, M['stehfalz'], 3.80, RX1 - d, RY1 - d - t / 2, RY1 - d + t / 2, zb, zt)              # Nord
        abox(ge, M['stehfalz'], RX0 + d - t / 2, RX0 + d + t / 2, RY0 + d, 5.54, zb, zt)              # West
    d = dd(9.80)
    abox(ge, M['alu'], RX0 + d - 0.03, RX1 - d + 0.03, RY0 + d - 0.03, RY0 + d + 0.03, 9.78, 9.82)
    abox(ge, M['alu'], RX1 - d - 0.03, RX1 - d + 0.03, RY0 + d, RY1 - d + 0.03, 9.78, 9.82)
    abox(ge, M['alu'], 3.80, RX1 - d, RY1 - d - 0.03, RY1 - d + 0.03, 9.78, 9.82)
    abox(ge, M['alu'], RX0 + d - 0.03, RX0 + d + 0.03, RY0 + d, 5.54, 9.78, 9.82)
    # geneigte Pfosten
    def posts(p_a, p_b, inward, n):
        for i in range(n + 1):
            p = p_a.lerp(p_b, i / n)
            beam(ge, M['alu'], V((p.x, p.y, 8.87)), V((p.x + inward.x * dd(9.80), p.y + inward.y * dd(9.80), 9.80)), 0.04, 0.04)
    posts(V((RX0, RY0)), V((RX1, RY0)), V((0, 1)), 3)
    posts(V((RX1, RY0)), V((RX1, RY1)), V((-1, 0)), 3)
    posts(V((RX0, RY0)), V((RX0, 5.54)), V((1, 0)), 2)

    # Treppenausstieg (+11,02) und Kamin/Schacht
    bxo = O(P + '_Ausstieg', coll)
    abox(bxo, M['putzw'], 1.0, 2.7, 5.54, L, 8.85, 10.92)
    cutbox(cX, M['innen'], O0, X_, Y_, Z_, 1.2, 2.5, 5.74, L - 0.2, 8.84, 10.72)
    window(fr, gl, V((0, 5.54, 0)), X_, Z_, -Y_, 1.55, 2.50, 8.87, 10.85, rec=0.08, cutcoll=cX, cutmat=M['putzw'], wall_t=0.2)
    window(fr, gl, V((2.7, 0, 0)), Y_, Z_, X_, 5.72, 6.52, 8.87, 10.85, rec=0.08, cutcoll=cX, cutmat=M['putzw'], wall_t=0.2)
    abox(da, M['alu'], 0.95, 2.75, 5.49, L, 10.92, 11.02)
    abox(da, M['putzw'], 2.83, 3.80, 6.65, 7.92, 8.85, 11.02)
    abox(da, M['alu'], 2.80, 3.83, 6.62, 7.95, 11.02, 11.06)

    # ---------- Innenraum (Decken/Boeden, damit Fenster nicht "durchsichtig" wirken)
    abox(inn, M['boden'], 0.3, W - 0.3, 0.3, L - 0.3, -0.03, 0.0)
    abox(inn, M['innen'], 0.365, W - 0.365, 0.365, L - 0.365, 2.61, 2.96)
    abox(inn, M['boden'], 0.365, W - 0.365, 0.365, L - 0.365, 2.96, 2.97)
    abox(inn, M['boden'], bx0 + 0.3, bx1 - 0.3, -bd + 0.3, 0.3, -0.03, 0.0)
    abox(inn, M['boden'], XD0 + 0.22, XD1 - 0.22, 1.3, L - 0.22, 6.0, 6.01)
    abox(inn, M['innen'], 3.6, 3.8, 0.365, L - 0.365, 0.0, 2.61)       # Trennwand EG (Sichtschutz)
    abox(inn, M['innen'], 3.6, 3.8, 0.365, L - 0.365, 2.97, 5.49)      # Trennwand OG
    abox(inn, M['innen'], 3.9, 4.05, 2.0, L - 0.22, 6.01, 8.15)         # Trennwand DG
    return [n for n in OBJS if n.startswith(P + '_')]

A_objs = build_house('A', '01_Haus_A', (1.60, 6.40, 1.14, 2.25, 5.74))
B_objs = build_house('B', '02_Haus_B', (0.75, 7.25, 2.015, 1.88, 6.13))

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
abox(mi_, M['innen'], 3.95, 4.05, L, YB0, 5.71, 8.30)                 # Trennwand Galerie
abox(mi_, M['innen'], 3.95, 4.05, L, YB0, 3.01, 5.53)                 # Trennwand OG

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
# Westliche 45-Grad-Flaeche vollverglast
window(mf, mg, *FW45, 0.06, MID - 0.06, 0.06, lw45 - 0.10, rec=-0.07, fd=0.08, cols=ndiv(0.06, MID - 0.06, 6),
       cutcoll='CUT_M', cutmat=M['stehfalz'], wall_t=0.35)
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
HP = 1.60                         # Pfeilerhoehe (+ Abdeckplatte)
ORIGINS = {}
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
    o = O(name, ce)
    sgn = 1 if xe > xh else -1
    a, b = xh + sgn * 0.02, xe - sgn * 0.01
    x0, x1 = min(a, b), max(a, b)
    abox(o, M['alu'], x0, x0 + 0.06, YF - 0.03, YF + 0.03, 0.06, 1.45)
    abox(o, M['alu'], x1 - 0.06, x1, YF - 0.03, YF + 0.03, 0.06, 1.45)
    abox(o, M['alu'], x0, x1, YF - 0.03, YF + 0.03, 1.39, 1.45)
    abox(o, M['alu'], x0, x1, YF - 0.03, YF + 0.03, 0.06, 0.12)
    stabfeld(o, x0 + 0.06, x1 - 0.06, 0.12, 1.39)
    for zb in (0.25, 1.20):                     # Baender
        abox(o, M['alu'], xh - sgn * 0.0 - 0.015 if sgn > 0 else xh - 0.015, xh + 0.015, YF - 0.045, YF + 0.045, zb, zb + 0.10)
    ORIGINS[name] = (xh, YF, 0.0)
xm_w = (-3.12 + -0.20) / 2
xm_o = (8.20 + 11.15) / 2
fluegel('Tor_West_Fluegel_links', -3.12, xm_w)
fluegel('Tor_West_Fluegel_rechts', -0.20, xm_w)
fluegel('Tor_Ost_Fluegel_links', 8.20, xm_o)
fluegel('Tor_Ost_Fluegel_rechts', 11.15, xm_o)

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
    bpy.ops.export_scene.gltf(filepath=base + '.glb', export_format='GLB', use_selection=True)
    bpy.ops.wm.obj_export(filepath=base + '.obj', export_selected_objects=True, export_materials=True,
                          forward_axis='NEGATIVE_Z', up_axis='Y', export_uv=True, export_normals=True)

# ------------------------------------------------------------------ Vorschau-Renderings
if os.environ.get('RENDER', '1') == '1':
    kontext = colls.get('06_Kontext_Nachbarn')
    only = os.environ.get('CAMS', '')
    for c in CAMS:
        if only and not any(k in c.name for k in only.split(',')):
            continue
        aerial = 'Vogel' in c.name
        ortho = 'ORTHO' in c.name
        if ortho: scene.render.resolution_x, scene.render.resolution_y = (1600, 800) if ('Ost' in c.name or 'West' in c.name) else (1000, 800)
        else: scene.render.resolution_x, scene.render.resolution_y = int(os.environ.get('RESX', '1600')), int(os.environ.get('RESY', '900'))
        for o in kontext.objects:
            o.hide_render = not aerial
        scene.camera = c
        scene.render.filepath = os.path.join(OUT, 'vorschau', c.name + '.png')
        bpy.ops.render.render(write_still=True)
        print('rendered', c.name)
    for o in kontext.objects:
        o.hide_render = False
    bpy.ops.wm.save_as_mainfile(filepath=base + '.blend', compress=True)
print('DONE')
