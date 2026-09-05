"""与論島ガイド ビルド (Python だけで完結 — ローカルでも GitHub Actions でも同じ)
  入力: yoron-guide.template.html / manifest.json / use/*.jpg / (あれば) private.json
  出力: docs/index.html (公開版・GitHub Pages)  /  dist/yoron-trip-guide-2026-09.html (自分用・private.json がある時だけ)
  マーカー: {{PV:key|公開テキスト}} … private.json[key] があれば自分用版でそちらに置換。公開版は常に公開テキスト。
           {{IMG:slug}} / {{CREDIT:slug}} / {{CREDITS_LIST}} … use/<slug>.jpg と manifest.json から base64 と帰属を生成
           {{BUILT}} … ビルド時刻 (JST)。冒頭の「最終更新」と奥付に入る (Actions でビルドされるので公開時刻になる)
"""
import json, re, html, os, base64, sys
from datetime import datetime, timezone, timedelta
BUILT=datetime.now(timezone(timedelta(hours=9))).strftime('%Y-%m-%d (%a) %H:%M JST').replace('(Sat)','(土)').replace('(Sun)','(日)').replace('(Mon)','(月)').replace('(Tue)','(火)').replace('(Wed)','(水)').replace('(Thu)','(木)').replace('(Fri)','(金)')
H=os.path.dirname(os.path.abspath(__file__)); os.chdir(H)
man=json.load(open('manifest.json',encoding='utf-8'))
tpl=open('yoron-guide.template.html',encoding='utf-8').read()
priv=json.load(open('private.json',encoding='utf-8')) if os.path.exists('private.json') else None
def strip(s): return html.unescape(re.sub(r'<[^>]+>','',s or '')).strip()
lic_url={'CC BY-SA 4.0':'https://creativecommons.org/licenses/by-sa/4.0/','CC BY-SA 3.0':'https://creativecommons.org/licenses/by-sa/3.0/','CC BY-SA 2.0':'https://creativecommons.org/licenses/by-sa/2.0/','CC BY 4.0':'https://creativecommons.org/licenses/by/4.0/','CC BY 3.0':'https://creativecommons.org/licenses/by/3.0/','CC BY 2.0':'https://creativecommons.org/licenses/by/2.0/','CC0':'https://creativecommons.org/publicdomain/zero/1.0/','Public domain':'https://commons.wikimedia.org/wiki/Commons:Licensing','Attribution':'https://commons.wikimedia.org/wiki/Commons:Licensing'}
PV=re.compile(r'\{\{PV:([a-z0-9_]+)\|(.*?)\}\}',re.S)
def build(public):
    src=PV.sub(lambda m: m.group(2) if (public or priv is None) else priv.get(m.group(1),m.group(2)), tpl).replace('{{BUILT}}',BUILT)
    used=sorted(set(re.findall(r'\{\{IMG:([A-Za-z0-9_\-]+)\}\}',src)))
    items=[]; missing=[]
    for s in used:
        m=man.get(s); f=f'use/{s}.jpg'; mime='jpeg'
        if not os.path.exists(f) and os.path.exists(f'use/{s}.png'): f=f'use/{s}.png'; mime='png'
        if not m or not os.path.exists(f): missing.append(s); continue
        artist=strip(m['artist']); artist=re.sub(r'No machine-readable author provided\.?\s*','',artist).strip()
        n=len(artist)//2
        if n and artist[:n]==artist[n:]: artist=artist[:n]
        artist=(artist or '不明')[:40]; lic=m['license'] or 'see Commons'
        src=src.replace('{{CREDIT:'+s+'}}',f'<span class="credit">写真: {html.escape(artist)} / <a href="{lic_url.get(lic,m["url"])}">{html.escape(lic)}</a> / <a href="{m["url"]}">Commons</a></span>')
        b64=base64.b64encode(open(f,'rb').read()).decode()
        src=src.replace('{{IMG:'+s+'}}',f'<img src="data:image/{mime};base64,{b64}" alt="{s}" loading="lazy">')
        items.append(f'<li><b>{s}</b> — {html.escape(m["file"].replace("File:",""))} · {html.escape(artist)} · <a href="{lic_url.get(lic,m["url"])}">{html.escape(lic)}</a> · <a href="{m["url"]}">Commons</a></li>')
    src=src.replace('{{CREDITS_LIST}}','\n'.join(items)).replace('全 32 枚',f'全 {len(used)} 枚')
    if public:
        src=src.replace('"title":"与論島ガイドブック 2026-09-05〜07"','"title":"与論島ガイドブック 2026-09-05〜07 (公開版)"').replace('<title>与論島ガイドブック 2026-09-05〜07','<title>与論島ガイドブック 2026-09-05〜07 (公開版)')
    if missing: raise SystemExit('missing images: '+','.join(missing))
    left=re.findall(r'\{\{(?:PV|IMG|CREDIT)[^}]*\}\}',src)
    if left: raise SystemExit('placeholder left: '+str(left[:5]))
    return src, used
os.makedirs('docs',exist_ok=True)
pub,used=build(True)
for k in (priv or {}).values():
    for token in re.findall(r'[A-Z0-9]{6,}|\d{2,3},\d{3}',k):
        if token in pub: raise SystemExit('LEAK in public: '+token)
open('docs/index.html','w',encoding='utf-8').write(pub)
print('public  -> docs/index.html  %.2f MB  images=%d'%(len(pub.encode())/1e6,len(used)))
if priv is not None:
    os.makedirs('dist',exist_ok=True)
    pv,_=build(False); open('dist/yoron-trip-guide-2026-09.html','w',encoding='utf-8').write(pv)
    open('dist/yoron-trip-guide-2026-09-share.html','w',encoding='utf-8').write(pub)
    print('private -> dist/yoron-trip-guide-2026-09.html  %.2f MB'%(len(pv.encode())/1e6))
