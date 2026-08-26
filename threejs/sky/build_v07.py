from pathlib import Path
import re

src=Path('threejs/sky/v06/index.html')
dst=Path('threejs/sky/v07/index.html')
dst.parent.mkdir(parents=True, exist_ok=True)
s=src.read_text()

s=s.replace('<!-- Living Field branch: v05 meadow + responsive sky + richer rainbow morph / v06 -->','<!-- Living Field v07: original flyers + separate compact vivid rainbow swarms -->',1)
s=s.replace('BRANCH · v06 · responsive sky × richer rainbow morph','Living Field v07 · separate rainbow swarms',1)
s=s.replace('v06 ／ 飛翔体そのものが虹色の粒子群へ変形 ／ 同一重心・同一軌道 ／ compact vivid rainbow swarm','元の飛翔体と虹色パーティクルを別系統で共存 ／ compact vivid rainbow swarms ／ shared wind field',1)
s=s.replace('Three.js · GLSL · shared wind field · v06','Three.js · GLSL · shared wind field · v07',1)
s=s.replace('草・空・飛翔体が同じ風場で動き、一部の飛翔体そのものが同じ重心と軌道を保ったまま彩度の高い虹色の粒子群へ変形するv06','草・空・飛翔体が同じ風場で動き、元の飛翔体とは独立した彩度の高い虹色パーティクル群も別系統で流れるv07',1)

