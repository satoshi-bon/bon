from pathlib import Path
import re

src=Path('threejs/sky/v07/index.html')
dst=Path('threejs/sky/v08/index.html')
s=src.read_text()

s=s.replace('<!-- Living Field v07: original flyers + separate compact vivid rainbow swarms -->','<!-- Living Field v08: original flyers + small rainbow flyer flocks -->')
s=s.replace('草・空・飛翔体が同じ風場で動き、元の飛翔体とは独立した彩度の高い虹色パーティクル群も別系統で流れるv07','草・空・飛翔体が同じ風場で動き、元の飛翔体とは独立した小さい虹色飛翔体の群が別系統で流れるv08')
s=s.replace('Living Field v07 · separate rainbow swarms','Living Field v08 · small rainbow flyer flocks')
s=s.replace('元の飛翔体と虹色パーティクルを別系統で共存 ／ compact vivid rainbow swarms ／ shared wind field','虹色パーティクルを廃止 ／ 小さい虹色の飛翔体が群として飛行 ／ original flyers remain separate')
s=s.replace('Three.js · GLSL · shared wind field · v07','Three.js · GLSL · shared wind field · v08')

old_consts='const MAX_RAINBOW_CLUSTERS=mobile?2:3;\nconst RAINBOW_PARTS=mobile?30:48;\nconst RAINBOW_ELIGIBLE_RATE=.14;'
new_consts='const RAINBOW_GROUP_COUNT=mobile?2:3;\nconst RAINBOW_FLYERS_PER_GROUP=mobile?10:14;\nconst RAINBOW_FLYER_COUNT=RAINBOW_GROUP_COUNT*RAINBOW_FLYERS_PER_GROUP;'
if old_consts not in s:
    raise SystemExit('rainbow constants marker not found')
s=s.replace(old_consts,new_consts,1)

old_reset='it.rainbowEligible=Math.random()<RAINBOW_ELIGIBLE_RATE;it.rainbowCooldown=initial?rand(1,7):rand(7,14);it.rainbowing=false;'
s=s.replace(old_reset,'',1)

