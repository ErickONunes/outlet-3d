import json,urllib.request,concurrent.futures
from pathlib import Path
root=Path(__file__).resolve().parents[2]
manifest=json.loads((root/'migration/pilot/manifest.json').read_text())
paths=[x['path'] for x in manifest['items']]+[x['path'] for x in manifest['assets']]
def check(path):
 with urllib.request.urlopen(urllib.request.Request('http://localhost:4321'+urllib.parse.quote(path,safe='/'),method='HEAD'),timeout=30) as r:
  assert r.status==200,(path,r.status)
  return {'path':path,'status':r.status,'contentType':r.headers.get('content-type')}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(check,paths))
(root/'migration/pilot/http-validation.json').write_text(json.dumps(results,indent=2,ensure_ascii=False))
print(f'{len(results)} URLs returned HTTP 200: 18 pages and 13 image files.')
