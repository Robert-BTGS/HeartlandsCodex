from pathlib import Path
import os
import re
from collections import defaultdict
from datetime import datetime

DOCS = Path(__file__).resolve().parents[2] / 'docs'
INDEX_DIR = DOCS / 'Indexes'
TAGS_DIR = DOCS / 'Tags'

CATEGORY_MAP = {
    'Items': ['item'],
    'NPCs': ['npc'],
    'Locations': ['location'],
    'Quests': ['quest'],
    'Factions': ['faction'],
    'Races': ['race'],
    'Creatures': ['creature'],
    'Spells': ['spell'],
    'Skills': ['skill'],
    'Classes': ['class'],
}

GAME_TAGS = {
    'Heartlands': 'heartlands',
    'Heartlands_TheArena': 'the-arena',
    'Heartlands_TLC': 'the-lost-colony',
}

FRONT_MATTER_RE = re.compile(r'^---\n(.*?)\n---\n', re.DOTALL)
TAG_LINE_RE = re.compile(r'^tags:\s*\[(.*?)\]\s*$', re.MULTILINE)


def read_front_matter(text):
    m = FRONT_MATTER_RE.match(text)
    return m.group(1) if m else None


def parse_tags(text):
    fm = read_front_matter(text)
    if not fm:
        return []
    t = TAG_LINE_RE.search(fm)
    if not t:
        return []
    raw = t.group(1).strip()
    if not raw:
        return []
    return [x.strip().strip('"\'') for x in raw.split(',') if x.strip()]


def write_front_matter(text, tags):
    fm = read_front_matter(text)
    tag_line = f"tags: [{', '.join(tags)}]"
    if fm is None:
        return f"---\n{tag_line}\n---\n\n" + text
    if TAG_LINE_RE.search(fm):
        new_fm = TAG_LINE_RE.sub(tag_line, fm)
    else:
        new_fm = fm + "\n" + tag_line
    return f"---\n{new_fm}\n---\n" + text[len(fm)+8:]


def detect_category(path: Path):
    parts = path.parts
    for cat in CATEGORY_MAP.keys():
        if cat in parts:
            return cat
    return None


def detect_game(path: Path):
    for folder, tag in GAME_TAGS.items():
        if folder in path.parts:
            return tag
    return None


def seed_tags():
    changed = 0
    for p in DOCS.rglob('*.md'):
        if p.parts[1] in {'Indexes', 'Tags', 'Templates'}:
            continue
        if p.name.lower() == 'index.md':
            continue
        text = p.read_text()
        tags = parse_tags(text)
        new_tags = set(tags)

        cat = detect_category(p)
        if cat:
            new_tags.update(CATEGORY_MAP[cat])
        game = detect_game(p)
        if game:
            new_tags.add(game)

        if new_tags != set(tags) and new_tags:
            updated = write_front_matter(text, sorted(new_tags))
            p.write_text(updated)
            changed += 1
    return changed


def title_from_md(md_path: Path):
    for line in md_path.read_text().splitlines():
        if line.startswith('# '):
            return line[2:].strip()
    return md_path.stem.replace('_', ' ')


def gather_category(game_root: Path, category_dir: str):
    base = game_root / category_dir
    if not base.exists():
        return []
    out = []
    for q in base.rglob('*.md'):
        if q.name.lower() == 'index.md':
            continue
        out.append(q)
    return sorted(out)


def write_indexes():
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    idx_lines = [
        '# Indexes',
        '',
        'Quick access lists for major categories across the series.',
        '',
    ]
    for cat in CATEGORY_MAP.keys():
        idx_lines.append(f'* [{cat}]({cat}.md)')
    idx_lines.append('')
    (INDEX_DIR / 'index.md').write_text('\n'.join(idx_lines))

    games = {
        'Heartlands': DOCS / 'Heartlands',
        'Heartlands: The Arena': DOCS / 'Heartlands_TheArena',
        'Heartlands: The Lost Colony': DOCS / 'Heartlands_TLC',
    }

    for cat in CATEGORY_MAP.keys():
        lines = [f'# {cat} Index', '']
        any_items = False
        for game_name, root in games.items():
            items = gather_category(root, cat)
            if not items:
                continue
            any_items = True
            lines.append(f'## {game_name}')
            lines.append(f'{len(items)} entries')
            lines.append('')
            for p in items:
                title = title_from_md(p)
                link = os.path.relpath(p, INDEX_DIR)
                lines.append(f'* [{title}]({Path(link).as_posix()})')
            lines.append('')
        if not any_items:
            lines.append('No entries found yet.')
            lines.append('')
        (INDEX_DIR / f'{cat}.md').write_text('\n'.join(lines))


def tag_to_filename(tag: str) -> str:
    safe = re.sub(r'[^a-zA-Z0-9_-]+', '-', tag.strip()).strip('-')
    return f'{safe}.md'


def write_tags():
    TAGS_DIR.mkdir(parents=True, exist_ok=True)
    tag_map = defaultdict(list)

    for p in DOCS.rglob('*.md'):
        if p.parts[1] in {'Indexes', 'Tags', 'Templates'}:
            continue
        text = p.read_text()
        tags = parse_tags(text)
        for tag in tags:
            tag_map[tag].append(p)

    lines = [
        '# Tags',
        '',
        'Tags help group related pages. Add tags in a page front matter block like this:',
        '',
        '```yaml',
        '---',
        'tags: [example, lore, faction]',
        '---',
        '```',
        '',
    ]

    if not tag_map:
        lines.append('No tags have been added yet.')
    else:
        lines.append('## Tag List')
        lines.append('')
        for tag in sorted(tag_map.keys(), key=str.lower):
            lines.append(f'* [{tag}]({tag_to_filename(tag)})')
    lines.append('')
    (TAGS_DIR / 'index.md').write_text('\n'.join(lines))

    for tag, pages in tag_map.items():
        lines = [f'# Tag: {tag}', '']
        for p in sorted(pages):
            title = title_from_md(p)
            link = os.path.relpath(p, TAGS_DIR)
            lines.append(f'* [{title}]({Path(link).as_posix()})')
        lines.append('')
        (TAGS_DIR / tag_to_filename(tag)).write_text('\n'.join(lines))


def update_home_latest():
    home = DOCS / 'index.md'
    text = home.read_text()

    candidates = []
    for p in DOCS.rglob('*.md'):
        if p.parts[1] in {'Indexes', 'Tags', 'Templates'}:
            continue
        if p.name == 'index.md' and p.parent in {DOCS, INDEX_DIR, TAGS_DIR, DOCS / 'Templates'}:
            continue
        candidates.append(p)

    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    recent = candidates[:6]

    lines = ['## Latest Additions', '']
    for p in recent:
        title = title_from_md(p)
        link = os.path.relpath(p, DOCS)
        mod = datetime.fromtimestamp(p.stat().st_mtime).strftime('%Y-%m-%d')
        lines.append(f'* [{title}]({Path(link).as_posix()}) — {mod}')
    lines.append('')

    pattern = re.compile(r'^## Latest Additions[\s\S]*$', re.MULTILINE)
    if '## Latest Additions' in text:
        text = pattern.sub('\n'.join(lines), text).strip() + '\n'
    else:
        text = text.strip() + '\n\n' + '\n'.join(lines)
    home.write_text(text)


def main():
    tagged = seed_tags()
    write_indexes()
    write_tags()
    update_home_latest()
    print(f'Tagged pages updated: {tagged}')


if __name__ == '__main__':
    main()
