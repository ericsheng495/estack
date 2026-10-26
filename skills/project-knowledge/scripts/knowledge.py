#!/usr/bin/env python3
"""Initialize, validate, and retrieve repository-local feature knowledge. Stdlib only."""

import argparse
from datetime import date
import json
from pathlib import Path
import re
import subprocess
import sys


INDEX = Path('.estack/knowledge/index.json')
MARKER = '<!-- estack:project-knowledge -->'
POINTER = '''<!-- estack:project-knowledge -->
## Feature context

Before changing a feature, search `.estack/knowledge/index.json` and read the matching feature documents and relevant live sources. Load only context needed for the task. After changing behavior, update that feature's entry, constraints, and actual verification results. Knowledge is navigation, not proof that current code works.
<!-- /estack:project-knowledge -->
'''


def local_path(root, value):
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ValueError(f'Expected a relative project path: {value!r}')
    path = (root / value).resolve()
    if not path.is_relative_to(root):
        raise ValueError(f'Path escapes project: {value}')
    return path


def load(root):
    data = json.loads(local_path(root, str(INDEX)).read_text())
    if not isinstance(data, dict) or type(data.get('version')) is not int or data['version'] != 1:
        raise ValueError('Expected knowledge schema version 1')
    if not isinstance(data.get('features'), list):
        raise ValueError('features must be a list')
    seen = set()
    for entry in data['features']:
        if not isinstance(entry, dict):
            raise ValueError('Each feature must be an object')
        slug = entry.get('id')
        if not isinstance(slug, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug) or slug in seen:
            raise ValueError(f'Invalid or duplicate feature ID: {slug!r}')
        seen.add(slug)
        for key in ('summary', 'verification'):
            if not isinstance(entry.get(key), str) or not entry[key].strip():
                raise ValueError(f'{slug}: {key} must be nonempty text')
        if entry.get('status') not in ('implemented', 'partial', 'removed'):
            raise ValueError(f'{slug}: invalid status')
        document = local_path(root, entry.get('document'))
        if not document.is_file():
            raise ValueError(f'{slug}: missing feature document')
        sources = entry.get('source_paths')
        if not isinstance(sources, list) or not sources:
            raise ValueError(f'{slug}: source_paths must be a nonempty list')
        for source in sources:
            if not local_path(root, source).exists() and entry['status'] != 'removed':
                raise ValueError(f'{slug}: missing source {source}')
        commit = entry.get('reviewed_commit')
        if 'reviewed_commit' not in entry or (commit is not None and (not isinstance(commit, str) or not re.fullmatch(r'(?:[0-9a-f]{40}|[0-9a-f]{64})', commit))):
            raise ValueError(f'{slug}: reviewed_commit must be a full Git object ID or null')
        try:
            if not isinstance(entry.get('reviewed_at'), str):
                raise ValueError()
            date.fromisoformat(entry['reviewed_at'])
        except ValueError:
            raise ValueError(f'{slug}: reviewed_at must be an ISO date') from None
    return data


def git(root, *args):
    return subprocess.run(['git', '-C', str(root), *args], capture_output=True, text=True, timeout=10)


def freshness(root, entry):
    commit = entry['reviewed_commit']
    if not commit:
        return 'unknown: no reviewed source commit'
    try:
        if git(root, 'cat-file', '-e', commit + '^{commit}').returncode:
            return 'unknown: reviewed commit unavailable'
        if git(root, 'merge-base', '--is-ancestor', commit, 'HEAD').returncode:
            return 'unknown: reviewed commit is not an ancestor of HEAD'
        paths = entry['source_paths']
        delta = git(root, 'diff', '--name-only', commit, '--', *paths)
        untracked = git(root, 'ls-files', '--others', '--exclude-standard', '--', *paths)
        if delta.returncode or untracked.returncode:
            return 'unknown: Git comparison failed'
        if delta.stdout.strip() or untracked.stdout.strip():
            return 'stale: listed sources changed since review'
        return 'unchanged: listed sources only; behavior not rechecked'
    except (OSError, subprocess.TimeoutExpired):
        return 'unknown: Git unavailable'


def initialize(root, wire):
    index = local_path(root, str(INDEX))
    index.parent.mkdir(parents=True, exist_ok=True)
    if not index.exists():
        index.write_text(json.dumps({'version': 1, 'features': []}, indent=2) + '\n')
    # Check an existing index before modifying project instructions.
    load(root)
    local_path(root, '.estack/knowledge/features').mkdir(exist_ok=True)
    if wire:
        agents = local_path(root, 'AGENTS.md')
        existing = agents.read_text() if agents.exists() else ''
        if MARKER not in existing:
            agents.write_text(existing + ('\n\n' if existing else '') + POINTER)
    print(f'Knowledge ready: {index}')


def context(root, query, limit, max_chars):
    data = load(root)
    terms = set(re.findall(r'[a-z0-9]+', query.lower()))
    matches = []
    for entry in data['features']:
        # Search metadata and feature prose, then load only selected documents.
        prose = local_path(root, entry['document']).read_text()
        words = set(re.findall(r'[a-z0-9]+', ' '.join([entry['id'], entry['summary'], *entry['source_paths'], prose]).lower()))
        score = len(terms & words)
        if score:
            matches.append((score, entry, prose))
    matches.sort(key=lambda match: (-match[0], match[1]['id']))
    result = {'query': query[:120], 'matches': [], 'truncated': len(matches) > limit}
    for _, entry, prose in matches[:limit]:
        item = dict(entry, freshness=freshness(root, entry), content=prose)
        result['matches'].append(item)
        if len(json.dumps(result, ensure_ascii=False)) <= max_chars:
            continue
        result['truncated'] = True
        item['content'] = ''
        room = max_chars - len(json.dumps(result, ensure_ascii=False))
        if room < 0:
            result['matches'].pop()
            break
        # JSON escaping can expand prose. Fit the serialized output exactly.
        low, high = 0, min(len(prose), room)
        while low < high:
            middle = (low + high + 1) // 2
            item['content'] = prose[:middle]
            if len(json.dumps(result, ensure_ascii=False)) <= max_chars:
                low = middle
            else:
                high = middle - 1
        item['content'] = prose[:low]
        break
    if not result['matches']:
        result['note'] = 'No feature context returned; search live sources or increase the output budget.'
    print(json.dumps(result, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    for name in ('init', 'check', 'context'):
        command = commands.add_parser(name)
        command.add_argument('--project', type=Path, default=Path.cwd())
        if name == 'init':
            command.add_argument('--wire-agents', action='store_true')
        if name == 'context':
            command.add_argument('--query', required=True)
            command.add_argument('--limit', type=int, default=3)
            command.add_argument('--max-chars', type=int, default=6000)
    args = parser.parse_args()
    root = args.project.resolve()
    if not root.is_dir():
        parser.error('Project directory does not exist')
    try:
        if args.command == 'init':
            initialize(root, args.wire_agents)
        elif args.command == 'check':
            print(f'Valid knowledge: {len(load(root)["features"])} features (structure and paths only)')
        else:
            if not 1 <= args.limit <= 20 or not 512 <= args.max_chars <= 50000:
                parser.error('limit must be 1..20 and max-chars must be 512..50000')
            context(root, args.query, args.limit, args.max_chars)
    except (ValueError, OSError) as error:
        print(f'Knowledge error: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
