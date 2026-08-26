from pathlib import Path
import re

src=Path('threejs/sky/v09/index.html')
dst=Path('threejs/sky/v10/index.html')
s=src.read_text()

s=s.replace('<!-- Living Field v09: original flyers + clearly visible rainbow flyer flocks -->','<!-- Living Field v10: fixed-color rainbow flyer flocks -->')
s=s.replace('草・空・飛翔体が同じ風場で動き、元の飛翔体とは独立した見やすい小型虹色飛翔体群が別系統で流れるv09','草・空・通常飛翔体が同じ風場で動き、固定色マテリアルの小型虹色飛翔体群が確実に見えるv10')
s=s.replace('Living Field v09 · visible rainbow flyer flocks','Living Field v10 · fixed-color rainbow flyer flocks')
s=s.replace('小型虹色飛翔体を約2倍強に拡大 ／ 手前に出現 ／ vivid instance colors ／ original flyers remain separate','虹色群を固定色マテリアル化 ／ 初期群を画面内に常時出現 ／ vivid fixed colors ／ original flyers remain separate')
s=s.replace('Three.js · GLSL · shared wind field · v09','Three.js · GLSL · shared wind field · v10')

start=s.index('// v08: rainbow particles are removed.')
end=s.index('function updateFragments(dt,t){', start)
block=r'''// v10: rainbow flyers use fixed-color materials instead of instanceColor.
// This avoids white-looking instances and guarantees vivid red/orange/yellow/green/cyan/blue/magenta flyers.
const RAINBOW_PALETTE=[0xff304f,0xff8a1f,0xffd62e,0x28d76f,0x22c8e8,0x3478ff,0xb742ff];
const rainbowFlyerMeshes=RAINBOW_PALETTE.map((hex)=>{
  const mat=new THREE.MeshBasicMaterial({color:hex,transparent:true,opacity:1,side:THREE.DoubleSide,depthWrite:false,toneMapped:false});
  const mesh=new THREE.InstancedMesh(fragGeom,mat,RAINBOW_FLYER_COUNT);
  mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);mesh.frustumCulled=false;mesh.renderOrder=6;scene.add(mesh);return mesh;
});
const rainbowFlyerDummy=new THREE.Object3D();
const rainbowFlyerGroups=[];
const rainbowFlyerSeeds=[];
const tmpRainbowWind=new THREE.Vector2();
let nextRainbowGroupTime=2.6+Math.random()*1.2;

for(let g=0;g<RAINBOW_GROUP_COUNT;g++){
  rainbowFlyerGroups.push({active:false,x:0,y:0,z:0,vx:0,vy:0,vz:0,life:0,duration:7,phase:rand(0,Math.PI*2),spread:.72});
  for(let j=0;j<RAINBOW_FLYERS_PER_GROUP;j++){
    const idx=g*RAINBOW_FLYERS_PER_GROUP+j;
    rainbowFlyerSeeds.push({group:g,color:idx%RAINBOW_PALETTE.length,r:Math.pow(Math.random(),1.5),angle:rand(0,Math.PI*2),y:rand(-1,1),depth:rand(-1,1),phase:rand(0,Math.PI*2),spin:rand(-1.8,1.8),scale:rand(.30,.44),flutter:rand(.8,1.5)});
  }
}
function hideRainbowFlyer(idx){
  const seed=rainbowFlyerSeeds[idx];
  rainbowFlyerDummy.position.set(9999,9999,9999);rainbowFlyerDummy.scale.setScalar(0);rainbowFlyerDummy.updateMatrix();
  rainbowFlyerMeshes[seed.color].setMatrixAt(idx,rainbowFlyerDummy.matrix);
}
for(let i=0;i<RAINBOW_FLYER_COUNT;i++)hideRainbowFlyer(i);
rainbowFlyerMeshes.forEach(m=>m.instanceMatrix.needsUpdate=true);

function activateRainbowGroup(group,t,first=false){
  group.active=true;
  group.x=first?5.2:rand(-9,9);group.z=first?-8.5:rand(-20,2);group.y=first?3.35:rand(2.1,5.4);
  group.life=0;group.duration=first?8.5:rand(6.0,8.0);group.phase=rand(0,Math.PI*2);group.spread=first?.72:rand(.58,.82);
  const wind=sampleWind(group.x,group.z,t,tmpRainbowWind),speed=1.65+wind.strength*2.5;
  group.vx=tmpRainbowWind.x*speed+rand(-.10,.10);group.vz=tmpRainbowWind.y*speed+rand(-.08,.08);group.vy=rand(.01,.06)+wind.lift*.30;
}
activateRainbowGroup(rainbowFlyerGroups[0],0,true);

function hideRainbowGroup(groupIndex){
  const base=groupIndex*RAINBOW_FLYERS_PER_GROUP;
  for(let j=0;j<RAINBOW_FLYERS_PER_GROUP;j++)hideRainbowFlyer(base+j);
}
function updateRainbowFlyerGroups(dt,t){
  const motion=reduced?.18:1;
  for(let g=0;g<RAINBOW_GROUP_COUNT;g++){
    const group=rainbowFlyerGroups[g];
    if(!group.active){hideRainbowGroup(g);continue;}
    group.life+=dt;
    if(group.life>=group.duration||group.z<-94||group.z>10||Math.abs(group.x)>42||group.y>12.5||group.y<-.2){group.active=false;hideRainbowGroup(g);continue;}
    const wind=sampleWind(group.x,group.z,t,tmpRainbowWind);
    const inertia=Math.min(1,dt*(1.75+wind.strength*1.35)),targetSpeed=1.65+wind.strength*3.0;
    group.vx+=(tmpRainbowWind.x*targetSpeed-group.vx)*inertia;group.vz+=(tmpRainbowWind.y*targetSpeed-group.vz)*inertia;group.vy+=(wind.lift*.48+.012-group.vy*.24)*dt;
    group.x+=group.vx*dt*motion;group.z+=group.vz*dt*motion;group.y+=group.vy*dt*motion;
    const speed=Math.hypot(group.vx,group.vz)||1,dirX=group.vx/speed,dirZ=group.vz/speed,sideX=-dirZ,sideZ=dirX;
    const fade=Math.min(1,group.life/.22,Math.max(0,(group.duration-group.life)/.50));
    const base=g*RAINBOW_FLYERS_PER_GROUP;
    for(let j=0;j<RAINBOW_FLYERS_PER_GROUP;j++){
      const idx=base+j,seed=rainbowFlyerSeeds[idx],angle=seed.angle+Math.sin(t*.55+seed.phase)*.15,radius=group.spread*(.16+.52*seed.r);
      const along=Math.cos(angle)*radius*.88+seed.depth*.13,side=Math.sin(angle)*radius*.58;
      const px=group.x+dirX*along+sideX*side,pz=group.z+dirZ*along+sideZ*side,py=group.y+seed.y*radius*.42+Math.sin(t*seed.flutter+seed.phase)*.065;
      const flutter=Math.sin(t*seed.flutter*2.1+seed.phase);
      rainbowFlyerDummy.position.set(px,py,pz);rainbowFlyerDummy.rotation.set(Math.sin(t*.62+seed.phase)*.52,t*seed.spin*.45+seed.phase,flutter*.82);
      const sc=seed.scale*fade*(.95+.07*flutter);rainbowFlyerDummy.scale.set(sc*.82,sc*1.12,1);rainbowFlyerDummy.updateMatrix();
      rainbowFlyerMeshes[seed.color].setMatrixAt(idx,rainbowFlyerDummy.matrix);
    }
  }
  if(!reduced&&t>=nextRainbowGroupTime&&rainbowFlyerGroups.some(g=>!g.active)){
    const group=rainbowFlyerGroups.find(g=>!g.active);activateRainbowGroup(group,t,false);nextRainbowGroupTime=t+rand(3.0,4.8);
  }
  rainbowFlyerMeshes.forEach(m=>m.instanceMatrix.needsUpdate=true);
}

'''
s=s[:start]+block+s[end:]

dst.parent.mkdir(parents=True,exist_ok=True)
dst.write_text(s)

router=Path('threejs/sky/index.html')
r=router.read_text()
r=r.replace("const raw=new URLSearchParams(location.search).get('v')||'09';","const raw=new URLSearchParams(location.search).get('v')||'10';")
r=r.replace("const target=v==='03'?'v03/':(v==='05'?'v05/':(v==='06'?'v06/':(v==='07'?'v07/':(v==='08'?'v08/':'v09/'))));","const target=v==='03'?'v03/':(v==='05'?'v05/':(v==='06'?'v06/':(v==='07'?'v07/':(v==='08'?'v08/':(v==='09'?'v09/':'v10/')))));" )
r=r.replace('<p><a href="v09/">Living Field v09</a> / ','<p><a href="v10/">Living Field v10</a> / <a href="v09/">Living Field v09</a> / ')
router.write_text(r)

m=re.search(r'<script type="module">\n(.*?)\n</script>',s,re.S)
assert m
Path('/tmp/v10.mjs').write_text(m.group(1))
