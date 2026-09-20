#!/usr/bin/env python3
"""Derive the semver bump each plugin needs from what actually changed.

Usage:
    python scripts/bump-versions.py                      # check against origin/main
    python scripts/bump-versions.py --base <ref>         # check against another ref
    python scripts/bump-versions.py --worktree           # include uncommitted work
    python scripts/bump-versions.py --apply              # write the bumps
    python scripts/bump-versions.py --format github      # annotations for CI

Impact is read from *structure*, not from diff size. A one-line change can be
breaking (adding `disable-model-invocation` removes the model's reach) while a
500-line deletion inside a reference file is a patch, so line counts are not
used at all.

  major  skill removed or renamed · skill `name:` changed · plugin removed or
         renamed · `disable-model-invocation` added · agent or command removed
  minor  skill, agent, command, or plugin added · `disable-model-invocation`
         removed
  patch  everything else

Conventional-commit types in the range can raise that floor but never lower it:
`feat` implies at least minor, and `!` or a `BREAKING CHANGE:` footer implies
major. Structure wins ties because it is derived from the artifact rather than
from what someone remembered to type.

The committed version only has to be *at or above* the floor. Bumping higher
than the tool asks is always fine, so pre-bumping locally never trips the check.

Exit codes: 0 satisfied · 1 below floor · 2 below floor on a major.
"""
import argparse
import io
import json
import os
import re
import subprocess
import sys

LEVELS = ('patch', 'minor', 'major')
PLUGINS_DIR = 'plugins'
UNREGISTERED = {'product-team'}


