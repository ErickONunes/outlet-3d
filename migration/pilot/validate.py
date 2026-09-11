"""Validate generated output against independent WordPress snapshots, not importer output alone."""
import json,re,html,hashlib,urllib.parse,xml.etree.ElementTree as ET
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[2];DIST=ROOT/'dist'
class Inspect(HTMLParser):
 def __init__(self,s):
  super().__init__(convert_charrefs=True);self.links=[];self.images=[];self.meta={};self.canonical=None;self.ids=set();self.titles=[];self.title=False;self.content=[];self.depth=0;self.capture=False;self.scripts=[];self.script=None;self.h1s=0;self.feed(s)
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='h1':self.h1s+=1
  if t=='a':self.links.append(a.get('href',''))
  if t=='img':self.images.append(a.get('src',''))
  if 'id' in a:self.ids.add(a['id'])
  if t=='title':self.title=True
  if t=='meta':self.meta[a.get('name') or a.get('property')]=a.get('content')
  if t=='link' and a.get('rel')=='canonical':self.canonical=a['href']
  if t=='script':self.script={'type':a.get('type',''),'body':''}
  if t=='div':
   if 'data-migrated-content' in a:self.capture=True;self.depth=1
   elif self.capture:self.depth+=1
 def handle_endtag(self,t):
  if t=='title':self.title=False
  if t=='script' and self.script is not None:self.scripts.append(self.script);self.script=None
  if t=='div' and self.capture:
   self.depth-=1
   if self.depth==0:self.capture=False
 def handle_data(self,d):
  if self.title:self.titles.append(d)
  if self.capture and self.script is None:self.content.append(d)
  if self.script is not None:self.script['body']+=d

def normal(s):return re.sub(r'\s+',' ',s).strip()
def visible(s):
 s=re.sub(r'<(script|style)\b[^>]*>.*?</\1>','',s,flags=re.S|re.I)
 return normal(html.unescape(re.sub(r'<[^>]*>','',s)))
records=json.loads((ROOT/'src/data/migrated.json').read_text());source={p['id']:p for p in json.loads((ROOT/'migration/pilot/source/selection.json').read_text())}
manifest=json.loads((ROOT/'migration/pilot/manifest.json').read_text());errors=[];results=[];unmigrated=set();anchors=[]
assert len(records)==18 and sum(r['kind']=='post' for r in records)==10
parsed={}
for f in DIST.rglob('*.html'):parsed[f]=Inspect(f.read_text())
for r in records:
 f=DIST/r['path'].lstrip('/')/'index.html'
 if f not in parsed:errors.append('Missing route '+r['path']);continue
 page=parsed[f];p=source[r['id']];expected=p['content']['rendered']
 if p['id']==1150:
  expected=re.sub(r'\[contact-form-7[^\]]*\]','Enviar e-mail para contato@outlet3d.com.br',expected).replace('Basta preencher o formulário abaixo e já já te respondo!','Envie sua mensagem pelo e-mail abaixo.')
 # Sobre e Contato receberam uma apresentação própria depois do piloto; as demais
 # páginas continuam com o conteúdo visível comparado à fotografia de origem.
 redesigned_page=r['path'] in {'/sobre/','/contato/'}
 expected_schema_count=len(r['seo']['schemas'])+1+(r['kind']=='post')  # Schema original + artigo + Organization/WebSite global
 checks={'text':redesigned_page or visible(expected)==normal(''.join(page.content)),'canonical':page.canonical==p['link'],'title':''.join(page.titles)==r['seo']['title'],'description':page.meta.get('description')==r['seo']['description'],'single_h1':page.h1s==1,'no_shortcode':'[contact-form-7' not in f.read_text(),'dates':r['kind']!='post' or all(d in f.read_text() for d in [r['date'],r['modified']]),'schema':len([s for s in page.scripts if s['type']=='application/ld+json'])==expected_schema_count}
 for script in page.scripts:
  if script['type']=='application/ld+json':json.loads(script['body'])
 for key,ok in checks.items():
  if not ok:errors.append(f'{r["path"]}: {key}')
 results.append({'id':r['id'],'path':r['path'],'redesigned_after_pilot':redesigned_page,'checks':checks})
for f,p in parsed.items():
 for value in p.links+p.images:
  if not value:continue
  u=urllib.parse.urlsplit(value)
  if u.hostname=='outlet3d.com.br' and not (DIST/urllib.parse.unquote(u.path).lstrip('/')).exists():unmigrated.add(value)
  if u.scheme or u.netloc:continue
  if not u.path:target=f
  else:
   target=DIST/urllib.parse.unquote(u.path).lstrip('/') if u.path.startswith('/') else f.parent/urllib.parse.unquote(u.path)
   if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(f'Broken local link {f.relative_to(DIST)} -> {value}')
  elif u.fragment and target in parsed and urllib.parse.unquote(u.fragment) not in parsed[target].ids:anchors.append({'page':str(f.relative_to(DIST)),'link':value})
for a in manifest['assets']:
 f=DIST/a['path'].lstrip('/')
 if not f.exists() or hashlib.sha256(f.read_bytes()).hexdigest()!=a['sha256']:errors.append('Image not copied intact '+a['path'])
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
sitemap_urls={n.text for f in DIST.glob('sitemap-*.xml') for n in ET.parse(f).findall('s:url/s:loc',ns)}
for r in records:
 if r['url'] not in sitemap_urls:errors.append('Missing in sitemap '+r['url'])
report={'passed':not errors,'migrated':len(results),'images':len(manifest['assets']),'errors':errors,'checks':results,'links_to_production_not_in_pilot':sorted(unmigrated),'fragment_warnings':anchors}
(ROOT/'migration/pilot/validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ['checks','links_to_production_not_in_pilot']},ensure_ascii=False,indent=2));print('Links intentionally left on production:',len(unmigrated))
if errors:raise SystemExit(1)
