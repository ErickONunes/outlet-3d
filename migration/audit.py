import urllib.request,json,concurrent.futures,re,csv
from pathlib import Path
base='https://outlet3d.com.br/wp-json/wp/v2/'
def get(endpoint,params='per_page=100'):
 req=urllib.request.Request(base+endpoint+'?'+params,headers={'User-Agent':'Outlet3D-Migration-Audit/1.0'})
 with urllib.request.urlopen(req,timeout=60) as r:return json.load(r),dict(r.headers)
def fetch(endpoint):
 data,h=get(endpoint)
 pages=int(h.get('X-WP-TotalPages',h.get('x-wp-totalpages',1)))
 for page in range(2,pages+1):data.extend(get(endpoint,'per_page=100&page='+str(page))[0])
 Path('migration/'+endpoint+'.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
 return endpoint,data
results={}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for f in [pool.submit(fetch,e) for e in ['posts','pages','categories','tags','media','users']]:
  try:
   key,data=f.result();results[key]=data;print(key,len(data),flush=True)
  except Exception as e:print('ERROR',str(e),flush=True)
posts=results.get('posts',[]);pages=results.get('pages',[])
with open('migration/url-inventory.csv','w') as f:
 w=csv.writer(f);w.writerow(['type','id','title','url','slug','date','modified','featured_media','word_count','images_in_content'])
 for kind,items in [('post',posts),('page',pages)]:
  for p in items:
   body=p.get('content',{}).get('rendered','');words=len(re.sub('<[^>]+>',' ',body).split())
   w.writerow([kind,p['id'],p['title']['rendered'],p['link'],p['slug'],p['date'],p['modified'],p.get('featured_media',0),words,len(re.findall('<img\\b',body))])
summary={'counts':{k:len(v) for k,v in results.items()},'post_date_range':[min((p['date'] for p in posts),default=''),max((p['date'] for p in posts),default='')],'posts_with_featured_images':sum(bool(p.get('featured_media')) for p in posts),'featured_image_ids':len(set(p['featured_media'] for p in posts if p.get('featured_media'))),'images_in_posts':sum(len(re.findall('<img\\b',p['content']['rendered'])) for p in posts),'categories':[{'name':p['name'],'count':p['count'],'link':p['link']} for p in results.get('categories',[])],'pages':[{'title':p['title']['rendered'],'link':p['link']} for p in pages],'media_types':{},'media_bytes_original':sum(p.get('media_details',{}).get('filesize',0) for p in results.get('media',[]))}
for m in results.get('media',[]):
 mime=m.get('mime_type','unknown');summary['media_types'][mime]=summary['media_types'].get(mime,0)+1
Path('migration/summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps(summary,ensure_ascii=False,indent=2))
