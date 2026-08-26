from pathlib import Path
import re

src=Path('threejs/sky/v10/index.html')
dst=Path('threejs/sky/v11/index.html')
s=src.read_text()

s=s.replace('<!-- Living Field v10: fixed-color rainbow flyer flocks -->','<!-- Living Field v11: more simultaneous fixed-color rainbow flyer flocks -->')
s=s.replace('Living Field v10 · fixed-color rainbow flyer flocks','Living Field v11 · more rainbow flyer flocks')
s=s.replace('虹色群を固定色マテリアル化 ／ 初期群を画面内に常時出現 ／ vivid fixed colors ／ original flyers remain separate','虹色飛翔体の群数を増加 ／ 初期2群 ／ mobile 3 groups / desktop 5 groups ／ vivid fixed colors')
s=s.replace('Three.js · GLSL · shared wind field · v10','Three.js · GLSL · shared wind field · v11')
s=s.replace('固定色マテリアルの小型虹色飛翔体群が確実に見えるv10','固定色マテリアルの小型虹色飛翔体群が複数同時に流れるv11')
s=s.replace('const RAINBOW_GROUP_COUNT=mobile?2:3;','const RAINBOW_GROUP_COUNT=mobile?3:5;')
s=s.replace('let nextRainbowGroupTime=2.6+Math.random()*1.2;','let nextRainbowGroupTime=1.2+Math.random()*.8;')
s=s.replace('activateRainbowGroup(rainbowFlyerGroups[0],0,true);','activateRainbowGroup(rainbowFlyerGroups[0],0,true);\nif(rainbowFlyerGroups[1]) activateRainbowGroup(rainbowFlyerGroups[1],0,false);')
s=s.replace('nextRainbowGroupTime=t+rand(3.0,4.8);','nextRainbowGroupTime=t+rand(1.8,3.0);')

# Ensure no accidental v10 labeling remains in visible version metadata.
assert 'Living Field v11 · more rainbow flyer flocks' in s
assert 'const RAINBOW_GROUP_COUNT=mobile?3:5;' in s
assert 'activateRainbowGroup(rainbowFlyerGroups[1],0,false);' in s
assert 'nextRainbowGroupTime=t+rand(1.8,3.0);' in s

dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text(s)

# Update version router, preserving previous versions.
r=Path('threejs/sky/index.html')
rt=r.read_text()
rt=rt.replace("get('v')||'10'","get('v')||'11'")
rt=rt.replace("(v==='09'?'v09/':'v10/')","(v==='09'?'v09/':(v==='10'?'v10/':'v11/'))")
rt=rt.replace('<p><a href="v10/">Living Field v10</a> / ','<p><a href="v11/">Living Field v11</a> / <a href="v10/">Living Field v10</a> / ')
assert "get('v')||'11'" in rt
assert "'v11/'" in rt
r.write_text(rt)

# Extract module JS for syntax validation by workflow.
m=re.search(r'<script type="module">\n(.*?)\n</script>',s,re.S)
assert m
Path('/tmp/v11.mjs').write_text(m.group(1))
