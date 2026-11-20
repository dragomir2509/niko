import { useEffect, useRef, useState } from "react";

/**
 * MunichMap — interaktive Halbton-Karte für das Ankaufsprofil.
 * Profil A: ganze Stadt + Landkreis. Profil B: Zoom auf die Innenstadt (Mittlerer Ring).
 * Koordinaten der Lagen sind echte Geokoordinaten, projiziert (equirectangular, cos(48.13°)).
 * Farben über currentColor/CSS-Variablen; Basiskarte als statisches SVG-Markup.
 */
export type Profile = "A" | "B";
type Pt = { name: string; profile: "A" | "B" | "AB"; side: "start" | "end"; x: number; y: number };

const W = 1000, H = 1077;
const FULL: [number, number, number, number] = [0, 0, W, H];
const ZOOM: [number, number, number, number] = [315, 258, 520, 560]; // same aspect as W:H
export const MAP_POINTS: Pt[] = [{"name": "Obermenzing", "profile": "A", "side": "end", "x": 259.4, "y": 426.1}, {"name": "Pasing", "profile": "A", "side": "end", "x": 237.5, "y": 491.7}, {"name": "Solln", "profile": "A", "side": "end", "x": 431.2, "y": 819.4}, {"name": "Obersendling", "profile": "A", "side": "end", "x": 471.9, "y": 739.8}, {"name": "Harlaching", "profile": "A", "side": "start", "x": 568.8, "y": 753.8}, {"name": "Berg am Laim", "profile": "A", "side": "start", "x": 775.0, "y": 613.4}, {"name": "Moosach", "profile": "A", "side": "end", "x": 400.0, "y": 351.1}, {"name": "Milbertshofen", "profile": "AB", "side": "start", "x": 593.7, "y": 337.1}, {"name": "Bogenhausen", "profile": "A", "side": "start", "x": 728.1, "y": 477.5}, {"name": "Gräfelfing", "profile": "A", "side": "end", "x": 150.0, "y": 646.1}, {"name": "Pullach", "profile": "A", "side": "end", "x": 428.1, "y": 908.3}, {"name": "Grünwald", "profile": "A", "side": "end", "x": 434.4, "y": 1011.3}, {"name": "Maxvorstadt", "profile": "B", "side": "end", "x": 568.8, "y": 496.3}, {"name": "Lehel", "profile": "B", "side": "start", "x": 634.4, "y": 547.8}, {"name": "Schwabing", "profile": "B", "side": "start", "x": 625.0, "y": 421.4}, {"name": "Au", "profile": "B", "side": "end", "x": 625.0, "y": 608.6}, {"name": "Haidhausen", "profile": "B", "side": "start", "x": 665.6, "y": 585.2}, {"name": "Obergiesing", "profile": "B", "side": "start", "x": 640.6, "y": 669.6}];

