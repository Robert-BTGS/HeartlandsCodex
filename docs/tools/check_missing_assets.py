from pathlib import Path
import re
import os

DOCS = Path(__file__).resolve().parents[2] / 'docs'

IMG_RE = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')
HL_INFOBOX_RE = re.compile(r'<div class="hl-infobox">', re.IGNORECASE)

# Heuristics for pages that should have stats
STAT_HEADERS = {
    'item stats',
    'base attributes',
    'skill bonuses',
    'profile',
    'at a glance',
    'quest info',
}


def has_infobox(text: str) -> bool:
    return bool(HL_INFOBOX_RE.search(text))


def has_stats_heading(text: str) -> bool:
    for line in text.splitlines():
        if line.strip().startswith('## '):
            heading = line.strip()[3:].strip().lower()
            if heading in STAT_HEADERS:
                return True
    return False


def find_missing_images(md_path: Path):
    missing = []
    text = md_path.read_text()
    for m in IMG_RE.finditer(text):
        src = m.group(1).strip()
        if src.startswith('http://') or src.startswith('https://'):
            continue
        # Resolve relative to the markdown file
        target = (md_path.parent / src).resolve()
        if not target.exists():
            missing.append(src)
    return missing


def main():
    report = []
    missing_image_pages = []
    missing_stats_pages = []

    for md in DOCS.rglob('*.md'):
        if md.parts[1] in {'Indexes', 'Tags', 'Templates'}:
            continue
        if md.name.lower() == 'index.md':
            continue

        # Missing images
        missing_imgs = find_missing_images(md)
        if missing_imgs:
            missing_image_pages.append((md, missing_imgs))

        # Missing stats infobox if a stats-like heading exists
        text = md.read_text()
        if has_stats_heading(text) and not has_infobox(text):
            missing_stats_pages.append(md)

    # Output
    print('Missing Images')
    print('==============')
    if not missing_image_pages:
        print('None')
    else:
        for md, imgs in missing_image_pages:
            rel = md.relative_to(DOCS)
            print(f'- {rel}')
            for img in imgs:
                print(f'  - {img}')

    print('\nMissing Stats Infoboxes')
    print('========================')
    if not missing_stats_pages:
        print('None')
    else:
        for md in missing_stats_pages:
            rel = md.relative_to(DOCS)
            print(f'- {rel}')


if __name__ == '__main__':
    main()
