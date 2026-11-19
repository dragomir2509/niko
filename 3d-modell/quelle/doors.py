import pymupdf, json, math, sys
S = 72/25.4*10
d = pymupdf.open(sys.argv[1]); p = d[0]
OFF = {'EG':(1250,700,2268,1250,48.906,29.729),'OG':(0,72,1116,630,9.536,7.308),'DG':(1188,72,2268,594,48.907,7.31),'UG':(54,666,1116,1260,9.536,29.73)}
def bc(P0,P1,P2,P3):
    # center from tangents
    t0=(P1[0]-P0[0],P1[1]-P0[1]); t3=(P3[0]-P2[0],P3[1]-P2[1])
    n0=(-t0[1],t0[0]); n3=(-t3[1],t3[0])
    # P0 + a n0 = P3 + b n3
    det = n0[0]*(-n3[1]) - n0[1]*(-n3[0])
    if abs(det)<1e-9: return None
    rx,ry=P3[0]-P0[0],P3[1]-P0[1]
    a=(rx*(-n3[1]) - ry*(-n3[0]))/det
    return (P0[0]+a*n0[0], P0[1]+a*n0[1])
out={k:[] for k in OFF}
for x in p.get_drawings():
    if x.get('fill') is not None and x.get('color') is None: continue
    segs=[it for it in x['items'] if it[0]=='c']
    if not segs: continue
    for reg,(x0,y0,x1,y1,ox,oy) in OFF.items():
        r=x['rect']
        if not (r.x0>=x0 and r.x1<=x1 and r.y0>=y0 and r.y1<=y1): continue
        arcs=[]
        for it in segs:
            P=[( (q.x/S-ox), (q.y/S-oy) ) for q in it[1:5]]   # (Y, X) building
            c=bc(*P)
            if c is None: continue
            r0=math.dist(c,P[0]); r3=math.dist(c,P[3])
            if abs(r0-r3)>0.03: continue
            a0=math.atan2(P[0][1]-c[1],P[0][0]-c[0]); a3=math.atan2(P[3][1]-c[1],P[3][0]-c[0])
            arcs.append(dict(c=c,r=r0,p0=P[0],p3=P[3]))
        # merge consecutive arcs with same center
        merged=[]
        for a in arcs:
            if merged and math.dist(merged[-1]['c'],a['c'])<0.03 and abs(merged[-1]['r']-a['r'])<0.03 and math.dist(merged[-1]['p3'],a['p0'])<0.01:
                merged[-1]['p3']=a['p3']
            else: merged.append(dict(a))
        for a in merged:
            if not (0.55<=a['r']<=1.15): continue
            v0=(a['p0'][0]-a['c'][0],a['p0'][1]-a['c'][1]); v3=(a['p3'][0]-a['c'][0],a['p3'][1]-a['c'][1])
            ang=math.degrees(math.acos(max(-1,min(1,(v0[0]*v3[0]+v0[1]*v3[1])/(a['r']**2)))))
            if 80<ang<100:
                # store as X,Y building coords
                sw=lambda t:(round(t[1],4),round(t[0],4))
                out[reg].append(dict(c=sw(a['c']),r=round(a['r'],3),e1=sw(a['p0']),e2=sw(a['p3'])))
for k in out: print(k,len(out[k]))
json.dump(out,open('door_arcs.json','w'))
