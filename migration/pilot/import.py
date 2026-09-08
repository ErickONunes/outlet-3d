"""Idempotent, bounded WordPress pilot. Never modifies the production site."""
import json,re,html,hashlib,urllib.request,urllib.parse,concurrent.futures
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'migration/pilot/source'
VOID=set('area base br col embed hr img input link meta param source track wbr'.split())
class Node:
 def __init__(self,tag='',attrs=None):self.tag=tag;self.attrs=dict(attrs or []);self.children=[]
class Parser(HTMLParser):
 def __init__(self,markup):
  super().__init__(convert_charrefs=True);self.root=Node();self.stack=[self.root];self.feed(markup)
 def handle_starttag(self,t,a):
  n=Node(t,a);self.stack[-1].children.append(n)
  if t not in VOID:self.stack.append(n)
 def handle_startendtag(self,t,a):
  self.handle_starttag(t,a)
  if t not in VOID:self.handle_endtag(t)
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==t:self.stack=self.stack[:i];break
 def handle_data(self,d):self.stack[-1].children.append(d)
def walk(n):
 if isinstance(n,Node):
  yield n
  for c in n.children:yield from walk(c)
def text(n):
 return n if isinstance(n,str) else ''.join(text(c) for c in n.children)
def plain(markup):return re.sub(r'\s+',' ',text(Parser(markup).root)).strip()
selection=json.loads((SOURCE/'selection.json').read_text())
assert len(selection)==18 and sum(p['kind']=='post' for p in selection)==10
routes={urllib.parse.urlsplit(p['link']).path for p in selection}|{'/','/autor/'}
media={p['id']:p for p in json.loads((ROOT/'migration/media.json').read_text())}
authors={p['id']:p for p in json.loads((ROOT/'migration/users.json').read_text())}
categories={p['id']:p for p in json.loads((ROOT/'migration/categories.json').read_text())}
assets={};changes=[]
def local_asset(url):
 u=urllib.parse.urlsplit(urllib.parse.urljoin('https://outlet3d.com.br',html.unescape(url)))
 if u.hostname not in ['outlet3d.com.br','www.outlet3d.com.br'] or not u.path.startswith('/wp-content/uploads/'):raise ValueError('Unexpected asset '+url)
 path=urllib.parse.unquote(u.path)
 if '..' in Path(path).parts:raise ValueError('Invalid path')
 assets['https://outlet3d.com.br'+urllib.parse.quote(path,safe='/')]=path
 return path
def link(url):
 u=urllib.parse.urlsplit(urllib.parse.urljoin('https://outlet3d.com.br',url))
 if u.scheme not in ['http','https','mailto','tel']:return '#' if url.startswith('#') else ''
 if url.startswith('#'):return url
 if u.hostname in ['outlet3d.com.br','www.outlet3d.com.br']:
  if u.path in routes:return u.path+('?' +u.query if u.query else '')+('#'+u.fragment if u.fragment else '')
  return urllib.parse.urlunsplit(('https','outlet3d.com.br',u.path,u.query,u.fragment))
 return url
ALLOWED=set('p div span h1 h2 h3 h4 h5 h6 a img figure figcaption strong b em i u s del ins ul ol li table thead tbody tfoot tr th td caption colgroup col blockquote br hr pre code sup sub details summary dl dt dd abbr time'.split())
DROP=set('script style iframe object embed form input button textarea select option link meta noscript svg'.split())
def render(n):
 if isinstance(n,str):return html.escape(n,quote=False)
 if n.tag in DROP:return ''
 body=''.join(render(c) for c in n.children)
 if not n.tag or n.tag not in ALLOWED:return body
 tag='h2' if n.tag=='h1' else n.tag
 attrs={k:v for k,v in n.attrs.items() if k in ['id','title','alt','width','height','colspan','rowspan','scope','start','type','datetime','open'] and v is not None}
 if tag=='a':
  attrs['href']=link(n.attrs.get('href',''))
  if n.attrs.get('target')=='_blank':attrs.update(target='_blank',rel='noopener noreferrer')
 if tag=='img':
  src=n.attrs.get('data-lazy-src') or n.attrs.get('src')
  if not src:return ''
  attrs.update(src=local_asset(src),loading='lazy',decoding='async')
  attrs.setdefault('alt','')
 return '<'+tag+''.join(' '+k+'="'+html.escape(v,quote=True)+'"' for k,v in attrs.items())+'>'+('' if tag in VOID else body+'</'+tag+'>')