const BASE = `<defs>
<pattern id="d1" width="10" height="10" patternUnits="userSpaceOnUse"><circle cx="5" cy="5" r="1" fill="#111111" fill-opacity=".22"/></pattern>
<pattern id="d2" width="10" height="10" patternUnits="userSpaceOnUse"><circle cx="5" cy="5" r="1.7" fill="#111111" fill-opacity=".42"/></pattern>
<pattern id="d3" width="10" height="10" patternUnits="userSpaceOnUse"><circle cx="5" cy="5" r="2.3" fill="#111111" fill-opacity=".62"/></pattern>
</defs>
<rect x="-2000" y="-2000" width="5000" height="5077" fill="url(#d1)"/>
<path d="M421.9 46.8 C489.6 46.8 599.0 54.6 671.9 70.2 C744.8 85.8 807.3 93.6 859.4 140.5 C911.5 187.3 955.7 277.0 984.4 351.2 C1013.0 425.3 1036.5 518.9 1031.2 585.3 C1026.0 651.6 1002.6 702.3 953.1 749.1 C903.6 795.9 802.1 842.8 734.4 866.2 C666.7 889.6 596.4 888.0 546.9 889.6 C497.4 891.2 476.6 891.2 437.5 875.5 C398.4 859.9 343.7 828.7 312.5 795.9 C281.2 763.2 269.8 714.0 250.0 678.9 C230.2 643.8 225.0 624.3 193.7 585.3 C162.5 546.2 92.2 491.6 62.5 444.8 C32.8 398.0 7.8 351.2 15.6 304.3 C23.4 257.5 67.7 202.9 109.4 163.9 C151.0 124.9 213.5 89.7 265.6 70.2 C317.7 50.7 354.2 46.8 421.9 46.8 Z" fill="#F5F4EF"/><path d="M421.9 46.8 C489.6 46.8 599.0 54.6 671.9 70.2 C744.8 85.8 807.3 93.6 859.4 140.5 C911.5 187.3 955.7 277.0 984.4 351.2 C1013.0 425.3 1036.5 518.9 1031.2 585.3 C1026.0 651.6 1002.6 702.3 953.1 749.1 C903.6 795.9 802.1 842.8 734.4 866.2 C666.7 889.6 596.4 888.0 546.9 889.6 C497.4 891.2 476.6 891.2 437.5 875.5 C398.4 859.9 343.7 828.7 312.5 795.9 C281.2 763.2 269.8 714.0 250.0 678.9 C230.2 643.8 225.0 624.3 193.7 585.3 C162.5 546.2 92.2 491.6 62.5 444.8 C32.8 398.0 7.8 351.2 15.6 304.3 C23.4 257.5 67.7 202.9 109.4 163.9 C151.0 124.9 213.5 89.7 265.6 70.2 C317.7 50.7 354.2 46.8 421.9 46.8 Z" fill="url(#d2)"/>
<path d="M562.5 388.6 C585.9 385.5 620.8 390.2 640.6 398.0 C660.4 405.8 672.4 415.9 681.2 435.4 C690.1 454.9 692.2 488.5 693.7 515.0 C695.3 541.6 696.4 571.2 690.6 594.6 C684.9 618.0 675.5 639.9 659.4 655.5 C643.2 671.1 616.7 685.1 593.7 688.3 C570.8 691.4 542.2 683.6 521.9 674.2 C501.6 664.9 482.8 652.4 471.9 632.1 C460.9 611.8 457.8 578.2 456.3 552.5 C454.7 526.7 455.2 500.2 462.5 477.6 C469.8 454.9 483.3 431.5 500.0 416.7 C516.7 401.9 539.1 391.7 562.5 388.6 Z" fill="#F5F4EF"/><path d="M562.5 388.6 C585.9 385.5 620.8 390.2 640.6 398.0 C660.4 405.8 672.4 415.9 681.2 435.4 C690.1 454.9 692.2 488.5 693.7 515.0 C695.3 541.6 696.4 571.2 690.6 594.6 C684.9 618.0 675.5 639.9 659.4 655.5 C643.2 671.1 616.7 685.1 593.7 688.3 C570.8 691.4 542.2 683.6 521.9 674.2 C501.6 664.9 482.8 652.4 471.9 632.1 C460.9 611.8 457.8 578.2 456.3 552.5 C454.7 526.7 455.2 500.2 462.5 477.6 C469.8 454.9 483.3 431.5 500.0 416.7 C516.7 401.9 539.1 391.7 562.5 388.6 Z" fill="url(#d3)"/>
<path d="M428.1 1076.9 C430.7 1061.3 439.6 1012.1 443.7 983.2 C447.9 954.4 444.8 930.9 453.1 903.6 C461.5 876.3 480.2 845.1 493.7 819.4 C507.3 793.6 522.4 772.5 534.4 749.1 C546.4 725.7 552.6 702.3 565.6 678.9 C578.6 655.5 601.0 628.2 612.5 608.7 C624.0 589.2 625.5 579.8 634.4 561.8 C643.2 543.9 657.8 524.4 665.6 501.0 C673.4 477.6 674.0 450.3 681.2 421.4 C688.5 392.5 699.5 359.0 709.4 327.7 C719.3 296.5 728.6 269.2 740.6 234.1 C752.6 199.0 767.7 156.1 781.2 117.1 C794.8 78.0 815.1 19.5 821.9 0.0" fill="none" stroke="#F5F4EF" stroke-width="12"/>
<path d="M428.1 1076.9 C430.7 1061.3 439.6 1012.1 443.7 983.2 C447.9 954.4 444.8 930.9 453.1 903.6 C461.5 876.3 480.2 845.1 493.7 819.4 C507.3 793.6 522.4 772.5 534.4 749.1 C546.4 725.7 552.6 702.3 565.6 678.9 C578.6 655.5 601.0 628.2 612.5 608.7 C624.0 589.2 625.5 579.8 634.4 561.8 C643.2 543.9 657.8 524.4 665.6 501.0 C673.4 477.6 674.0 450.3 681.2 421.4 C688.5 392.5 699.5 359.0 709.4 327.7 C719.3 296.5 728.6 269.2 740.6 234.1 C752.6 199.0 767.7 156.1 781.2 117.1 C794.8 78.0 815.1 19.5 821.9 0.0" fill="none" stroke="#111111" stroke-opacity=".55" stroke-width="1"/>
<path d="M421.9 46.8 C489.6 46.8 599.0 54.6 671.9 70.2 C744.8 85.8 807.3 93.6 859.4 140.5 C911.5 187.3 955.7 277.0 984.4 351.2 C1013.0 425.3 1036.5 518.9 1031.2 585.3 C1026.0 651.6 1002.6 702.3 953.1 749.1 C903.6 795.9 802.1 842.8 734.4 866.2 C666.7 889.6 596.4 888.0 546.9 889.6 C497.4 891.2 476.6 891.2 437.5 875.5 C398.4 859.9 343.7 828.7 312.5 795.9 C281.2 763.2 269.8 714.0 250.0 678.9 C230.2 643.8 225.0 624.3 193.7 585.3 C162.5 546.2 92.2 491.6 62.5 444.8 C32.8 398.0 7.8 351.2 15.6 304.3 C23.4 257.5 67.7 202.9 109.4 163.9 C151.0 124.9 213.5 89.7 265.6 70.2 C317.7 50.7 354.2 46.8 421.9 46.8 Z" fill="none" stroke="#111111" stroke-opacity=".35" stroke-width="1"/>
<path d="M562.5 388.6 C585.9 385.5 620.8 390.2 640.6 398.0 C660.4 405.8 672.4 415.9 681.2 435.4 C690.1 454.9 692.2 488.5 693.7 515.0 C695.3 541.6 696.4 571.2 690.6 594.6 C684.9 618.0 675.5 639.9 659.4 655.5 C643.2 671.1 616.7 685.1 593.7 688.3 C570.8 691.4 542.2 683.6 521.9 674.2 C501.6 664.9 482.8 652.4 471.9 632.1 C460.9 611.8 457.8 578.2 456.3 552.5 C454.7 526.7 455.2 500.2 462.5 477.6 C469.8 454.9 483.3 431.5 500.0 416.7 C516.7 401.9 539.1 391.7 562.5 388.6 Z" fill="none" stroke="#111111" stroke-width="1.4" stroke-dasharray="6 5"/>
<g font-family="IBM Plex Mono, ui-monospace, monospace" font-size="11" letter-spacing="1.6" fill="#111111" fill-opacity=".7">
<text x="769" y="234">ISAR</text>
<text x="442" y="367">MITTLERER RING</text>
<text x="16" y="1061">48.0250° N · 11.3850° E</text>
<text x="984" y="26" text-anchor="end">48.2550° N · 11.7050° E</text>
<text x="984" y="1061" text-anchor="end">STADT &amp; LANDKREIS MÜNCHEN</text>
</g>
<path d="M589.3 550.6h12M595.3 544.6v12" stroke="#111111" stroke-width="1"/>`;