def sh(*args):
    r = subprocess.run(args, capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    return r.stdout if r.returncode == 0 else None


def higher(a, b):
    return a if LEVELS.index(a) >= LEVELS.index(b) else b


def parse_version(v):
    parts = (v or '0.0.0').split('.')
    while len(parts) < 3:
        parts.append('0')
    try:
        return tuple(int(x) for x in parts[:3])
    except ValueError:
        return (0, 0, 0)


def bump(version, level):
    major, minor, patch = parse_version(version)
    if level == 'major':
        return '%d.0.0' % (major + 1)
    if level == 'minor':
        return '%d.%d.0' % (major, minor + 1)
    return '%d.%d.%d' % (major, minor, patch + 1)


WORKTREE = 'WORKTREE'  # sentinel: read from disk, not from a git ref


def read_at(ref, path):
    """File content at a ref, or None if it did not exist there.

    The WORKTREE sentinel reads the working tree instead, so the check can run
    on uncommitted changes before a PR exists.
    """
    path = path.replace(os.sep, '/')
    if ref == WORKTREE:
        if not os.path.exists(path):
            return None
        return io.open(path, encoding='utf-8', errors='replace').read()
    return sh('git', 'show', '%s:%s' % (ref, path))


def frontmatter(text):
    if not text:
        return {}
    m = re.match(r'^---\n(.*?)\n---', text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ':' in line and not line.startswith(' '):
            k, _, v = line.partition(':')
            out[k.strip()] = v.strip().strip('"\'')
    return out


def tree_files(ref, prefix):
    """Paths under prefix at ref. Empty when the prefix does not exist."""
    if ref == WORKTREE:
        found = set()
        root = prefix.rstrip('/')
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d != '.git']
            for f in filenames:
                found.add(os.path.join(dirpath, f).replace(os.sep, '/'))
        return found
    out = sh('git', 'ls-tree', '-r', '--name-only', ref, '--', prefix)
    return set(out.splitlines()) if out else set()


def skill_map(ref, plugin):
    """skill directory -> frontmatter, at a ref."""
    prefix = '%s/%s/' % (PLUGINS_DIR, plugin)
    out = {}
    for p in tree_files(ref, prefix):
        if p.endswith('/SKILL.md'):
            out[os.path.dirname(p)] = frontmatter(read_at(ref, p))
    return out


def component_files(ref, plugin, kind):
    prefix = '%s/%s/%s/' % (PLUGINS_DIR, plugin, kind)
    return {p for p in tree_files(ref, prefix) if p.endswith('.md')}


def plugins_at(ref):
    names = set()
    for p in tree_files(ref, PLUGINS_DIR + '/'):
        parts = p.split('/')
        if len(parts) > 2:
            names.add(parts[1])
    return names - UNREGISTERED


def is_hidden(fm):
    return str(fm.get('disable-model-invocation', '')).lower() == 'true'


def content_changed(base, head, path):
    """Whether anything under path differs, in one git call."""
    if head == WORKTREE:
        out = sh('git', 'status', '--porcelain', '--', path)
        if out and out.strip():
            return True
        out = sh('git', 'diff', '--name-only', base, '--', path)
    else:
        out = sh('git', 'diff', '--name-only', base, head, '--', path)
    return bool(out and out.strip())


def classify(plugin, base, head):
    """Structural bump level for one plugin, with human-readable reasons."""
    level, reasons = 'patch', []
    b_skills, h_skills = skill_map(base, plugin), skill_map(head, plugin)

    for gone in sorted(set(b_skills) - set(h_skills)):
        level = higher(level, 'major')
        reasons.append('skill removed: %s' % os.path.basename(gone))
    for new in sorted(set(h_skills) - set(b_skills)):
        level = higher(level, 'minor')
        reasons.append('skill added: %s' % os.path.basename(new))

    for both in sorted(set(b_skills) & set(h_skills)):
        bf, hf = b_skills[both], h_skills[both]
        if bf.get('name') != hf.get('name'):
            level = higher(level, 'major')
            reasons.append('skill renamed: %s -> %s' % (bf.get('name'), hf.get('name')))
        if not is_hidden(bf) and is_hidden(hf):
            level = higher(level, 'major')
            reasons.append('no longer model-invocable: %s' % hf.get('name'))
        elif is_hidden(bf) and not is_hidden(hf):
            level = higher(level, 'minor')
            reasons.append('now model-invocable: %s' % hf.get('name'))

    for kind in ('agents', 'commands'):
        b, h = component_files(base, plugin, kind), component_files(head, plugin, kind)
        for gone in sorted(b - h):
            level = higher(level, 'major')
            reasons.append('%s removed: %s' % (kind[:-1], os.path.basename(gone)))
        for new in sorted(h - b):
            level = higher(level, 'minor')
            reasons.append('%s added: %s' % (kind[:-1], os.path.basename(new)))

    if not reasons:
        if content_changed(base, head, '%s/%s' % (PLUGINS_DIR, plugin)):
            reasons.append('content changed')
        else:
            return None, []
    return level, reasons


def commit_floor(base, head, plugin):
    """Highest level implied by conventional-commit subjects touching a plugin."""
    log = sh('git', 'log', '--format=%s%n%b%n--',
             '%s..%s' % (base, 'HEAD' if head == WORKTREE else head))
    if not log:
        return 'patch'
    level = 'patch'
    for msg in log.split('\n--\n'):
        if not msg.strip():
            continue
        subject = msg.strip().splitlines()[0]
        m = re.search(r'\b(feat|fix|refactor|chore|docs|perf|test)(\(([^)]*)\))?(!)?:', subject)
        if not m:
            continue
        scope = (m.group(3) or '').strip()
        if scope and scope not in (plugin, 'marketplace', '*'):
            continue
        if m.group(4) or 'BREAKING CHANGE' in msg:
            level = higher(level, 'major')
        elif m.group(1) == 'feat':
            level = higher(level, 'minor')
    return level


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='origin/main')
    ap.add_argument('--head', default='HEAD')
    ap.add_argument('--worktree', action='store_true',
                    help='compare the working tree, including uncommitted changes')
    ap.add_argument('--apply', action='store_true', help='write the bumps')
    ap.add_argument('--format', choices=('text', 'github'), default='text')
    a = ap.parse_args()
    if a.worktree:
        a.head = WORKTREE

    if sh('git', 'rev-parse', '--verify', a.base) is None:
        print('base ref not found: %s' % a.base, file=sys.stderr)
        return 3

    mkt_path = '.claude-plugin/marketplace.json'
    mkt = json.load(io.open(mkt_path, encoding='utf-8'))
    entries = {e['name']: e for e in mkt['plugins']}

    base_plugins, head_plugins = plugins_at(a.base), plugins_at(a.head)
    roster_changed = base_plugins != head_plugins

    rows, worst_shortfall = [], 'patch'
    for name in sorted(head_plugins):
        mf = '%s/%s/.claude-plugin/plugin.json' % (PLUGINS_DIR, name)
        cur_raw = read_at(a.head, mf)
        if not cur_raw:
            continue
        current = json.loads(cur_raw).get('version', '0.0.0')

        base_raw = read_at(a.base, mf)
        if not base_raw:
            rows.append((name, '-', current, 'new', 'new plugin', True))
            continue

        previous = json.loads(base_raw).get('version', '0.0.0')
        level, reasons = classify(name, a.base, a.head)
        if level is None:
            continue
        level = higher(level, commit_floor(a.base, a.head, name))
        floor = bump(previous, level)
        ok = parse_version(current) >= parse_version(floor)
        if not ok:
            worst_shortfall = higher(worst_shortfall, level)
        rows.append((name, previous, current, level, '; '.join(reasons[:4]), ok))

    if not rows:
        print('No plugin changes against %s.' % a.base)
        return 0

    width = max(len(r[0]) for r in rows)
    print('%-*s  %-8s  %-8s  %-6s  %s' % (width, 'plugin', 'base', 'current', 'needs', 'why'))
    failures = []
    for name, prev, cur, level, why, ok in rows:
        if level == 'new':
            print('%-*s  %-8s  %-8s  %-6s  %s' % (width, name, prev, cur, '-', why))
            continue
        floor = bump(prev, level)
        mark = 'ok' if ok else 'BELOW -> needs >= %s' % floor
        print('%-*s  %-8s  %-8s  %-6s  %s  [%s]' % (width, name, prev, cur, level, why, mark))
        if not ok:
            failures.append((name, floor, level))

    if a.apply:
        for name, floor, _ in failures:
            mf = '%s/%s/.claude-plugin/plugin.json' % (PLUGINS_DIR, name)
            d = json.load(io.open(mf, encoding='utf-8'))
            d['version'] = floor
            io.open(mf, 'w', encoding='utf-8', newline='\n').write(
                json.dumps(d, indent=2, ensure_ascii=False) + '\n')
            entries[name]['version'] = floor
            print('applied: %s -> %s' % (name, floor))
        if failures or roster_changed:
            prev_mkt = json.loads(read_at(a.base, mkt_path) or '{}')
            mkt['metadata']['version'] = bump(
                prev_mkt.get('metadata', {}).get('version', '0.0.0'),
                'minor' if roster_changed else 'patch')
            io.open(mkt_path, 'w', encoding='utf-8', newline='\n').write(
                json.dumps(mkt, indent=2, ensure_ascii=False) + '\n')
            print('marketplace -> %s' % mkt['metadata']['version'])
        return 0

    if not failures:
        print('\nAll plugin versions are at or above the required floor.')
        return 0

    print('\n%d plugin(s) below the floor. Fix with:\n  python scripts/bump-versions.py --base %s --apply'
          % (len(failures), a.base))
    if a.format == 'github':
        for name, floor, level in failures:
            kind = 'error' if level == 'major' else 'warning'
            print('::%s file=plugins/%s/.claude-plugin/plugin.json::%s needs version >= %s (%s change)'
                  % (kind, name, name, floor, level))
    return 2 if worst_shortfall == 'major' else 1


if __name__ == '__main__':
    sys.exit(main())
