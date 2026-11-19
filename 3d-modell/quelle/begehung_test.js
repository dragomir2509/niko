global.THREE = require('three');
const fs = require('fs');
eval(fs.readFileSync('node_modules/three/examples/js/loaders/GLTFLoader.js','utf8'));
const buf = fs.readFileSync(process.argv[2]);
const ab = buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength);
new THREE.GLTFLoader().parse(ab, '', g => run(g.scene), e => console.log('ERR', e));
function run(model){
  const scene = new THREE.Scene(); scene.add(model); model.updateMatrixWorld(true);
  const colliders=[], doors=[];
  model.traverse(o=>{ if(o.userData&&o.userData.drehwinkel!==undefined){o.userData.base=o.rotation.y; doors.push(o);} if(o.isMesh&&!/Pflanzen|Licht/.test(o.name)){ o.userData.bb=new THREE.Box3().setFromObject(o); colliders.push(o);} });
  console.log('Kollisionsobjekte', colliders.length, 'Tueren', doors.length);
  const NORD=13.8*Math.PI/180, CN=Math.cos(NORD), SN=Math.sin(NORD), OX=4.0, OY=10.0275;
  const B2T=(X,Y,Z)=>{const dx=X-OX, dy=Y-OY; return new THREE.Vector3(CN*dx-SN*dy, Z, -(SN*dx+CN*dy));};
  const T2B=v=>{const bx=v.x, by=-v.z; return {X:CN*bx+SN*by+OX, Y:-SN*bx+CN*by+OY, Z:v.y};};
  const dirYaw=(dX,dY)=>{const wx=CN*dX-SN*dY, wz=-(SN*dX+CN*dY); return Math.atan2(-wx,-wz);};
  const P={pos:new THREE.Vector3(), yaw:0, vy:0};
  const RAD=0.26, STEP=0.36; const ray=new THREE.Raycaster(); const near=[];
  function refreshNear(){ near.length=0; const c=P.pos; for(const m of colliders){ const b=m.userData.bb; if(c.x>b.min.x-2&&c.x<b.max.x+2&&c.z>b.min.z-2&&c.z<b.max.z+2&&c.y>b.min.y-3&&c.y<b.max.y+2) near.push(m);} }
  function cast(o,d,far){ ray.set(o,d); ray.far=far; const h=ray.intersectObjects(near,false); return h.length?h[0]:null; }
  const tmpV=new THREE.Vector3(), up=new THREE.Vector3(0,1,0), down=new THREE.Vector3(0,-1,0);
  function moveH(dx,dz){ let mv=new THREE.Vector3(dx,0,dz);
    for(let it=0; it<3 && mv.lengthSq()>1e-10; it++){ const len=mv.length(), dir=mv.clone().normalize(); let blocked=null;
      for(const h of [STEP+0.05,0.95,1.55]){ const o=tmpV.set(P.pos.x,P.pos.y+h,P.pos.z);
        for(const a of [0,0.5,-0.5]){ const d=dir.clone().applyAxisAngle(up,a); const rr=(h<0.5?0.12:RAD); const hit=cast(o,d,len+rr);
          if(hit){ const dd=hit.distance*Math.cos(a)+(RAD-rr); if(!blocked||dd<blocked.d){ const n=hit.face?hit.face.normal.clone().transformDirection(hit.object.matrixWorld):d.clone().negate(); n.y=0; if(n.lengthSq()<1e-6) n.copy(d).negate(); n.normalize(); blocked={d:dd,n,name:hit.object.name}; } } } }
      if(!blocked){ P.pos.add(mv); return null; }
      const allow=Math.max(0,blocked.d-RAD); P.pos.addScaledVector(dir,Math.min(allow,len));
      const rest=mv.clone().multiplyScalar(1-Math.min(allow,len)/len); const vn=rest.dot(blocked.n); if(vn<0) rest.addScaledVector(blocked.n,-vn); mv=rest; P.lastBlock=blocked.name; } }
  function settle(dt){ const o=tmpV.set(P.pos.x,P.pos.y+STEP,P.pos.z); const hit=cast(o,down,40);
    if(hit){ const fy=hit.point.y; if(fy>=P.pos.y-0.02){ P.pos.y+=(fy-P.pos.y)*Math.min(1,dt*18); P.vy=0; } else { P.vy-=9.81*dt; P.pos.y=Math.max(fy,P.pos.y+P.vy*dt); if(P.pos.y===fy) P.vy=0; } P.floor=hit.object.name; }
    else { P.vy-=9.81*dt; P.pos.y+=P.vy*dt; } }
  function walkTo(X,Y,secs=8){ const dt=1/60; for(let t=0;t<secs;t+=dt){ const b=T2B(P.pos); const dX=X-b.X, dY=Y-b.Y; const dist=Math.hypot(dX,dY); if(dist<0.08) break;
      P.yaw=dirYaw(dX,dY); if(Math.round(t*60)%15===0) refreshNear(); const sp=1.5*dt; const fx=-Math.sin(P.yaw), fz=-Math.cos(P.yaw); moveH(fx*Math.min(sp,dist), fz*Math.min(sp,dist)); settle(dt); }
    for(let k=0;k<30;k++) settle(1/60);
    const b=T2B(P.pos); console.log('  Ziel', X.toFixed(2), Y.toFixed(2), '-> erreicht', b.X.toFixed(2), b.Y.toFixed(2), 'Z', b.Z.toFixed(2), 'Boden', P.floor, P.lastBlock?('(zuletzt geblockt: '+P.lastBlock+')'):''); P.lastBlock=null; }
  function spawn(X,Y,Z){ P.pos.copy(B2T(X,Y,Z)); P.vy=0; refreshNear(); for(let k=0;k<30;k++) settle(1/60); const b=T2B(P.pos); console.log('Start', X,Y,Z,'-> Z', b.Z.toFixed(2), P.floor); }
  const SP=[['A EG Wohnen',4.6,3.9,0],['A EG Diele',1.0,6.9,0],['A UG',1.0,6.9,-2.88],['A OG Diele',1.0,6.9,2.96],['A OG Kizi2',5.0,6.1,2.96],['A DG Schlafen',2.6,4.6,5.84],['A Dach',4.2,3.6,8.89],
   ['B EG Wohnen',3.6,15.5,0],['B EG Diele',7.05,13.4,0],['B UG',2.4,14.4,-2.88],['B OG Diele',7.05,13.4,2.96],['B OG Kizi2',3.0,14.2,2.96],['B DG Schlafen',2.0,15.0,5.84],['B Dach',3.8,16.4,8.89],['Gehweg',9.8,-6.0,0],['Terrasse A',3.6,-2.6,0.03]];
  for(const s_ of SP){ process.stdout.write(s_[0]+': '); spawn(s_[1],s_[2],s_[3]); }
  console.log('--- UG A: Treppe runter und in die Diele');
  spawn(1.0,6.9,0); walkTo(1.0,3.0); walkTo(2.53,3.3); walkTo(2.53,7.25,12); walkTo(1.0,7.0); walkTo(1.0,4.0);
  console.log('--- B OG -> Mittelbau (Arbeiten)');
  spawn(7.05,13.4,2.96); walkTo(7.05,12.7); walkTo(6.0,12.6); walkTo(6.0,11.5); walkTo(4.0,10.5);
  console.log('--- B DG Ostterrasse -> Aussentreppe -> Dach');
  spawn(7.3,16.0,6.04); walkTo(7.3,14.45); walkTo(6.61,14.2); walkTo(6.61,13.35,4); walkTo(6.4,12.75); walkTo(5.7,12.75); walkTo(5.7,13.35); walkTo(5.7,14.85,6); walkTo(4.5,15.5);
}
