import json, urllib.request, urllib.parse, os, sys, time
UA={'User-Agent':'yuta-explainer/1.0 (no423yt@gmail.com)'}
C=json.load(open(sys.argv[1],encoding='utf-8'))
man=json.load(open('manifest.json',encoding='utf-8'))
def api(params):
    url='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params)
    return json.load(urllib.request.urlopen(urllib.request.Request(url,headers=UA)))
titles=['File:'+v for v in C.values()]
for i in range(0,len(titles),10):
    d=api({'action':'query','titles':'|'.join(titles[i:i+10]),'prop':'imageinfo','iiprop':'url|extmetadata|size','iiurlwidth':1400,'format':'json'})
    nmap={n['to']:n['from'] for n in d['query'].get('normalized',[])}
    for p in d['query']['pages'].values():
        t=p['title']; orig=nmap.get(t,t)
        slug=[s for s,v in C.items() if 'File:'+v in (t,orig)]
        if not slug or 'imageinfo' not in p: print('MISS',t); continue
        ii=p['imageinfo'][0]; em=ii.get('extmetadata',{})
        g=lambda k: em.get(k,{}).get('value','')
        man[slug[0]]={'file':t,'thumb':ii.get('thumburl',ii['url']),'w':ii['width'],'h':ii['height'],'license':g('LicenseShortName'),'artist':g('Artist'),'desc':g('ImageDescription')[:200],'url':'https://commons.wikimedia.org/wiki/'+urllib.parse.quote(t.replace(' ','_'))}
for s in C:
    m=man.get(s); out=f'imgs/{s}.jpg'
    if not m or os.path.exists(out): continue
    try:
        open(out,'wb').write(urllib.request.urlopen(urllib.request.Request(m['thumb'],headers=UA)).read())
        print('OK',s,m['license'],os.path.getsize(out)//1024,'KB')
    except Exception as e: print('ERR',s,e)
    time.sleep(0.3)
json.dump(man,open('manifest.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
