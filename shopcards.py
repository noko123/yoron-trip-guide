# 店リストの <table> を、食べログ OGP 画像つきカードに置換する (一度だけ実行)
import json, re
og=json.load(open('tabelog_og.json',encoding='utf-8'))
src=open('yoron-guide.template.html',encoding='utf-8').read()
shops=[
 ('tara','ヨロンの味 たら','鶏飯・モリンガ麺 (創作料理)。11:30〜14:00 / 18:00〜20:00・要予約','9/6 昼の本命'),
 ('aoisangosho','蒼い珊瑚礁','食堂。もずくそば・もずく天ぷら定食。海沿い','9/6 or 9/7 昼'),
 ('misaki','味咲 (みさき)','麺類・かき氷・沖縄料理。茶花','軽い昼・おやつ'),
 ('bashotei','芭蕉亭','食堂・郷土料理。カレー・定食。口コミ 22 件と島で最多級','9/7 昼 (茶花)'),
 ('musubi','麺処 むすび','ラーメン。茶花','雨の日の昼'),
 ('embercove','EMBER COVE','ハンバーガー。那間 (北東)','寺崎・皆田の帰りに'),
 ('yunnucafe','ゆんぬカフェ','自家焙煎コーヒーとデザート。観光協会 (ゆいパンタ) の隣・立長','プリシアから最寄りのカフェ'),
 ('castanet','カスタネット商店','カフェ。茶花','午後の休憩'),
 ('littlebeach','LITTLE BEACH 3540','カフェ。古里 (南)','与論城跡・民俗村の帰り'),
 ('hyokin','居酒屋 ひょうきん','海鮮系居酒屋。奄美黒ほろほろ鳥の刺し。役場から 250m','<b>9/5 19:00 (予約済)</b>。与論献奉が出るならここ'),
 ('kayoibune','かよい舟','居酒屋。島の魚と野菜の郷土料理 100 種超。ゆいパンタの建物内','予備の夜'),
 ('tuktuk','旬彩 Tuk Tuk','創作居酒屋。個室あり','8 人で個室が要る時'),
 ('masamunu','食音酒場 MASAMUNU','居酒屋。与論・沖縄料理と泡盛。立長 (プリシア寄り)','徒歩圏の夜'),
]
cards=[]
for k,name,desc,use in shops:
    o=og[k]; sid=o['url'].rstrip('/').split('/')[-1]
    photos=f'https://tabelog.com/kagoshima/A4605/A460502/{sid}/dtlphotolst/'
    cards.append(f'''      <a class="shop" href="{o['url']}"><img src="{o['img']}" alt="{name}" loading="lazy" referrerpolicy="no-referrer"><div class="sb"><div class="sn">{name}</div><div class="sd">{desc}</div><div class="su">{use}</div><div class="sl"><span>食べログ</span> · <span data-href="{photos}">写真一覧</span></div></div></a>''')
cards.append('''      <div class="shop"><div class="no-photo" style="aspect-ratio:1/1">空港</div><div class="sb"><div class="sn">空港の「ブルースカイ」</div><div class="sd">軽食。席が少ない</div><div class="su">復路直前</div></div></div>''')
block='    <div class="shops">\n'+'\n'.join(cards)+'\n    </div>'
pat=re.compile(r'    <div class="tbl-wrap"><table>\s*<thead><tr><th>店</th>.*?</table></div>',re.S)
assert pat.search(src), 'shop table not found'
src=pat.sub(lambda m: block, src, count=1)
src=src.replace('<b>店内や料理の写真は各店と食べログの著作物なのでこのページには焼き込まない</b>。リンク先の「写真」タブで見る。','サムネイルは各店の食べログページの代表写真 (OGP 画像) を<b>食べログのサーバーから直接参照</b>している (このページには複製していない。食べログ側で URL が変わると表示されなくなる)。カードを押すと食べログの店ページ、「写真一覧」で写真タブへ。')
css='''  /* ---- shop cards (食べログ OGP サムネ) ---- */
  .shops{display:grid; grid-template-columns:1fr 1fr; gap:14px; margin:1.2em 0;}
  .shop{display:grid; grid-template-columns:104px 1fr; gap:0; background:var(--panel); border:1px solid var(--line2); border-radius:6px; overflow:hidden; color:inherit; border-bottom:1px solid var(--line2); text-decoration:none;}
  .shop img,.shop .no-photo{width:104px; height:104px; object-fit:cover; display:block; background:var(--sand);}
  .shop .no-photo{aspect-ratio:auto; font-size:1rem;}
  .shop .sb{padding:9px 12px 10px; min-width:0;}
  .shop .sn{font-family:var(--serif); font-weight:700; color:var(--ink); font-size:1.02rem; line-height:1.3;}
  .shop .sd{font-size:.84rem; color:var(--soft); margin-top:3px; line-height:1.5;}
  .shop .su{font-size:.84rem; color:var(--accent); margin-top:4px;}
  .shop .sl{font-family:var(--mono); font-size:10.5px; color:var(--muted); margin-top:5px;}
  .shop:hover{border-color:var(--accent);}
'''
src=src.replace('  /* ---- day plan (ステッパー) ---- */', css+'  /* ---- day plan (ステッパー) ---- */',1)
src=src.replace('    .grid-2,.grid-3,.spots,.photos,.photos.two{grid-template-columns:1fr;}','    .grid-2,.grid-3,.spots,.photos,.photos.two,.shops{grid-template-columns:1fr;}',1)
# 写真一覧リンクはカード全体が <a> なので span の data-href をクリックで開く
js='''  document.querySelectorAll('.shop .sl span[data-href]').forEach(function(s){ s.style.textDecoration='underline'; s.addEventListener('click',function(e){ e.preventDefault(); e.stopPropagation(); window.open(s.dataset.href,'_blank'); }); });
'''
src=src.replace("  /* side toc active */", js+"  /* side toc active */",1)
open('yoron-guide.template.html','w',encoding='utf-8').write(src)
print('ok', src.count('class="shop"'))