start=s.index('// v07: original flyers and rainbow particle swarms are separate systems.')
end=s.index('function updateFragments(dt,t){', start)
block=r'''// v08: rainbow particles are removed. Small rainbow flyer flocks are a separate system.
// They use the same flyer geometry as the original airborne objects, only smaller and vividly colored.
const rainbowFlyerMat=new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:.94,side:THREE.DoubleSide,depthWrite:false});
const rainbowFlyers=new THREE.InstancedMesh(fragGeom,rainbowFlyerMat,RAINBOW_FLYER_COUNT);
rainbowFlyers.instanceMatrix.setUsage(THREE.DynamicDrawUsage);rainbowFlyers.frustumCulled=false;rainbowFlyers.renderOrder=5;scene.add(rainbowFlyers);
const rainbowFlyerDummy=new THREE.Object3D();
const rainbowFlyerGroups=[];
const rainbowFlyerSeeds=[];
const tmpRainbowWind=new THREE.Vector2();
const tmpRainbowColor=new THREE.Color();
let nextRainbowGroupTime=2.8+Math.random()*3.8;

for(let g=0;g<RAINBOW_GROUP_COUNT;g++){
  rainbowFlyerGroups.push({active:false,x:0,y:0,z:0,vx:0,vy:0,vz:0,life:0,duration:4,phase:rand(0,Math.PI*2),spread:1});
  for(let j=0;j<RAINBOW_FLYERS_PER_GROUP;j++){
    const idx=g*RAINBOW_FLYERS_PER_GROUP+j;
    const hue=(j/RAINBOW_FLYERS_PER_GROUP+g*.11)%1;
    tmpRainbowColor.setHSL(hue,.98,.55);
    rainbowFlyers.setColorAt(idx,tmpRainbowColor);
    rainbowFlyerSeeds.push({
      group:g,
      r:Math.pow(Math.random(),1.65),
      angle:rand(0,Math.PI*2),
      y:rand(-1,1),
      depth:rand(-1,1),
      phase:rand(0,Math.PI*2),
      spin:rand(-1.8,1.8),
      scale:rand(.16,.25),
      flutter:rand(.8,1.5)
    });
    rainbowFlyerDummy.position.set(9999,9999,9999);rainbowFlyerDummy.scale.setScalar(0);rainbowFlyerDummy.updateMatrix();rainbowFlyers.setMatrixAt(idx,rainbowFlyerDummy.matrix);
  }
}
rainbowFlyers.instanceColor.needsUpdate=true;rainbowFlyers.instanceMatrix.needsUpdate=true;

function startRainbowFlyerGroup(t){
  const group=rainbowFlyerGroups.find(g=>!g.active);if(!group)return false;
  group.active=true;group.x=rand(-11,11);group.z=rand(-48,-4);group.y=rand(1.0,7.0);group.life=0;group.duration=rand(3.4,5.4);group.phase=rand(0,Math.PI*2);group.spread=rand(.72,1.05);
  const wind=sampleWind(group.x,group.z,t,tmpRainbowWind),speed=1.7+wind.strength*2.7;
  group.vx=tmpRainbowWind.x*speed+rand(-.16,.16);group.vz=tmpRainbowWind.y*speed+rand(-.10,.10);group.vy=rand(.015,.09)+wind.lift*.36;
  nextRainbowGroupTime=t+rand(4.2,7.2);return true;
}

function hideRainbowGroup(groupIndex){
  const base=groupIndex*RAINBOW_FLYERS_PER_GROUP;
  for(let j=0;j<RAINBOW_FLYERS_PER_GROUP;j++){
    rainbowFlyerDummy.position.set(9999,9999,9999);rainbowFlyerDummy.scale.setScalar(0);rainbowFlyerDummy.updateMatrix();rainbowFlyers.setMatrixAt(base+j,rainbowFlyerDummy.matrix);
  }
}

function updateRainbowFlyerGroups(dt,t){
  const motion=reduced?.18:1;
  for(let g=0;g<RAINBOW_GROUP_COUNT;g++){
    const group=rainbowFlyerGroups[g];
    if(!group.active){hideRainbowGroup(g);continue;}
    group.life+=dt;
    if(group.life>=group.duration||group.z<-94||group.z>10||Math.abs(group.x)>42||group.y>12.5||group.y<-.2){group.active=false;hideRainbowGroup(g);continue;}
    const wind=sampleWind(group.x,group.z,t,tmpRainbowWind);
    const inertia=Math.min(1,dt*(1.8+wind.strength*1.45)),targetSpeed=1.7+wind.strength*3.15;
    group.vx+=(tmpRainbowWind.x*targetSpeed-group.vx)*inertia;group.vz+=(tmpRainbowWind.y*targetSpeed-group.vz)*inertia;group.vy+=(wind.lift*.55+.015-group.vy*.25)*dt;
    group.x+=group.vx*dt*motion;group.z+=group.vz*dt*motion;group.y+=group.vy*dt*motion;
    const speed=Math.hypot(group.vx,group.vz)||1,dirX=group.vx/speed,dirZ=group.vz/speed,sideX=-dirZ,sideZ=dirX;
    const fade=Math.min(1,group.life/.38,Math.max(0,(group.duration-group.life)/.62));
    const base=g*RAINBOW_FLYERS_PER_GROUP;
    for(let j=0;j<RAINBOW_FLYERS_PER_GROUP;j++){
      const idx=base+j,seed=rainbowFlyerSeeds[idx];
      const angle=seed.angle+Math.sin(t*.55+seed.phase)*.18;
      const radius=group.spread*(.18+.55*seed.r);
      const along=Math.cos(angle)*radius*.90+seed.depth*.16;
      const side=Math.sin(angle)*radius*.62;
      const px=group.x+dirX*along+sideX*side;
      const pz=group.z+dirZ*along+sideZ*side;
      const py=group.y+seed.y*radius*.48+Math.sin(t*seed.flutter+seed.phase)*.08;
      const flutter=Math.sin(t*seed.flutter*2.1+seed.phase);
      rainbowFlyerDummy.position.set(px,py,pz);
      rainbowFlyerDummy.rotation.set(Math.sin(t*.62+seed.phase)*.55,t*seed.spin*.45+seed.phase,flutter*.85);
      const sc=seed.scale*fade*(.94+.08*flutter);
      rainbowFlyerDummy.scale.set(sc*.82,sc*1.12,1);
      rainbowFlyerDummy.updateMatrix();rainbowFlyers.setMatrixAt(idx,rainbowFlyerDummy.matrix);
    }
  }
  if(!reduced&&t>=nextRainbowGroupTime&&rainbowFlyerGroups.some(g=>!g.active))startRainbowFlyerGroup(t);
  rainbowFlyers.instanceMatrix.needsUpdate=true;
}

'''
s=s[:start]+block+s[end:]
s=s.replace('updateRainbowClusters(dt,elapsed)','updateRainbowFlyerGroups(dt,elapsed)')

# Update router to make v08 explicit and default.
router=Path('threejs/sky/index.html')
r=router.read_text()
r=r.replace("const raw=new URLSearchParams(location.search).get('v')||'07';","const raw=new URLSearchParams(location.search).get('v')||'08';")
r=r.replace("const target=v==='03'?'v03/':(v==='05'?'v05/':(v==='06'?'v06/':'v07/'));","const target=v==='03'?'v03/':(v==='05'?'v05/':(v==='06'?'v06/':(v==='07'?'v07/':'v08/')));")
r=r.replace('<p><a href="v07/">Living Field v07</a> / <a href="v06/">Living Field v06</a> / <a href="v05/">Living Field v05</a> / <a href="v03/">Living Field v03</a></p>','<p><a href="v08/">Living Field v08</a> / <a href="v07/">Living Field v07</a> / <a href="v06/">Living Field v06</a> / <a href="v05/">Living Field v05</a> / <a href="v03/">Living Field v03</a></p>')
router.write_text(r)

dst.parent.mkdir(parents=True,exist_ok=True)
dst.write_text(s)

m=re.search(r'<script type="module">\n(.*?)\n</script>',s,re.S)
if not m: raise SystemExit('module script not found')
Path('/tmp/v08.mjs').write_text(m.group(1))
