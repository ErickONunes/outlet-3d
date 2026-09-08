import urllib.request,xml.etree.ElementTree as E,json,concurrent.futures
from pathlib import Path
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls=[e.text for e in E.parse('migration/sitemap-index.xml').findall('s:sitemap/s:loc',ns)]
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Outlet3D-Migration-Audit/1.0"}),timeout=45) as r:b=r.read()
 Path('migration/'+url.rsplit('/',1)[-1]).write_bytes(b)
 root=E.fromstring(b);locs=[x.text for x in root.findall('s:url/s:loc',ns)]
 return {'sitemap':url,'count':len(locs),'urls':locs}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 results=list(pool.map(get,urls))
Path('migration/sitemap-inventory.json').write_text(json.dumps(results,indent=2,ensure_ascii=False))
for r in results:print(r['sitemap'],r['count'],r['urls'][:2])
with urllib.request.urlopen('https://outlet3d.com.br/wp-json/wp/v2/types',timeout=30) as r:types=json.load(r)
print('TYPES',[(k,v.get('rest_base')) for k,v in types.items()])
Path('migration/types.json').write_text(json.dumps(types,indent=2,ensure_ascii=False))