records=[]
for p in selection:
 raw=(SOURCE/(str(p['id'])+'.html')).read_text();dom=Parser(raw).root
 meta={n.attrs.get('name') or n.attrs.get('property'):n.attrs.get('content','') for n in walk(dom) if n.tag=='meta'}
 title=next((text(n) for n in walk(dom) if n.tag=='title'),html.unescape(p['title']['rendered']))
 canonical=next((n.attrs.get('href') for n in walk(dom) if n.tag=='link' and n.attrs.get('rel')=='canonical'),p['link'])
 assert urllib.parse.urlsplit(canonical).path==urllib.parse.urlsplit(p['link']).path,(p['id'],canonical)
 schemas=[]
 for n in walk(dom):
  if n.tag=='script' and n.attrs.get('type')=='application/ld+json':
   try:schemas.append(json.loads(text(n)))
   except json.JSONDecodeError:changes.append({'id':p['id'],'reason':'Invalid source JSON-LD omitted; source HTML retained for review.'})
 def register_schema_images(value):
  if isinstance(value,dict):
   for v in value.values():register_schema_images(v)
  elif isinstance(value,list):
   for v in value:register_schema_images(v)
  elif isinstance(value,str) and re.match(r'https://(?:www\.)?outlet3d\.com\.br/wp-content/uploads/.*\.(?:png|jpe?g|webp)(?:\?.*)?$',value,re.I):local_asset(value)
 register_schema_images(schemas)
 extra_meta={k:v for k,v in meta.items() if k and (k.startswith('twitter:') or k.startswith('article:') or k.startswith('og:image') or k in ['og:locale','og:site_name','og:updated_time'])}
 for k,v in extra_meta.items():
  if k in ['og:image','og:image:secure_url','twitter:image'] and '/wp-content/uploads/' in v:local_asset(v)
 content=p['content']['rendered']
 if p['id']==1150:
  content=re.sub(r'\[contact-form-7[^\]]*\]','<a href="mailto:contato@outlet3d.com.br">Enviar e-mail para contato@outlet3d.com.br</a>',content)
  content=content.replace('Basta preencher o formulário abaixo e já já te respondo!','Envie sua mensagem pelo e-mail abaixo.')
  changes.append({'id':p['id'],'reason':'Broken Contact Form 7 shortcode replaced with explicit mailto; form invitation adjusted.'})
 if not content.strip():changes.append({'id':p['id'],'reason':'Empty body confirmed in both REST API and rendered production HTML.'})
 body=render(Parser(content).root)
 feat=media.get(p.get('featured_media'));cover=None
 if feat:
  d=feat.get('media_details',{});cover={'src':local_asset(feat['source_url']),'alt':feat.get('alt_text') or html.unescape(p['title']['rendered']),'width':d.get('width',1200),'height':d.get('height',800)}
 date=p['date_gmt']+'Z';modified=p['modified_gmt']+'Z'
 records.append({'id':p['id'],'kind':p['kind'],'path':urllib.parse.urlsplit(p['link']).path,'url':p['link'],'title':html.unescape(p['title']['rendered']),'html':body,'emptySource':not body.strip(),'excerpt':plain(p.get('excerpt',{}).get('rendered','')),'author':authors[p['author']]['name'],'date':date,'modified':modified,'categories':[{'name':html.unescape(categories[c]['name']),'url':categories[c]['link']} for c in p.get('categories',[])],'cover':cover,'seo':{'schemas':schemas,'extraMeta':extra_meta,'title':title,'description':meta.get('description') or None,'canonical':canonical,'robots':meta.get('robots','index, follow'),'ogTitle':meta.get('og:title',title),'ogDescription':meta.get('og:description') or None,'ogType':meta.get('og:type','article')},'readingMinutes':max(1,round(len(plain(body).split())/220))})

def download(item):
 url,path=item;dest=ROOT/'public'/path.lstrip('/');dest.parent.mkdir(parents=True,exist_ok=True)
 if not dest.exists():
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Outlet3D-Migration-Audit/1.0'}),timeout=60) as r:
   content_type=r.headers.get('Content-Type','');data=r.read()
  if not content_type.startswith('image/'):raise ValueError('Non-image response '+url)
  temp=dest.with_suffix(dest.suffix+'.tmp');temp.write_bytes(data);temp.replace(dest)
 data=dest.read_bytes()
 if len(data)<100:raise ValueError('Invalid image '+url)
 return {'source':url,'path':path,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:downloaded=list(pool.map(download,assets.items()))
(ROOT/'src/data/migrated.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
(ROOT/'migration/pilot/manifest.json').write_text(json.dumps({'items':[{'id':r['id'],'kind':r['kind'],'path':r['path'],'url':r['url']} for r in records],'assets':downloaded,'adjustments':changes},ensure_ascii=False,indent=2))
print(json.dumps({'items':len(records),'articles':10,'pages':8,'images':len(downloaded),'bytes':sum(a['bytes'] for a in downloaded),'adjustments':changes},ensure_ascii=False,indent=2))
