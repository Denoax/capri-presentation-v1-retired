#!/usr/bin/env python3
"""Validate the CAPRI export's immutable sources, local links and media budgets."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / 'showcase/capri'


def main():
    from PIL import Image, ImageChops, ImageStat
    errors = []
    source = json.loads((ROOT / 'docs/SOURCE_MANIFEST.json').read_text())
    for record in source['files']:
        path = ROOT / record['public_path']
        if not path.is_file():
            errors.append('Missing inherited file: ' + record['public_path'])
            continue
        data = path.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if hashlib.sha256(data).hexdigest() != record['sha256'] or blob != record['git_blob']:
            errors.append('Changed inherited bytes: ' + record['public_path'])


    expected = {
        'capri-hero-loop.gif': ((990, 352), 3 * 1024**2, (5000, 8000)),
        'workflow-loop.gif': ((990, 240), 400 * 1024, (4000, 7000)),
        'capri-divider-loop.gif': ((990, 24), 100 * 1024, (1000, 5000)),
        'capri-social-1280x640.png': ((1280, 640), 1000000, None),
    }
    assets = []
    for path in sorted(MEDIA.iterdir()):
        if path.suffix not in ('.png', '.gif', '.svg'):
            continue
        data = path.read_bytes()
        record = {'path': path.name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                  'source': 'Original authored vector/motion code; no external media input',
                  'license': 'Owner license selection pending'}
        if path.suffix != '.svg':
            with Image.open(path) as im:
                size = im.size
                record.update(width=size[0], height=size[1], frames=im.n_frames)
                durations = []
                first = last = None
                for i in range(im.n_frames):
                    im.seek(i)
                    current = im.convert('RGB')
                    if first is None:
                        first = current.copy()
                    last = current.copy()
                    durations.append(im.info.get('duration', 0))
                if path.suffix == '.gif':
                    record.update(duration_ms=sum(durations), loop=im.info.get('loop'),
                                  seamless_first_last=ImageChops.difference(first, last).getbbox() is None)
                    if im.info.get('loop') != 0 or not all(d > 0 for d in durations):
                        errors.append('Invalid GIF loop/timing: ' + path.name)
                    if not record['seamless_first_last']:
                        errors.append('Nonmatching loop seam: ' + path.name)
                    poster_path = path.with_name(path.name.replace('-loop.gif', '-static.png'))
                    with Image.open(poster_path) as poster:
                        mean = sum(ImageStat.Stat(ImageChops.difference(first, poster.convert('RGB'))).mean) / 3
                    record['first_frame_poster_mean_rgb_difference'] = round(mean, 4)
                    if mean > 4:
                        errors.append('Poster differs from first GIF frame: ' + path.name)
                if path.name in expected:
                    dimensions, budget, duration_range = expected[path.name]
                    if size != dimensions or len(data) > budget:
                        errors.append('Media dimension/weight budget: ' + path.name)
                    if duration_range and not duration_range[0] <= sum(durations) <= duration_range[1]:
                        errors.append('Media duration budget: ' + path.name)
        assets.append(record)
    embedded = sum(x['bytes'] for x in assets if x['path'].endswith('-loop.gif'))
    if embedded > 10 * 1024**2:
        errors.append('Embedded README exceeds 10 MiB media budget')
    (MEDIA / 'MEDIA.json').write_text(json.dumps({'embedded_gif_bytes': embedded, 'assets': assets}, indent=2) + '\n')
    checked_links = 0
    for path in ROOT.rglob('*.md'):
        if any(part in ('.git', '.venv', '.media-venv') for part in path.relative_to(ROOT).parts):
            continue
        text = path.read_text()
        targets = re.findall(r'!?\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)', text)
        targets += re.findall(r'(?:src|href)="([^"]+)"', text)
        for target in targets:
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue
            target_path = (path.parent / unquote(url.path)).resolve() if url.path else path
            if not target_path.is_relative_to(ROOT) or not target_path.exists():
                errors.append(f'Broken local link: {path.relative_to(ROOT)} -> {target}')
                continue
            if url.fragment and target_path.suffix == '.md':
                headings = re.findall(r'^#{1,6}\s+(.+?)\s*#*$', target_path.read_text(), re.M)
                anchors = set()
                counts = {}
                for heading in headings:
                    slug = re.sub(r'[^\w\- ]', '', re.sub(r'<[^>]+>', '', heading.lower())).replace(' ', '-')
                    count = counts.get(slug, 0)
                    counts[slug] = count + 1
                    anchors.add(slug + (f'-{count}' if count else ''))
                if unquote(url.fragment) not in anchors:
                    errors.append(f'Broken heading: {path.relative_to(ROOT)} -> {target}')
            checked_links += 1

    result = {'status': 'FAIL' if errors else 'PASS', 'inherited_files': len(source['files']),
              'local_links_checked': checked_links, 'embedded_gif_bytes': embedded, 'errors': errors,
              'scope': 'Source bytes, local paths/headings, decoded media timing/seams/first frames and budgets; not runtime qualification or human motion/visual approval'}
    print(json.dumps(result, indent=2))
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
