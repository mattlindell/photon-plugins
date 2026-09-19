#!/usr/bin/env python3
"""Check that every relative markdown link and heading anchor resolves.

Usage:
    python scripts/lint-links.py [path ...]     # defaults to plugins/ and docs/

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


def main(roots) -> int:
    problems = []
    for root in roots:
        if os.path.isfile(root):
            problems += check(root)
            continue
        for dirpath, _, filenames in os.walk(root):
            for name in sorted(filenames):
                if name.endswith('.md'):
                    problems += check(os.path.join(dirpath, name))
    if problems:
        print('Broken links (%d):' % len(problems))
        for path, lineno, target, why in problems:
            print('  %s:%d  %s  (%s)' % (path.replace(os.sep, '/'), lineno,
                                         target, why))
        return 1
    print('All relative links and anchors resolve.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:] or ['plugins', 'docs']))
