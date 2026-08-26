from pathlib import Path
import hashlib, os

path = Path('threejs/sky/index.html')
s = path.read_text()
expected_blob = '68d8e9367a316e0a59179217083abbe40fb79fc5'
b = s.encode()
actual_blob = hashlib.sha1(f'blob {len(b)}\0'.encode() + b).hexdigest()
if os.getenv('SKIP_BASE_HASH') != '1' and actual_blob != expected_blob:
    raise SystemExit(f'Expected exact v03 blob {expected_blob}, got {actual_blob}')

def one(old, new):
    global s
    if s.count(old) != 1:
        raise SystemExit(f'Anchor count {s.count(old)} for: {old[:90]!r}')
    s = s.replace(old, new, 1)

one('<!-- Living Field branch: v05 meadow + skyborne + responsive sky / branch 03 -->',
    '<!-- Living Field branch: v05 meadow + responsive sky + rebuilt rainbow morph / branch 04R -->')
one('aria-label="v05の草原と同じ風場が、草、空中を舞うもの、空の霞と光の濃淡まで連続して動かす分岐案"',
    'aria-label="v05の草原と同じ風場が草・飛翔体・空を動かし、一部の飛翔体だけが時折虹色のパーティクル集合へほどける分岐案"')
one('<div class="version">BRANCH · v05 meadow × responsive sky</div>',
    '<div class="version">BRANCH · v03 base × rainbow morph</div>')
one('<div class="change">草 ／ 飛翔体 ／ 空の霞・光が同一の風向・gust packet・whirl に連動</div>',
    '<div class="change">v03から再構築 ／ 一部の飛翔体のみ、共有風場の強い地点で虹色パーティクル集合へ変化</div>')
one('<div class="tech">Three.js · GLSL · shared wind field · branch 03</div>',
    '<div class="tech">Three.js · GLSL · shared wind field · branch 04R</div>')
one('const MAX_WHIRLS=2;', '''const MAX_WHIRLS=2;
const MAX_RAINBOW_CLUSTERS=mobile?1:2;
const RAINBOW_PARTS=mobile?26:42;
const RAINBOW_ELIGIBLE_RATE=.11;''')
one('it.age=initial?rand(0,7):0;}',
    'it.age=initial?rand(0,7):0;it.rainbowEligible=Math.random()<RAINBOW_ELIGIBLE_RATE;it.rainbowCooldown=initial?rand(1,7):rand(7,14);it.rainbowing=false;}')

rainbow = r'''
// Rebuilt from exact v03: a rare fragment itself dissolves into a small rainbow Points cloud.
const rainbowClusters=[];
const tmpRainbowWind=new THREE.Vector2();
const tmpRainbowColor=new THREE.Color();
let nextRainbowTime=4.0+Math.random()*4.0;
for(let c=0;c<MAX_RAINBOW_CLUSTERS;c++){
  const positions=new Float32Array(RAINBOW_PARTS*3),colors=new Float32Array(RAINBOW_PARTS*3),seeds=[];
  for(let p=0;p<RAINBOW_PARTS;p++){positions[p*3]=9999;positions[p*3+1]=9999;positions[p*3+2]=9999;seeds.push({angle:rand(0,Math.PI*2),radius:rand(.18,1),height:rand(-1,1),depth:rand(-1,1),phase:rand(0,Math.PI*2),hue:p/RAINBOW_PARTS+rand(-.04,.04)});}
  const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.BufferAttribute(positions,3));geo.setAttribute('color',new THREE.BufferAttribute(colors,3));
  const mat=new THREE.PointsMaterial({size:mobile?.09:.115,sizeAttenuation:true,vertexColors:true,transparent:true,opacity:0,depthWrite:false});
  const points=new THREE.Points(geo,mat);points.frustumCulled=false;points.renderOrder=5;scene.add(points);
  rainbowClusters.push({active:false,owner:-1,x:0,y:0,z:0,vx:0,vy:0,vz:0,life:0,duration:1.65,spread:.55,spin:1,hue:0,geo,mat,seeds});
}
function startRainbow(ownerIndex,it,t){
  const cl=rainbowClusters.find(c=>!c.active);if(!cl)return false;
  cl.active=true;cl.owner=ownerIndex;cl.x=it.x;cl.y=it.y;cl.z=it.z;cl.vx=it.vx;cl.vy=Math.max(.03,it.vy);cl.vz=it.vz;cl.life=0;cl.duration=rand(1.35,2.05);cl.spread=rand(.34,.62)*(0.78+it.base*.72);cl.spin=Math.random()<.5?-1:1;cl.hue=Math.random();cl.mat.opacity=0;
  it.rainbowing=true;it.rainbowCooldown=rand(8,16);nextRainbowTime=t+rand(5.2,9.8);return true;
}
function finishRainbow(cl){
  if(cl.owner>=0&&fragItems[cl.owner]){const it=fragItems[cl.owner];it.rainbowing=false;resetFrag(it,false);it.rainbowCooldown=rand(8,16);}
  cl.active=false;cl.owner=-1;cl.mat.opacity=0;const pos=cl.geo.attributes.position.array;for(let p=0;p<RAINBOW_PARTS;p++){pos[p*3]=9999;pos[p*3+1]=9999;pos[p*3+2]=9999;}cl.geo.attributes.position.needsUpdate=true;
}
function updateRainbowClusters(dt,t){
  const motion=reduced?.18:1;
  for(const cl of rainbowClusters){if(!cl.active)continue;cl.life+=dt;
    const wind=sampleWind(cl.x,cl.z,t,tmpRainbowWind),inertia=Math.min(1,dt*(1.8+wind.strength*1.5)),targetSpeed=1.65+wind.strength*3.55;
    cl.vx+=(tmpRainbowWind.x*targetSpeed-cl.vx)*inertia;cl.vz+=(tmpRainbowWind.y*targetSpeed-cl.vz)*inertia;cl.vy+=(wind.lift*.72+.018-cl.vy*.24)*dt;cl.x+=cl.vx*dt*motion;cl.z+=cl.vz*dt*motion;cl.y+=cl.vy*dt*motion;
    if(cl.life>=cl.duration||cl.z<-95||Math.abs(cl.x)>44||cl.y>13.3){finishRainbow(cl);continue;}
    const u=cl.life/cl.duration,fadeIn=Math.min(1,cl.life/.16),fadeOut=Math.min(1,(cl.duration-cl.life)/.42),fade=Math.max(0,Math.min(fadeIn,fadeOut)),open=1-Math.pow(1-u,2.2),pos=cl.geo.attributes.position.array,col=cl.geo.attributes.color.array;
    for(let p=0;p<RAINBOW_PARTS;p++){const seed=cl.seeds[p],o=p*3,radius=(.025+cl.spread*open)*seed.radius,angle=seed.angle+cl.spin*cl.life*(1.0+.72*seed.radius)+Math.sin(t*.72+seed.phase)*.16,wake=open*.34*seed.radius;
      pos[o]=cl.x+Math.cos(angle)*radius-tmpRainbowWind.x*wake;pos[o+1]=cl.y+Math.sin(angle*1.29)*radius*.72+seed.height*radius*.30+Math.sin(t*1.5+seed.phase)*.018;pos[o+2]=cl.z+Math.sin(angle*.71+seed.phase)*radius*.46+seed.depth*radius*.22-tmpRainbowWind.y*wake;
      const hue=(cl.hue+seed.hue*.82+t*.014)%1;tmpRainbowColor.setHSL(hue,.72,.60);col[o]=tmpRainbowColor.r;col[o+1]=tmpRainbowColor.g;col[o+2]=tmpRainbowColor.b;}
    cl.mat.opacity=.78*fade;cl.geo.attributes.position.needsUpdate=true;cl.geo.attributes.color.needsUpdate=true;}
}
'''
marker='\nfunction updateFragments(dt,t)'
if s.count(marker) != 1: raise SystemExit('updateFragments marker missing')
s=s.replace(marker, '\n'+rainbow+marker, 1)

