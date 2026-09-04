import json, urllib.request, urllib.parse, os, sys, time
UA={'User-Agent':'yuta-explainer/1.0 (no423yt@gmail.com)'}
C={
'yurigahama':'Yurigahama.jpg',
'aerial_katsuu':'Yoron Island seen from Mount Katsuu 202607.jpg',
'aerial_2008':'Yoronjima Island Aerial photograph.2008.jpg',
'zenkei':'Yoronzenkei.jpg',
'island_2008':'Yoron Island 20080622.jpg',
'island_flickr':'Yoron Island (8407010599).jpg',
'banner':'Yoron Island banner.jpg',
'pricia1':'Yoron PRICIA 0122.jpg',
'pricia2':'プリシアリゾート.jpg',
'pricia3':'プリシアリゾート2.jpg',
'pricia_beach':'プリシアリゾートプライベートビーチ.jpg',
'pricia_bbq':'プリシアリゾートのバーベキューテラス - panoramio.jpg',
'minata1':'2021-04-10 Beach Minata,Amami,Kagoshima (皆田海岸) DJI Mini2-0050.jpg',
'minata2':'2021-04-10 Beach Minata,Amami,Kagoshima (皆田海岸) DJI Mini2-0048.jpg',
'minata3':'2021-04-10 Beach Minata,Amami,Kagoshima (皆田海岸)-DJI Mini2-0043.jpg',
'underwater':'与論の海の中 - panoramio.jpg',
'beach':'与論島のビーチ.jpg',
'sea':'与論島の海.jpg',
'station1':'Yoron Station as a fictional train station - October 2024 (1).jpg',
'station2':'Yoron Station as a fictional train station - October 2024 (2).jpg',
'station_2019':'ヨロン駅モニュメント2019.jpg',
'airport_terminal':'Terminal building in Yoron Airport Kagoshima, JAPAN.jpg',
'airport_counter':'与論空港カウンター2019.jpg',
'airport_apron':'与論空港駐機場2019.jpg',
'airport_rnj':'RNJ.JPG',
'airport_aerial':'Yoron airport aerial photograph.jpg',
'chabana_aerial':'2021-04-10 Chabana-Yoron,Oshima,Kagoshima 鹿児島県大島郡与論町茶花DJI Mini2-0063.jpg',
'chabana_port':'2021-04-09 Chabana-gyoko 茶花漁港 DJI Mini2-0033.jpg',
'town_center':'与論町中心部.jpg',
'town_hall':'与論町役場.jpg',
'yunnu':'Yunnu Rakuen.jpg',
'port':'Yoron Port.jpg',
'tomb_prewar':'Yoron Island Tomb in Pre-war Showa era.JPG',
'map_1944':'Map by the US Army Map Service - Yoron Jima - ryukyu retto 50k - txu-pclmaps-oclc-6618161-yoron-jima.jpg',
'seito':'2021-04-09 Yoronjima-seito 与論島製糖（株）DJI Mini2-0023.jpg',
'kunigami_monument':'Yoron kunigami friendship monument.jpg',
'ferry':'Queen Coral Plus near Island of Yoronjima.jpg',
'rac_naha':'Ryukyu Air Commuter Q400 at Okinawa Naha (32686326443).jpg',
'rac_q400cc':'Ryukyu Air Commuter Bombardier DHC8-Q400CC (JA82RC).jpg',
'rac_shisa':'Shisa on the tail of a plane.jpg',
'rac_tarama':'多良間空港のボンバルディアDHC8-Q400CC機.jpg',
'keihan':"Keihan (Amami Oshima's country dishes) Kagoshima,JAPAN.jpg",
'keihan2':'Chicken soup rice 鶏飯定食 (2038424703).jpg',
'kokuto_shochu':'Bottled amami kokuto shochu.jpg',
'mozuku':'沖縄産もずく.jpg',
'amami_agemono':'Amami agemono 3shu.JPG',
'cider':'ヨロンブルーサイダー.jpg',
'yoron_st_old':'Yoron st.jpg',
}
def api(params):
    url='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params)
    return json.load(urllib.request.urlopen(urllib.request.Request(url,headers=UA)))
man={}
titles=['File:'+v for v in C.values()]
for i in range(0,len(titles),10):
    d=api({'action':'query','titles':'|'.join(titles[i:i+10]),'prop':'imageinfo','iiprop':'url|extmetadata|size','iiurlwidth':1400,'format':'json'})
    norm=d['query'].get('normalized',[])
    nmap={n['to']:n['from'] for n in norm}
    for p in d['query']['pages'].values():
        t=p['title']; orig=nmap.get(t,t)
        slug=[s for s,v in C.items() if 'File:'+v in (t,orig)]
        if not slug or 'imageinfo' not in p: print('MISS',t); continue
        ii=p['imageinfo'][0]; em=ii.get('extmetadata',{})
        g=lambda k: em.get(k,{}).get('value','')
        man[slug[0]]={'file':t,'thumb':ii.get('thumburl',ii['url']),'w':ii['width'],'h':ii['height'],'license':g('LicenseShortName'),'artist':g('Artist'),'desc':g('ImageDescription')[:200],'url':'https://commons.wikimedia.org/wiki/'+urllib.parse.quote(t.replace(' ','_'))}
for s,m in man.items():
    out=f'imgs/{s}.jpg'
    if os.path.exists(out): continue
    try:
        open(out,'wb').write(urllib.request.urlopen(urllib.request.Request(m['thumb'],headers=UA)).read())
        print('OK',s,m['license'],os.path.getsize(out)//1024,'KB')
    except Exception as e: print('ERR',s,e)
    time.sleep(0.3)
json.dump(man,open('manifest.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
W=['与論城','百合ヶ浜','与論民俗村','赤崎鍾乳洞','サザンクロスセンター','与論島','与論空港','琉球エアーコミューター','鶏飯','黒糖焼酎','与論町','与論献奉','与論の十五夜踊り']
for t in W:
    url='https://ja.wikipedia.org/w/api.php?'+urllib.parse.urlencode({'action':'query','titles':t,'prop':'images','imlimit':50,'format':'json','redirects':1})
    d=json.load(urllib.request.urlopen(urllib.request.Request(url,headers=UA)))
    for p in d['query']['pages'].values():
        print('WP',t,'->',[i['title'] for i in p.get('images',[]) if not i['title'].lower().endswith('.svg')][:30] if 'images' in p else 'NOPAGE')
