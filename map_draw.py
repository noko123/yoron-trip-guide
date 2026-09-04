# basemap_z15.png に番号マーカーを描いて use/map_osm.jpg に出す。spots.json も書く (Leaflet 用)
import json, math
from PIL import Image, ImageDraw, ImageFont
Z,tx0,ty0,cx0,cy0,LAT0,LON0,LAT1,LON1=[float(v) for v in open('basemap_meta.txt').read().split()]
def px(lat,lon):
    n=2**Z; x=(lon+180)/360*n; y=(1-math.log(math.tan(math.radians(lat))+1/math.cos(math.radians(lat)))/math.pi)/2*n
    return (x-tx0)*256-cx0,(y-ty0)*256-cy0
S=[ # (番号, 名前, lat, lon, 種別, 概略か)
 (1,'与論空港',27.04384,128.4017,'交通',False),
 (2,'プリシアリゾートヨロン',27.04911,128.39852,'宿',False),
 (3,'ヨロン駅',27.04011,128.39799,'名所',False),
 (4,'与論港 (フェリー)',27.03637,128.40097,'交通',False),
 (5,'茶花 (役場・郵便局 ATM・A コープ)',27.0460,128.4175,'町',False),
 (6,'与論徳洲会病院',27.04384,128.41634,'病院',False),
 (7,'居酒屋 ひょうきん (9/5 19:00)',27.0455,128.4205,'食',True),
 (8,'有村酒造 (島有泉)',27.0465,128.4145,'食',True),
 (9,'ウドノスビーチ',27.05208,128.41473,'海',False),
 (10,'舵引きの丘 (神話の聖地)',27.04689,128.4281,'名所',False),
 (11,'寺崎海岸',27.06076,128.44498,'海',False),
 (12,'皆田海岸',27.0555,128.4495,'海',True),
 (13,'大金久海岸 (グラスボート乗り場)',27.03907,128.45404,'海',False),
 (14,'百合ヶ浜',27.03889,128.46553,'海',False),
 (15,'与論民俗村',27.0251,128.45285,'名所',False),
 (16,'赤崎鍾乳洞',27.0215,128.4470,'名所',True),
 (17,'サザンクロスセンター・観光協会 (ゆいパンタ)',27.02868,128.42941,'名所',False),
 (18,'与論城跡・地主神社',27.02754,128.42913,'名所',False),
]
im=Image.open('basemap_z15.png').convert('RGB')
d=ImageDraw.Draw(im)
f=ImageFont.truetype('C:/Windows/Fonts/meiryob.ttc',26); fn=ImageFont.truetype('C:/Windows/Fonts/meiryob.ttc',22)
COL={'交通':'#1B2732','宿':'#B4452F','名所':'#0F8B8D','町':'#6F7B86','病院':'#B4452F','食':'#C2410C','海':'#0F8B8D'}
for n,name,lat,lon,kind,approx in S:
    x,y=px(lat,lon); r=19
    d.ellipse((x-r,y-r,x+r,y+r),fill=COL[kind],outline='white',width=3)
    if approx: d.ellipse((x-r-5,y-r-5,x+r+5,y+r+5),outline=COL[kind],width=2)
    tw=d.textlength(str(n),font=fn); d.text((x-tw/2,y-14),str(n),fill='white',font=fn)
    label=name.split(' (')[0]
    lx,ly=x+r+6,y-15
    if n==13: lx,ly=x-r-6-d.textlength(label,font=f),y+r+2
    if n==8: lx,ly=x-40,y-r-34
    for dx,dy in ((-2,0),(2,0),(0,-2),(0,2),(-2,-2),(2,2),(-2,2),(2,-2)): d.text((lx+dx,ly+dy),label,fill='white',font=f)
    d.text((lx,ly),label,fill=COL[kind],font=f)
# scale bar 1km at lat 27 (z15: 4.777 m/px * cos(27°))
mpp=156543.03*math.cos(math.radians(27.04))/2**Z; L=1000/mpp
d.rectangle((40,im.height-60,40+L,im.height-50),fill='#1B2732'); d.text((40,im.height-95),'1 km',fill='#1B2732',font=f)
d.text((im.width-560,im.height-40),'© OpenStreetMap contributors',fill='#1B2732',font=fn)
im=im.resize((1600,round(im.height*1600/im.width)),Image.LANCZOS)
im.save('use/map_osm.jpg','JPEG',quality=85,optimize=True)
json.dump([{'n':n,'name':name,'lat':lat,'lon':lon,'kind':kind,'approx':approx} for n,name,lat,lon,kind,approx in S],open('spots.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
man=json.load(open('manifest.json',encoding='utf-8'))
man['map_osm']={'file':'OpenStreetMap tiles z15 (stitched)','thumb':'','w':im.width,'h':im.height,'license':'ODbL','artist':'OpenStreetMap contributors','desc':'与論島の地図。OSM タイルを貼り合わせ、番号マーカーを描いた','url':'https://www.openstreetmap.org/copyright'}
json.dump(man,open('manifest.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('ok',im.size)
