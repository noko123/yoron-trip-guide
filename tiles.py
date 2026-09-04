# OSM タイルを z=15 で貼り合わせて与論島の下地を作る (use/basemap_z15.png)。帰属: © OpenStreetMap contributors (ODbL)
import math, os, urllib.request, time
from PIL import Image
Z=15; LAT0,LAT1=27.070,27.012; LON0,LON1=128.383,128.478   # 北西 → 南東
UA={'User-Agent':'yuta-explainer/1.0 (no423yt@gmail.com) travel-guide-basemap'}
def t(lat,lon,z):
    n=2**z; x=(lon+180)/360*n; y=(1-math.log(math.tan(math.radians(lat))+1/math.cos(math.radians(lat)))/math.pi)/2*n
    return x,y
x0,y0=t(LAT0,LON0,Z); x1,y1=t(LAT1,LON1,Z)
tx0,ty0,tx1,ty1=int(x0),int(y0),int(x1),int(y1)
os.makedirs('tiles',exist_ok=True)
W=(tx1-tx0+1)*256; H=(ty1-ty0+1)*256
im=Image.new('RGB',(W,H),'white')
n=0
for tx in range(tx0,tx1+1):
    for ty in range(ty0,ty1+1):
        p=f'tiles/{Z}_{tx}_{ty}.png'
        if not os.path.exists(p):
            url=f'https://tile.openstreetmap.org/{Z}/{tx}/{ty}.png'
            open(p,'wb').write(urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=30).read()); time.sleep(0.25); n+=1
        im.paste(Image.open(p).convert('RGB'),((tx-tx0)*256,(ty-ty0)*256))
# crop to exact bbox
cx0=(x0-tx0)*256; cy0=(y0-ty0)*256; cx1=(x1-tx0)*256; cy1=(y1-ty0)*256
im=im.crop((int(cx0),int(cy0),int(cx1),int(cy1)))
im.save('basemap_z15.png')
print('tiles downloaded',n,'size',im.size,'origin px',cx0,cy0)
open('basemap_meta.txt','w').write(f'{Z} {tx0} {ty0} {cx0} {cy0} {LAT0} {LON0} {LAT1} {LON1}')
