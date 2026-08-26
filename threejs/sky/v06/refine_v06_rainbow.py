from pathlib import Path
import re

p=Path('threejs/sky/v06/index.html')
s=p.read_text()
s=s.replace(
    'v05を基礎に発展 ／ 虹色パーティクルクラスタを少し増量 ／ rainbow particle size ×3',
    'v06 ／ 飛翔体そのものが虹色の粒子群へ変形 ／ 同一重心・同一軌道 ／ compact vivid rainbow swarm'
)
s=s.replace(
    'v05の草原と同じ風場が草・飛翔体・空を動かし、一部の飛翔体だけが時折虹色のパーティクル集合へほどける分岐案',
    '草・空・飛翔体が同じ風場で動き、一部の飛翔体そのものが同じ重心と軌道を保ったまま彩度の高い虹色の粒子群へ変形するv06'
)
start=s.index('// Rebuilt from exact v03:')
end=s.index('function resize(){', start)
block=r'''// v06 refinement: the fragment itself morphs into one compact, vivid rainbow swarm.
// The fragment item remains the single source of truth for position and velocity during the morph.
const rainbowClusters=[];
const tmpRainbowColor=new THREE.Color();
let nextRainbowTime=4.0+Math.random()*4.0;
for(let c=0;c<MAX_RAINBOW_CLUSTERS;c++){
  const positions=new Float32Array(RAINBOW_PARTS*3),colors=new Float32Array(RAINBOW_PARTS*3),seeds=[];
  for(let p=0;p<RAINBOW_PARTS;p++){
    positions[p*3]=9999;positions[p*3+1]=9999;positions[p*3+2]=9999;
    seeds.push({angle:rand(0,Math.PI*2),radius:.08+.92*Math.pow(Math.random(),1.75),height:rand(-1,1),depth:rand(-1,1),phase:rand(0,Math.PI*2),hue:(p/RAINBOW_PARTS+rand(-.025,.025)+1)%1});
  }
  const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.BufferAttribute(positions,3));geo.setAttribute('color',new THREE.BufferAttribute(colors,3));
  const mat=new THREE.PointsMaterial({size:mobile?.27:.345,sizeAttenuation:true,vertexColors:true,transparent:true,opacity:0,depthWrite:false});
  const points=new THREE.Points(geo,mat);points.frustumCulled=false;points.renderOrder=5;scene.add(points);
  rainbowClusters.push({active:false,owner:-1,life:0,duration:1.8,spread:.26,spin:1,hue:0,geo,mat,seeds});
}
function clearRainbowGeometry(cl){const pos=cl.geo.attributes.position.array;for(let p=0;p<RAINBOW_PARTS;p++){pos[p*3]=9999;pos[p*3+1]=9999;pos[p*3+2]=9999;}cl.geo.attributes.position.needsUpdate=true;}
function startRainbow(ownerIndex,it,t){const cl=rainbowClusters.find(c=>!c.active);if(!cl)return false;cl.active=true;cl.owner=ownerIndex;cl.life=0;cl.duration=rand(1.55,2.15);cl.spread=rand(.20,.29)*(0.86+it.base*.34);cl.spin=Math.random()<.5?-1:1;cl.hue=Math.random();cl.mat.opacity=0;it.rainbowing=true;it.rainbowCooldown=rand(9,17);nextRainbowTime=t+rand(5.0,9.0);return true;}
function finishRainbow(cl){if(cl.owner>=0&&fragItems[cl.owner]){const it=fragItems[cl.owner];it.rainbowing=false;it.rainbowCooldown=rand(9,17);}cl.active=false;cl.owner=-1;cl.mat.opacity=0;clearRainbowGeometry(cl);}
function updateRainbowClusters(dt,t){
  for(const cl of rainbowClusters){if(!cl.active)continue;const it=fragItems[cl.owner];if(!it||!it.rainbowing){finishRainbow(cl);continue;}cl.life+=dt;if(cl.life>=cl.duration){finishRainbow(cl);continue;}
    const u=cl.life/cl.duration,fadeIn=Math.min(1,cl.life/.14),fadeOut=Math.min(1,(cl.duration-cl.life)/.34),fade=Math.max(0,Math.min(fadeIn,fadeOut));
    const speed=Math.hypot(it.vx,it.vz)||1,dirX=it.vx/speed,dirZ=it.vz/speed,sideX=-dirZ,sideZ=dirX;
    const compact=.74+.26*Math.sin(Math.min(1,u)*Math.PI*.5),breathe=.96+.055*Math.sin(t*2.1+cl.hue*6.283),pos=cl.geo.attributes.position.array,col=cl.geo.attributes.color.array;
    for(let p=0;p<RAINBOW_PARTS;p++){const seed=cl.seeds[p],o=p*3,angle=seed.angle+cl.spin*cl.life*(.58+.42*seed.radius)+Math.sin(t*.66+seed.phase)*.075,radius=cl.spread*seed.radius*compact*breathe,along=Math.cos(angle)*radius*1.12+seed.depth*radius*.16,side=Math.sin(angle)*radius*.58;pos[o]=it.x+dirX*along+sideX*side;pos[o+1]=it.y+seed.height*radius*.52+Math.sin(t*1.35+seed.phase)*radius*.075;pos[o+2]=it.z+dirZ*along+sideZ*side;const hue=(seed.hue+cl.hue*.11+t*.012)%1,light=.50+.07*Math.sin(seed.phase+t*.25);tmpRainbowColor.setHSL(hue,.98,light);col[o]=tmpRainbowColor.r;col[o+1]=tmpRainbowColor.g;col[o+2]=tmpRainbowColor.b;}
    cl.mat.opacity=.96*fade;cl.geo.attributes.position.needsUpdate=true;cl.geo.attributes.color.needsUpdate=true;
  }
}
function updateFragments(dt,t){
  const motion=reduced?.20:1;let candidate=-1,candidateScore=.96;
  for(let i=0;i<FRAG_COUNT;i++){const it=fragItems[i],wind=sampleWind(it.x,it.z,t,tmpWind);it.rainbowCooldown-=dt;const inertia=Math.min(1,dt*(1.7+wind.strength*1.5)),targetSpeed=1.5+wind.strength*3.4;it.vx+=(tmpWind.x*targetSpeed-it.vx)*inertia;it.vz+=(tmpWind.y*targetSpeed-it.vz)*inertia;const flutterLift=Math.sin(t*1.6+it.phase)*.035+Math.sin(t*.63+it.phase2)*.022;it.vy+=(wind.lift+flutterLift-it.vy*.28)*dt;it.x+=it.vx*dt*motion;it.z+=it.vz*dt*motion;it.y+=it.vy*dt*motion;it.age+=dt;
    if(it.z<-94||it.z>12||Math.abs(it.x)>42||it.y>13.0||it.y<-.15||it.age>24){const owned=rainbowClusters.find(c=>c.active&&c.owner===i);if(owned)finishRainbow(owned);resetFrag(it,false);continue;}
    if(!it.rainbowing&&!reduced&&t>=nextRainbowTime&&it.rainbowEligible&&it.rainbowCooldown<=0&&it.age>.8&&it.z>-48&&it.z<7&&it.y>.28&&it.y<9.4&&wind.strength>candidateScore){candidate=i;candidateScore=wind.strength;}
    if(it.rainbowing){dummy.position.set(9999,9999,9999);dummy.scale.setScalar(0);dummy.updateMatrix();fragments.setMatrixAt(i,dummy.matrix);}else{const flutter=Math.sin(t*it.tumble*2.25+it.phase);dummy.position.set(it.x,it.y,it.z);dummy.rotation.set(Math.sin(t*.72+it.phase2)*.72,t*it.spin*.53+it.phase,flutter*1.05+Math.sin(t*.39+it.phase2)*.28);const sc=it.base*(.92+.10*flutter);dummy.scale.set(sc*(.70+.18*Math.sin(it.phase2)),sc*(1.08+.16*Math.sin(it.phase)),1);dummy.updateMatrix();fragments.setMatrixAt(i,dummy.matrix);}
  }
  if(candidate>=0&&rainbowClusters.some(c=>!c.active)&&startRainbow(candidate,fragItems[candidate],t)){dummy.position.set(9999,9999,9999);dummy.scale.setScalar(0);dummy.updateMatrix();fragments.setMatrixAt(candidate,dummy.matrix);}fragments.instanceMatrix.needsUpdate=true;
}

'''
s=s[:start]+block+s[end:]
p.write_text(s)

m=re.search(r'<script type="module">\n(.*?)\n</script>',s,re.S)
assert m
Path('/tmp/v06.mjs').write_text(m.group(1))
