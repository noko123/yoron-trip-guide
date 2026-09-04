# 略図 SVG の figure を、OSM 静止画 + 凡例 + Leaflet 対話地図に置換する (一度だけ)
import json, re
S=json.load(open('spots.json',encoding='utf-8'))
src=open('yoron-guide.template.html',encoding='utf-8').read()
pat=re.compile(r'    <figure class="diagram">\s*<svg viewBox="0 0 760 470".*?</figcaption>\s*</figure>',re.S)
assert pat.search(src), 'old map figure not found'
APX=' <span class="muted">(概略)</span>'
legend='\n'.join('      <li><span class="n">%d</span>%s%s</li>'%(s['n'],s['name'],APX if s['approx'] else '') for s in S)
spots_js=json.dumps([{k:s[k] for k in ('n','name','lat','lon','approx')} for s in S],ensure_ascii=False)
block=f'''    <figure class="photo">{{{{IMG:map_osm}}}}<figcaption>OpenStreetMap の実地図 (ズーム 15) に 18 か所を番号で置いた。二重丸の 4 か所 (ひょうきん・有村酒造・皆田海岸・赤崎鍾乳洞) は住所からの概略位置。黄色の線が島を 1 周する県道 623 号。© OpenStreetMap contributors (ODbL)。</figcaption></figure>
    <ol class="legend">
{legend}
    </ol>
    <h4>拡大できる地図 — マーカーを押すと Google マップへ</h4>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
    <div id="livemap"></div>
    <p class="note" style="font-family:var(--mono);font-size:12px;color:var(--muted)">オンライン時だけ表示される (地図タイルは OpenStreetMap)。圏外では上の静止画を使う。ピンチで拡大、番号を押すと「Google マップで開く / ここへの経路」。</p>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
    <script>
    (function(){{
      if(!window.L) return;
      var S={spots_js};
      var m=L.map('livemap',{{scrollWheelZoom:false}}).setView([27.042,128.43],13);
      L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{maxZoom:19,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}}).addTo(m);
      S.forEach(function(s){{
        var ic=L.divIcon({{className:'pin'+(s.approx?' approx':''),html:'<span>'+s.n+'</span>',iconSize:[26,26],iconAnchor:[13,13],popupAnchor:[0,-12]}});
        var q=s.lat+','+s.lon;
        L.marker([s.lat,s.lon],{{icon:ic}}).addTo(m).bindPopup('<b>'+s.n+'. '+s.name+'</b>'+(s.approx?'<br><small>概略位置 — 現地で確認</small>':'')+'<br><a href="https://www.google.com/maps/search/?api=1&query='+q+'" target="_blank" rel="noopener">Google マップで開く</a> ・ <a href="https://www.google.com/maps/dir/?api=1&destination='+q+'" target="_blank" rel="noopener">ここへの経路</a>');
      }});
    }})();
    </script>'''
src=pat.sub(lambda m: block, src, count=1)
src=src.replace('<h3>島の略図 — どこに何があるか</h3>','<h3>島の地図 — 18 か所</h3>')
css='''  /* ---- map (OSM 静止画の凡例 + Leaflet) ---- */
  ol.legend{list-style:none; columns:2; column-gap:24px; margin:.6em 0 1.2em; font-size:.9rem;}
  ol.legend li{padding:3px 0; break-inside:avoid;}
  ol.legend .n{display:inline-block; min-width:22px; font-family:var(--mono); color:var(--accent); font-weight:600; margin-right:6px;}
  #livemap{height:480px; border:1px solid var(--line2); border-radius:6px; background:var(--sea); margin:.6em 0 .4em;}
  .pin{background:var(--accent); color:#fff; border:2px solid #fff; border-radius:50%; display:flex; align-items:center; justify-content:center; font-family:var(--mono); font-size:12px; font-weight:600; box-shadow:0 1px 4px rgba(0,0,0,.45);}
  .pin.approx{background:var(--muted);}
  .leaflet-popup-content{font-family:var(--sans); font-size:14px; line-height:1.6;}
'''
src=src.replace('  /* ---- day plan (ステッパー) ---- */', css+'  /* ---- day plan (ステッパー) ---- */',1)
src=src.replace('    ol.legend{columns:1;}','')
src=src.replace('    .check{columns:1;}','    .check{columns:1;} ol.legend{columns:1;} #livemap{height:380px;}',1)
# 位置の誤りを訂正
src=src.replace('9/5 の到着日はプリシアから車 2 分の距離なので、15:30 の買い出しのついでに寄ると 3 日間使える。','案内所はサザンクロスセンターの隣 (プリシアから車 8 分・地図 17) なので、9/6 午後に与論城跡へ行く時に買うのが自然。9/5 のうちに欲しければ買い出しの後に足を伸ばす。')
src=src.replace('プリシアから最寄りのカフェ','サザンクロス・与論城跡の行き帰りに')
open('yoron-guide.template.html','w',encoding='utf-8').write(src)
print('ok')
