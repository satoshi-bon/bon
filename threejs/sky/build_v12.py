from pathlib import Path
import re

src=Path('threejs/sky/v11/index.html')
dst=Path('threejs/sky/v12/index.html')
s=src.read_text()

s=s.replace('<!-- Living Field v11: more simultaneous fixed-color rainbow flyer flocks -->','<!-- Living Field v12: balanced rainbow flyer flocks with varied sizes -->')
s=s.replace('Living Field v11 · more rainbow flyer flocks','Living Field v12 · balanced rainbow flyer flocks')
s=s.replace('虹色飛翔体の群数を増加 ／ 初期2群 ／ mobile 3 groups / desktop 5 groups ／ vivid fixed colors','手前の未初期化三角を除去 ／ 虹色飛翔体のサイズを多様化 ／ mobile 4 groups / desktop 7 groups ／ stratified random spawn')
s=s.replace('Three.js · GLSL · shared wind field · v11','Three.js · GLSL · shared wind field · v12')
s=s.replace('同じ風場で動き、固定色マテリアルの小型虹色飛翔体群が確実に見えるv11','同じ風場で動き、サイズの異なる虹色飛翔体群が偏りなく出現するv12')
s=s.replace('const RAINBOW_GROUP_COUNT=mobile?3:5;','const RAINBOW_GROUP_COUNT=mobile?4:7;')
s=s.replace("scale:rand(.30,.44)","scale:.12+Math.pow(Math.random(),1.25)*.32")

old_init="""for(let i=0;i<RAINBOW_FLYER_COUNT;i++)hideRainbowFlyer(i);\nrainbowFlyerMeshes.forEach(m=>m.instanceMatrix.needsUpdate=true);"""
new_init="""// Initialize every instance of every fixed-color mesh off-screen.\n// This removes the stray foreground triangles caused by untouched identity matrices.\nfor(const mesh of rainbowFlyerMeshes){\n  for(let i=0;i<RAINBOW_FLYER_COUNT;i++){\n    rainbowFlyerDummy.position.set(9999,9999,9999);rainbowFlyerDummy.scale.setScalar(0);rainbowFlyerDummy.updateMatrix();\n    mesh.setMatrixAt(i,rainbowFlyerDummy.matrix);\n  }\n  mesh.instanceMatrix.needsUpdate=true;\n}"""
if old_init not in s:
    raise SystemExit('v11 initialization block not found')
s=s.replace(old_init,new_init)

old_spawn="""function activateRainbowGroup(group,t,first=false){\n  group.active=true;\n  group.x=first?5.2:rand(-9,9);group.z=first?-8.5:rand(-20,2);group.y=first?3.35:rand(2.1,5.4);\n  group.life=0;group.duration=first?8.5:rand(6.0,8.0);group.phase=rand(0,Math.PI*2);group.spread=first?.72:rand(.58,.82);\n  const wind=sampleWind(group.x,group.z,t,tmpRainbowWind),speed=1.65+wind.strength*2.5;\n  group.vx=tmpRainbowWind.x*speed+rand(-.10,.10);group.vz=tmpRainbowWind.y*speed+rand(-.08,.08);group.vy=rand(.01,.06)+wind.lift*.30;\n}\nactivateRainbowGroup(rainbowFlyerGroups[0],0,true);\nif(rainbowFlyerGroups[1]) activateRainbowGroup(rainbowFlyerGroups[1],0,false);"""
new_spawn="""// Stratified random spawning: each cycle uses every x/z cell once before reshuffling,\n// preventing accidental clustering in one part of the sky.\nconst SPAWN_COLS=4,SPAWN_ROWS=3;\nlet spawnOrder=[],spawnCursor=0;\nfunction resetSpawnOrder(){\n  spawnOrder=Array.from({length:SPAWN_COLS*SPAWN_ROWS},(_,i)=>i);\n  for(let i=spawnOrder.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));const tmp=spawnOrder[i];spawnOrder[i]=spawnOrder[j];spawnOrder[j]=tmp;}\n  spawnCursor=0;\n}\nfunction nextSpawnPoint(){\n  if(spawnCursor>=spawnOrder.length)resetSpawnOrder();\n  const slot=spawnOrder[spawnCursor++],col=slot%SPAWN_COLS,row=Math.floor(slot/SPAWN_COLS);\n  const x0=-10+col*(20/SPAWN_COLS),x1=-10+(col+1)*(20/SPAWN_COLS);\n  const z0=-20+row*(22/SPAWN_ROWS),z1=-20+(row+1)*(22/SPAWN_ROWS);\n  return {x:rand(x0+.45,x1-.45),z:rand(z0+.45,z1-.45),y:rand(2.0,5.5)};\n}\nresetSpawnOrder();\nfunction activateRainbowGroup(group,t){\n  const p=nextSpawnPoint();\n  group.active=true;group.x=p.x;group.z=p.z;group.y=p.y;\n  group.life=0;group.duration=rand(6.2,8.4);group.phase=rand(0,Math.PI*2);group.spread=rand(.58,.84);\n  const wind=sampleWind(group.x,group.z,t,tmpRainbowWind),speed=1.65+wind.strength*2.5;\n  group.vx=tmpRainbowWind.x*speed+rand(-.10,.10);group.vz=tmpRainbowWind.y*speed+rand(-.08,.08);group.vy=rand(.01,.06)+wind.lift*.30;\n}\nfor(let i=0;i<Math.min(3,rainbowFlyerGroups.length);i++)activateRainbowGroup(rainbowFlyerGroups[i],0);"""
if old_spawn not in s:
    raise SystemExit('v11 spawn block not found')
s=s.replace(old_spawn,new_spawn)
s=s.replace('activateRainbowGroup(group,t,false);nextRainbowGroupTime=t+rand(1.8,3.0);','activateRainbowGroup(group,t);nextRainbowGroupTime=t+rand(1.4,2.3);')

# v12 header text if the aria-label version number remained elsewhere.
s=s.replace('v11">','v12">')

dst.parent.mkdir(parents=True,exist_ok=True)
dst.write_text(s)

router=Path('threejs/sky/index.html')
r=router.read_text()
r=r.replace("const raw=new URLSearchParams(location.search).get('v')||'11';","const raw=new URLSearchParams(location.search).get('v')||'12';")
old_target="const target=v==='03'?'v03/':(v==='05'?'v05/':(v==='06'?'v06/':(v==='07'?'v07/':(v==='08'?'v08/':(v==='09'?'v09/':(v==='10'?'v10/':'v11/'))))));"
new_target="const target=v==='03'?'v03/':(v==='05'?'v05/':(v==='06'?'v06/':(v==='07'?'v07/':(v==='08'?'v08/':(v==='09'?'v09/':(v==='10'?'v10/':(v==='11'?'v11/':'v12/')))))));"
if old_target not in r:
    raise SystemExit('v11 router target not found')
r=r.replace(old_target,new_target)
r=r.replace('<p><a href="v11/">Living Field v11</a> / ','<p><a href="v12/">Living Field v12</a> / <a href="v11/">Living Field v11</a> / ')
router.write_text(r)

m=re.search(r'<script type="module">(.*?)</script>',s,re.S)
if not m:
    raise SystemExit('module script not found')
Path('/tmp/v12.mjs').write_text(m.group(1))
