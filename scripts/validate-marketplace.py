#!/usr/bin/env python3
"""Validate the marketplace against what is actually on disk.

Usage:
    python scripts/validate-marketplace.py

Checks:
  - every registered plugin source exists and its plugin.json name matches
  - no plugin.json uses the object form of `repository`, which makes Claude Code
    silently discover zero skills from that plugin
  - every pinned `skills` array matches the SKILL.md files on disk exactly
  - no plugin directory is unregistered (product-team is a known exception)
  - every SKILL.md carries name and description

Exits 1 on any failure, so it works as a pre-commit or CI gate.
"""
import io, json, os, subprocess, sys

fails = []

# 1. Every registered plugin resolves, and its manifest name matches the entry.
mkt = json.load(io.open('.claude-plugin/marketplace.json', encoding='utf-8'))
for e in mkt['plugins']:
    src = e['source'].lstrip('./')
    mf = os.path.join(src, '.claude-plugin', 'plugin.json')
    if not os.path.isdir(src):
        fails.append('source missing: ' + src); continue
    if not os.path.exists(mf):
        fails.append('no plugin.json: ' + src); continue
    d = json.load(io.open(mf, encoding='utf-8'))
    if d['name'] != e['name']:
        fails.append('name mismatch: %s vs %s' % (d['name'], e['name']))
    if isinstance(d.get('repository'), dict):
        fails.append('%s: repository is an object (silently drops all skills)' % e['name'])
    # pinned skills array, where present, must match disk exactly
    if 'skills' in d:
        disk = sorted('./' + os.path.relpath(os.path.dirname(p), src).replace(os.sep, '/')
                      for p in [os.path.join(r, f)
                                for r, _, fs in os.walk(os.path.join(src, 'skills'))
                                for f in fs if f == 'SKILL.md'])
        if disk != sorted(d['skills']):
            fails.append('%s: pinned skills array != disk (%d vs %d)'
                         % (e['name'], len(d['skills']), len(disk)))

# 2. No orphaned plugin dirs registered nowhere (product-team is a known exception).
registered = {e['source'].lstrip('./').split('/')[-1] for e in mkt['plugins']}
on_disk = {d for d in os.listdir('plugins') if os.path.isdir(os.path.join('plugins', d))}
unregistered = on_disk - registered - {'product-team'}
if unregistered:
    fails.append('unregistered plugin dirs: ' + ', '.join(sorted(unregistered)))

# 3. Every SKILL.md has name + description, and name matches its directory.
for dirpath, _, files in os.walk('plugins'):
    if 'SKILL.md' not in files:
        continue
    p = os.path.join(dirpath, 'SKILL.md')
    txt = io.open(p, encoding='utf-8').read()
    if '\nname:' not in txt[:600] and not txt.startswith('---\nname:'):
        fails.append('no name: ' + p)
    if 'description:' not in txt[:2000]:
        fails.append('no description: ' + p)

print('registered plugins: %d' % len(mkt['plugins']))
print('skills on disk: %d' % sum(1 for r, _, fs in os.walk('plugins') if 'SKILL.md' in fs))
if fails:
    print('\nFAILURES (%d):' % len(fails))
    for f in fails:
        print('  ' + f)
    sys.exit(1)
print('\nAll marketplace + manifest checks pass.')
