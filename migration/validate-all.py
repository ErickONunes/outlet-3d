"""Validate the complete imported content after `npm run build`."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
records = json.loads((ROOT / 'src/data/migrated.json').read_text())
errors = []
paths = [record['path'] for record in records]
if len(records) != 467:
    errors.append(f'Expected 467 records, got {len(records)}')
if len(paths) != len(set(paths)):
    errors.append('Duplicate content paths')

for record in records:
    output = DIST / record['path'].lstrip('/') / 'index.html'
    if not output.exists():
        errors.append(f'Missing output: {record["path"]}')
    for image in re.findall(r'<img\b[^>]*\bsrc="([^"]+)"', record['html']):
        if image.startswith('/wp-content/') and not (ROOT / 'public' / image.lstrip('/')).exists():
            errors.append(f'Missing body image: {record["path"]} -> {image}')
    cover = record.get('cover')
    if cover and not (ROOT / 'public' / cover['src'].lstrip('/')).exists():
        errors.append(f'Missing cover: {record["path"]} -> {cover["src"]}')

category_slugs = {category['slug'] for record in records if record['kind'] == 'post' for category in record['categories']}
for slug in category_slugs:
    if not (DIST / 'categoria' / slug / 'index.html').exists():
        errors.append(f'Missing category output: {slug}')

print(json.dumps({'passed': not errors, 'records': len(records), 'posts': sum(record['kind'] == 'post' for record in records), 'pages': sum(record['kind'] == 'page' for record in records), 'categories': len(category_slugs), 'errors': errors}, ensure_ascii=False, indent=2))
if errors:
    raise SystemExit(1)
