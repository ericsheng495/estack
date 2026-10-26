"""Behavior checks using isolated project repositories; no network or dependencies."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name('knowledge.py')
spec = importlib.util.spec_from_file_location('knowledge', SCRIPT)
knowledge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(knowledge)


class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()

    def run_cli(self, command, *args, expected=0):
        result = subprocess.run([sys.executable, str(SCRIPT), command, '--project', str(self.root), *args], capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stderr)
        return result

    def git(self, *args):
        result = subprocess.run(['git', '-C', str(self.root), *args], capture_output=True, text=True, check=True)
        return result.stdout.strip()

    def seed(self, **overrides):
        self.run_cli('init')
        (self.root / 'source.py').write_text('FEATURE = "export"\n')
        document = '.estack/knowledge/features/export.md'
        (self.root / document).write_text('# Export\nDownload filtered search results.\n')
        entry = dict(id='csv-export', summary='Export filtered search results', status='implemented', document=document, source_paths=['source.py'], reviewed_commit=None, reviewed_at='2026-10-26', verification='Not run; source review only')
        entry.update(overrides)
        self.write_entries([entry])
        return entry

    def write_entries(self, entries):
        (self.root / knowledge.INDEX).write_text(json.dumps(dict(version=1, features=entries)))

    def commit(self):
        self.git('init', '-b', 'main')
        self.git('add', '.')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-m', 'initial feature')
        return self.git('rev-parse', 'HEAD')

    def test_init_preserves_instructions_and_entries(self):
        instructions = '# Existing project\nKeep this instruction.\n'
        (self.root / 'AGENTS.md').write_text(instructions)
        entry = self.seed()
        self.run_cli('init', '--wire-agents')
        first = (self.root / 'AGENTS.md').read_text()
        self.run_cli('init', '--wire-agents')
        self.assertEqual((self.root / 'AGENTS.md').read_text(), first)
        self.assertTrue(first.startswith(instructions))
        self.assertEqual(knowledge.load(self.root)['features'], [entry])

    def test_check_does_not_claim_behavior_verified(self):
        self.seed()
        self.assertIn('structure and paths only', self.run_cli('check').stdout)

    def test_retrieves_matching_feature_and_unknown_freshness(self):
        self.seed()
        result = json.loads(self.run_cli('context', '--query', 'filtered export').stdout)
        self.assertEqual(result['matches'][0]['id'], 'csv-export')
        self.assertIn('Download filtered', result['matches'][0]['content'])
        self.assertTrue(result['matches'][0]['freshness'].startswith('unknown:'))

    def test_context_bound_survives_json_escaping(self):
        entry = self.seed()
        (self.root / entry['document']).write_text('export\n' + '\\"\n' * 10000)
        result = self.run_cli('context', '--query', 'export', '--max-chars', '1100').stdout.strip()
        self.assertLessEqual(len(result), 1100)
        self.assertTrue(json.loads(result)['truncated'])

    def test_context_bound_when_metadata_cannot_fit(self):
        self.seed(summary='export ' * 1000)
        result = self.run_cli('context', '--query', 'export', '--max-chars', '512').stdout.strip()
        self.assertLessEqual(len(result), 512)
        self.assertEqual(json.loads(result)['matches'], [])

    def test_missing_match_is_explicit(self):
        self.seed()
        result = json.loads(self.run_cli('context', '--query', 'frobnicator').stdout)
        self.assertEqual(result['matches'], [])
        self.assertIn('search live sources', result['note'])

    def test_feature_count_limit(self):
        entry = self.seed()
        self.write_entries([dict(entry, id=f'export-{number}') for number in range(5)])
        result = json.loads(self.run_cli('context', '--query', 'export', '--limit', '2').stdout)
        self.assertEqual(len(result['matches']), 2)
        self.assertTrue(result['truncated'])

    def test_duplicate_and_missing_sources_fail(self):
        entry = self.seed()
        self.write_entries([entry, entry])
        self.assertIn('duplicate', self.run_cli('check', expected=1).stderr)
        entry['source_paths'] = ['nonexistent.py']
        self.write_entries([entry])
        self.assertIn('missing source', self.run_cli('check', expected=1).stderr)

    def test_traversal_and_symlink_escape_fail(self):
        entry = self.seed(source_paths=['../outside'])
        self.assertIn('escapes project', self.run_cli('check', expected=1).stderr)
        (self.root / 'escape').symlink_to(self.root.parent, target_is_directory=True)
        entry['source_paths'] = ['escape']
        self.write_entries([entry])
        self.assertIn('escapes project', self.run_cli('check', expected=1).stderr)

    def test_unknown_commit_is_not_current(self):
        entry = self.seed(reviewed_commit='a' * 40)
        self.commit()
        self.assertTrue(knowledge.freshness(self.root, entry).startswith('unknown:'))

    def test_git_freshness_detects_committed_and_local_changes(self):
        entry = self.seed()
        entry['reviewed_commit'] = self.commit()
        self.assertTrue(knowledge.freshness(self.root, entry).startswith('unchanged:'))
        (self.root / 'source.py').write_text('FEATURE = "new behavior"\n')
        self.assertTrue(knowledge.freshness(self.root, entry).startswith('stale:'))
        self.git('add', 'source.py')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-m', 'change feature')
        self.assertTrue(knowledge.freshness(self.root, entry).startswith('stale:'))

    def test_removed_sources_are_valid_but_stale(self):
        entry = self.seed()
        entry['reviewed_commit'] = self.commit()
        (self.root / 'source.py').unlink()
        entry['status'] = 'removed'
        self.write_entries([entry])
        self.run_cli('check')
        self.assertTrue(knowledge.freshness(self.root, entry).startswith('stale:'))

    def test_untracked_source_under_directory_is_stale(self):
        entry = self.seed()
        (self.root / 'src').mkdir()
        (self.root / 'src/original.py').write_text('FEATURE = True\n')
        entry['source_paths'] = ['src']
        self.write_entries([entry])
        entry['reviewed_commit'] = self.commit()
        (self.root / 'src/new.py').write_text('NEW_FEATURE = True\n')
        self.assertTrue(knowledge.freshness(self.root, entry).startswith('stale:'))


if __name__ == '__main__':
    unittest.main()
