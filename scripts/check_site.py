#!/usr/bin/env python3
"""Check local HTML links, fragments, image dimensions, and original figure records."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
# Existing content is preserved. Keep this exception explicit, narrow and documented.
KNOWN_LEGACY = {('blog/unet.html', 'mask-rcnn.html')}

class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.images, self.errors = set(), [], [], []
        self.viewport = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids:
                self.errors.append('duplicate id: ' + a['id'])
            self.ids.add(a['id'])
        if tag == 'meta' and a.get('name') == 'viewport':
            self.viewport = 'width=device-width' in a.get('content', '')
        if tag in ('a', 'link') and a.get('href'):
            self.links.append(a['href'])
        if tag == 'img':
            self.links.append(a.get('src', ''))
            self.images.append(a)

def main():
    docs = {p.resolve(): Document(p.read_text()) for p in ROOT.rglob('*.html') if 'templates' not in p.parts and 'content' not in p.parts}
    errors, warnings = [], []
    for path, doc in docs.items():
        rel = path.relative_to(ROOT).as_posix()
        errors.extend(f'{rel}: {e}' for e in doc.errors)
        if not doc.viewport:
            errors.append(f'{rel}: missing responsive viewport')
        for href in doc.links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            target = ((ROOT / unquote(url.path.lstrip('/'))) if url.path.startswith('/') else (path.parent / unquote(url.path))).resolve() if url.path else path
            if target.is_dir():
                target = target / 'index.html'
            if ROOT not in target.parents and target != ROOT:
                errors.append(f'{rel}: path escapes repository: {href}')
            elif not target.is_file():
                msg = f'{rel}: missing local target: {href}'
                (warnings if (rel, href) in KNOWN_LEGACY else errors).append(msg)
            elif url.fragment and target in docs and unquote(url.fragment) not in docs[target].ids:
                errors.append(f'{rel}: missing fragment: {href}')
        for image in doc.images:
            if not image.get('alt'):
                errors.append(f'{rel}: image missing alt')
            if rel in ('blog/solo.html', 'blog/solov2.html') and not all(image.get(k) for k in ('width','height')):
                errors.append(f'{rel}: image missing layout dimensions')
    manifest = json.loads((ROOT / 'assets/figures/sources.json').read_text())
    documented = set()
    for entry in manifest['figures']:
        path = ROOT / 'assets/figures' / entry['file']
        documented.add(path.resolve())
        if not path.is_file():
            errors.append('Missing documented figure: ' + entry['file'])
            continue
        tree = ET.parse(path)
        if 'viewBox' not in tree.getroot().attrib:
            errors.append('SVG missing viewBox: ' + entry['file'])
        if not entry.get('source_url') or not entry.get('verified'):
            errors.append('Incomplete source record: ' + entry['file'])
    for path in (ROOT / 'assets/figures').rglob('*.svg'):
        if path.resolve() not in documented:
            errors.append('Figure missing source record: ' + str(path.relative_to(ROOT)))
    for warning in warnings:
        print('KNOWN LEGACY ISSUE: ' + warning)
    for error in errors:
        print('ERROR: ' + error, file=sys.stderr)
    print(f'Checked {len(docs)} pages and {len(documented)} figures; {len(errors)} errors, {len(warnings)} documented legacy issue(s).')
    return bool(errors)

if __name__ == '__main__':
    raise SystemExit(main())
