import json,urllib.request,concurrent.futures
from pathlib import Path
base=Path('migration/pilot/source')
posts=json.load(open('migration/posts.json'))[:10];pages=json.load(open('migration/pages.json'))
selection=[dict(p,kind='post') for p in posts]+[dict(p,kind='page') for p in pages]
(base/'selection.json').write_text(json.dumps(selection,ensure_ascii=False,indent=2))
def fetch(p):
 req=urllib.request.Request(p['link'],headers={'User-Agent':'Outlet3D-Migration-Audit/1.0'})
 with urllib.request.urlopen(req,timeout=60) as r:body=r.read()
 (base/(str(p['id'])+'.html')).write_bytes(body)
 return (p['id'],len(body))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for r in pool.map(fetch,selection):print(r,flush=True)