export function MunichMap({ profile, onSelect }: { profile: Profile; onSelect?: (name: string) => void }) {
  const target = profile === "B" ? ZOOM : FULL;
  const [vb, setVb] = useState(target);
  const raf = useRef<number | undefined>(undefined);
  const from = useRef(vb);
  useEffect(() => {
    const reduce = typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce) { setVb(target); return; }
    from.current = vb; const t0 = performance.now(); const dur = 900;
    const ease = (t: number) => 1 - Math.pow(1 - t, 3);
    const tick = (now: number) => {
      const k = ease(Math.min(1, (now - t0) / dur));
      setVb(from.current.map((v, i) => v + (target[i] - v) * k) as typeof vb);
      if (k < 1) raf.current = requestAnimationFrame(tick);
    };
    raf.current = requestAnimationFrame(tick);
    return () => { if (raf.current) cancelAnimationFrame(raf.current); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [profile]);
  const s = W / vb[2]; // zoom factor -> counter-scale markers & labels
  const [hover, setHover] = useState<string | null>(null);
  return (
    <svg viewBox={vb.join(" ")} className="block h-full w-full text-loden" role="img"
      aria-label={profile === "A" ? "Karte: Lagen für Grundstücke und Häuser in München und im Landkreis" : "Karte: Lagen für Mehrfamilienhäuser und Hotels in der Münchner Innenstadt"}>
      <g dangerouslySetInnerHTML={{ __html: BASE }} />
      {MAP_POINTS.map((p) => {
        const on = p.profile.includes(profile);
        const r = 7 / s, fs = 12 / s, dx = (p.side === "end" ? -14 : 14) / s;
        if (!on) return <circle key={p.name} cx={p.x} cy={p.y} r={3 / s} fill="none" stroke="currentColor" strokeOpacity={0.35} strokeWidth={1 / s} />;
        const active = hover === p.name;
        return (
          <g key={p.name} className="cursor-pointer" role="button" tabIndex={0} aria-label={`${p.name}: Objekt in dieser Lage anbieten`}
            onMouseEnter={() => setHover(p.name)} onMouseLeave={() => setHover(null)} onFocus={() => setHover(p.name)} onBlur={() => setHover(null)}
            onClick={() => onSelect?.(p.name)} onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); onSelect?.(p.name); } }}>
            <rect x={p.x - r} y={p.y - r} width={2 * r} height={2 * r} fill={active ? "var(--paper)" : "currentColor"} stroke="currentColor" strokeWidth={1 / s} />
            <path d={`M${p.x - 4 / s} ${p.y}h${8 / s}M${p.x} ${p.y - 4 / s}v${8 / s}`} stroke={active ? "currentColor" : "var(--paper)"} strokeWidth={1.2 / s} />
            <text x={p.x + dx} y={p.y + 4 / s} textAnchor={p.side} fontSize={fs} letterSpacing={1 / s}
              fontFamily="IBM Plex Mono, ui-monospace, monospace" fill="currentColor"
              style={{ paintOrder: "stroke", stroke: "var(--paper)", strokeWidth: 3 / s }}>{p.name.toUpperCase()}</text>
          </g>
        );
      })}
    </svg>
  );
}