start=s.index('function updateFragments(dt,t){')
end=s.index('\n\nfunction resize()', start)
new_update=r'''function updateFragments(dt,t){
  const motion=reduced?.20:1;let candidate=-1,candidateScore=.96;
  for(let i=0;i<FRAG_COUNT;i++){const it=fragItems[i];
    if(it.rainbowing){dummy.position.set(9999,9999,9999);dummy.scale.setScalar(0);dummy.updateMatrix();fragments.setMatrixAt(i,dummy.matrix);continue;}
    const wind=sampleWind(it.x,it.z,t,tmpWind);it.rainbowCooldown-=dt;const inertia=Math.min(1,dt*(1.7+wind.strength*1.5)),targetSpeed=1.5+wind.strength*3.4;
    it.vx+=(tmpWind.x*targetSpeed-it.vx)*inertia;it.vz+=(tmpWind.y*targetSpeed-it.vz)*inertia;const flutterLift=Math.sin(t*1.6+it.phase)*.035+Math.sin(t*.63+it.phase2)*.022;it.vy+=(wind.lift+flutterLift-it.vy*.28)*dt;it.x+=it.vx*dt*motion;it.z+=it.vz*dt*motion;it.y+=it.vy*dt*motion;it.age+=dt;
    if(it.z<-94||it.z>12||Math.abs(it.x)>42||it.y>13.0||it.y<-.15||it.age>24){resetFrag(it,false);continue;}
    if(!reduced&&t>=nextRainbowTime&&it.rainbowEligible&&it.rainbowCooldown<=0&&it.age>.8&&it.z>-48&&it.z<7&&it.y>.28&&it.y<9.4&&wind.strength>candidateScore){candidate=i;candidateScore=wind.strength;}
    const flutter=Math.sin(t*it.tumble*2.25+it.phase);dummy.position.set(it.x,it.y,it.z);dummy.rotation.set(Math.sin(t*.72+it.phase2)*.72,t*it.spin*.53+it.phase,flutter*1.05+Math.sin(t*.39+it.phase2)*.28);const sc=it.base*(.92+.10*flutter);dummy.scale.set(sc*(.70+.18*Math.sin(it.phase2)),sc*(1.08+.16*Math.sin(it.phase)),1);dummy.updateMatrix();fragments.setMatrixAt(i,dummy.matrix);}
  if(candidate>=0&&rainbowClusters.some(c=>!c.active)&&startRainbow(candidate,fragItems[candidate],t)){dummy.position.set(9999,9999,9999);dummy.scale.setScalar(0);dummy.updateMatrix();fragments.setMatrixAt(candidate,dummy.matrix);}fragments.instanceMatrix.needsUpdate=true;
}'''
s=s[:start]+new_update+s[end:]
one('updateWhirls(dt,elapsed);updateFragments(dt,elapsed);renderer.render(scene,camera);',
    'updateWhirls(dt,elapsed);updateFragments(dt,elapsed);updateRainbowClusters(dt,elapsed);renderer.render(scene,camera);')
path.write_text(s)
print('patched', path)
