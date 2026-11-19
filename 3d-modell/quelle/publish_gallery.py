import os, json, sys
from PIL import Image, ImageFilter, ImageEnhance, ImageChops, ImageDraw
SRC = sys.argv[1]; DST = sys.argv[2]; os.makedirs(DST, exist_ok=True)
T = {
 'EXT_01_Strasse_Abendsonne': ('Außen', 'Ankommen in der Abendsonne'),
 'EXT_02_SuperSUV_Carport': ('Zufahrt West', 'Carport Haus A'),
 'EXT_03_Gelaendewagen': ('Zufahrt Ost', 'Carport Haus B'),
 'EXT_04_Vogel_Abendsonne': ('Überblick', 'Doppelhaus mit Dachterrassen'),
 'EXT_05_Garten_Lounge': ('Garten Süd', 'Lounge auf der Terrasse'),
 'INT_01_A_Wohnen': ('Haus A · EG', 'Wohnen mit Marmor-Wohnwand'),
 'INT_02_A_Kueche_Essen': ('Haus A · EG', 'Kochinsel und Essplatz'),
 'INT_03_B_Kueche': ('Haus B · EG', 'Küche und Essen'),
 'INT_04_B_Wohnwand': ('Haus B · EG', 'Wohnen mit Wohnwand'),
 'INT_05_A_DG_Schlafen': ('Haus A · DG', 'Master-Schlafzimmer'),
 'INT_06_A_OG_Bad': ('Haus A · OG', 'Bad'),
 'PANO_A_EG_Wohnen': ('360° · Haus A', 'Wohnen, Essen, Küche'),
 'PANO_B_EG_Kueche': ('360° · Haus B', 'Küche und Essen'),
 'PANO_A_DG_Schlafen': ('360° · Haus A', 'Schlafen'),
 'PANO_A_Dachterrasse': ('360°', 'Dachterrasse'),
 'PANO_Garten_Sued': ('360°', 'Garten Süd'),
}
order = list(T)
def grade(im, pano):
    im = im.convert('RGB')
    im = ImageEnhance.Contrast(im).enhance(1.06); im = ImageEnhance.Color(im).enhance(1.05)
    # Glow aus Lichtern
    hi = im.point(lambda v: max(0, v - 200) * 3).filter(ImageFilter.GaussianBlur(radius=max(6, im.width // 160)))
    im = ImageChops.add(im, hi, scale=2.2)
    if not pano:
        w, h = im.size; m = Image.new('L', (w, h), 0); d = ImageDraw.Draw(m)
        d.ellipse([-w * 0.25, -h * 0.35, w * 1.25, h * 1.35], fill=255); m = m.filter(ImageFilter.GaussianBlur(radius=w // 9))
        dark = ImageEnhance.Brightness(im).enhance(0.78); im = Image.composite(im, dark, m)
        im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=40, threshold=2))
    return im
bilder, panos = [], []
for k in order:
    f = os.path.join(SRC, k + '.jpg')
    if not os.path.exists(f): continue
    pano = k.startswith('PANO')
    im = grade(Image.open(f), pano); out = k + '.jpg'; im.save(os.path.join(DST, out), quality=90, optimize=True, progressive=True)
    (panos if pano else bilder).append({'f': out, 'k': T[k][0], 't': T[k][1]})
json.dump({'bilder': bilder, 'panoramen': panos}, open(os.path.join(DST, 'galerie.json'), 'w'), ensure_ascii=False, indent=1)
print(len(bilder), 'Bilder,', len(panos), 'Panoramen')
