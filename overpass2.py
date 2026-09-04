import json, urllib.request, urllib.parse
q='''[out:json][timeout:60];
(
  nwr["tourism"](26.99,128.37,27.09,128.49);
  nwr["historic"](26.99,128.37,27.09,128.49);
  nwr["natural"="cave_entrance"](26.99,128.37,27.09,128.49);
  nwr["natural"="water"](26.99,128.37,27.09,128.49);
  nwr["natural"="beach"](26.99,128.37,27.09,128.49);
  nwr["amenity"~"restaurant|cafe|bar|pub|fast_food"](26.99,128.37,27.09,128.49);
  nwr["shop"](26.99,128.37,27.09,128.49);
  nwr["craft"](26.99,128.37,27.09,128.49);
  nwr["amenity"="car_rental"](26.99,128.37,27.09,128.49);
);
out center tags;'''
req=urllib.request.Request('https://overpass.kumi.systems/api/interpreter',data=urllib.parse.urlencode({'data':q}).encode(),headers={'User-Agent':'yuta-explainer/1.0 (no423yt@gmail.com)'})
d=json.load(urllib.request.urlopen(req,timeout=120))
for e in d['elements']:
    t=e.get('tags',{})
    lat=e.get('lat') or e.get('center',{}).get('lat'); lon=e.get('lon') or e.get('center',{}).get('lon')
    kind=t.get('tourism') or t.get('historic') or t.get('natural') or t.get('amenity') or t.get('shop') or t.get('craft')
    print(round(lat,5),round(lon,5),kind,'|',t.get('name',''),t.get('name:en',''),t.get('name:ja',''))
