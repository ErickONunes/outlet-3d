"""Import all public WordPress posts and pages from the local audit snapshot.

The importer is repeatable: it rebuilds src/data/migrated.json and downloads only
missing local WordPress-upload assets. It never writes to the production site.
"""
import concurrent.futures
import hashlib
import html
import json
import re
import time
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
SOURCE_HOSTS = {'outlet3d.com.br', 'www.outlet3d.com.br'}
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())
ALLOWED = set('p div span h1 h2 h3 h4 h5 h6 a img figure figcaption strong b em i u s del ins ul ol li table thead tbody tfoot tr th td caption colgroup col blockquote br hr pre code sup sub details summary dl dt dd abbr time'.split())
DROP = set('script style iframe object embed form input button textarea select option link meta noscript svg'.split())


class Node:
    def __init__(self, tag='', attrs=None):
        self.tag = tag
        self.attrs = dict(attrs or [])
        self.children = []


class Parser(HTMLParser):
    def __init__(self, markup):
        super().__init__(convert_charrefs=True)
        self.root = Node()
        self.stack = [self.root]
        self.feed(markup or '')

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                self.stack = self.stack[:index]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def text(node):
    return node if isinstance(node, str) else ''.join(text(child) for child in node.children)


def plain(markup):
    return re.sub(r'\s+', ' ', text(Parser(markup).root)).strip()


def clean_name(value):
    return html.unescape(value or '').strip()


def description_for(item):
    excerpt = plain(item.get('excerpt', {}).get('rendered', ''))
    excerpt = re.sub(r'^(Leia mais|Continue lendo).*', '', excerpt, flags=re.I).strip()
    if len(excerpt) >= 70:
        return excerpt[:158].rsplit(' ', 1)[0].rstrip(' ,;:') + '.'
    return f"Guia da Outlet 3D sobre {clean_name(item['title']['rendered'])}."


posts = json.loads((ROOT / 'migration/posts.json').read_text())
pages = json.loads((ROOT / 'migration/pages.json').read_text())
media = {item['id']: item for item in json.loads((ROOT / 'migration/media.json').read_text())}
authors = {item['id']: item for item in json.loads((ROOT / 'migration/users.json').read_text())}
categories = {item['id']: item for item in json.loads((ROOT / 'migration/categories.json').read_text())}

all_items = [*posts, *pages]
source_paths = {urllib.parse.urlsplit(item['link']).path for item in all_items}
category_paths = {
    urllib.parse.urlsplit(item['link']).path: f"/categoria/{item['slug']}/"
    for item in categories.values()
}
source_paths.update(category_paths)
source_paths.update({'/', '/autor/'})
assets = {}


def local_asset(value):
    url = urllib.parse.urlsplit(urllib.parse.urljoin('https://outlet3d.com.br', html.unescape(value)))
    if url.hostname not in SOURCE_HOSTS or not url.path.startswith('/wp-content/uploads/'):
        raise ValueError(f'Unexpected local asset: {value}')
    path = urllib.parse.unquote(url.path)
    if '..' in Path(path).parts:
        raise ValueError(f'Unsafe asset path: {path}')
    assets[f'https://outlet3d.com.br{urllib.parse.quote(path, safe="/")}'] = path
    return path


def internal_link(value):
    if not value:
        return ''
    if value.startswith('#'):
        return value
    url = urllib.parse.urlsplit(urllib.parse.urljoin('https://outlet3d.com.br', html.unescape(value)))
    if url.scheme and url.scheme not in {'http', 'https', 'mailto', 'tel'}:
        return ''
    if url.scheme in {'mailto', 'tel'}:
        return value
    if url.hostname in SOURCE_HOSTS:
        path = category_paths.get(url.path, url.path)
        if path in source_paths:
            return urllib.parse.urlunsplit(('', '', path, url.query, url.fragment))
        return urllib.parse.urlunsplit(('https', 'outlet3d.com.br', url.path, url.query, url.fragment))
    return value


def render(node):
    if isinstance(node, str):
        return html.escape(node, quote=False)
    if node.tag in DROP:
        return ''
    if not node.tag or node.tag not in ALLOWED:
        return ''.join(render(child) for child in node.children)
    tag = 'h2' if node.tag == 'h1' else node.tag
    body = ''.join(render(child) for child in node.children)
    attrs = {key: value for key, value in node.attrs.items() if key in {'id', 'title', 'alt', 'width', 'height', 'colspan', 'rowspan', 'scope', 'start', 'type', 'datetime', 'open'} and value is not None}
    if tag == 'a':
        href = internal_link(node.attrs.get('href', ''))
        if not href:
            return body
        attrs['href'] = href
        if node.attrs.get('target') == '_blank' or href.startswith('http'):
            attrs.update(target='_blank', rel='noopener noreferrer')
    if tag == 'img':
        source = node.attrs.get('data-lazy-src') or node.attrs.get('data-src') or node.attrs.get('src')
        if not source:
            return ''
        try:
            attrs['src'] = local_asset(source)
        except ValueError:
            return ''
        attrs.update(loading='lazy', decoding='async')
        attrs.setdefault('alt', '')
    attribute_string = ''.join(f' {key}="{html.escape(str(value), quote=True)}"' for key, value in attrs.items())
    return f'<{tag}{attribute_string}>' + ('' if tag in VOID else f'{body}</{tag}>')


