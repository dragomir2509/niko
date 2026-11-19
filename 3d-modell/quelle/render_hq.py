# -*- coding: utf-8 -*-
"""Fotorealistische Renderings (Cycles) aus Gerlichstr8_Doppelhaus.blend:
prozedurale Materialien, Kantenrundung, Rasen aus Halmen, Sonne/Himmel nach Tageszeit, Innenlicht, 360-Grad-Panoramen."""
import bpy, math, os, sys
from mathutils import Vector as V, Matrix

BLEND = os.environ['BLEND']; OUT = os.environ.get('HQOUT', '/tmp/hq'); os.makedirs(OUT, exist_ok=True)
ONLY = os.environ.get('SHOTS', ''); SCALE = float(os.environ.get('SCALE', '1.0')); SPP = int(os.environ.get('SPP', '128'))
bpy.ops.wm.open_mainfile(filepath=BLEND)
sc = bpy.context.scene
root = bpy.data.objects['Gerlichstr8_ROOT_Nordausrichtung']
for c in list(bpy.data.collections):
    if c.name.startswith('06_Kontext'):
        for o in c.objects: o.hide_render = False
for o in list(bpy.data.objects):
    if o.type == 'LIGHT' or (o.type == 'CAMERA'):
        bpy.data.objects.remove(o, do_unlink=True)

# ------------------------------------------------------------------ Materialien
def nodes(m):
    nt = m.node_tree; return nt, nt.nodes, nt.links
def bsdf(m): return m.node_tree.nodes.get('Principled BSDF')
def uvco(nt):
    n = nt.nodes.new('ShaderNodeTexCoord'); return n.outputs['UV']
def add_bevel_bump(m, bump_height=None, bump_strength=0.0, radius=0.006):
    nt, N, Lk = nodes(m); b = bsdf(m)
    bev = N.new('ShaderNodeBevel'); bev.inputs['Radius'].default_value = radius; bev.samples = 6
    if bump_height is not None:
        bu = N.new('ShaderNodeBump'); bu.inputs['Strength'].default_value = bump_strength; bu.inputs['Distance'].default_value = 0.01
        Lk.new(bump_height, bu.inputs['Height']); Lk.new(bev.outputs['Normal'], bu.inputs['Normal']); Lk.new(bu.outputs['Normal'], b.inputs['Normal'])
    else:
        Lk.new(bev.outputs['Normal'], b.inputs['Normal'])
def noise(nt, scale, detail=6, rough=0.55, vec=None):
    n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = scale; n.inputs['Detail'].default_value = detail; n.inputs['Roughness'].default_value = rough
    if vec is not None: nt.links.new(vec, n.inputs['Vector'])
    return n
def ramp(nt, inp, c0, c1, p0=0.3, p1=0.7):
    r = nt.nodes.new('ShaderNodeValToRGB'); r.color_ramp.elements[0].position = p0; r.color_ramp.elements[1].position = p1
    r.color_ramp.elements[0].color = (*c0, 1); r.color_ramp.elements[1].color = (*c1, 1); nt.links.new(inp, r.inputs['Fac']); return r
def lin(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)
def mapping(nt, vec, sx=1, sy=1, sz=1, rz=0):
    mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (sx, sy, sz); mp.inputs['Rotation'].default_value = (0, 0, rz)
    nt.links.new(vec, mp.inputs['Vector']); return mp.outputs['Vector']
def setp(b, **kw):
    for k, v in kw.items():
        try: b.inputs[k].default_value = v
        except Exception: pass

