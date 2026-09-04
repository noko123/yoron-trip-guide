import re, json, urllib.request, time, sys
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36','Accept-Language':'ja'}
shops={'tara':'46000848','aoisangosho':'46005164','misaki':'46007513','bashotei':'46005158','musubi':'46018015','embercove':'46019115','yunnucafe':'46017915','castanet':'46014949','littlebeach':'46016854','hyokin':'46000823','kayoibune':'46005153','tuktuk':'46011162','masamunu':'46017879'}
out={}
for k,i in shops.items():
    url=f'https://tabelog.com/kagoshima/A4605/A460502/{i}/'
    try:
        html=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=30).read().decode('utf-8','ignore')
        m=re.search(r'<meta property="og:image" content="([^"]+)"',html)
        t=re.search(r'<meta property="og:title" content="([^"]+)"',html)
        img=m.group(1).replace('&amp;','&') if m else None
        status=None
        if img:
            req=urllib.request.Request(img,headers={'User-Agent':UA['User-Agent']},method='HEAD')
            try: status=urllib.request.urlopen(req,timeout=30).status
            except Exception as e: status=str(e)[:40]
        out[k]={'url':url,'img':img,'title':t.group(1) if t else None,'img_status':status}
        print(k,status,(t.group(1) if t else '')[:30],img)
    except Exception as e:
        print(k,'ERR',e); out[k]={'url':url,'img':None,'err':str(e)[:80]}
    time.sleep(1.5)
json.dump(out,open('tabelog_og.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
