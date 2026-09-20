#!/usr/bin/env python3
"""Check that every relative markdown link and heading anchor resolves.

Usage:
    python scripts/lint-links.py [path ...]            # defaults to plugins/ and docs/
    python scripts/lint-links.py --exclude product-team

Skips fenced code blocks and template placeholders, both of which legitimately
contain example links that point nowhere.

Exits 1 if anything is broken, so it works as a pre-commit or CI gate.
"""
import os
import re
import sys

FENCE = re.compile(r'^\s*(```|~~~)')
LINK = re.compile(r'\]\((?!https?:|mailto:)([^)]+)\)')
# Placeholder targets that are illustrative, not real: (link), (<some thing>),
# (path/to/x). A target containing < or > is a template slot by convention.
PLACEHOLDER = re.compile(r'^(link|url|path|\.\.\.)$|[<>]')


def slugify(heading: str) -> str:
    s = re.sub(r'`|\*|_', '', heading.strip().lower())
    s = re.sub(r'[^\w\s-]', '', s)
    return re.sub(r'\s+', '-', s).strip('-')


def headings(path: str) -> set:
    try:
        text = open(path, encoding='utf-8').read()
    except OSError:
        return set()
    return {slugify(h) for h in re.findall(r'^#{1,6}\s+(.*)$', text, re.M)}


def unfenced_lines(text: str):
    """Yield (lineno, line) for lines outside fenced code blocks."""
    in_fence = False
    for i, line in enumerate(text.splitlines(), 1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield i, line


def check(path: str) -> list:
    problems = []
    text = open(path, encoding='utf-8').read()
    base = os.path.dirname(path)
    for lineno, line in unfenced_lines(text):
        for m in LINK.finditer(line):
            target = m.group(1).strip()
            if PLACEHOLDER.search(target):
                continue
            filepart, _, fragment = target.partition('#')
            resolved = path if not filepart else os.path.normpath(
                os.path.join(base, filepart))
            if filepart and not os.path.exists(resolved):
                problems.append((path, lineno, target, 'missing file'))
                continue
            if fragment and resolved.endswith('.md'):
                if slugify(fragment) not in headings(resolved):
                    problems.append((path, lineno, target, 'no such anchor'))
    return problems


def main(argv) -> int:
    excluded = set()
    roots = []
    it = iter(argv)
    for arg in it:
        if arg == '--exclude':
            excluded.update(next(it, '').split(','))
        elif arg.startswith('--exclude='):
            excluded.update(arg.split('=', 1)[1].split(','))
        else:
            roots.append(arg)
    roots = roots or ['plugins', 'docs']

    def skip(path):
        parts = path.replace(os.sep, '/').split('/')
        return any(e and e in parts for e in excluded)

    problems = []
    for root in roots:
        if os.path.isfile(root):
            if not skip(root):
                problems += check(root)
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if not skip(os.path.join(dirpath, d))]
            for name in sorted(filenames):
                if name.endswith('.md'):
                    problems += check(os.path.join(dirpath, name))
    if excluded:
        print('(excluded: %s)' % ', '.join(sorted(excluded)))
    if problems:
        print('Broken links (%d):' % len(problems))
        for path, lineno, target, why in problems:
            print('  %s:%d  %s  (%s)' % (path.replace(os.sep, '/'), lineno,
                                         target, why))
        return 1
    print('All relative links and anchors resolve.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