for m in bpy.data.materials:
    if not m.node_tree or not bsdf(m): continue
    nt, N, Lk = nodes(m); b = bsdf(m); name = m.name
    uv = uvco(nt)
    if name.startswith('Putz') or name.startswith('Innen_Wand'):
        n = noise(nt, 140, 8, 0.6, uv); add_bevel_bump(m, n.outputs['Fac'], 0.06, 0.008)
        setp(b, Roughness=0.9)
    elif name.startswith('Parkett'):
        br = N.new('ShaderNodeTexBrick'); Lk.new(mapping(nt, uv, 1, 1, 1), br.inputs['Vector'])
        br.inputs['Scale'].default_value = 1.0; br.inputs['Brick Width'].default_value = 1.9; br.inputs['Row Height'].default_value = 0.19
        br.inputs['Mortar Size'].default_value = 0.0025; br.offset = 0.37; br.inputs['Bias'].default_value = 0.0
        br.inputs['Color1'].default_value = (*lin('#C7A57C'), 1); br.inputs['Color2'].default_value = (*lin('#B08A60'), 1); br.inputs['Mortar'].default_value = (*lin('#6A5038'), 1)
        wv = N.new('ShaderNodeTexWave'); wv.inputs['Scale'].default_value = 3.0; wv.inputs['Distortion'].default_value = 8; wv.inputs['Detail'].default_value = 4
        Lk.new(mapping(nt, uv, 0.15, 6, 1), wv.inputs['Vector'])
        mix = N.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.blend_type = 'MULTIPLY'; mix.inputs['Factor'].default_value = 0.22
        Lk.new(br.outputs['Color'], mix.inputs['A']); Lk.new(wv.outputs['Color'], mix.inputs['B']); Lk.new(mix.outputs['Result'], b.inputs['Base Color'])
        setp(b, Roughness=0.38); add_bevel_bump(m, br.outputs['Fac'], 0.25, 0.004)
    elif 'Marmor' in name:
        n = noise(nt, 2.5, 4, 0.5, uv)
        wv = N.new('ShaderNodeTexWave'); wv.inputs['Scale'].default_value = 0.6; wv.inputs['Distortion'].default_value = 9; wv.inputs['Detail'].default_value = 10; wv.inputs['Detail Scale'].default_value = 2.5
        Lk.new(uv, wv.inputs['Vector'])
        r = ramp(nt, wv.outputs['Fac'], lin('#B7B2AB'), lin('#F3F0EB'), 0.0, 0.05)
        Lk.new(r.outputs['Color'], b.inputs['Base Color']); setp(b, Roughness=0.08); setp(b, **{'Coat Weight': 0.4})
        add_bevel_bump(m, None, 0, 0.004)
    elif 'Travertin' in name:
        wv = N.new('ShaderNodeTexWave'); wv.inputs['Scale'].default_value = 6; wv.inputs['Distortion'].default_value = 5; Lk.new(uv, wv.inputs['Vector'])
        r = ramp(nt, wv.outputs['Fac'], lin('#C9B99E'), lin('#E2D7C4'), 0.2, 0.8); Lk.new(r.outputs['Color'], b.inputs['Base Color'])
        n = noise(nt, 90, 6, 0.7, uv); add_bevel_bump(m, n.outputs['Fac'], 0.2, 0.006); setp(b, Roughness=0.55)
    elif any(k in name for k in ('Nussbaum', 'Eiche', 'Teak', 'Kueche_Front', 'Schrank')):
        wv = N.new('ShaderNodeTexWave'); wv.inputs['Scale'].default_value = 4; wv.inputs['Distortion'].default_value = 6; wv.inputs['Detail'].default_value = 3
        Lk.new(mapping(nt, uv, 0.25, 8, 1), wv.inputs['Vector'])
        base = tuple(b.inputs['Base Color'].default_value)[:3]
        r = ramp(nt, wv.outputs['Fac'], tuple(c * 0.72 for c in base), tuple(min(1, c * 1.15) for c in base), 0.25, 0.85)
        Lk.new(r.outputs['Color'], b.inputs['Base Color']); add_bevel_bump(m, wv.outputs['Fac'], 0.03, 0.005); setp(b, Roughness=0.45)
    elif any(k in name for k in ('Boucle', 'Teppich', 'Outdoor_Polster', 'Vorhang', 'Bettwaesche')):
        n = noise(nt, 260 if 'Boucle' in name else 160, 4, 0.8, uv); add_bevel_bump(m, n.outputs['Fac'], 0.35, 0.02); setp(b, Roughness=0.95)
        setp(b, **{'Sheen Weight': 0.6})
        if 'Vorhang' in name: setp(b, **{'Transmission Weight': 0.35}); b.inputs['Alpha'].default_value = 0.85
    elif 'Leder' in name:
        n = noise(nt, 220, 6, 0.7, uv); add_bevel_bump(m, n.outputs['Fac'], 0.15, 0.02); setp(b, Roughness=0.42); setp(b, **{'Coat Weight': 0.15})
    elif any(k in name for k in ('Fliesen', 'Terrassenplatten', 'Pflaster', 'Gehweg')):
        br = N.new('ShaderNodeTexBrick'); Lk.new(uv, br.inputs['Vector'])
        big = 'Terrassen' in name or 'Fliesen' in name
        br.inputs['Scale'].default_value = 1.0; br.inputs['Brick Width'].default_value = 1.2 if big else 0.3; br.inputs['Row Height'].default_value = 0.6 if big else 0.15
        br.inputs['Mortar Size'].default_value = 0.004; br.offset = 0.5
        base = tuple(b.inputs['Base Color'].default_value)[:3]
        br.inputs['Color1'].default_value = (*base, 1); br.inputs['Color2'].default_value = (*[c * 0.92 for c in base], 1); br.inputs['Mortar'].default_value = (*[c * 0.6 for c in base], 1)
        Lk.new(br.outputs['Color'], b.inputs['Base Color']); add_bevel_bump(m, br.outputs['Fac'], 0.3, 0.004); setp(b, Roughness=0.5 if big else 0.8)
    elif 'Rasen' in name:
        n = noise(nt, 6, 6, 0.6, uv); r = ramp(nt, n.outputs['Fac'], lin('#3E6524'), lin('#6E8F3A')); Lk.new(r.outputs['Color'], b.inputs['Base Color']); setp(b, Roughness=0.9)
    elif 'Asphalt' in name:
        n = noise(nt, 300, 6, 0.8, uv); r = ramp(nt, n.outputs['Fac'], lin('#2C2E31'), lin('#4A4C50')); Lk.new(r.outputs['Color'], b.inputs['Base Color']); add_bevel_bump(m, n.outputs['Fac'], 0.3)
    elif 'Kies' in name or 'Gruendach' in name:
        vo = N.new('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value = 60; Lk.new(uv, vo.inputs['Vector']); add_bevel_bump(m, vo.outputs['Distance'], 0.6)
    elif m.name == 'Glas' or 'Fahrzeug_Glas' in name:
        setp(b, Roughness=0.0, IOR=1.52, **{'Transmission Weight': 1.0 if m.name == 'Glas' else 0.0}); setp(b, **{'Coat Weight': 1.0 if 'Fahrzeug' in name else 0.0})
        if 'Fahrzeug' in name: setp(b, Metallic=0.0, Roughness=0.02)
    elif 'PV_Module' in name:
        br = N.new('ShaderNodeTexBrick'); Lk.new(uv, br.inputs['Vector']); br.inputs['Scale'].default_value = 1.0
        br.inputs['Brick Width'].default_value = 0.16; br.inputs['Row Height'].default_value = 0.16; br.inputs['Mortar Size'].default_value = 0.006; br.offset = 0.0
        br.inputs['Color1'].default_value = (*lin('#141C2A'), 1); br.inputs['Color2'].default_value = (*lin('#18223A'), 1); br.inputs['Mortar'].default_value = (*lin('#7E8796'), 1)
        Lk.new(br.outputs['Color'], b.inputs['Base Color']); setp(b, Roughness=0.06, Metallic=0.2); setp(b, **{'Coat Weight': 1.0})
    elif 'Lack' in name:
        n = noise(nt, 2500, 2, 0.5, uv); setp(b, Metallic=0.75, Roughness=0.32); setp(b, **{'Coat Weight': 1.0, 'Coat Roughness': 0.02})
        Lk.new(n.outputs['Fac'], b.inputs['Roughness']) if False else None
    elif 'Licht_weiss' in name or 'Licht_rot' in name or 'Leuchte' in name:
        col = tuple(b.inputs['Base Color'].default_value)[:3]
        setp(b, **{'Emission Color': (*col, 1), 'Emission Strength': 4.0 if 'Leuchte' in name else 2.0})
    elif 'Baum_Laub' in name or 'Pflanze' in name or 'Hecke' in name:
        n = noise(nt, 30, 6, 0.7, uv); base = tuple(b.inputs['Base Color'].default_value)[:3]
        r = ramp(nt, n.outputs['Fac'], tuple(c * 0.6 for c in base), tuple(min(1, c * 1.25) for c in base)); Lk.new(r.outputs['Color'], b.inputs['Base Color'])
        add_bevel_bump(m, n.outputs['Fac'], 0.8, 0.02); setp(b, Roughness=0.7); setp(b, **{'Subsurface Weight': 0.15})
    elif any(k in name for k in ('Alu', 'Metall', 'Stehfalz', 'Fassadenpaneel', 'Haustuer', 'Bronze', 'Edelstahl')):
        add_bevel_bump(m, None, 0, 0.004)
    else:
        add_bevel_bump(m, None, 0, 0.005)

# Fahrzeuge: Glaettung, Karosserie-Kanten
for o in bpy.data.objects:
    if o.type != 'MESH': continue
    if o.name.startswith('Fahrzeug_SuperSUV_Karosserie'):
        mod = o.modifiers.new('sub', 'SUBSURF'); mod.levels = 1; mod.render_levels = 2
    if o.name.startswith('Fahrzeug_Gelaendewagen_Karosserie'):
        mod = o.modifiers.new('bev', 'BEVEL'); mod.width = 0.035; mod.segments = 4; mod.limit_method = 'ANGLE'
        for p in o.data.polygons: p.use_smooth = True
        try: o.data.shade_smooth()
        except Exception: pass
    if o.name.startswith('Fahrzeug_') and 'Details' in o.name:
        for p in o.data.polygons: p.use_smooth = True

# ------------------------------------------------------------------ Rasen aus Halmen
rasen_mat = bpy.data.materials.get('Rasen')
def lawn(name, x0, x1, y0, y1, dens=900):
    me = bpy.data.meshes.new(name); me.from_pydata([(x0, y0, -0.015), (x1, y0, -0.015), (x1, y1, -0.015), (x0, y1, -0.015)], [], [(0, 1, 2, 3)])
    ob = bpy.data.objects.new(name, me); sc.collection.objects.link(ob); ob.parent = root; me.materials.append(rasen_mat)
    ps = ob.modifiers.new('gras', 'PARTICLE_SYSTEM').particle_system; st = ps.settings
    st.type = 'HAIR'; st.count = int((x1 - x0) * (y1 - y0) * dens); st.hair_length = 0.055; st.use_advanced_hair = False
    st.child_type = 'INTERPOLATED'; st.rendered_child_count = 6; st.child_length = 1.0; st.roughness_2 = 0.03; st.roughness_endpoint = 0.02
    st.root_radius = 1.0; st.tip_radius = 0.0; st.radius_scale = 0.003
    st.material_slot = rasen_mat.name if hasattr(st, 'material_slot') else st.material_slot
for nm, rect in [('Gras_Sued_W', (-0.05, 1.55, -4.40, -1.20)), ('Gras_Sued_O', (5.75, 7.85, -4.40, -1.20)), ('Gras_Sued_M', (1.55, 5.75, -4.40, -3.48)),
                 ('Gras_Nord', (-3.40, 8.10, 24.15, 26.20)), ('Gras_West', (-3.45, -1.70, 10.85, 24.15)), ('Gras_Ost_Streifen', (9.60, 10.48, -3.10, 6.38))]:
    lawn(nm, *rect)

# ------------------------------------------------------------------ Blattwerk (Hecken, Baumkronen) als instanzierte Blaetter
leafme = bpy.data.meshes.new('Blatt')
import math as _m
leafme.from_pydata([(0.035 * _m.cos(a), 0.017 * _m.sin(a), 0.006 * (1 - abs(_m.cos(a)))) for a in [k * _m.pi / 5 for k in range(10)]], [], [tuple(range(10))])
lm = bpy.data.materials.new('Blatt_Instanz'); lm.use_nodes = True if hasattr(lm, 'use_nodes') else None
lb = lm.node_tree.nodes['Principled BSDF']; lb.inputs['Base Color'].default_value = (*lin('#3F5E26'), 1); lb.inputs['Roughness'].default_value = 0.55
try: lb.inputs['Subsurface Weight'].default_value = 0.25; lb.inputs['Transmission Weight'].default_value = 0.15
except Exception: pass
lnt = lm.node_tree; ri = lnt.nodes.new('ShaderNodeObjectInfo'); rr = ramp(lnt, ri.outputs['Random'], lin('#2F4A1C'), lin('#6F8A3A'), 0.0, 1.0); lnt.links.new(rr.outputs['Color'], lb.inputs['Base Color'])
leafme.materials.append(lm)
leaf = bpy.data.objects.new('Blatt', leafme); sc.collection.objects.link(leaf); leaf.location = (0, 0, 0)
def foliage(objname, per_m2, size=1.0):
    o = bpy.data.objects.get(objname)
    if not o: return
    area = sum(p.area for p in o.data.polygons)
    ps = o.modifiers.new('laub', 'PARTICLE_SYSTEM').particle_system; st = ps.settings
    st.type = 'HAIR'; st.use_advanced_hair = False; st.count = int(area * per_m2); st.hair_length = 0.04
    st.render_type = 'OBJECT'; st.instance_object = leaf; st.particle_size = (1.25 if 'Baeume' in objname else 0.95) * size / st.hair_length; st.size_random = 0.6
    st.use_rotations = True; st.rotation_mode = 'NOR'; st.rotation_factor_random = 0.85; st.phase_factor_random = 2.0
    st.emit_from = 'FACE'; st.use_emit_random = True
    print('Laub', objname, st.count)
for m_ in bpy.data.materials:
    if ('Hecke' in m_.name or 'Baum_Laub' in m_.name) and bsdf(m_):
        for l_ in list(m_.node_tree.links):
            if l_.to_socket == bsdf(m_).inputs['Base Color']: m_.node_tree.links.remove(l_)
        bsdf(m_).inputs['Base Color'].default_value = (*lin('#1C2E12'), 1)
for nm_, d_ in [('Gelaende_Hecken_hoch', 3800), ('Einfriedung_Hecke', 3800), ('Aussen_Baeume', 2600), ('A_Pflanzen_Platzhalter', 900), ('B_Pflanzen_Platzhalter', 900), ('Moebel_Wohnen', 0)]:
    if d_ == 0: continue
    foliage(nm_, d_)
for o in bpy.data.objects:
    if o.name.startswith('Tuer_'): o.hide_render = True

# ------------------------------------------------------------------ Licht, Welt, Kamera
def B(x, y, z): return root.matrix_world @ V((x, y, z))
world = sc.world; wnt = world.node_tree
sky = next((n for n in wnt.nodes if n.type == 'TEX_SKY'), None)
bgn = wnt.nodes.get('Background')
sd = bpy.data.lights.new('Sonne', 'SUN'); sd.angle = math.radians(0.55)
sun = bpy.data.objects.new('Sonne', sd); sc.collection.objects.link(sun)
NORD = math.radians(13.8)
def set_time(az_deg, el_deg, strength=4.2, sky_str=1.0):
    """az: Kompass (0=N, 90=O, 180=S, 270=W)"""
    az = math.radians(az_deg); el = math.radians(el_deg)
    d = V((math.sin(az) * math.cos(el), math.cos(az) * math.cos(el), math.sin(el)))
    sun.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()
    sd.energy = strength * max(0.0, min(1.0, (el_deg + 1) / 6)); sd.color = (1.0, 0.92, 0.82) if el_deg > 18 else (1.0, 0.72, 0.48)
    if sky:
        try:
            sky.sun_elevation = el; sky.sun_rotation = math.radians(90 - az_deg) + 0.0
            sky.sun_disc = False
        except Exception: pass
    bgn.inputs[1].default_value = sky_str
interior_lights = []
def interior_on(power):
    for o in interior_lights: bpy.data.objects.remove(o, do_unlink=True)
    interior_lights.clear()
    if power <= 0: return
    spots = [(4.5, 3.4, 2.58), (1.0, 5.5, 2.58), (6.3, 2.0, 2.58), (5.8, 5.6, 5.46), (2.6, 1.2, 5.46), (6.0, 2.6, 5.46), (4.4, 4.4, 8.10),
             (3.4, 15.6, 2.58), (5.6, 19.2, 2.58), (7.0, 15.0, 2.58), (2.2, 15.6, 5.46), (2.0, 18.5, 5.46), (3.4, 15.2, 8.10), (4.0, 10.0, 5.2), (4.0, 10.0, 7.8)]
    for i, p in enumerate(spots):
        ld = bpy.data.lights.new('Innen_%d' % i, 'AREA'); ld.shape = 'RECTANGLE'; ld.size = 1.6; ld.size_y = 1.6; ld.energy = power; ld.color = (1.0, 0.80, 0.58)
        lo = bpy.data.objects.new(ld.name, ld); sc.collection.objects.link(lo); lo.parent = root; lo.location = p; lo.rotation_euler = (0, 0, 0); lo.visible_camera = False; lo.visible_glossy = False; interior_lights.append(lo)
def leuchten(strength):
    for m in bpy.data.materials:
        if 'Leuchte' in m.name and bsdf(m): bsdf(m).inputs['Emission Strength'].default_value = strength
camd = bpy.data.cameras.new('Kamera'); cam = bpy.data.objects.new('Kamera', camd); sc.collection.objects.link(cam); sc.camera = cam
def aim(pos, tgt, lens=24, shift_y=0.0, pano=False, dof=None):
    p = B(*pos); t = B(*tgt); cam.location = p
    cam.rotation_euler = (t - p).to_track_quat('-Z', 'Y').to_euler()
    if pano:
        camd.type = 'PANO'
        try: camd.panorama_type = 'EQUIRECTANGULAR'
        except Exception: camd.cycles.panorama_type = 'EQUIRECTANGULAR'
        cam.rotation_euler = (math.pi / 2, 0, (t - p).to_track_quat('Y', 'Z').to_euler().z)
    else:
        camd.type = 'PERSP'; camd.lens = lens; camd.sensor_width = 36; camd.shift_y = shift_y
    camd.dof.use_dof = dof is not None
    if dof: camd.dof.focus_distance = dof[0]; camd.dof.aperture_fstop = dof[1]

cy = sc.cycles; sc.render.engine = 'CYCLES'; cy.device = 'CPU'; cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.025
cy.use_denoising = True; cy.max_bounces = 8; cy.diffuse_bounces = 4; cy.glossy_bounces = 4; cy.transmission_bounces = 8; cy.caustics_reflective = False; cy.caustics_refractive = False
cy.sample_clamp_indirect = 8.0; sc.render.use_persistent_data = True
sc.view_settings.view_transform = 'AgX'
try: sc.view_settings.look = 'AgX - Medium High Contrast'
except Exception: pass
sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 92

# Aufnahmen: (name, pos, ziel, lens, shift, sonne(az,el), innenlicht W, leuchten, belichtung, pano, dof)
SHOTS = [
    ('EXT_01_Strasse_Abendsonne', (18.6, -14.6, 1.6), (4.5, 6.5, 4.4), 24, 0.10, (248, 17), 0, 4, 0.2, False, None),
    ('EXT_02_SuperSUV_Carport',   (-2.9, -3.2, 1.45), (-1.3, 9.0, 1.4), 26, 0.05, (255, 14), 0, 4, 0.0, False, None),
    ('EXT_03_Gelaendewagen',      (9.25, 11.6, 1.45), (10.05, 23.5, 1.15), 28, 0.04, (215, 38), 0, 3, 0.0, False, None),
    ('EXT_04_Vogel_Abendsonne',   (31.0, -24.0, 23.0), (4.0, 10.0, 3.0), 35, 0.0, (262, 9), 0, 3, 0.0, False, None),
    ('EXT_05_Garten_Lounge',      (7.55, -4.25, 1.5), (2.6, 0.6, 2.6), 22, 0.06, (205, 42), 0, 3, 0.0, False, None),
    ('INT_01_A_Wohnen',           (7.40, 7.35, 1.45), (3.1, 4.6, 1.05), 18, 0.0, (130, 30), 26, 3, 1.85, False, None),
    ('INT_02_A_Kueche_Essen',     (4.45, 6.55, 1.5), (4.6, 0.8, 1.0), 20, 0.0, (130, 30), 26, 3, 1.85, False, None),
    ('INT_03_B_Kueche',           (1.85, 16.62, 1.55), (5.5, 20.6, 0.95), 20, 0.0, (250, 25), 26, 3, 1.85, False, None),
    ('INT_04_B_Wohnwand',         (1.55, 16.7, 1.35), (4.8, 14.5, 1.2), 20, 0.0, (250, 25), 26, 3, 1.85, False, None),
    ('INT_05_A_DG_Schlafen',      (6.35, 2.95, 7.3), (4.3, 5.9, 6.6), 20, 0.0, (120, 35), 26, 3, 1.9, False, None),
    ('INT_06_A_OG_Bad',           (3.0, 2.25, 4.45), (1.6, 0.6, 3.5), 16, 0.0, (180, 45), 26, 4, 1.9, False, None),
    ('PANO_A_EG_Wohnen',          (5.2, 3.6, 1.6), (2.0, 3.6, 1.6), 0, 0.0, (130, 30), 26, 3, 1.85, True, None),
    ('PANO_B_EG_Kueche',          (3.4, 16.5, 1.6), (6.0, 20.0, 1.6), 0, 0.0, (250, 25), 26, 3, 1.85, True, None),
    ('PANO_A_DG_Schlafen',        (3.35, 3.2, 7.45), (5.0, 4.6, 7.45), 0, 0.0, (120, 35), 26, 3, 1.9, True, None),
    ('PANO_A_Dachterrasse',       (4.4, 4.2, 10.45), (4.4, 0.0, 10.45), 0, 0.0, (250, 18), 0, 3, 0.0, True, None),
    ('PANO_Garten_Sued',          (6.6, -2.7, 1.6), (4.0, 3.0, 1.6), 0, 0.0, (205, 42), 0, 3, 0.0, True, None),
]
SHOTS.sort(key=lambda t: next((i for i, k in enumerate(['EXT_02', 'EXT_01', 'INT_01', 'EXT_03', 'INT_03', 'INT_02', 'PANO_A_EG', 'EXT_04', 'INT_05', 'PANO_B_EG', 'PANO_A_Dach', 'EXT_05', 'INT_04', 'INT_06', 'PANO_A_DG', 'PANO_Garten']) if t[0].startswith(k)), 99))
for (nm, pos, tgt, lens, sh, (az, el), ipow, leu, expo, pano, dof) in SHOTS:
    if ONLY and not any(k in nm for k in ONLY.split(',')): continue
    set_time(az, el, sky_str=0.35 if el < 0 else 1.0); interior_on(ipow); leuchten(leu)
    for c in bpy.data.collections:
        if c.name.startswith('06_Kontext'):
            for o in c.objects: o.hide_render = not ('Vogel' in nm)
    sc.view_settings.exposure = expo
    aim(pos, tgt, lens, sh, pano, dof)
    if pano: sc.render.resolution_x, sc.render.resolution_y = int(3072 * SCALE), int(1536 * SCALE); cy.samples = max(16, int(SPP * 0.5))
    else: sc.render.resolution_x, sc.render.resolution_y = int(1600 * SCALE), int(900 * SCALE); cy.samples = SPP
    sc.render.filepath = os.path.join(OUT, nm + '.jpg')
    bpy.ops.render.render(write_still=True)
    print('HQ', nm, flush=True)
print('HQDONE')
