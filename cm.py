import sys, json, urllib.request, urllib.parse
UA={'User-Agent':'yuta-explainer/1.0 (no423yt@gmail.com)'}
def q(params):
    url='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params)
    return json.load(urllib.request.urlopen(urllib.request.Request(url,headers=UA)))
seen=set()
for term in sys.argv[1:]:
    d=q({'action':'query','list':'search','srsearch':term,'srnamespace':6,'srlimit':50,'format':'json'})
    print('==',term)
    for r in d['query']['search']:
        t=r['title']
        if t not in seen:
            seen.add(t); print(t)
