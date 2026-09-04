import json, urllib.request, urllib.parse
q='''[out:json][timeout:60];
(
  node["name"](26.99,128.37,27.09,128.49);
  way["name"](26.99,128.37,27.09,128.49);
);
out center tags;'''
req=urllib.request.Request('https://overpass-api.de/api/interpreter',data=urllib.parse.urlencode({'data':q}).encode(),headers={'User-Agent':'yuta-explainer/1.0 (no423yt@gmail.com)'})
d=json.load(urllib.request.urlopen(req,timeout=120))
rows=[]
for e in d['elements']:
    t=e.get('tags',{}); name=t.get('name','')
    lat=e.get('lat') or e.get('center',{}).get('lat'); lon=e.get('lon') or e.get('center',{}).get('lon')
    kind=t.get('tourism') or t.get('amenity') or t.get('natural') or t.get('shop') or t.get('aeroway') or t.get('leisure') or t.get('historic') or t.get('place') or t.get('highway') or ''
    rows.append((name,kind,lat,lon))
json.dump(rows,open('osm_names.json','w',encoding='utf-8'),ensure_ascii=False)
keys=['百合','大金久','ウドノス','寺崎','皆田','城','サザン','民俗','鍾乳','鳩','駅','酒造','兼母','ひょうきん','たら','珊瑚','コープ','徳洲会','プリシア','空港','港','郵便','役場','観光','トゥマイ','赤崎','ゆいパンタ','かよい','Tuk','MASAMUNU','芭蕉','味咲','むすび','EMBER','カフェ','スーパー','トップ','マソー','フロント','オーシャン','ニシムタ','てんてん','南国','野口','コロ','サンセット','海岸','ビーチ','展望']
for r in rows:
    if any(k in r[0] for k in keys): print(r)
print('total',len(rows))