start=s.index('// v06 refinement:')
end=s.index('function resize(){', start)
block=r'''// v07: original flyers and rainbow particle swarms are separate systems.
// Both sample the same wind field, but neither replaces nor hides the other.
const rainbowClusters=[];
const tmpRainbowWind=new THREE.Vector2();
const tmpRainbowColor=new THREE.Color();
let nextRainbowTime=2.8+Math.random()*3.5;
for(let c=0;c<MAX_RAINBOW_CLUSTERS;c++){
  const positions=new Float32Array(RAINBOW_PARTS*3),colors=new Float32Array(RAINBOW_PARTS*3),seeds=[];
  for(let p=0;p<RAINBOW_PARTS;p++){
    positions[p*3]=9999;positions[p*3+1]=9999;positions[p*3+2]=9999;
    seeds.push({
      angle:rand(0,Math.PI*2),
      radius:.06+.94*Math.pow(Math.random(),1.9),
      height:rand(-1,1),
      depth:rand(-1,1),
      phase:rand(0,Math.PI*2),
      hue:(p/RAINBOW_PARTS+rand(-.02,.02)+1)%1
    });
  }
  const geo=new THREE.BufferGeometry();
  geo.setAttribute('position',new THREE.BufferAttribute(positions,3));
  geo.setAttribute('color',new THREE.BufferAttribute(colors,3));
  const mat=new THREE.PointsMaterial({size:mobile?.27:.345,sizeAttenuation:true,vertexColors:true,transparent:true,opacity:0,depthWrite:false});
  const points=new THREE.Points(geo,mat);points.frustumCulled=false;points.renderOrder=5;scene.add(points);
  rainbowClusters.push({active:false,x:0,y:0,z:0,vx:0,vy:0,vz:0,life:0,duration:1.9,spread:.25,spin:1,hue:0,geo,mat,seeds});
}
function clearRainbowGeometry(cl){
  const pos=cl.geo.attributes.position.array;
  for(let p=0;p<RAINBOW_PARTS;p++){pos[p*3]=9999;pos[p*3+1]=9999;pos[p*3+2]=9999;}
  cl.geo.attributes.position.needsUpdate=true;
}
function startRainbow(t){
  const cl=rainbowClusters.find(c=>!c.active);if(!cl)return false;
  cl.active=true;
  cl.x=rand(-11.5,11.5);cl.z=rand(-46,-5);cl.y=rand(1.0,7.2);
  const wind=sampleWind(cl.x,cl.z,t,tmpRainbowWind);
  const speed=1.7+wind.strength*2.7;
  cl.vx=tmpRainbowWind.x*speed+rand(-.18,.18);cl.vz=tmpRainbowWind.y*speed+rand(-.12,.12);cl.vy=rand(.02,.11)+wind.lift*.42;
  cl.life=0;cl.duration=rand(1.65,2.35);cl.spread=rand(.21,.30);cl.spin=Math.random()<.5?-1:1;cl.hue=Math.random();cl.mat.opacity=0;
  nextRainbowTime=t+rand(3.8,7.0);return true;
}
function finishRainbow(cl){cl.active=false;cl.mat.opacity=0;clearRainbowGeometry(cl);}
function updateRainbowClusters(dt,t){
  const motion=reduced?.18:1;
  for(const cl of rainbowClusters){
    if(!cl.active)continue;
    cl.life+=dt;
    if(cl.life>=cl.duration||cl.z<-94||cl.z>10||Math.abs(cl.x)>42||cl.y>12.5||cl.y<-.2){finishRainbow(cl);continue;}
    const wind=sampleWind(cl.x,cl.z,t,tmpRainbowWind);
    const inertia=Math.min(1,dt*(1.8+wind.strength*1.45)),targetSpeed=1.75+wind.strength*3.2;
    cl.vx+=(tmpRainbowWind.x*targetSpeed-cl.vx)*inertia;cl.vz+=(tmpRainbowWind.y*targetSpeed-cl.vz)*inertia;cl.vy+=(wind.lift*.64+.012-cl.vy*.23)*dt;
    cl.x+=cl.vx*dt*motion;cl.z+=cl.vz*dt*motion;cl.y+=cl.vy*dt*motion;
    const u=cl.life/cl.duration,fadeIn=Math.min(1,cl.life/.12),fadeOut=Math.min(1,(cl.duration-cl.life)/.34),fade=Math.max(0,Math.min(fadeIn,fadeOut));
    const speed=Math.hypot(cl.vx,cl.vz)||1,dirX=cl.vx/speed,dirZ=cl.vz/speed,sideX=-dirZ,sideZ=dirX;
    const compact=.76+.10*Math.sin(t*1.7+cl.hue*6.283),pos=cl.geo.attributes.position.array,col=cl.geo.attributes.color.array;
    for(let p=0;p<RAINBOW_PARTS;p++){
      const seed=cl.seeds[p],o=p*3;
      const angle=seed.angle+cl.spin*cl.life*(.54+.34*seed.radius)+Math.sin(t*.58+seed.phase)*.055;
      const radius=cl.spread*seed.radius*compact;
      const along=Math.cos(angle)*radius*1.04+seed.depth*radius*.11,side=Math.sin(angle)*radius*.52;
      pos[o]=cl.x+dirX*along+sideX*side;
      pos[o+1]=cl.y+seed.height*radius*.46+Math.sin(t*1.22+seed.phase)*radius*.05;
      pos[o+2]=cl.z+dirZ*along+sideZ*side;
      const hue=(seed.hue+cl.hue*.08+t*.009)%1,light=.49+.10*Math.sin(seed.phase+t*.20);
      tmpRainbowColor.setHSL(hue,1.0,light);
      col[o]=tmpRainbowColor.r;col[o+1]=tmpRainbowColor.g;col[o+2]=tmpRainbowColor.b;
    }
    cl.mat.opacity=.98*fade;
    cl.geo.attributes.position.needsUpdate=true;cl.geo.attributes.color.needsUpdate=true;
  }
  if(!reduced&&t>=nextRainbowTime&&rainbowClusters.some(c=>!c.active))startRainbow(t);
}

function updateFragments(dt,t){
  const motion=reduced?.20:1;
  for(let i=0;i<FRAG_COUNT;i++){
    const it=fragItems[i],wind=sampleWind(it.x,it.z,t,tmpWind);it.rainbowCooldown-=dt;
    const inertia=Math.min(1,dt*(1.7+wind.strength*1.5)),targetSpeed=1.5+wind.strength*3.4;
    it.vx+=(tmpWind.x*targetSpeed-it.vx)*inertia;it.vz+=(tmpWind.y*targetSpeed-it.vz)*inertia;
    const flutterLift=Math.sin(t*1.6+it.phase)*.035+Math.sin(t*.63+it.phase2)*.022;
    it.vy+=(wind.lift+flutterLift-it.vy*.28)*dt;
    it.x+=it.vx*dt*motion;it.z+=it.vz*dt*motion;it.y+=it.vy*dt*motion;it.age+=dt;
    if(it.z<-94||it.z>12||Math.abs(it.x)>42||it.y>13.0||it.y<-.15||it.age>24){resetFrag(it,false);continue;}
    const flutter=Math.sin(t*it.tumble*2.25+it.phase);
    dummy.position.set(it.x,it.y,it.z);
    dummy.rotation.set(Math.sin(t*.72+it.phase2)*.72,t*it.spin*.53+it.phase,flutter*1.05+Math.sin(t*.39+it.phase2)*.28);
    const sc=it.base*(.92+.10*flutter);dummy.scale.set(sc*(.70+.18*Math.sin(it.phase2)),sc*(1.08+.16*Math.sin(it.phase)),1);
    dummy.updateMatrix();fragments.setMatrixAt(i,dummy.matrix);
  }
  fragments.instanceMatrix.needsUpdate=true;
}

'''
s=s[:start]+block+s[end:]
dst.write_text(s)

router=Path('threejs/sky/index.html')
r=router.read_text()
r=r.replace("const raw=new URLSearchParams(location.search).get('v')||'06';","const raw=new URLSearchParams(location.search).get('v')||'07';")
r=r.replace("const target=v==='03'?'v03/':(v==='05'?'v05/':'v06/');","const target=v==='03'?'v03/':(v==='05'?'v05/':(v==='06'?'v06/':'v07/'));")
r=r.replace('<p><a href="v06/">Living Field v06</a> / <a href="v05/">Living Field v05</a> / <a href="v03/">Living Field v03</a></p>','<p><a href="v07/">Living Field v07</a> / <a href="v06/">Living Field v06</a> / <a href="v05/">Living Field v05</a> / <a href="v03/">Living Field v03</a></p>')
router.write_text(r)

m=re.search(r'<script type="module">\n(.*?)\n</script>',s,re.S)
assert m
Path('/tmp/v07.mjs').write_text(m.group(1))
