from pathlib import Path
import re

src=Path('threejs/sky/v08/index.html')
dst=Path('threejs/sky/v09/index.html')
s=src.read_text()

# Version labels / descriptions
s=s.replace('<!-- Living Field v08: original flyers + small rainbow flyer flocks -->','<!-- Living Field v09: original flyers + clearly visible rainbow flyer flocks -->')
s=s.replace('草・空・飛翔体が同じ風場で動き、元の飛翔体とは独立した小さい虹色飛翔体の群が別系統で流れるv08','草・空・飛翔体が同じ風場で動き、元の飛翔体とは独立した見やすい小型虹色飛翔体群が別系統で流れるv09')
s=s.replace('Living Field v08 · small rainbow flyer flocks','Living Field v09 · visible rainbow flyer flocks')
s=s.replace('虹色パーティクルを廃止 ／ 小さい虹色の飛翔体が群として飛行 ／ original flyers remain separate','小型虹色飛翔体を約2倍強に拡大 ／ 手前に出現 ／ vivid instance colors ／ original flyers remain separate')
s=s.replace('Three.js · GLSL · shared wind field · v08','Three.js · GLSL · shared wind field · v09')

# Make the rainbow flyer colors more explicit and visible.
s=s.replace(
    "const rainbowFlyerMat=new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:.94,side:THREE.DoubleSide,depthWrite:false});",
    "const rainbowFlyerMat=new THREE.MeshBasicMaterial({color:0xffffff,vertexColors:true,transparent:true,opacity:.98,side:THREE.DoubleSide,depthWrite:false,toneMapped:false});"
)
s=s.replace("tmpRainbowColor.setHSL(hue,.98,.55);","tmpRainbowColor.setHSL(hue,1.0,.50);",1)

# Larger, clearly recognizable small flyers.
s=s.replace("scale:rand(.16,.25),","scale:rand(.34,.50),")

# Bring flocks closer and make them a little tighter.
s=s.replace("let nextRainbowGroupTime=2.8+Math.random()*3.8;","let nextRainbowGroupTime=.7+Math.random()*1.0;")
s=s.replace("group.active=true;group.x=rand(-11,11);group.z=rand(-48,-4);group.y=rand(1.0,7.0);group.life=0;group.duration=rand(3.4,5.4);group.phase=rand(0,Math.PI*2);group.spread=rand(.72,1.05);",
            "group.active=true;group.x=rand(-10,10);group.z=rand(-26,4);group.y=rand(.9,5.8);group.life=0;group.duration=rand(5.0,7.0);group.phase=rand(0,Math.PI*2);group.spread=rand(.58,.86);")
s=s.replace("nextRainbowGroupTime=t+rand(4.2,7.2);return true;","nextRainbowGroupTime=t+rand(3.0,5.2);return true;")

# Update router to v09 while preserving old versions.
router=Path('threejs/sky/index.html')
r=router.read_text()
r=r.replace("const raw=new URLSearchParams(location.search).get('v')||'08';","const raw=new URLSearchParams(location.search).get('v')||'09';")
r=r.replace("const target=v==='03'?'v03/':(v==='05'?'v05/':(v==='06'?'v06/':(v==='07'?'v07/':'v08/')));",
            "const target=v==='03'?'v03/':(v==='05'?'v05/':(v==='06'?'v06/':(v==='07'?'v07/':(v==='08'?'v08/':'v09/'))));")
r=r.replace('<p><a href="v08/">Living Field v08</a> / <a href="v07/">Living Field v07</a> / <a href="v06/">Living Field v06</a> / <a href="v05/">Living Field v05</a> / <a href="v03/">Living Field v03</a></p>',
            '<p><a href="v09/">Living Field v09</a> / <a href="v08/">Living Field v08</a> / <a href="v07/">Living Field v07</a> / <a href="v06/">Living Field v06</a> / <a href="v05/">Living Field v05</a> / <a href="v03/">Living Field v03</a></p>')

# Guards: fail rather than silently publish an incomplete v09.
assert 'Living Field v09 · visible rainbow flyer flocks' in s
assert 'scale:rand(.34,.50)' in s
assert 'group.z=rand(-26,4)' in s
assert 'vertexColors:true' in s
assert "||'09'" in r
assert "v==='08'?'v08/':'v09/'" in r

dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text(s)
router.write_text(r)

# Extract module for node --check in Actions.
m=re.search(r'<script type="module">\n(.*?)\n</script>',s,re.S)
assert m
Path('/tmp/v09.mjs').write_text(m.group(1))