records = []
for item in all_items:
    body = item.get('content', {}).get('rendered', '')
    if item['id'] == 1150:
        body = re.sub(r'\[contact-form-7[^\]]*\]', '<a href="mailto:contato@outlet3d.com.br">Enviar e-mail para contato@outlet3d.com.br</a>', body)
    rendered = render(Parser(body).root)
    featured = media.get(item.get('featured_media'))
    cover = None
    if featured:
        details = featured.get('media_details', {})
        try:
            cover = {
                'src': local_asset(featured['source_url']),
                'alt': clean_name(featured.get('alt_text')) or clean_name(item['title']['rendered']),
                'width': details.get('width', 1200),
                'height': details.get('height', 800),
            }
        except (KeyError, ValueError):
            pass
    item_categories = [
        {'name': clean_name(categories[category_id]['name']), 'slug': categories[category_id]['slug'], 'url': f"/categoria/{categories[category_id]['slug']}/"}
        for category_id in item.get('categories', []) if category_id in categories
    ]
    record = {
        'id': item['id'],
        'kind': item['type'],
        'path': urllib.parse.urlsplit(item['link']).path,
        'url': item['link'],
        'title': clean_name(item['title']['rendered']),
        'html': rendered,
        'emptySource': not plain(rendered),
        'excerpt': plain(item.get('excerpt', {}).get('rendered', '')),
        'author': clean_name(authors.get(item.get('author'), {}).get('name', 'Outlet 3D')),
        'date': f"{item['date_gmt']}Z",
        'modified': f"{item['modified_gmt']}Z",
        'categories': item_categories,
        'tags': item.get('tags', []),
        'cover': cover,
        'seo': {
            'title': f"{clean_name(item['title']['rendered'])} | Outlet 3D",
            'description': description_for(item),
            'canonical': item['link'],
            'robots': 'index, follow',
            'ogTitle': clean_name(item['title']['rendered']),
            'ogDescription': description_for(item),
            'ogType': 'article' if item['type'] == 'post' else 'website',
            'schemas': [],
        },
        'readingMinutes': max(1, round(len(plain(rendered).split()) / 220)),
    }
    records.append(record)


def download(entry):
    source, path = entry
    destination = PUBLIC / path.lstrip('/')
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        last_error = None
        for attempt in range(3):
            try:
                request = urllib.request.Request(source, headers={'User-Agent': 'Outlet3D-Migration/1.0'})
                with urllib.request.urlopen(request, timeout=90) as response:
                    content_type = response.headers.get('Content-Type', '')
                    data = response.read()
                if not content_type.startswith('image/') or len(data) < 100:
                    raise ValueError(f'Invalid image response: {source}')
                temporary = destination.with_suffix(destination.suffix + '.tmp')
                temporary.write_bytes(data)
                temporary.replace(destination)
                break
            except Exception as error:
                last_error = error
                if '404' in str(error):
                    break
                time.sleep(attempt + 1)
        if not destination.exists():
            raise last_error
    data = destination.read_bytes()
    return {'source': source, 'path': path, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


errors = []
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    futures = {pool.submit(download, entry): entry for entry in assets.items()}
    downloaded = []
    for future in concurrent.futures.as_completed(futures):
        try:
            downloaded.append(future.result())
        except Exception as error:
            errors.append({'source': futures[future][0], 'error': str(error)})

failed_paths = {assets[item['source']] for item in errors}
for record in records:
    for path in failed_paths:
        record['html'] = re.sub(rf'<img\b[^>]*\bsrc="{re.escape(path)}"[^>]*>', '', record['html'])
    if record['cover'] and record['cover']['src'] in failed_paths:
        record['cover'] = None

(ROOT / 'src/data/migrated.json').write_text(json.dumps(records, ensure_ascii=False, indent=2))
(ROOT / 'migration/import-all-manifest.json').write_text(json.dumps({
    'items': [{'id': record['id'], 'kind': record['kind'], 'path': record['path'], 'url': record['url']} for record in records],
    'assets': sorted(downloaded, key=lambda asset: asset['path']),
    'unavailable_assets': errors,
    'categories': [{'id': category['id'], 'name': clean_name(category['name']), 'slug': category['slug'], 'count': category['count']} for category in categories.values()],
}, ensure_ascii=False, indent=2))
print(json.dumps({'items': len(records), 'posts': len(posts), 'pages': len(pages), 'categories': len(categories), 'images': len(downloaded), 'bytes': sum(asset['bytes'] for asset in downloaded)}, ensure_ascii=False))
